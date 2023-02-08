# <a name="example1"></a>Exploring the <code>SLURMClusterCallback</code> Object

In this example, we take a closer look at the `SLURMClusterCallback`object. This is the object that your decorated function is both stored in as a callback and returned when calling your function. For more details on the methods and attributes of this class, you can look [here](../callbacks/slurmcluster.md).

The code in this example demonstrates what the decorator is doing behind the scenes when you attach it to a function in your code.

The source code for this example can be found at `examples/slurmclustercallback`.

## Running the Example from the Cloned Repository
*See a Jupyter Notebook code sample for this example [here](../code_samples/example1.ipynb) if you're not interested in runnning it yourself*

📍 Move into the example directory and load <code>anaconda3/2021.05</code> (or your favourite version, as long as python >= 3.6)

<div class="termy">

```console
$ cd examples/slurmclustercallback/
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
// to view the object that would be returned when calling a decorated function
$ python3 slurmclustercallback.py
   
// to view the cluster object returned and submit a function as a job to the cluster
$ python3 slurmclustercallback.py -s
```

</div>