SHELL := /bin/bash

test:
	coverage run -m unittest
	coverage report -m
