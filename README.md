<h1 style="color: white; background-color: #af9cd9; padding: 2em 0; text-align: center">PySLURM Decorators<img align="left" width="60" height="40" src="/static/pyslurmdec.png"></h1>

Python decorator for submitting decorated Python functions to a SLURM cluster

Take a look at the documentation [here](https://fcp4agithdp02.bocad.bank-banque-canada.ca/pages/BOCAE/pyslurm_decorators/)

## General Overview
To schedule functions as jobs on a SLURM cluster, the Dask distributed and job_queue libraries are used. Currently the goal is only to launch functions locally from Edith, but the hope is to be able to remotely launch jobs from within a Python instance that can reach Edith or any other SLURM HPC. 

The design of the decorators in this project are based heavily on the methodology implemeneted by the [Click CLI library for Python](https://github.com/pallets/click). The basic steps that occur when attaching the decorator to your function are as follows:

1. A decorated function is taken as an inpute to the decorater, which processes the function and attaches it to a base class <code>SLURMClusterCallback</code> which extends the <code>JobQueueCluster</code>, both adapated from [Dask job_queue](https://github.com/dask/dask-jobqueue/tree/main/dask_jobqueue)
2. The user calls the function, which returns the SLURMClusterCallback class with the function attached. This cluster instance exposes a <code>submit_job(*args)</code> method that submits the job to the cluster and takes any <code>args</code> for the function.
3. If the function returns a result, the result is retrieved.
  
## Components
### Component Diagram
<img align="centered" width="900" height="950" src="/static/pyslurm_decorators_components.png"></img>

#### Notes
---

### Dependency Graph
<div style="text-align:center"><img align="centered" width="1500" height="2500" src="/static/pyslurm_decorators.svg"></div>

#### Notes

## Usage

### @slurm
