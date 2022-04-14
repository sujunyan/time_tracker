# Time Tracker 
This is a time tracker for my personal use. Previously I used some apps to record how long I work every day. But those apps are not supported for exporting data and I want to draw some fancy graphs myself. So I am thinking of develop my own one.

This "app" is python based and I want to keep it simple and neat. It is now command line based. I am currently not sure if I want to add a simple GUI...

## Usage

Use the following command to start a recording
```[Python]
python main.py --task meeting
```
where `meeting` is a task name. One can also change the task list in [globals.py](globals.py).


## Data Analysis 

Use the following command to do the data analysis:
```[Python]
python plot.py --days 1
```
Currently, I plan to have the following features:
- Print statistics summary
- Plot pie chart
- Plot timeline
- Plot working time along date/month



