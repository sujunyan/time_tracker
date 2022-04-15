import pathlib
import time
import sys
import pandas as pd
from datetime import datetime, timedelta
import platform
from util import get_data_dir, strfdelta
from globals import task_list

def read_command(argv):
    from optparse import OptionParser
    usage_str = """
        USAGE:      python main.py --task [taskname]
        """
    parser = OptionParser(usage_str)
    parser.add_option('--task', dest='task', type=str)
    # parser.add_option('--plot', dest='plot', action='store_true', default=False)
    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    if not options.task:
        parser.error("Task name not given")

    if options.task not in task_list:
        parser.error(f"The task {options.task} not in the task list: {task_list}!")

    return options

def record(task, start, end, data_dir: pathlib.Path):
    print(f"record {task}, {start}, {end}")
    pc_name = platform.node()
    data_path = data_dir.joinpath(f"{pc_name}.csv")
    data_dict = {
        "task" : [task],
        "start": [start],
        "end": [end]
    }
    if not data_path.exists():
        df = pd.DataFrame(columns=["task", "start", "end"])
    else:
        df = pd.read_csv(data_path)
    df2 = pd.DataFrame(data_dict)
    df1 = pd.concat([df, df2])
    # df1 = df.append(data_dict, ignore_index=True)
    df1.to_csv(data_path, sep=",", index=False)


def loop(t_begin):

    print("Press 'ctrl-c' to stop.")
    try: 
        while True:
            t_diff: timedelta = datetime.now() - t_begin
            # sys.stdout.write("\r")
            t_diff_str = strfdelta(t_diff)
            print(f"{t_diff_str}", flush=True, end="\r") 
            time.sleep(1)
    except KeyboardInterrupt as e:
        return

if __name__ == '__main__':

    data_dir = get_data_dir()
    
    opt = read_command(sys.argv[1:])
    task = opt.task

    t_begin = datetime.now()
    print(f"starting task: {task} at {t_begin}.")
    loop(t_begin) 
    t_end = datetime.now()
    t_diff = t_end - t_begin
    t_diff_tol = timedelta(minutes=0, seconds=0)
    if t_diff <= t_diff_tol:
        print(f"Total time {t_diff} less than {t_diff_tol}, not record it.")
    else:
        record(task, t_begin, t_end, data_dir)

    # print(opt)
    print("done.")
    