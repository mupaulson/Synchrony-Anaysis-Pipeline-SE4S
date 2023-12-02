# get sshtest
test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest

. ssshtest


# test outputs exist for each transformation
run test_load_data python ../../src/show_correlations.py from_csv 'correlations_test.csv'
assert_stderr
assert_exit_code 1

run test_data_to_df python ../../src/show_correlations.py animal_data_to_df 
assert_stderr
assert_exit_code 1

run test_correlations python ../../src/show_correlations.py correlation_matrix
assert_stderr
assert_exit_code 1
