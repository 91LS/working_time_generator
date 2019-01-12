import calendar
import sys

import holidays
import xlsxwriter

from arg_parser import get_args

# all_holidays = holidays.Polish()
#
# print(date(2019, 4, 23) in all_holidays)


class WorkingTimeGenerator:
    def __init__(self, year, month, furlough=None, work=None):
        self.month = calendar.monthcalendar(year, month)
        self.furlough = furlough
        self.work = work


def main():
    args = get_args()
    wt_gen = WorkingTimeGenerator(*args.month, args.furlough)
    a = []


if __name__ == '__main__':

        main()

