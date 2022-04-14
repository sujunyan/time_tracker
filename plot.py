from datetime import datetime, timedelta
import pathlib
import pandas as pd
import numpy as np
from util import strfdelta, get_data_dir

def get_data(data_dir: pathlib.Path):
    csv_path_list = list(data_dir.glob("*.csv"))
    df = pd.DataFrame()
    for csv_path in csv_path_list:
        df1 = pd.read_csv(csv_path,sep=",",parse_dates=["start", "end"], )
        df = df.append(df1)
    df = df.set_index("start")
    return df

def get_data_dict(df: pd.DataFrame, t_begin):
    """
    t_begin: The begin time from which to process the data
    return: {task: total time}
    """
    def task_time(task):
        """
        return: float in seconds
        """
        mask = df1["task"] == task
        df2 = df1.loc[mask]
        end_time_arr = np.array(df2["end"])
        start_time_arr = np.array(df2.index)
        total_time = np.sum(end_time_arr - start_time_arr)
        return total_time/ np.timedelta64(1,'s')
        
    df1 = df[t_begin:]
    task_set = set(df["task"])
    task_time_list = [task_time(task) for task in task_set]
    for (task, t) in zip(task_set, task_time_list):
        t = timedelta(seconds=t)
        t_str = strfdelta(t, "{hours:02d} hours {minutes:02d} minutes")
        print(f"For {task}, {t_str}")
        pass
    print("done")



if __name__ == "__main__":
    data_dir = get_data_dir()
    df = get_data(data_dir)
    t_begin = datetime(year=2022, month=4, day=1)
    get_data_dict(df, t_begin)
    print("plot.py done.")
