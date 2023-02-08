import sys
from pathlib import Path 
import dask
import dask.dataframe as dd

# Reading the csv file into a dask dataframe
df = dd.read_csv('~/pyslurm_decorators/test/data/010121.csv', dtype={'Active':'float64'})

sys.path.append(str(Path(*list(Path(__file__).parent.resolve().parts[:-1]))))
from pyslurm_decorators import slurm

# Calling the Slurm Decorator function
@slurm(cores=2,
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
# Function that calculates the mean of the number of active cases from all of the countries
def calc_mean():
    res_a = (df.Active.mean())
    return res_a
# Submitting the function to the Slurm cluster
result = calc_mean.submit()
# Displaying the results
print("\nMean of confirmed global COVID-19 cases reported 01/01/2021:  ", result, "\n")

# Calling the Slurm Decorator function again
@slurm(cores=4,
    n_workers=2,
    processes=2, 
    memory="5GB",
    shebang='#!/usr/bin/env bash',
    queue="normal",
    walltime="00:30:00",
    local_directory='/tmp',
    death_timeout="15s",
    log_directory=f"{str(Path.home())}/dask-test",
    project="boc",
    show_progress=True)
# Function that generates table of average confirmed cases/country 
def calc_conf_mean():
    res_b = df.groupby("Country_Region")[['Confirmed']].mean()
    return res_b
# Submitting the function to the Slurm cluster
result2 = calc_conf_mean.submit()
# Displaying the table
print("\nTable showing the average confirmed cases per country on 01/01/2021:\n")
print(result2)






