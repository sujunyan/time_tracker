# Time Tracker 
This is a time tracker for my personal use. Previously I used pomotodo to record how long I work every day. But it does not support for exporting data. I want to draw some fancy graphs in a more flexible way. So I am thinking of developing my own one.

This "app" is python based and I want to keep it simple and neat. It is now command line based. I am currently not sure if I want to add a simple GUI...

## Usage

Use the following command to start a recording
```[Python]
python main.py --task meeting
```
where `meeting` is a task name. One can also change the task list in [config.py](config.py).

Some shortcut command can also be found in the [Makefile](Makefile).

## Data Analysis 

Use the following command to do the data analysis:
```[Python]
python plot.py --days 1
```
All the figures are stored in the [figs/](figs/) folder.
It has the following features:
### Print statistics summary
```
Statistics for previous 3 days
[TA        ]:    03 hours 42 minutes
[code      ]:    02 hours 05 minutes
[meeting   ]:    00 hours 31 minutes
[misc      ]:    01 hours 02 minutes
[presentation]:  02 hours 09 minutes
[reading   ]:    01 hours 58 minutes
[writing   ]:    00 hours 56 minutes
[Total time]:    12 hours 27 minutes
[Time per day]:  04 hours 09 minutes
```
### Plot pie chart

<img src="figs/pie.png" width="400">

### Plot timetable

<img src="figs/timetable.png" width="400">

### Plot working time along date/month (timebar)

<img src="figs/timebar.png" width="400">

