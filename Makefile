plot:
	python plot.py --days 1 --tabdays 14 --bardays 14 --nots

plotMonth:
	python plot.py --days 30 --tabdays 30 --bardays 30

plotWeek:
	python plot.py --days 7 --tabdays 14 --bardays 14

plotYearCN:
	python plot.py --days 365 --cn

plotAll:
	python plot.py --all 

plotAllCN:
	python plot.py --all --cn



# Some short-cuts
###############################

lang:
	python main.py --task language

code:
	python main.py --task code

figure:
	python main.py --task figure

write:
	python main.py --task writing

pre:
	python main.py --task presentation

meet:
	python main.py --task meeting

read:
	python main.py --task reading

misc:
	python main.py --task misc

job:
	python main.py --task job

think:
	python main.py --task thinking

ta:
	python main.py --task TA

startup:
	python main.py --task startup
