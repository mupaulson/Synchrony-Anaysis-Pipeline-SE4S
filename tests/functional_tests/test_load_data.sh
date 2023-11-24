#!/bin/bash

test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest

. ssshtest

# === load_data.py ===
file_read() {
	# Test for loading and saving csv without time remapping (positive case)
	python3 ../../src/load_data.py -i "../data/4807-test.csv" -o "../data/4807-test-output.csv"
	cat ../data/4807-test-output.csv 
	rm ../data/4807-test-output.csv
}
run test_load_data file_read
assert_in_stdout "0,1657027819.110297,0.0,18.97811,-2.564069,5.828868"

run test_load_data_nonexistent python3 ../../src/load_data.py -i "nonexistent.csv" -o "../data/output.csv"
assert_exit_code 1
assert_in_stderr "File not found"

run test_load_data_invalid_format python3 ../../src/load_data.py -i "../data/1234-invalid-format.csv" -o "../data/output.csv"
assert_exit_code 1
assert_in_stderr "Error: "

run test_missing_arguments python3 ../../src/load_data.py
assert_exit_code 2
assert_in_stderr "arguments are required"