plot:
	python plot.py --days 1 --tabdays 14 --bardays 14

plotMonth:
	python plot.py --days 30 --tabdays 30 --bardays 30

plotWeek:
	python plot.py --days 7 --tabdays 14 --bardays 14

plotAll:
	python plot.py --all 

plotAllCN:
	python plot.py --all --cn



# Some short-cuts
###############################
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

think:
	python main.py --task thinking

ta:
	python main.py --task TA

startup:
	python main.py --task startup
