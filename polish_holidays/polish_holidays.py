import bs4 as bs
import requests
import time


HOLIDAYS_URL = 'https://publicholidays.pl/pl/{year}-dates/'
HOLIDAYS_TABLE = 'publicholidays phgtable'

GET = 'GET'
HTML_PARSER = 'html.parser'
TD = 'td'
YEAR_FORMAT = '%Y'

MONTHS_MAP = {
    'stycznia': 1,
    'lutego': 2,
    'marca': 3,
    'kwietnia': 4,
    'maja': 5,
    'czerwca': 6,
    'lipca': 7,
    'sierpnia': 8,
    'września': 9,
    'października': 10,
    'listopada': 11,
    'grudnia': 12
}


class PolishHolidays:
    def __init__(self):
        self.holidays = self._get_holidays()

    def _get_holidays(self):
        """
        Return list of holidays.
            Example:
                ['1 stycznia, 3 maja, ...]
        :return: list
        """
        current_year = time.strftime(YEAR_FORMAT)
        url = HOLIDAYS_URL.format(year=current_year)
        holidays_response = requests.request(GET, url)
        soup = bs.BeautifulSoup(holidays_response.content, HTML_PARSER)
        public_holidays_table = soup.find(class_=HOLIDAYS_TABLE)
        all_days = public_holidays_table.find_all(TD)
        holidays = [day.text for day in all_days[::3]]  # returns [1 stycznia, 3 maja, ...]
        return self._get_formatted_holidays(holidays)

    @staticmethod
    def _get_formatted_holidays(holidays):
        formatted_holidays = {}
        for holiday in holidays:
            day, month_name = holiday.split()
            month_number = MONTHS_MAP[month_name]
            month_days = formatted_holidays.setdefault(month_number, [])
            month_days.append(int(day))
        return formatted_holidays

PolishHolidays()