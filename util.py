import pathlib
from datetime import datetime, timedelta
import numpy as np

def strfdelta(tdelta, fmt="{hours:02d}:{minutes:02d}:{seconds:02d}"):
    if np.isscalar(tdelta):
        tdelta = timedelta(seconds=float(tdelta))
    # d = {"days": tdelta.days}
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(int(tdelta.total_seconds()), 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

def get_data_dir():
    cur_dir = pathlib.Path(__file__).parent.resolve()
    data_dir = cur_dir.joinpath("time_tracker_data")
    return data_dir

def get_fig_dir():
    cur_dir = pathlib.Path(__file__).parent.resolve()
    fig_dir = cur_dir.joinpath("figs")
    return fig_dir

def today():
    t = datetime.today() 
    t = t.replace(hour=0,second=0,minute=0,microsecond=0)
    return t