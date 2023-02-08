import sys
from dask.local import MultiprocessingPoolExecutor
from distributed.client import futures_of
from distributed.utils import LoopRunner
from distributed.diagnostics.progress import Progress, MultiProgress, format_time
from distributed.diagnostics.progressbar import (ProgressBar, 
                                                 ProgressWidget,
                                                 MultiProgressWidget, 
                                                 get_scheduler)
from tornado.ioloop import IOLoop
from contextlib import suppress
from rich import inspect
from tqdm import tqdm
from IPython import get_ipython


class ColorProgressBar(ProgressBar):
    """
    Extension of Dask TextProgressBar, but implementing tqdm package
    for progress bars.
    """
    def __init__(
        self,
        keys,
        scheduler=None,
        interval="100ms",
        width=40,
        loop=None,
        complete=True,
        start=True,
        **kwargs,
    ):
        super().__init__(keys, scheduler, interval, complete)
        self.width = width
        self.loop = loop or IOLoop()

        self.tqdm_pbar = None
        self.completed = 0

        self.color = kwargs.pop('color', 'GREEN')

        self.ip = get_ipython()

        if start:
            loop_runner = LoopRunner(self.loop)
            loop_runner.run_sync(self.listen)

    def _check_bar_initialized(self, all, remaining):
        if self.tqdm_pbar is None:
            self.all = all
            self.complete = all - remaining

            # Not the most robust: test progress bar in IPython Shell
            if self.ip is None:
                return tqdm(total=all, initial=self.complete, colour=self.color,
                    leave=True, dynamic_ncols=True, 
                    bar_format="{desc}: {percentage:.2f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}]")
                    
            else:
                return tqdm(total=all, initial=self.complete, colour=self.color,
                    leave=True, ncols=75,
                    bar_format="{desc}: {percentage:.2f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}]")
        else:
            return self.tqdm_pbar

    def _draw_bar(self, remaining, all, **kwargs):
        self.tqdm_pbar = self._check_bar_initialized(all, remaining)

        total_complete = all - remaining
        delta_complete = total_complete - self.complete 
        self.complete = total_complete
 
        with suppress(ValueError):
            self.tqdm_pbar.update(delta_complete)

    def _draw_stop(self, **kwargs):
        self.tqdm_pbar.close()


def progress(*futures, notebook=None, multi=True, complete=True, **kwargs):
    """
    Track the progress of futures

    This will automatically adjust it's behaviour depending of if being
    run in the console or in a IPython/Jupyter.
    """    
    futures = futures_of(futures)
    if not isinstance(futures, (set, list)):
        futures = [futures]

    ColorProgressBar(futures, complete=complete, **kwargs)
