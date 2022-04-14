import pathlib

def strfdelta(tdelta, fmt="{hours:02d}:{minutes:02d}:{seconds:02d}"):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

def get_data_dir():
    cur_dir = pathlib.Path(__file__).parent.resolve()
    data_dir = cur_dir.joinpath("time_tracker_data")
    return data_dir