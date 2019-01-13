from datetime import date
import calendar
import random

import holidays
import xlsxwriter

from arg_parser import get_args


class WorkingTimeGenerator:
    def __init__(self, year, month, hours_range, furlough=None, work=None):
        self.polish_holidays = holidays.Polish()
        self.year = year
        self.month = month
        self.month_calendar = calendar.monthcalendar(year, month)
        self.hours_range = hours_range
        self.furlough = furlough
        self.work = work
        self.worked_days = self.get_worked_days()

    def get_worked_days(self):
        worked_days = []
        for week in self.month_calendar:
            worked_week = [0 for _ in range(7)]
            for week_day, day in enumerate(week):
                if day == 0:
                    continue
                worked_week[week_day] = self.get_working_time(week_day, day)
            worked_days.append(worked_week)
        self.recalculate_worked_days(worked_days)
        return worked_days

    def get_working_time(self, week_day, day):
        is_holiday = week_day > 4 or date(self.year, self.month, day) in self.polish_holidays
        if day in self.furlough and not is_holiday:
            return 'U'
        elif day not in self.work and is_holiday:
            return 0
        return self.get_random_working_time()

    def get_random_working_time(self):
        return random.randint(*self.hours_range)

    @staticmethod
    def recalculate_worked_days(worked_days):
        pass



def main():
    args = get_args()
    wt_gen = WorkingTimeGenerator(*args.month, args.range, args.furlough, args.work)
    a = []


if __name__ == '__main__':

        main()

