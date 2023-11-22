#!/bin/bash

test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest

. ssshtest

# Test for loading and saving csv without time remapping (positive case)
file_read() {
	python3 ../../src/load_data.py -i "../data/4807-test.csv" -o "../data/4807-test-output.csv"
	cat ../data/4807-test-output.csv 
}
run test_load_data file_read
assert_in_stdout "0,1657027819.110297,0.0,18.97811,-2.564069,5.828868"

