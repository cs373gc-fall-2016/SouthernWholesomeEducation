.DEFAULT_GOAL := test

FILES :=                              \
    .gitignore                        \
    .travis.yml                       \
    makefile                          \
    apiary.apib						  \
    project/IDB1.py					  \
    project/models.py				  \
    project/tests.py				  \
    requirements.txt				  \
    IDB1.html						  \
	IDB1.log						  \
    IDB1.pdf						  \
    models.html

ifeq ($(shell uname), Darwin)          # Apple
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
else ifeq ($(CI), true)                # Travis CI
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3
    AUTOPEP8 := autopep8
else ifeq ($(shell uname -p), unknown) # Docker
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
else                                   # UTCS
    PYTHON   := python3.5
    PIP      := pip3
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
endif

pylint:
	$(PYLINT) --disable=locally-disabled --reports=no --generate-rcfile > $@

venv:
	virtualenv -p python3.5 venv

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

run:
	python project/IDB1.py

update:
	git pull --all
	make install

html:
	pydoc3 -w project/*.py

log:
	git log > IDB1.log

test:
	python project/tests.py
	$(COVERAGE) run --branch project/tests.py > project/tests.py.tmp 2>&1
	$(COVERAGE) report -m >> project/tests.py.tmp

push:
	git push
	ssh ec2-user@ec2-54-187-105-249.us-west-2.compute.amazonaws.com 'cd SouthernWholesomeEducation/project && git pull && ./deploy.sh'

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  .pylintrc
	rm -f  *.pyc
	rm -rf __pycache__

format:
	$(AUTOPEP8) -i project/models.py
	$(AUTOPEP8) -i project/IDB1.py

test:
	git push
	ssh ec2-user@ec2-54-187-105-249.us-west-2.compute.amazonaws.com 'cd backEnd/SouthernWholesomeEducation && git pull && python3 project/tests.py'

populate:
	git push
	ssh ec2-user@ec2-54-187-105-249.us-west-2.compute.amazonaws.com 'cd backEnd/SouthernWholesomeEducation && git pull && python3 project/api_calls.py && PGPASSWORD=ec2-user psql swe'

testTravis:
	ssh -o StrictHostKeyChecking=no -i deploy_key ec2-user@ec2-54-187-105-249.us-west-2.compute.amazonaws.com 'cd SouthernWholesomeEducation && git pull && python3 project/tests.py'

prep:
	format
	pylint
	freeze
	html
	log
	check

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

versions:
	which make
	make --version
	@echo
	which git
	git --version
	@echo
	which $(PYTHON)
	$(PYTHON) --version
	@echo
	which $(PIP)
	$(PIP) --version
	@echo
	which $(PYLINT)
	$(PYLINT) --version
	@echo
	which $(COVERAGE)
	$(COVERAGE) --version
	@echo
	which $(PYDOC)
	$(PYDOC) --version
	@echo
	which $(AUTOPEP8)
	$(AUTOPEP8) --version
	@echo
	$(PIP) list
