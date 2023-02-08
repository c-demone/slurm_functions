from pathlib import Path
import dask.array as da
from rich import inspect
import sys

# import decorator
sys.path.append(str(Path(*list(Path(__file__).parent.resolve().parts[:-2]))))
from pyslurm_decorators import slurm
from pyslurm_decorators import SLURMClusterCallback
from pyslurm_decorators.schemas.slurm import Options

# define the cluster options
options = Options(cores=2,
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

# define a function you want submitted to the cluster
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

# instantiate the cluster object
cluster = SLURMClusterCallback(callback=calc_pi_mc, options=options)

# take a look at the object: this is what is returned when calling 
# a @slurm decorated function
inspect(cluster, methods='all')

# submit the function the cluster and return the result
if '-s' in sys.argv:
    result = cluster.submit(size_in_bytes=1e9)
    print("My Pi Estimate is: ", result)