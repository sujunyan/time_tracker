import time
import sys
import pandas as pd
from datetime import datetime, timedelta
from inputimeout import inputimeout, TimeoutOccurred

def read_command(argv):
    from optparse import OptionParser
    usage_str = """
        USAGE:      python main.py <options>
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

def record(task, begin, end):
    print(f"record {task}, {begin}, {end}")
    pass

def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

def loop(t_begin):

    print("Press 'ctrl-c' to stop.")
    try: 
        while True:
            #try:
            #    s = inputimeout("\r",timeout=2)
            #except TimeoutOccurred:
            #    s = None
            #if s == 'c':
            #    break
            #elif s is not None:
            #    print("Press 'c' to stop.")

            t_diff: timedelta = datetime.now() - t_begin
            # sys.stdout.write("\r")
            t_diff_str = strfdelta(t_diff, "{hours:02d}:{minutes:02d}:{seconds:02d}")
            print(f"{t_diff_str}", flush=True, end="\r") 
            time.sleep(1)
    except KeyboardInterrupt as e:
        return

if __name__ == '__main__':
    task_list = [
        "research.code",
        "misc"
    ]
    
    opt = read_command(sys.argv[1:])
    task = opt.task

    t_begin = datetime.now()
    print(f"starting task: {task} at {t_begin}.")
    loop(t_begin) 
    t_end = datetime.now()
    t_diff = t_end - t_begin
    t_diff_tol = timedelta(minutes=1)
    if t_diff <= t_diff_tol:
        print(f"Total time {t_diff} less than {t_diff_tol}, not record it.")
    else:
        record(task, t_begin, t_end)

    # print(opt)
    print("done.")
    