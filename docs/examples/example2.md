# <a name="example2"></a> Using the <code>@slurm</code> Decorator to Estimate Pi

<div style="text-align:center">
<img src="https://upload.wikimedia.org/wikipedia/commons/8/84/Pi_30K.gif" 
     width="50%" 
     align=center
     alt="PI monte-carlo estimate">(https://en.wikipedia.org/wiki/Pi#Monte_Carlo_methods)
</div>

Here we explore the usage of the `@slurm` decorator with a simple function that returns the result of a computation using Dask Arrays. When a function returns a Dask-like object such as this, we refer to it as a Dask-like function. Otherwise, the function is considered a non-Dask-like function.

The `@slurm` decorated takes arguments that define resources assigned to the SLURM job that will execute your function. The options that can be specified are detailed [here](../decorators/slurm.md#options_model).

In the previous example, we manually initialized the `Options` model and the `SLURMClusterCallback` class to submit the same function to a SLURM cluster. In this example, the `@slurm` decorator takes care of that work for us by attaching the decorated function to an instance of `SLURMClusterCallback` and using the defined arguments within the decorator to define the `Options` model. Together, this process transforms your function into an initialized instance of the `SLURMClusterCallback` class, exposing along with it all of the methods and information needed to submit the function as a job to a SLURM cluster.

The source code for this example can be found at `examples/decorated_function`.


## Running the Example from the Cloned Repository
*See a Jupyter Notebook code sample for this example [here](../code_samples/example2.ipynb) if you're not interested in runnning it yourself*

📍 Move into the example directory and load <code>anaconda3/2021.05</code> (or your favourite version, as long as python >= 3.6)

<div class="termy">

```console
$ cd examples/decorated_function/
$ module load anaconda3/2021.05
```
</div>
</br>

📍 **Unload the proxy** (or you won't be able to connect to the API)

<div class="termy">

```console
$ module unload proxy
```

</div>
</br>

📍 Execute the code

<div class="termy">

```console
// to submit the function as a job to a SLURM cluster, print a progress bar
// and return/print the result
$ python3 decorated_function.py
```

</div>