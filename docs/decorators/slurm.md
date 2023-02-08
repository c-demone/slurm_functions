# <a name='slurm_decorator'></a>SLURM Decorator

The slurm decorator works by taking the function it decorates as an argument and attaching to *callback* class, such as the [`SLURMClusterCallback` class](../callbacks/slurmcluster.md). Arguments defined within the decorator are also passed to the *callback* class and used for defining job specific options for running the decorated function, or callback, as a job in a SLURM cluster. When calling a function decorated by the `@slurm` decorator, it is the attached *callback* class which is actually being called along with all of the information it stores and the methods it exposes. Amongst these methods are the `submit` methods that submits the attached function as a job to a SLURM cluster.

![SLURM decorator process](/img/pyslurm_decorators_process.png)

::: pyslurm_decorators.lib.decorators.slurm

The helper function `_initiate_slurm_cluster` attaches the callback function and defined attributes for the job to the [`SLURMClusterCallback` class](../callbacks/slurmcluster.md)
::: pyslurm_decorators.lib.decorators._initiate_slurm_cluster

##<a name="options_model"></a><code>Options</code> model
::: pyslurm_decorators.schemas.slurm.Options