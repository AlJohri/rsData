all:
	$(MAKE) -C dataBase 
	$(MAKE) -C crawlers
	$(MAKE) -C analyze

