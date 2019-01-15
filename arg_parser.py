from sys import exit
import argparse
import calendar
import datetime
import time

from consts import *


def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-m', '--month',
                        metavar=DATE,
                        help=MONTH_ARG_HELP,
                        default=time.strftime(MONTH_YEAR_FORMAT),
                        type=month_arg_assert)
    parser.add_argument('-r', '--range',
                        metavar=CSV,
                        help=RANGE_ARG_HELP,
                        default=DEFAULT_RANGE,
                        type=csv_range_assert)
    parser.add_argument('--worker',
                        metavar=STRING,
                        help=WORKER_ARG_HELP,
                        default=DEFAULT_WORKER,
                        type=str)
    parser.add_argument('-f', '--furlough',
                        metavar=CSV,
                        help=FURLOUGH_ARG_HELP,
                        default=[],
                        type=csv_days_assert)
    parser.add_argument('-w', '--work',
                        metavar=CSV,
                        help=WORK_ARG_HELP,
                        default=[],
                        type=csv_days_assert)
    parsed_args = parser.parse_args()
    post_args_assert(parsed_args)
    return parsed_args


# pre asserts
def month_arg_assert(month_date):
    if '-' not in month_date:
        month_date = '{}-{}'.format(month_date, time.strftime(YEAR_FORMAT))
    try:
        datetime.datetime.strptime(month_date, MONTH_YEAR_FORMAT)
        return [int(date_part) for date_part in month_date.split('-')[::-1]]
    except ValueError:
        exit_with_error('Incorrect data format, should be M-YYYY, MM-YYYY, M or MM')


def csv_range_assert(hours_range):
    hours_range = hours_range.split(',')
    if len(hours_range) != 2:
        exit_with_error('Incorrect data format, too many commas, should be like 6,10')
    try:
        hours_min, hours_max = int(hours_range[0]), int(hours_range[1])
    except ValueError:
        exit_with_error('Incorrect data format, try with ints')
    if hours_min > hours_max:
        exit_with_error('Incorrect data format, {} is greater than {}'.format(hours_min, hours_max))
    if hours_min < 1:
        exit_with_error('Incorrect data format, {} is lower than 1 (min allowed)'.format(hours_min))
    if hours_min > 8:
        exit_with_error('Incorrect data format, {} is greater than 8 (max allowed)'.format(hours_min))
    if hours_max > 24:
        exit_with_error('Incorrect data format, {} is greater than 24 (max allowed)'.format(hours_max))
    return hours_min, hours_max


def csv_days_assert(days):
    try:
        days = days.strip().split(',')
        return [int(day) for day in days]
    except ValueError:
        exit_with_error('Incorrect data format, should be 1,3,4,10,...')


# post asserts
def post_args_assert(parsed_args):
    _, days_in_month = calendar.monthrange(*parsed_args.month)
    furlough_post_assert(days_in_month, parsed_args.furlough)
    work_post_assert(days_in_month, parsed_args.work)
    day_collision_assert(parsed_args.furlough, parsed_args.work)


def furlough_post_assert(days_in_month, furlough):
    days_in_month_assert(days_in_month, furlough)


def work_post_assert(days_in_month, work_days):
    days_in_month_assert(days_in_month, work_days)


def days_in_month_assert(days_in_month, days):
    for day in days:
        if not (1 <= day <= days_in_month):
            exit_with_error('Incorrect data format, day out of month range.')


def day_collision_assert(days, other_days):
    if set(days).intersection(set(other_days)):
        exit_with_error('Incorrect data format, furlough and work day can not intersect.')


def exit_with_error(message):
    print(message)
    exit(1)
