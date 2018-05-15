#   Makefile
#

PYTHON3 := $(shell which python3)
PYTHON3_VERSION := $(shell $(PYTHON3) --version)
PACKAGE_PREFIX := stock_investing
API_KEY = ${QUANDL_WIKI_API_KEY}

PYFLAKES_ALL_FILES := $(shell find $(PACKAGE_PREFIX) -type f  -name '*.py' ! '(' -name '__init__.py' ')')

REQ_FILE := requirements.txt
TOOLS_REQ_FILE := requirements-tools.txt

check-env:
ifndef QUANDL_WIKI_API_KEY
	$(error QUANDL_WIKI_API_KEY is undefined)
endif

clean:
	@echo "======================================================"
	@echo clean $(PACKAGE_PREFIX)
	@echo "======================================================"
	@rm -fR __pycache__
	@rm -fR *.pyc
	@rm -fR tmp
	@rm -fR *.zip

install-memcached:
	@echo "======================================================"
	@echo install-memcached
	@echo "======================================================"
	brew update
	brew install memcached

upgrade-memcached:
	@echo "======================================================"
	@echo upgrade-memcached
	@echo "======================================================"
	@brew upgrade memcached

flush-memcached:
	@echo "======================================================"
	@echo flush-memcached
	@echo "======================================================"
	@echo 'flush_all' | nc localhost 11211

install-pip:
	@echo "======================================================"
	@echo install-pip
	@echo "======================================================"
	$(PYTHON3) tools/get-pip.py
	$(PYTHON3) -m pip install --upgrade pip

install-freeze:
	@echo "======================================================"
	@echo install-freeze
	@echo "======================================================"
	$(PYTHON3) -m pip install --upgrade pip
	$(PYTHON3) -m pip freeze | grep pyfortified-cache
	$(PYTHON3) -m pip freeze | grep pyfortified-logging
	$(PYTHON3) -m pip freeze | grep pyfortified-requests
	$(PYTHON3) -m pip freeze | grep pymemcache-client
	$(PYTHON3) -m pip freeze | grep ujson
	$(PYTHON3) -m pip freeze | grep pandas

install-requirements: $(REQ_FILE)
	@echo "======================================================"
	@echo requirements $(PACKAGE_PREFIX)
	@echo "======================================================"
	$(PYTHON3) -m pip install --upgrade pip
	$(PYTHON3) -m pip install --upgrade -r $(REQ_FILE)

install-tools-requirements: $(TOOLS_REQ_FILE)
	@echo "======================================================"
	@echo tools-requirements $(PACKAGE_PREFIX)
	@echo "======================================================"
	$(PYTHON3) -m pip install --upgrade -r $(TOOLS_REQ_FILE)

pyflakes: install-tools-requirements
	@echo "======================================================"
	@echo pyflakes $(PACKAGE_PREFIX)
	@echo "======================================================"
	$(PYTHON3) -m pip install --upgrade pyflakes
	$(PYTHON3) -m pyflakes $(PYFLAKES_ALL_FILES)


run-example-avg-monthly-open-close: check-env
	@echo "======================================================"
	@echo run-example-avg-monthly-open-close
	@echo "======================================================"
	$(PYTHON3) stock_investing/worker.py --api-key '$(API_KEY)' --start-date '2017-01-01' --end-date '2017-06-30' --avg-monthly-open-close

run-example-max-daily-profit: check-env
	@echo "======================================================"
	@echo run-example-max-daily-profit
	@echo "======================================================"
	$(PYTHON3) stock_investing/worker.py --api-key '$(API_KEY)' --start-date '2017-01-01' --end-date '2017-06-30' --max-daily-profit

run-example-busy-day: check-env
	@echo "======================================================"
	@echo run-example-busy-day
	@echo "======================================================"
	$(PYTHON3) stock_investing/worker.py --api-key '$(API_KEY)' --start-date '2017-01-01' --end-date '2017-06-30' --busy-day

run-example-biggest-loser: check-env
	@echo "======================================================"
	@echo run-example-biggest-loser
	@echo "======================================================"
	$(PYTHON3) stock_investing/worker.py --api-key '$(API_KEY)' --start-date '2017-01-01' --end-date '2017-06-30' --biggest-loser

list:
	cat Makefile | grep "^[a-z]" | awk '{print $$1}' | sed "s/://g" | sort
