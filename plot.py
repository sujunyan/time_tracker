from datetime import datetime, timedelta, date
import pathlib
import pandas as pd
import numpy as np
from util import strfdelta
import sys
import matplotlib.pyplot as plt

import globals
import util

def get_data(data_dir: pathlib.Path, t_begin, t_end=datetime.max):
    csv_path_list = list(data_dir.glob("*.csv"))
    df = pd.DataFrame()
    for csv_path in csv_path_list:
        df1 = pd.read_csv(csv_path,sep=",",parse_dates=["start", "end"], )
        df = df.append(df1)
    df = df.set_index("start")
    if t_end > df.index.max():
        t_end = df.index.max()
    return df[t_begin: t_end]

class DataProcessor:
    def __init__(self, opt) -> None:
        self.opt = opt
        data_dir = util.get_data_dir()
        self.t_begin = util.today() - timedelta(days=opt.days-1)
        self.t_end = datetime.max
        self.df = get_data(data_dir, self.t_begin, self.t_end)
    
    def task_time(self, task):
        """
        return: float in seconds
        """
        mask = self.df["task"] == task
        df2 = self.df.loc[mask]
        end_time_arr = np.array(df2["end"])
        start_time_arr = np.array(df2.index)
        total_time = np.sum(end_time_arr - start_time_arr)
        return total_time/ np.timedelta64(1,'s')
    
    @property
    def task_set(self):
        return sorted(list(set(self.df["task"])))
    
    @property
    def task_time_list(self):
        l = [self.task_time(task) for task in self.task_set]
        return l
    
    def print_stat(self):
        print(f"Statistics for previous {self.opt.days} days")
        task_time_list = [timedelta(seconds=t) for t in self.task_time_list]
        for (task, t) in zip(self.task_set, task_time_list):
            t_str = strfdelta(t, "{hours:02d} hours {minutes:02d} minutes")
            print(f"[{task:10s}]:\t {t_str}")

        t_str = strfdelta(np.sum(task_time_list), "{hours:02d} hours {minutes:02d} minutes")
        print(f"[Total Time]:\t {t_str}")
        print("done")
    
    def plot_pie(self):
        """
        plot pie chart
        """
        fig, ax = plt.subplots()
        # The offset 
        explode = np.zeros(len(self.task_set))
        ax.pie(self.task_time_list, explode=explode, labels=self.task_set, shadow=True, startangle=0, colors=globals.color_list) #, autopct='%1.1f%%')
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        self.savefig(fig, "pie.png")
    
    def savefig(self, fig, name):
        fig_dir = util.get_fig_dir()
        fig_path = fig_dir.joinpath(name)
        fig.savefig(fig_path)

def read_command(argv):
    from optparse import OptionParser
    usage_str = """
        USAGE:      python main.py --task [taskname]
        """
    parser = OptionParser(usage_str)
    parser.add_option('--days', dest='days', type=int, default=1)
    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
   
    return options


if __name__ == "__main__":
    opt = read_command(sys.argv[1:])
    t_begin = util.today()
    dp = DataProcessor(opt)
    dp.print_stat()
    dp.plot_pie()
    print("plot.py done.")
