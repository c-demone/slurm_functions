import sys
import pathlib
from rich import inspect

sys.path.append(str(pathlib.Path(__file__).parent.resolve().parent.absolute()))

from pyslurm_decorators import slurm

@slurm(cores=36,
    processes=1,
    memory="10GB",
    shebang='#!/usr/bin/env bash',
    queue="normal",
    walltime="00:30:00",
    local_directory='/tmp',
    death_timeout="15s",
    log_directory=f"{str(pathlib.Path.home())}/dask-test",
    project="boc")
def calc_sum(x):
    """Calculate simple sum"""
    return x + (2.5 * x)


chunks = [100 * n for n in (0.01, 10, 100)]

result = calc_sum.map(chunks).gather()
print(result)