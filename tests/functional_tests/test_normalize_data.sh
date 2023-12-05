test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run normalize_data python ../../src/normalize_data.py --file_name ../data/4807-test.csv --out_file test_norm.csv
assert_equal $"test_norm.csv" $(ls test_norm.csv)
assert_exit_code 0

run normalize_data_bad_data python ../../src/normalize_data.py --file_name ../data/string_matrix.csv --out_file test_norm.csv
assert_exit_code 1
