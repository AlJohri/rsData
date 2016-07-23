all: .test
	
.test:
	python -m unittest discover -p unit_test*.py

dbmodel:
	python -m pwiz -e sqlite house.db > DB_models.py
