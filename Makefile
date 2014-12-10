# This Makefile is the template for you to edit. You have to modify it so that we can run your strategy.
# Please note that all parameters could change.
PASS_WD=s5PMHD50Tb
NODE_LIMIT=300

all:
	python3 main.py $(PASS_WD) $(NODE_LIMIT)

clean:
	rm record.gpickle
