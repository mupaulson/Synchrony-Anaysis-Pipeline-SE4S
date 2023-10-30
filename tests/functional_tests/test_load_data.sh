#!/bin/bash

test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest

. ssshtest

# Test for loading and saving csv without time remapping (positive case)
noremap_test() {
	python3 ../../src/load_data.py -i "../data/4807-test2.csv" -o "../data/4807-test2-remap.csv"
	cat ../data/4807-test2-remap.csv 
}
run test_load_data noremap_test
assert_in_stdout "1657027819.110297,18.97811,-2.564069,5.828868"

# Test for loading and saving csv with time remapping (positive case)
remap_test() {
	python3 ../../src/load_data.py -i "../data/4807-test2.csv" -o "../data/4807-test2-remap.csv" -r
	cat ../data/4807-test2-remap.csv 
}
run test_load_data_remapped remap_test
assert_in_stdout "0.0,18.97811,-2.564069,5.828868"

