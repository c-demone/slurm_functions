# <a name="example3"></a>Using <code>.map()</code> to Execute Function for Multiple Inputs in Parallel

Sometimes it may be useful to run a given function a series of inputs. A good example is running a for loop. For non-Dask-like functions `.map()`provides a means of executing a single function on an array of inputs in parallel, returning back an array of corresponding outputs. *For Dask-like functions, the `.map()` method is not currently implemented.* However, Dask objects such as Arrays, DataFrames, or Bags have there own mapping methods that can be applied within a decorated function, without the need to the `.map()` method exposed by the `@slurm` decorator.

The `.map()` is exposed from the [SLURMClusterCallback](../callbacks/slurmcluster.md#slurm_clustercb) class, that is returned when calling a `@slurm` decorated function.

The source code for this example can be found at `examples/map_function`.

## Running the Example from the Cloned Repository
*See a Jupyter Notebook code sample for this example [here](../code_samples/example3.ipynb) if you're not interested in runnning it yourself*

📍 Move into the example directory and load <code>anaconda3/2021.05</code> (or your favourite version, as long as python >= 3.6)

<div class="termy">

```console
$ cd examples/map_function/
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
// to submit the function as a job to a SLURM cluster and return/print the result
$ python3 map_function.py
```

</div>