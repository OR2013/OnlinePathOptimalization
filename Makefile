SHELL := /bin/bash

DOCS = docs
HEADER = "noOpt,opt,size,alpha,rate,distance"
REPEATS = 10

.PHONY: test clean simulations simulation1 simulation2 simulation3\
	simulation4 simulation5 simulation6 simulation7 docs graphs

all: docs

test:
	@export PYTHONPATH=. ; python test/graph_test.py

docs: graphs
	@cd docs/latex; \
	printf "\rGenerating docs:\t(%3d%%)" 0; \
	pdflatex documentation.tex > /dev/null; \
	mv documentation.pdf ..; \
	printf "\rGenerating docs:\t(%3d%%)" 100; \
	cd ../..; \
	echo

graphs:
	@cd docs/graphs; \
	printf "\rGenerating graphs:\t(%3d%%)" 0; \
	Rscript time_size.R simulation1 > /dev/null; \
	printf "\rGenerating graphs:\t(%3d%%)" 14; \
	Rscript time_alpha.R simulation2 100 > /dev/null; \
	printf "\rGenerating graphs:\t(%3d%%)" 29; \
	Rscript time_alpha.R simulation3 1000 > /dev/null; \
	printf "\rGenerating graphs:\t(%3d%%)" 43; \
	Rscript time_rate.R simulation4 100 > /dev/null; \
	printf "\rGenerating graphs:\t(%3d%%)" 58; \
	Rscript time_rate.R simulation5 1000 > /dev/null; \
	printf "\rGenerating graphs:\t(%3d%%)" 72; \
	Rscript time_distance.R simulation6 100 > /dev/null; \
	printf "\rGenerating graphs:\t(%3d%%)" 86; \
	Rscript time_distance.R simulation7 1000 > /dev/null; \
	printf "\rGenerating graphs:\t(%3d%%)" 100; \
	echo

simulations: simulation1 simulation2 simulation3 simulation4 simulation5

# symulacja badająca zależność czasu przejazdu od parametru 'size'
# parametr alpha = 0.05
# parametr rate = 2
# parametr max-distance = 500
simulation1:
	@mkdir -p $(DOCS)
	@echo $(HEADER) > $(DOCS)/simulations/$@.csv
	@export SUMO_HOME=/usr/share/sumo; \
	SIZES=(10 20 30 40 50 60 70 80 90 100 200 300 400 500 600 700 800 900 1000); \
	printf "\rSimulation 1:\t(%3d%%)" 0; \
	for SIZE in $${!SIZES[*]}; do \
		for (( REPEAT=0; REPEAT<$(REPEATS); REPEAT++)); do \
			python src/simulation.py --nogui -s $${SIZES[$$SIZE]} >> $(DOCS)/simulations/$@.csv; \
			printf "\rSimulation 1:\t(%3d%%)" $$((($$SIZE * $(REPEATS) + $$REPEAT + 1) * 100 / ($${#SIZES[*]} * $(REPEATS)))); \
		done; \
	done; \
	echo

# symulacja badająca zależność czasu przejazdu od parametru 'alpha'
# parametr size = 100
# parametr rate = 2
# parametr max-distance = 500
simulation2:
	@mkdir -p $(DOCS)
	@echo $(HEADER) > $(DOCS)/simulations/$@.csv
	@export SUMO_HOME=/usr/share/sumo; \
	ALPHAS=(0.01 0.02 0.05 0.1 0.2 0.5 1 2 5 10); \
	printf "\rSimulation 2:\t(%3d%%)" 0; \
	for ALPHA in $${!ALPHAS[*]}; do \
		for (( REPEAT=0; REPEAT<$(REPEATS); REPEAT++)); do \
			python src/simulation.py --nogui -s 100 -a $${ALPHAS[$$ALPHA]} >> $(DOCS)/simulations/$@.csv; \
			printf "\rSimulation 2:\t(%3d%%)" $$((($$ALPHA * $(REPEATS) + $$REPEAT + 1) * 100 / ($${#ALPHAS[*]} * $(REPEATS)))); \
		done; \
	done; \
	echo

# symulacja badająca zależność czasu przejazdu od parametru 'alpha'
# parametr size = 1000
# parametr rate = 2
# parametr max-distance = 500
simulation3:
	@mkdir -p $(DOCS)
	@echo $(HEADER) > $(DOCS)/simulations/$@.csv
	@export SUMO_HOME=/usr/share/sumo; \
	ALPHAS=(0.01 0.02 0.05 0.1 0.2 0.5 1 2 5 10); \
	printf "\rSimulation 3:\t(%3d%%)" 0; \
	for ALPHA in $${!ALPHAS[*]}; do \
		for (( REPEAT=0; REPEAT<$(REPEATS); REPEAT++)); do \
			python src/simulation.py --nogui -s 1000 -a $${ALPHAS[$$ALPHA]} >> $(DOCS)/simulations/$@.csv; \
			printf "\rSimulation 3:\t(%3d%%)" $$((($$ALPHA * $(REPEATS) + $$REPEAT + 1) * 100 / ($${#ALPHAS[*]} * $(REPEATS)))); \
		done; \
	done; \
	echo

# symulacja badająca zależność czasu przejazdu od parametru 'rate'
# parametr size = 100
# parametr alpha = 0.05
# parametr max-distance = 500
simulation4:
	@mkdir -p $(DOCS)
	@echo $(HEADER) > $(DOCS)/simulations/$@.csv
	@export SUMO_HOME=/usr/share/sumo; \
	RATES=(1 2 3 4 5 6 7 8 9 10); \
	printf "\rSimulation 4:\t(%3d%%)" 0; \
	for RATE in $${!RATES[*]}; do \
		for (( REPEAT=0; REPEAT<$(REPEATS); REPEAT++)); do \
			python src/simulation.py --nogui -s 100 -r $${RATES[$$RATE]} >> $(DOCS)/simulations/$@.csv; \
			printf "\rSimulation 4:\t(%3d%%)" $$((($$RATE * $(REPEATS) + $$REPEAT + 1) * 100 / ($${#RATES[*]} * $(REPEATS)))); \
		done; \
	done; \
	echo

# symulacja badająca zależność czasu przejazdu od parametru 'rate'
# parametr size = 1000
# parametr alpha = 0.05
# parametr max-distance = 500
simulation5:
	@mkdir -p $(DOCS)
	@echo $(HEADER) > $(DOCS)/simulations/$@.csv
	@export SUMO_HOME=/usr/share/sumo; \
	RATES=(1 2 3 4 5 6 7 8 9 10); \
	printf "\rSimulation 5:\t(%3d%%)" 0; \
	for RATE in $${!RATES[*]}; do \
		for (( REPEAT=0; REPEAT<$(REPEATS); REPEAT++)); do \
			python src/simulation.py --nogui -s 1000 -r $${RATES[$$RATE]} >> $(DOCS)/simulations/$@.csv; \
			printf "\rSimulation 5:\t(%3d%%)" $$((($$RATE * $(REPEATS) + $$REPEAT + 1) * 100 / ($${#RATES[*]} * $(REPEATS)))); \
		done; \
	done; \
	echo

# symulacja badająca zależność czasu przejazdu od parametru 'max-distance'
# parametr size = 100
# parametr alpha = 0.05
# parametr rate = 2
simulation6:
	@mkdir -p $(DOCS)
	@echo $(HEADER) > $(DOCS)/simulations/$@.csv
	@export SUMO_HOME=/usr/share/sumo; \
	DISTANCES=(200 300 400 500 700 1000 1200 1500 1700 2000); \
	printf "\rSimulation 6:\t(%3d%%)" 0; \
	for DISTANCE in $${!DISTANCES[*]}; do \
		for (( REPEAT=0; REPEAT<$(REPEATS); REPEAT++)); do \
			python src/simulation.py --nogui -s 100 -d $${DISTANCES[$$DISTANCE]} >> $(DOCS)/simulations/$@.csv; \
			printf "\rSimulation 6:\t(%3d%%)" $$((($$DISTANCE * $(REPEATS) + $$REPEAT + 1) * 100 / ($${#DISTANCES[*]} * $(REPEATS)))); \
		done; \
	done; \
	echo

# symulacja badająca zależność czasu przejazdu od parametru 'max-distance'
# parametr size = 1000
# parametr alpha = 0.05
# parametr rate = 2
simulation7:
	@mkdir -p $(DOCS)
	@echo $(HEADER) > $(DOCS)/simulations/$@.csv
	@export SUMO_HOME=/usr/share/sumo; \
	DISTANCES=(200 300 400 500 700 1000 1200 1500 1700 2000); \
	printf "\rSimulation 7:\t(%3d%%)" 0; \
	for DISTANCE in $${!DISTANCES[*]}; do \
		for (( REPEAT=0; REPEAT<$(REPEATS); REPEAT++)); do \
			python src/simulation.py --nogui -s 1000 -d $${DISTANCES[$$DISTANCE]} >> $(DOCS)/simulations/$@.csv; \
			printf "\rSimulation 7:\t(%3d%%)" $$((($$DISTANCE * $(REPEATS) + $$REPEAT + 1) * 100 / ($${#DISTANCES[*]} * $(REPEATS)))); \
		done; \
	done; \
	echo

clean:
	rm -rf src/*.pyc
	rm -rf test/*.pyc
	rm -rf config/*
	rm -rf $(DOCS)/tables/*
	rm -rf $(DOCS)/latex/*.toc
	rm -rf $(DOCS)/latex/*.aux
	rm -rf $(DOCS)/latex/*.log
	rm -rf $(DOCS)/images/*.png
	rm -i $(DOCS)/simulations/*