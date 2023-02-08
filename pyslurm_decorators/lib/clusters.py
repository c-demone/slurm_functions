from re import I
import types
from typing import MutableSequence, Optional, Dict, Tuple, TypeVar, MutableMapping, Callable, Any, Type
from dask_jobqueue.slurm import SLURMJob, SLURMCluster
from dask.distributed import Client, TimeoutError#, progress
from traitlets.traitlets import Int
from ..schemas.slurm import Options
from ..diagnostics import progress

class SLURMClusterCallback:
    """
    The SLURMClusterCallback provides a wrapper for the `dask_joqueue` 
    [SLURMCluster](https://jobqueue.dask.org/en/latest/generated/dask_jobqueue.SLURMCluster.html) 
    and the `dask.distributed` [Client](https://distributed.dask.org/en/latest/client.html) objects. 
    When a function is decorated with the `@slurm` decorator, it passes 
    the attached function to this object where it is stored as an attribute,
    `callback`. When calling a decorated function, this object is returned.

    The two principal features of this object include:

    1. It holds the necessary information to start the Dask Client which runs both 
    the [Diagnostics dashboard](https://docs.dask.org/en/latest/diagnostics-distributed.html) 
    and the [Dask scheduler](https://docs.dask.org/en/latest/scheduler-overview.html), 
    as well as to launch the Dask workers through SLURM

    2. It exposes the necessary methods for executing work and returning results   

    Attributes:
        _state: a class attribute that passes the state of a previously called decorated function on to
            the next

        options: pyndantic model containing all kwargs for initializing the Dask SLURMCluster. For more
            details see the [Options model](../decorators/slurm.md#options_model)
        
        callback: <code>@slurm</code> decorated function to be submitted to the SLURM cluster

        n_workers: number of workers to scale Dask cluster to

        show_progress: whether to show progress bar while running submitted function (currently only
            works for Dask-like functions)
        
        cluster: the SLURM cluster object with the initialized Dask scheduler

        client: the Dask client object that will connect to the Dask scheduler and manager workers - the client
            is initialized by being passed the <code>cluster</code> object
        
        mappable: a sequence of arguments to map to a given decorated function, with each element of the sequence
            being passed to a Dask worker to execute the callback with. This is equivalent to iterating through
            arguments in a for-loop and passing them to the `submit` method
        
        futures: a sequence of futures corresponding to each of the mapped elements from `mappable. These are stored
            internally to compute and return the results
    
    **Methods**:

    """

    _state: dict = {}

    def __init__(self,
                 options: Options,
                 callback: Optional[Callable[..., Any]] = None
                ):

        self.options: Options = options
        self.callback: Callable[..., Any] = callback
        
        self.n_workers: int = self.options.pop('n_workers', 1)
        self.show_progress: bool = self.options.pop('show_progress', False)
        self.options.setdefault('job_name', self.callback.__name__)
   
        self.cluster: SLURMCluster = SLURMCluster(**self.options.collect())
        self.client: Client = Client(self.cluster)
        self.cluster.scale(self.n_workers)

        self.mappable: Optional[MutableSequence[Any]] = None
        self.futures: Optional[MutableSequence[Callable[..., Any]]] = None
        

    @property
    def job_script(self):
        return self.cluster.job_script()


    @property
    def _scheduler(self):
        return self.cluster.scheduler


    @property
    def scheduler_info(self):
        return self.client.scheduler_info() 


    def add_workers(self, n_workers: int):
        """
        Scale the number of Dask workers up to n_workers. 

        Args:
            n_workers: number of dask workers to initiate in cluster
        """
        self.n_workers = n_workers
        self.cluster.scale(n_workers)
        return self
             


    def submit(self,
               pure: Optional[bool] = True, 
               **kwargs: MutableMapping[str, Any]
               ):
        """
        Submit a function to a initated cluster with workers running
        
        Args:
            pure: whether to consider the callback as a pure 
                [Python function](https://toolz.readthedocs.io/en/latest/purity.html)
            kwargs: arguments to pass to the callback when being executed if the deorated function
                takes arguments

        """

        self.job = self.client.submit(self.callback, **kwargs, pure=pure)

        if self.show_progress:
            try:
                future_res = self.job.result().persist()
                progress(future_res)
            except AttributeError:
                future_res = self.job.result()
        else:
            future_res = self.job.result()
                
        try: 
            # function returns dask object (dask array/dataframe)
            try:
                result = future_res.compute()
                return result
            finally:
                self.cluster.close()
                self.client.close()
        except AttributeError:
            # function returns non-dask object (e.g normal function)
            try:
                return future_res
            finally:
                self.cluster.close()
                self.client.close()
    

    def map(self, mappable:MutableSequence[Any]):
        """
        Map an array of arguments to the function to run, rather
        than using for-loops (this will be faster)

        Args:
            mappable: a sequence of arguments to map to a given decorated function, with each element of the sequence
            being passed to a Dask worker to execute the callback with. This is equivalent to iterating through
            arguments in a for-loop and passing them to the `submit` method

        """
        self.mappable = mappable
        self.futures = self.client.map(self.callback, self.mappable)
        return self
    
    
    def gather(self):
        """
        Works for callbacks that return non-dask objects, and should be called after `map`. 
        Dask objects, such as Arrays, DataFrame or Bags should have there own map methods.

        ⚙️ *Usage*: results:list = myfunc.map(mappable).gather()
        """
        return self.client.gather(self.futures)