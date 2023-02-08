import sys
from pathlib import Path

# import decorator
sys.path.append(str(Path(*list(Path(__file__).parent.resolve().parts[:-2]))))
from pyslurm_decorators import slurm

# decorate function to be submitted with job options
@slurm(cores=1,
    n_workers=3,
    processes=1,
    memory="1GB",
    shebang='#!/usr/bin/env bash',
    queue="normal",
    walltime="00:30:00",
    local_directory='/tmp',
    death_timeout="15s",
    log_directory=f"{str(Path.home())}/dask-test",
    project="boc")
def calc_sum(x):
    """Calculate simple sum"""
    return x + (2.5 * x)


# generate a vector of values to map onto the decorated function
xvals = [100 * n for n in (0.01, 10, 100)]

# map the vector to the function and gather the results
result = calc_sum.map(xvals).gather()
print(result)