import sys
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Any, Type, Dict, no_type_check
from distributed.security import Security

object_setattr = object.__setattr__


class Options(BaseModel):
    """
    Cluster options model including all kwargs that can be passed to the 
    [SLURMCluster](https://jobqueue.dask.org/en/latest/generated/dask_jobqueue.SLURMCluster.html) 
    object for initializing the Dask scheduler

    Attributes:
        queue: destination queue for each worker job - this corresponds to the SLURM partition 
            the workers will be launched on. This is passed to the `#SBATCH -p` option
        
        project: accounting string associated with each worker job (on Edith this is 'boc').
            This is passed to the `#SBATCH -A` option
        
        cores: total number of cores per job

        memory: total amount of memory per job, specified as a string with units (e.g. '2GB')

        processes: number of processes to cut the job into. By default, `process ~= sqrt(cores)` 
            so that the number of processes and the number of threads per process are 
            roughly equal.
        
        interface: network interface like 'eth0' or 'ib0'(for Infiniband/Ominipath). This will be used
            by both the Dask scheduler and the Dask workers.
        
        nanny: whether or not to start a nanny process. More details 
            [here](https://distributed.dask.org/en/latest/worker.html#nanny)
        
        local_directory: dask worker local directory for file spilling

        death_timeout: seconds to wait for a scheduler before closing workers

        extra: additional arguments to pass to *dask-worker*

        env_extra: other commands to add to job script before launching worker (e.g. shell commands),
            where each element corresponds to a 'newline'
        
        header_skip: lines to skip in the SLURM header (`#SBATCH`). Header lines matching this text
            will be removed
        
        log_directory: log to store standard output and error logs from SLURM jobs, with the filenames
            taking the format: `{job_name}.err` and `{job_name}.out`
        
        shebang: path to desired intepreter for batch submission script for the Dask workers

        python: python executable used to launch the Dask workers. Defaults to the python
            that is currently loaded and submitting these jobs (e.g. `sys.executable`)
        
        config_name: section to use from jobqueue.yaml configuration file if global cluster
            configurations are setup for Dask
        
        name: name of Dask worker. This is typically set by the cluster and left as it's default

        n_workers: number of workers to start by default

        silence_logs: log level like 'debug', 'info', or 'error' to emit here if the scheduler 
            is started locally
        
        asynchronous: whether or not to run this cluster object with the async/await syntax

        security: a `dask.distributed` security object if a persistent scheduler is running using
            TLS/SSL to secure between the scheduler, client and workers.
        
        scheduler_options: used to pass additional arguments to the
            [Dask scheduler](https://docs.dask.org/en/latest/scheduler-overview.html)
        
        walltime: walltime limit for each worker job

        job_cpu: number of cpu to book in SLURM, if `None` defaults to `worker_threads * processes`

        job_mem: amount of memory to request in SLURM, if `None` defaults to `worker_processes * memory`

        job_extra: list of other slurm options to include in the Dask worker job scripts.

        show_progress: whether or not to display progress bar while running callback (currently
            only works for Dask-like functions/callbacks)

    """
    queue: str
    project: str
    cores: int
    memory: str
    processes: int
    interface: Optional[str] = None
    nanny: Optional[bool] = None
    local_directory: Optional[str] = '/tmp'
    death_timeout: Optional[str] = None
    extra: Optional[List[Any]] = None
    env_extra: Optional[List[Any]] = None
    header_skip: Optional[List[Any]] = None
    log_directory: Optional[str] = None
    shebang: Optional[str] = '#!/usr/bin/env bash'
    python: Optional[str] = sys.executable
    config_name: Optional[str] = None
    name: Optional[str] = None
    n_workers: Optional[int] = None
    silence_logs: Optional[str] = None
    asynchronous: Optional[bool] = None
    security: Optional[Type[Security]] = None
    scheduler_options: Optional[Dict[str, Any]] = None
    walltime: Optional[str] = None
    job_name: Optional[str] = None
    job_cpu: Optional[int] = None
    job_mem: Optional[str] = None
    job_extra: Optional[list] = None
    show_progress: Optional[bool] = False


    @no_type_check
    def __setitem__(self, name: str, value: Any):
        """
        Dunder method for allowing setting attributes dictionary style
        
        Args:
            name: name of attribute to set

            value: value to set attribute to
        """
        self.__setattr__(name, value)
    
    @no_type_check
    def __eq__(self, other):
        """
        Dunder method for allowing comparison of Options instances. If
        two instances are the same will return True

        Args:
            other: other instance of Options to compare with
        """

        # do not compare against unrelated types
        if not isinstance(other, Options):
            return NotImplemented
        return self.dict() == other.dict()


    def setdefault(self, keyname: str, value: Any):
        """
        Analogue to `dict.setdefault(keyname, value)` for Pydantic models

        Will set the value of the corresponding attribute, `keyname` if it has not been set
        
        Args:
            keyname: name of attribute to set default value for

            value: value to set if attribute has not been set to a non-default value already
        """
        if keyname not in self.__fields_set__:
            self[keyname] = value
            return value
        else:
            return self.dict().get(keyname)


    def pop(self, keyname: str, value: Any=None):
        """
        Analogue to `dict.pop(keyname, value)` for Pydantic models
        
        Will remove the attribute from the model and return it's value if it has been set,
        otherwise it will return `value`

        Args:
            keyname: name of attribute to remove and return it's value

            value: value to return if `keyname` attribute has not been set to a non-default value
        
        """
        _val = self.dict().pop(keyname, value)
        delattr(self, keyname)

        if _val is None:
            return value
        else:
            return _val


    def get(self, keyname: str, value: Any=None):
        """
        Analogue to `dict.get(keyname, value)` for Pydantic models

        Args:
            keyname: name of attribute for which to return the corresponding value

            value: value to return if `keyname` attribute has not been set to a non-default value
        """
        if keyname not in self.__fields__set__:
            return value
        else:
            return self.dict().get(keyname)
    

    def collect(self):
        """Return model as dictionary with all `None` value entries filtered out"""
        return {k: v for k, v in self.dict().items() if v is not None}