# Get the ssshtest framework
test -e ssshtest || curl -O https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest

. ssshtest

# Test successful line plot creation
run test_line_plot_creation python ../../src/create_plots.py \
    -f ../../data/4659_aligned_traces.csv \
    -c C000 C001 C002 \
    -o line_plot_test.png \
    -p line
# No error codes, no error output and the file exists locally
assert_exit_code 0
assert_no_stderr
assert_equal "line_plot_test.png" $(ls line_plot_test.png)

# Test successful correlation plot creation
run test_correlation_matrix python ../../src/create_plots.py \
    -f ../../data/4659_aligned_traces.csv \
    -c C000 C001 C003 \
    -o correlation_matrix_test.png \
    -p correlation
# No error codes, no error output and the file exists locally
assert_exit_code 0
assert_no_stderr
assert_equal "correlation_matrix_test.png" $(ls correlation_matrix_test.png)

# Test with a non existent file
run test_missing_file python ../../src/create_plots.py \
    -f non_existent_file.csv \
    -c C000 C001 \
    -o missing_file_test.png \
    -p line
# Error code expected, File not found in error message
assert_in_stderr "File not found"
assert_exit_code 1

# Remove the test files
rm line_plot_test.png correlation_matrix_test.png