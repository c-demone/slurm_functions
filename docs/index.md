<p align="center">
  <img width=600px height=600px, src=img/pyslurm-decorators-logo.png>
</p>

---
**<code>pyslurm_decorators</code> - Submit Python Functions to a SLURM Cluster**
---
<code>pyslurm_decorators</code> is a Python library that provides a set of useful decorators for submitting Python functions as jobs to a SLURM cluster. The hope is to allow certain compute-heavy functions to be offloaded to a SLURM cluster, while carrying out smaller work locally. 

The decorators are built on the Dask library, which was built as extension to Numpy arrays and Pandas Dataframes for managing large datasets. The dependency graph below shows hows `pyslurm_decorators` is dependent on the different components of dask including:

1. `dask`: provides all of the basic functionality of dask including Arrays, DataFrames, and Bags as well as some non-distributed diagnostic tools
2. `distributed`: where most of the code for running distributed workloads is found: this is where the distributed task scheduler lives along with distributed diagnostics
3. `dask_jobqueue`: deployment of Dask distributed library on batch job queueing systems such as PBS, SLURM, or SGE.


<p align="center">
  <img src=img/pyslurm_decorators_deps.png />
</p>


Daks is comparable to Apache Spark/PySpark, in that they both allow you to work with large datasets using familiar constructs such as `DataFrames`. However, Apache Spark is a Java/Scala project and ivolves starting workers as JVM processes whereas Dask can launch it's workers as batch processes through an appropriate batch scheduler, such as SLURM. While Spark is a full platform, including machine learning and data streaming in a adddition to data processing features, Dask is only built for data processing. In contrast to Dask, however, Apache Spark Arrays/DataFrames in PySpark are built as APIs for the Python Numpy/Pandas libraries rather than extensions to them. As a result, while Dask may not include machine learning libraries of it's own it does integrate well with most popular Python libraries such as [Scikit-Learn](https://scikit-learn.org/stable/) or [Keras](https://keras.io/). For data streaming Dask can be integrated with other Python libraries such as [Streamz](https://streamz.readthedocs.io/en/latest/). An online slide presentation is available that looks into [using the Streamz library with Dask for data streaming](https://matthewrocklin.com/slides/pydata-nyc-2017.html#/)

Since the decorators are built on Dask, they should in principal be applicable to both Dask and non-Dask workloads. In other words, you should be able to create functions that utilize Dask objects such as Arrays, DataFrames, or Bags and they should work equally as well as a function that return `"Hello World!"` as a string. This also means other Python libraries that are built on Dask can be utilized within a decorated function.

📝 **Note**: Currently only works when running locally on a SLURM HPC (e.g. Edith)

---
📋 **Key Features**
---

- [x] Provides `@slurm` decorator that will submit decorated function to a SLURM cluster as defined by the user

- [x] Allows working with Dask without having to iniate clusters manually

- [x] Enables off-loading of compute-heavy Python functions to a SLURM HPC, return results and pass on to other parts of your 
script that may be run locally.

- [x] Provides an in-depth view of your function's resource usage through the Dask dashboard that is initiated when calling your decorated fiunction.

**Note**: This project is still under development.

---
**Quickstart**
--
Clone the repository and try out some examples

📍 Move into the repo and load <code>anaconda3/2021.05</code> (or your favourite version, as long as python >= 3.6)

<div class="termy">

```console
$ cd pyslurm_decorators
$ module load anaconda3/2021.05
```

</div>


📍 Ensure the proxy is loaded and install all requirements for slurmjobs

<div class="termy">

```console
$ module load proxy
$ pip3 install --user -r requirements.txt
---> 100%
```
</div>

📍 Once all requirements are installed, the proxy should be unloaded.
<div class="termy">

```console
$ module unload proxy
```

</div>

📍 Then try some examples in the `examples` directory
<div class="termy">

```console
$ cd examples
```

</div>


## TODO
- [ ] Unit tests
- [ ] Find robust method for differentiating between Dask-like functions and non-Dask (normal) functions.
- [ ] Look into how to expose/utilize Dask distributed diagnostics
- [ ] Look into Dask Delayed for creating task graphs from regular functions (chaining functions together)