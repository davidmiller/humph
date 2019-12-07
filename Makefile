SHELL := /bin/bash

run:
	python -m humph

test:
	coverage run -m unittest
	coverage report -m
