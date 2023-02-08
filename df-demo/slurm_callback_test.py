import sys
import pathlib
from rich import inspect

sys.path.append(str(pathlib.Path(__file__).parent.resolve().parent.absolute()))
from pyslurm_decorators import SLURMClusterCallback
from pyslurm_decorators import slurm

# more of an example than a test currently

cluster = SLURMClusterCallback(
        walltime="00:02:00",
        cores=2,
        processes=1,
        memory="2GB",
        scheduler_options={"host": "10.54.0.2"},
        env_extra=['module load anaconda3/2020.02']
    )

print(cluster.job_script())

#QUEUE_WAIT=60
#with SLURMClusterCallback(cores=2, memory="2GB") as cluster:
    #print(cluster.job_cpu)
    #with Client(cluster) as client:
    #    future = client.submit(lambda x: x +1, 10)
    #    client.wait_for_workers(1)
    #    print(future.result(QUEUE_WAIT))


#cluster = SLURMClusterCallback()
#print(cluster)
#inspect(cluster, all=True)


@slurm(cores=2, memory="2GB", env_extra=['module load gcc/10.1.0', 'module load java'])
def my_test_func():
    print("Hello")

cluster = my_test_func

inspect(cluster, all=True)
print(cluster.job_script())