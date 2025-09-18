#!/bin/bash
source env/bin/activate
coverage run -m unittest ./tests/unit_test_publisher.py 
coverage run --append -m unittest ./tests/unit_test_subscriber.py
coverage report 
coverage report --format=markdown 
