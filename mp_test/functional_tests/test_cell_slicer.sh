test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run cell_slicer_top python ../../src/cell_slicer.py --file_name ../test_data/random_r_matrix.csv --out_file test_cell_pairs.txt --sorted_out_file test_corr_matrix.csv --query top --x_percent 20
assert_equal $"test_corr_matrix.csv" $(ls test_corr_matrix.csv)
assert_equal $"test_cell_pairs.txt" $(ls test_cell_pairs.txt)
assert_exit_code 0

run cell_slicer_sig python ../../src/cell_slicer.py --file_name ../test_data/random_r_matrix.csv --out_file test_cell_pairs2.txt --sorted_out_file test_corr_matrix2.csv --query sig --file_pvals ../test_data/random_p_matrix.csv --out_pvals test_p_matrix.csv
assert_equal $"test_corr_matrix2.csv" $(ls test_corr_matrix2.csv)
assert_equal $"test_cell_pairs2.txt" $(ls test_cell_pairs2.txt)
assert_equal $"test_p_matrix.csv" $(ls test_p_matrix.csv)
assert_exit_code 0

run cell_slicer_bad_args python ../../src/cell_slicer.py --file_name ../test_data/random_r_matrix.csv --out_file test_cell_pairs.txt --sorted_out_file test_corr_matrix.csv --query percent
assert_in_stdout Error query must be sig or top
Error above prevented cell_pairs file production.
assert_exit_code 1

run cell_slicer_bad_args_top python ../../src/cell_slicer.py --file_name ../test_data/random_r_matrix.csv --out_file test_cell_pairs.txt --sorted_out_file test_corr_matrix.csv --query top
assert_in_stdout Error if query is top must input x_per
Error above prevented cell_pairs file production.
assert_exit_code 1

run cell_slicer_bad_args_sig python ../../src/cell_slicer.py --file_name ../test_data/random_r_matrix.csv --out_file test_cell_pairs.txt --sorted_out_file test_corr_matrix.csv --query sig
assert_in_stdout Error if query is sig must input p_data
Error above prevented cell_pairs file production.
assert_exit_code 1

run cell_slicer_bad_data python ../../src/cell_slicer.py --file_name ../test_data/random_r_matrix.csv --out_file test_cell_pairs.txt --sorted_out_file test_corr_matrix.csv --query sig --file_pvals ../test_data/string_matrix.csv --out_pvals test_p_matrix.csv
assert_in_stdout p_data matrix not numbers
assert_exit_code 1

run cell_slicer_no_file python ../../src/cell_slicer.py --file_name ../test_data/empty.csv --out_file test_cell_pairs.txt --sorted_out_file test_corr_matrix.csv --query sig --file_pvals ../test_data/string_matrix.csv --out_pvals test_p_matrix.csv
assert_in_stdout Error: Could not find empty.csv &/or string_matrix.csv
assert_exit_code 1