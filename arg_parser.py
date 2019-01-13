import argparse
import calendar
import datetime
import time

from consts import *

from decorators import no_traceback


def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-m', '--month',
                        dest='month',
                        metavar='DATE',
                        help=MONTH_ARG_HELP,
                        default=time.strftime(MONTH_YEAR_FORMAT),
                        type=month_arg_assert)
    parser.add_argument('-f', '--furlough',
                        dest='furlough',
                        metavar=CSV,
                        help=FURLOUGH_ARG_HELP,
                        default=[],
                        type=csv_days_assert)
    parser.add_argument('-w', '--work',
                        dest='work',
                        metavar=CSV,
                        help=WORK_ARG_HELP,
                        default=[],
                        type=csv_days_assert)
    parser.add_argument('-r', '--range',
                        dest='range',
                        metavar=CSV,
                        help=RANGE_ARG_HELP,
                        default=(6, 10),
                        type=csv_range_assert)
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
        raise argparse.ArgumentTypeError('Incorrect data format, should be M-YYYY, MM-YYYY, M or MM.')


def csv_days_assert(days):
    try:
        days = days.strip().split(',')
        return [int(day) for day in days]
    except ValueError:
        raise argparse.ArgumentTypeError('Incorrect data format, should be 1,3,4,10,...')


def csv_range_assert(hours_range):
    hours_range = hours_range.split(',')
    if len(hours_range) != 2:
        raise argparse.ArgumentTypeError('Incorrect data format, too many commas, should be like 6,10')
    try:
        hours_min, hours_max = int(hours_range[0]), int(hours_range[1])
    except ValueError:
        raise argparse.ArgumentTypeError('Incorrect data format, try with 2 ints sparated by comma.')
    if hours_min > hours_max:
        raise argparse.ArgumentTypeError('Incorrect data format, {} is greater than {}'.format(hours_min, hours_max))
    if hours_min < 1:
        raise argparse.ArgumentTypeError('Incorrect data format, {} is lower than 1'.format(hours_min))
    if hours_max > 24:
        raise argparse.ArgumentTypeError('Incorrect data format, {} is greater than 24'.format(hours_max))
    return hours_min, hours_max


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


@no_traceback
def days_in_month_assert(days_in_month, days):
    for day in days:
        if not (1 <= day <= days_in_month):
            raise argparse.ArgumentTypeError('Incorrect data format, day out of month range.')


@no_traceback
def day_collision_assert(days, other_days):
    if set(days).intersection(set(other_days)):
        raise argparse.ArgumentTypeError('Incorrect data format, furlough and work day can not intersect.')
