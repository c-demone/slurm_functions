import sys
import pathlib
import dask.array as da

# import decorator
sys.path.append(str(pathlib.Path(__file__).parent.resolve().parent.absolute()))
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
    log_directory=f"{str(pathlib.Path.home())}/dask-test",
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


chunks = [1e9 * n for n in (1, 10, 100)]

result = calc_pi_mc.submit(size_in_bytes=1e9)
print(result)