import sys, dask
import dask.dataframe as dd
from pathlib import Path 
from loguru import logger 

# Importing the decorator function
sys.path.append(str(Path(*list(Path(__file__).parent.resolve().parts[:-1]))))
from pyslurm_decorators import slurm

# Relative path to the file
cur_path = Path.cwd()
csv1 = Path(cur_path, "data", "010121.csv")
csv2 = Path(cur_path, "data", "020121.csv")
csv3 = Path(cur_path, "data", "030121.csv")

# Reading multiple csv files into multiple dask dataframes
df = dd.read_csv(csv1, dtype={'Active':'float64'}) # dtypes specified to read csv properly
df2 = dd.read_csv(csv2, dtype={'Active':'float64'})
df3 = dd.read_csv(csv3, dtype={'Active':'float64'})

# Calling the Slurm Decorator function
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
# Function that merges three dataframes together
def merge_dfs():
    res_a = df.merge(df2).merge(df3)
    return res_a
# Submitting the job to the cluster
result = merge_dfs.submit()
# Displaying resultes
logger.info("\nTable of merged dataframes:\n{}", result)

# Calling the Slurm Decorator function again
@slurm(cores=8,
    n_workers=4,
    processes=4, 
    memory="5GB",
    shebang='#!/usr/bin/env bash',
    queue="normal",
    walltime="00:30:00",
    local_directory='/tmp',
    death_timeout="15s",
    log_directory=f"{str(Path.home())}/dask-test",
    project="boc",
    show_progress=True)
# Function that calculates the total number of confirmed cases from all of the countries based on Province or State
def calc_tot_conf():
    res_b = result.groupby("Province_State")[['Confirmed']].sum()
    return res_b
# Submitting the function to the Slurm cluster
result2 = calc_tot_conf.submit()
# Displaying the results
logger.info("\nTotal of confirmed global COVID-19 cases reported between 01/01/2021 - 03/03/2021:\n{}", result2)

