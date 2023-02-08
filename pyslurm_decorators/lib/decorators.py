import sys
from typing import Optional, Dict, TypeVar, MutableMapping, Callable, Any, Union, Type, List
from distributed.security import Security
from rich import inspect
from .clusters import SLURMClusterCallback
from ..schemas.slurm import Options

# function type
F = TypeVar("F", bound=Callable[..., Any])

# function class type
FC = TypeVar("FC", Callable[..., Any], SLURMClusterCallback)


def _initiate_slurm_cluster(
    f: F,
    attrs: MutableMapping[str, Any],
    cls: Type[SLURMClusterCallback]
) -> SLURMClusterCallback:


    return cls(
        options=Options(**attrs),
        callback=f
    )

def slurm(
    
    queue: str,
    project: str,
    cores: int,
    memory: str,
    processes: int,
    interface: Optional[str] = None,
    nanny: Optional[bool] = None,
    local_directory: Optional[str] = '/tmp',
    death_timeout: Optional[str] = None,
    extra: Optional[List[Any]] = None,
    env_extra: Optional[List[Any]] = None,
    header_skip: Optional[List[Any]] = None,
    log_directory: Optional[str] = None,
    shebang: Optional[str] = '#!/usr/bin/env bash',
    python: Optional[str] = sys.executable,
    config_name: Optional[str] = None,
    name: Optional[str] = None,
    n_workers: Optional[int] = None,
    asynchronous: Optional[bool] = None,
    security: Optional[Type[Security]] = None,
    scheduler_options: Optional[Dict[str, Any]] = None,
    walltime: Optional[str] = None,
    job_name: Optional[str] = None,
    job_cpu: Optional[int] = None,
    job_mem: Optional[str] = None,
    job_extra: Optional[list] = None,
    show_progress: Optional[bool] = False,
    cls: Optional[Type[SLURMClusterCallback]] = None,
) -> Callable[[F], SLURMClusterCallback]:
    """
    **SLURM decorator function** attaches a callback (e.g. Python function) to
    an instance of the `SLURMClusterCallback` object and returns that object
    with the corresponding methods for submitting the function to a SLURM
    cluster.

    The `kwargs` for the decorator, aside from `cls`, are taken from the 
    [Options model](../decorators/slurm.md#options_model). 

    `cls(Optional[SLURMClusterCallback])`
    : the callback class that the decorated function is attached to. Generally, this
    is not manipulated by the user, but rather initialized through this decorator
    function. However, it is possible to create your own custom callback class and
    pass it as an argument to the <code>@slurm</code> decorator.
    """
    if cls is None:
        cls = SLURMClusterCallback

    fargs = locals()    
    attrs  = {k: v for k,v in fargs.items() if k != 'cls' and v is not None}

    def decorator(f: Callable[..., Any]) -> SLURMClusterCallback:

        cluster = _initiate_slurm_cluster(f, attrs, cls)
        return cluster

    return decorator