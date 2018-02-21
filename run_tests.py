"""
Example of usage:

bin/python run_tests.py                      run tests for packages groups specified in DEFAULT_PACKAGES
bin/python run_tests.py openprocurement      specify packages groups to run tests for
bin/python run_tests.py --list-packages      show packages that will be tested without actually running them
"""
import argparse
import logging
import os
from pkg_resources import iter_entry_points

import nose

DEFAULT_PACKAGES = ['openprocurement']  # default groups of packages that should be tested
NOSE_ENV = {
    "NOSE_WITH_XUNIT": 1,
    "NOSE_WITH_COVERAGE": 1,
    "NOSE_COVER_PACKAGE": [],
    "NOSE_COVER_ERASE": 1,
    "NOSE_COVER_HTML": 1,
    "NOSE_PROCESSES": 0,
    "NOSE_WITH_DOCTEST": 1,
    "NOSE_NOCAPTURE": 1,
    "NOSE_VERBOSE": 1,
}
os.environ['PYTEST_ADDOPTS'] = '--ignore=src/ --junitxml=pytest.xml'


def get_tests(packages, test_type):
    """
    Collect tests from entry points of specified packages.
    :param packages: list of strings, which are representing groups of packages that should be tested.
    :param test_type: 'tests' or 'pytests' for unittest TestCases and pytest test respectively.
    :return: test suites collected from entry points;
             list of strings, which are representing packages that will be tested.
    """
    tested_packages = list()
    all_tests = list()
    for pack in packages:
        for entry_point in iter_entry_points(group='{}.{}'.format(pack, test_type)):
            package_name = '{}.{}'.format(pack, entry_point.name)
            tested_packages.append(package_name)
            suite = entry_point.load()
            if test_type == 'tests':
                for tests in suite():
                    all_tests.extend(tests)
            elif test_type == 'pytests':
                all_tests.append(suite)
    return all_tests, tested_packages


def setup_logger():
    logger = logging.getLogger('console_output')
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    return logger


def list_packages(cover_packages, pytest_packages, logger):
    """
    Print to console names of packages that will be tested, without running tests.
    """
    if cover_packages:
        logger.info('NOSETESTS:')
        for p in cover_packages:
            logger.info("> {}".format(p))
    if pytest_packages:
        logger.info('PYTESTS:')
        for p in pytest_packages:
            logger.info("> {}".format(p))


def run():
    logger = setup_logger()
    parser = argparse.ArgumentParser(description='Test some packages.')
    parser.add_argument('packages', metavar='P', type=str, nargs='*',
                        help='name of packages to test', default=DEFAULT_PACKAGES)
    parser.add_argument('--list-packages', dest='list_packages', action='store_const',
                        const=True, default=False,
                        help='List packages that can be tested')
    args = parser.parse_args()
    unique_packages = set(args.packages)
    nose_tests, cover_packages = get_tests(unique_packages, 'tests')
    pytests, pytest_packages = get_tests(unique_packages, 'pytests')
    if args.list_packages:
        list_packages(cover_packages, pytest_packages, logger)
    else:
        NOSE_ENV['NOSE_COVER_PACKAGE'] = cover_packages
        for suite in pytests:
            suite()
        nose.run(suite=nose_tests, env=NOSE_ENV)


if __name__ == '__main__':
    run()
