#   Makefile
#

PYTHON3 := $(shell which python3)
PYTHON3_VERSION := $(shell $(PYTHON3) --version)
PACKAGE_PREFIX := stock_investing

PYFLAKES_ALL_FILES := $(shell find $(PACKAGE_PREFIX) -type f  -name '*.py' ! '(' -name '__init__.py' ')')

REQ_FILE := requirements.txt
TOOLS_REQ_FILE := requirements-tools.txt

clean:
	@echo "======================================================"
	@echo clean $(PACKAGE_PREFIX)
	@echo "======================================================"
	@rm -fR __pycache__
	@rm -fR *.pyc
	@rm -fR tmp
	@rm -fR *.zip

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
	$(PYTHON3) -m pip freeze

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

list:
	cat Makefile | grep "^[a-z]" | awk '{print $$1}' | sed "s/://g" | sort