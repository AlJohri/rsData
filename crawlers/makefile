
all: .test

.test:
	python -m unittest discover -p unit_test*.py


run:
	scrapy crawl njmls -o items.json  2>&1 | tee debug.log
