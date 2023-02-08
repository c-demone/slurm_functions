from pathlib import Path 
import dask.array as da
from rich import inspect
import sys

# import decorator
sys.path.append(str(Path(*list(Path(__file__).parent.resolve().parts[:-2]))))
from pyslurm_decorators import slurm


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
def calc_pi_mc(size_in_bytes, chunksize_in_bytes=200e6):
    """Calculate PI using a Monte Carlo estimate."""
    
    size = int(size_in_bytes / 8)
    chunksize = int(chunksize_in_bytes / 8)
    
    xy = da.random.uniform(0, 1,
                           size=(size / 2, 2),
                           chunks=(chunksize / 2, 2))
    
    in_circle = ((xy ** 2).sum(axis=-1) < 1)
    pi = 4 * in_circle.mean()

    return pi

# initiate SLURM cluster object, submit the function to the cluster 
# and return the result
result = calc_pi_mc.submit(size_in_bytes=1e9)
print("My Pi Estimate is: ", result)