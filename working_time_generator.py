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
        self.worked_days = self._get_worked_days()

    def _get_worked_days(self):
        worked_days = []
        for week in self.month_calendar:
            worked_week = [0 for _ in range(7)]
            for week_day, day in enumerate(week):
                if day == 0:
                    continue
                worked_week[week_day] = self._get_working_time(week_day, day)
            worked_days.append(worked_week)
        self._recalculate_worked_days(worked_days)
        return worked_days

    def _get_working_time(self, week_day, day):
        is_holiday = week_day > 4 or date(self.year, self.month, day) in self.polish_holidays
        if day in self.furlough and not is_holiday:
            return 'U'
        elif day not in self.work and is_holiday:
            return 0
        return self._get_random_working_time()

    def _get_random_working_time(self):
        return random.randint(*self.hours_range)

    def _recalculate_worked_days(self, worked_days):
        current_hours, required_hours = self._get_worked_days_info(worked_days)
        if current_hours == required_hours:
            return
        recalculate_info = self._get_recalculate_info(worked_days, current_hours, required_hours)
        self._recalculate_days(worked_days, *recalculate_info)

    @staticmethod
    def _get_worked_days_info(worked_days):
        current_hours = 0
        required_hours = 0
        for num_week, week in enumerate(worked_days):
            for num_day, working_hours in enumerate(week):
                if isinstance(working_hours, int) and working_hours > 0:
                    current_hours += working_hours
                    required_hours += 8
        return current_hours, required_hours

    def _get_recalculate_info(self, worked_days, current_hours, required_hours):
        sign = 1 if current_hours < required_hours else -1
        delta = abs(current_hours - required_hours)
        possible_days = self._get_possible_days_to_recalculate(worked_days, sign)
        return delta, sign, possible_days

    def _get_possible_days_to_recalculate(self, worked_days, sign):
        min_working_time, max_working_time = self.hours_range
        possible_days = []
        for num_week, week in enumerate(worked_days):
            for num_day, working_hours in enumerate(week):
                if self._is_day_possible(working_hours, min_working_time, max_working_time, sign):
                    possible_days.append((num_week, num_day))
        return possible_days

    @staticmethod
    def _is_day_possible(working_hours, min_working_time, max_working_time, sign):
        if isinstance(working_hours, int) and working_hours > 0:
            if (sign == 1 and working_hours < max_working_time) or \
                    (sign == -1 and working_hours > min_working_time):
                return True
        return False

    def _recalculate_days(self, worked_days, delta, sign, possible_days):
        min_working_time, max_working_time = self.hours_range
        while delta:
            possible_day_idx = random.randrange(len(possible_days))
            possible_week, possible_day = possible_days[possible_day_idx]
            worked_days[possible_week][possible_day] += 1 * sign
            delta -= 1
            working_time = worked_days[possible_week][possible_day]
            if working_time == min_working_time or working_time == max_working_time:
                del possible_days[possible_day_idx]


def main():
    args = get_args()
    wt_gen = WorkingTimeGenerator(*args.month, args.range, args.furlough, args.work)

    current_hours = 0
    for num_week, week in enumerate(wt_gen.worked_days):
        for num_day, working_hours in enumerate(week):
            if isinstance(working_hours, int) and working_hours > 0:
                current_hours += working_hours
    import pprint
    print(current_hours)
    pprint.pprint(wt_gen.worked_days)


if __name__ == '__main__':
    main()
