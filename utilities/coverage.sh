#!/bin/bash
source env/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

coverage run -m unittest ./tests/unit_test_publisher.py 
coverage run --append -m unittest ./tests/unit_test_subscriber.py

coverage report
coverage html
coverage report --format=markdown
