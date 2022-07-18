from datetime import datetime, timedelta, date
from email.policy import default
import pathlib
import pandas as pd
import numpy as np
from util import strfdelta
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
from math import ceil, floor

import config
import util

def get_data(data_dir: pathlib.Path):
    csv_path_list = list(data_dir.glob("*.csv"))
    df = pd.DataFrame()
    for csv_path in csv_path_list:
        df1 = pd.read_csv(csv_path,sep=",",parse_dates=["start", "end"], )
        df = pd.concat([df, df1])
    # df = df.set_index("start")
    return df

class DataProcessor:
    def __init__(self, opt) -> None:
        self.opt = opt
        data_dir = util.get_data_dir()
        df = get_data(data_dir)
        self.df = df
        self.days = min(opt.days, self.total_days)
        if opt.all:
            self.days = self.total_days
    
    def slice_data(self, n):
        """
        slice data for previous n days
        """
        df = self.df
        t_begin = util.today() - timedelta(days=n-1)
        t_end = df["start"].max()
        mask = (df["start"] >= t_begin) & (df["start"] <= t_end)
        df1 = df.loc[mask]
        return df1
    
    def task_time(self, task, n):
        """
        n: analyze data for n days
        return: float in seconds
        """
        df = self.slice_data(n)
        mask = df["task"] == task
        df2 = df.loc[mask]
        end_time_arr = np.array(df2["end"])
        start_time_arr = np.array(df2["start"])
        total_time = np.sum(end_time_arr - start_time_arr)
        return total_time/ np.timedelta64(1,'s')

    def task_time_list(self, n=None):
        if n is None:
            n = self.days
        l = [self.task_time(task, n) for task in self.task_set]
        return l

    @property
    def task_set(self):
        l = sorted(list(set(self.df["task"])))
        return [x.split(".")[0] for x in l]
    
    @property
    def task_labels(self):
        if self.opt.cn:
            return [ config.trans_dict_cn[task] for task in self.task_set]
        else:
            return self.task_set
    
    @property
    def total_days(self):
        t = self.df["end"].max() - self.df["start"].min()
        return t.days + 1
    
    @property
    def color_dict(self):
        n = len(self.task_set)
        z = zip(self.task_set, config.color_list[:n])
        return dict(z)

    def print_stat(self):
        print(f"Statistics for previous {self.days} days")
        fmt = "{hours:3d} hours {minutes:02d} minutes"
        task_time_list = [timedelta(seconds=t) for t in self.task_time_list(self.days)]
        for (task, t) in zip(self.task_set, task_time_list):
            t_str = strfdelta(t, fmt)
            print(f"[{task:10s}]:\t {t_str}")

        total = np.sum(task_time_list)
        t_str = strfdelta(total, fmt)
        print(f"[Total time]:\t {t_str}")
        t_str = strfdelta(total/self.days, fmt)
        print(f"[Time per day]:\t {t_str}")
    
    def plot_pie(self):
        """
        plot pie chart
        refer to https://matplotlib.org/3.1.1/gallery/pie_and_polar_charts/pie_and_donut_labels.html#sphx-glr-gallery-pie-and-polar-charts-pie-and-donut-labels-py
        """
        if self.df.empty:
            print("Empty data frame, not plot pie chart.")
            return

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(aspect="equal"))
        # The offset 
        fmt = "{hours:02d} h {minutes:02d} m"
        def func(pct):
            total = np.sum(self.task_time_list())
            #str_list = [f"{t:.1f}" for t in self.task_time_list()]
            #tar_s = f"{pct/100*total:.1f}"
            for it,t in enumerate(self.task_time_list()):
                tt = pct/100.0*total
                if abs(t-tt) <= 1e-1:
                    return text(it)
            return "NaN"
            # return text(idx)

        def text(i):
            total = np.sum(self.task_time_list())
            pct = self.task_time_list()[i] / total * 100
            # If it is less than 1%, do not show it.
            if pct < 1:
                return ""
            task = self.task_labels[i]
            t = timedelta(seconds=self.task_time_list()[i])
            t_str = strfdelta(t, fmt)
            return f"{task}\n{t_str}"
        
        def time2str(t):
            return strfdelta(t, fmt)

        ntask = len(self.task_set)
        explode = np.zeros(len(self.task_set))

        wedges, texts, autotext = ax.pie(self.task_time_list(), explode=explode, wedgeprops=dict(width=1.0), startangle=-90, colors=config.color_list, autopct=func, shadow=False, labeldistance=None, labels=[text(i) for i in range(ntask)], pctdistance=0.8)

        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        total = np.sum(self.task_time_list())
        avg_time = total / self.days
        # ax.legend()
        days = self.days
        title = f"Total: {time2str(total)}  Average: {time2str(avg_time)} \nfor " + ("1 day" if days == 1 else f"{days} days")
        ax.set_title(title, pad=6, y=-0.1)
        fig.subplots_adjust(bottom=0.15, left=-0.05, right=1.0, top=1.0)        
        #fig.suptitle(f"Total: {t_str}", verticalalignment='bottom')
        self.savefig(fig, f"pie.{self.days}day.png")
    
    def savefig(self, fig, name):
        # fig.subplots_adjust(bottom=0.15, left=0.1, right=0.99, top=0.97, wspace=0.25, hspace=0)
        fig_dir = util.get_fig_dir()
        fig_path = fig_dir.joinpath(name)
        fig.savefig(fig_path, dpi=300)
    
    def get_one_day(self, date: datetime):
        """
        get data for one day
        """
        start = date.replace(hour=0, minute=0, second=0)
        end = date.replace(hour=23, minute=59, second=59)
        df_start_vec = self.df["start"]
        mask = (df_start_vec >= start) & (df_start_vec <= end)
        return self.df.loc[mask]
    
    def date_list(self, n):
        end_date = util.today()
        start_date = end_date - timedelta(days=n)
        date_list = [start_date + timedelta(days=iday) for iday in range(1,n+1)]
        return date_list
    
    def plot_timebar(self, n_day):
        """
        plot timebar for n days
        """
        fig, ax = plt.subplots(figsize=(n_day/1.5,3))
        date_list = self.date_list(n_day)
        
        t_list = []
        for iday, date in enumerate(date_list):
            df = self.get_one_day(date)
            if df.empty:
                t_list.append(0)
                continue
            t = np.sum(df["end"] - df["start"])
            t_list.append(t.seconds/3600)
        ax.set_ylabel("hours")
        color = ["#49a2e9", config.color_list[2]][1]
        x = range(0,n_day)
        ax.bar(x, t_list, width=0.5, color=color)
        ax.set_xticks(range(0,n_day))
        ax.yaxis.grid(ls='--')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_xticklabels([d.strftime("%m/%d") for d in date_list])
        fig.subplots_adjust(bottom=0.10, left=0.08, right=0.99, top=0.97)
        self.savefig(fig, f"timebar.{n_day}days.png")
    
    def plot_timetable(self, days=7):
        fig, ax = plt.subplots(figsize=(days/1.5,6))
        legend_dict = {}
        date_list = self.date_list(days)
        for iday, date in enumerate(date_list):
            df = self.get_one_day(date)
            if df.empty:
                continue
            for i,row in df.iterrows():
                xlen = 0.25
                x = [iday+1-xlen, iday+1+xlen]
                task = row["task"]
                start = (row["start"] - date).seconds
                end = (row["end"] - date).seconds
                y1 = [start, start]
                y2 = [end, end]
                color = self.color_dict[task]
                handle = ax.fill_between(x,y1,y2, color=color, label=task)
                legend_dict[task] = handle
            # print(f"For date {date}, df: {df}")
        ax.set_xticks(range(1,days+1))
        ax.set_xticklabels([d.strftime("%m/%d\n%a") for d in date_list])
        ax.invert_yaxis()
        ax.yaxis.grid(ls='--')
        
        ax.legend(labels=legend_dict.keys(), handles=legend_dict.values(), loc='center', bbox_to_anchor=(0.5,-0.14), ncol=ceil(len(legend_dict)/2), frameon=False)
        # Need to save twice to get the ytickslabels...
        # self.savefig(fig, f"timetable.png")

        def tick2label(tick):
            return strfdelta(tick,fmt="{hours:02d}:{minutes:02d}")
        
        def get_yticks():
            # yticks = ax.get_yticks()
            ymin,ymax = ax.get_ylim()
            max_y = round(ymin/3600.0)*3600
            min_y = round(ymax/3600.0)*3600
            max_y = min(max_y, 24*3600)
            min_y = max(min_y, 0)
            yticks = np.arange(min_y, max_y, 7200)
            # offset = 7200
            # ax.set_ylim((max_y+offset, min_y-offset))
            return yticks

        yticks = get_yticks()
        yticklabels = [tick2label(t) for t in yticks]
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)

        fig.subplots_adjust(bottom=0.15, left=0.10, right=0.99, top=0.97)
        self.savefig(fig, f"timetable.{days}days.png")

def read_command(argv):
    from optparse import OptionParser
    usage_str = """
        USAGE:      python main.py --task [taskname]
        """
    parser = OptionParser(usage_str)
    # days for statistic print and pie plot
    parser.add_option('--days', dest='days', type=int, default=1)
    parser.add_option('--tabdays', dest='tabdays', type=int, default=7)
    parser.add_option('--bardays', dest='bardays', type=int, default=7)
    parser.add_option('--cn', dest='cn', action="store_true", default=False)
    # plot all days
    parser.add_option('--all', dest='all', action='store_true', default=False)
    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
   
    return options


if __name__ == "__main__":
    opt = read_command(sys.argv[1:])
    if opt.cn:
        mpl.rc("font", family="sans", serif="SimHei")
        #mpl.rcParams["font.sans-serif"] = ["KaiTi"]
    t_begin = util.today()
    dp = DataProcessor(opt)
    print(dp.total_days)
    dp.print_stat()
    dp.plot_pie()
    dp.plot_timetable(days=opt.tabdays)
    dp.plot_timebar(opt.bardays)
    print("plot.py done.")
