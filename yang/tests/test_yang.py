import pytest
import os


def get_expected_passes():
    # Grab our tests directory
    test_dir = os.path.dirname(os.path.abspath(__file__))
    # Find the pass directory for tests, all these should return exit code 0
    pass_test_dir = os.path.join(test_dir, "test_passes_yml")
    expected_passes = [(pass_test_dir, file) for file in os.listdir(pass_test_dir)]
    return expected_passes


def get_expected_fails():
    # Grab our tests directory
    test_dir = os.path.dirname(os.path.abspath(__file__))
    # Find the pass directory for tests, all these should return an exit code other than 0
    pass_test_dir = os.path.join(os.path.join(test_dir, "test_fails_yml"))
    expected_fails = [(pass_test_dir, file) for file in os.listdir(pass_test_dir)]
    return expected_fails


@pytest.mark.parametrize("process_check", get_expected_passes(), indirect=True)
def test_passes(process_check):
    """
    Iterates through the tests that should pass in the test_passes_yml directory and try them one by one
    success == 0 exit/return code
    """
    process, filename = process_check
    print(f"Testing to ensure this file passes our tests - > {filename}")
    assert process.returncode == 0


@pytest.mark.parametrize("process_check", get_expected_fails(), indirect=True)
def test_fails(process_check):
    """
    Iterates through the tests that should pass in the test_fails_yml directory and try them one by one
    success != 0 exit/return code
    """
    process, filename = process_check
    print(f"Testing to ensure this file fails our tests - > {filename}")
    assert process.returncode != 0
