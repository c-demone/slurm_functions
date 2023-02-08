from pathlib import Path
from rich import inspect
import sys

# map graphing imports
import geopandas as gpd

# dask imports
import dask.dataframe as dd

# datashader imports
from datashader.utils import lnglat_to_meters

# plotting functions
from colorcet import fire
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import datashader as ds
import datashader.transfer_functions as tf
import imageio
import numpy as np

# import decorator
sys.path.append(str(Path(*list(Path(__file__).parent.resolve().parts[:-2]))))
from pyslurm_decorators import slurm


@slurm(cores=18,
    n_workers=2,
    processes=1, 
    memory="5GB",
    shebang='#!/usr/bin/env bash',
    queue="normal",
    walltime="00:30:00",
    local_directory='/tmp',
    death_timeout="15s",
    log_directory=f"{str(Path.home())}/dask-test",
    project="boc",
    show_progress=True)
def prepare_data(years, filter_cols=['Filing Date', 'LATITUDE', 'LONGITUDE']):
    """Load and prepare data for plotting with dask/datashader"""
    
    # coords must be in 3857: https://towardsdatascience.com/create-a-gif-with-3-million-points-using-dask-caf7dcd0667e
    permits = dd.read_csv('./data/dob_permit_issuance.csv', 
                     dtype={
                         'Lot': 'int64',
                         'Block': 'int64',
                         "Owner's Phone # ": 'float64',
                         "Owner’s House Zip Code": 'float64',
                         "Permittee's License #": 'float64',
                         "Zip Code":'int64' 
                     },
                     usecols=filter_cols)
    
    # change column time to datetime
    permits['Filling Date'] = dd.to_datetime(permits['Filling Date'])

    # create new column for the year
    permits = permits.assign(year=permits['Filling Date'].dt.strftime('%Y'))

    # conversion of longitude and latitude to web mercator
    # create new columnss 'x' (longitude), 'y' (latitude)
    permits['x'], permits['y'] = lnglat_to_meters(permits['LONGITUDE'],
                        permits['LATITUDE'])
    
    # clean up un-needed columns
    permits = permits.drop(['LONGITUDE', 'LATITUDE'], axis=1)

    # implement dask best practices
    # drop na to be able to set index
    permits = permits.dropna()

    # set index in dataframe so it is arranged by year
    # (indexing can take a while)
    permits_indexed = permits.set_index('year')

    # repartition the data
    permits_repartitioned = permits_indexed.repartitioned(divisions=years)

    return permits_repartitioned


def get_nyc_boroughs_boundaries():
    """Determine plotting boundaries for NYC Boroughs"""
    Boundaries = ("Boundaries", "nyc_boroughs nyc_bounds, x_range, y_range")
    # add nyc borough boundaries (coords must be espg:3857)
    nyc_boroughs = gpd.read_file('./data/bourough_boundaries')
    nyc_boroughs = nyc_boroughs.to_crs('espg:3857')

    # NYC limits: lng(east/west) and lat (north/south)
    nyc_bounds = (( -74.25,  -73.7), (40.50, 40.92))
    x_range, y_range = [list(r) for r in lnglat_to_meters(nyc_bounds[0],
                                                          nyc_bounds[1])]

    return Boundaries(nyc_boroughs, nyc_bounds, x_range, y_range)


@slurm(cores=4,
    n_workers=2,
    processes=1, 
    memory="4GB",
    shebang='#!/usr/bin/env bash',
    queue="normal",
    walltime="00:30:00",
    local_directory='/tmp',
    death_timeout="15s",
    log_directory=f"{str(Path.home())}/dask-test",
    project="boc",
    show_progress=True)
def create_image(df, x_range, y_range, plot_width, plot_height, cmap=fire):
    """Datashader function to create image from all points"""
    # create the canvas
    cvs = ds.Canvas(plot_width=plot_width, plot_height=plot_height, 
                                    x_range=x_range, y_range=y_range)
    
    # plot dropoff positions, coutning number of passengers
    agg = cvs.points(df, 'x', 'y')
    
    # shade
    img = tf.shade(agg, cmap=cmap, how='eq_hist')
    
    # return an PIL image
    return tf.set_background(img, "black").to_pil()


def plot_permits_by_year(fig, all_data, year, city_limits, x_range, y_range, 
                                                    plot_width, plot_height):
    """Plot the permits by a given year"""
    # trim to the specific year
    df_this_year = all_data.loc[year]

    # create the datashaded image
    img = create_image.submit(df=df_this_year, x_range=x_range, 
                                y_range=y_range, plot_width=plot_width, 
                                plot_height=plot_height)

    # plot the image on a matplotlib axes
    plt.clf()
    ax = fig.gca()
    ax.imshow(img, extent=[x_range[0], x_range[1], y_range[0], y_range[1]])
    ax.set_axis_off()
    
    # plot the city limits
    city_limits.plot(ax=ax, facecolor="none", edgecolor="white")

    # add a text label for the hour
    ax.text(
        0.0,
        0.9,
        "Yearly Construction Permits\nFiled in NYC",
        color="white",
        fontsize=20,
        ha="left",
        transform=ax.transAxes,
    )

    ax.text(
        0.7,
        0.1,
        year,
        color="white",
        fontsize=40,
        ha="left",
        transform=ax.transAxes,
    )
    # draw the figure and return the image
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image   

if __name__ == '__main__':

    # set date range in years to plot for
    years = [str(x) for x in list(range(1989, 2020))]

    # set plot dimensions
    plot_width = int(750)
    plot_height = int(plot_width/1.2)

    # get boundaries for nyc boroughs
    bounds = get_nyc_boroughs_boundaries()

    # create a figure
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')

    # read permit data and partition by year
    partitioned_permits = prepare_data.submit(years=years)
    
    # cerate an image for each hour
    imgs = []
    for year in years:
        img = plot_permits_by_year(fig, partitioned_permits, year, bounds.nyc_boroughs,
                    bounds.nyc_bounds, x_range=bounds.x_range, y_range=bounds.y_range)
        imgs.append(img)
    
    imageio.mimsave("1989_2020_permits.gif", imgs, fps=1)
