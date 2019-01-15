# date formats
YEAR_FORMAT = '%Y'
MONTH_YEAR_FORMAT = '%m-%Y'

# argparse
CSV = 'CSV'
DATE = 'DATE'
DEFAULT_RANGE = (6, 10)
STRING = 'STRING'
DEFAULT_WORKER = 'Łukasz Sadowski'

# help messages
MONTH_ARG_HELP = """Date for generate working time.
Supported date formats:
    * MM-YYY
    * M-YYYY
    * MM (default current year)
    * M (default current year)
Example:
    01-2019

Default:
    current month and year

"""

RANGE_ARG_HELP = """The most common range of working hours in day, separated by comma.
Example:
    7,9

Default:
    {}

""".format('{},{}'.format(*DEFAULT_RANGE))

WORKER_ARG_HELP = """Worker name.
Example:
    John Doe

Default:
    {}

""".format(DEFAULT_WORKER)

FURLOUGH_ARG_HELP = """Absent days in the month, separated by comma.
Example:
    1,5,10

"""

WORK_ARG_HELP = """Additional worked days in saturdays/sundays/holidays in the month, separated by comma.
Example:
    1,5,10

"""

# xlswriter

INFO_COL = 'B:B'
INFO_COL_WIDTH = 12

HOURS_COLS = 'C:N'
HOURS_COLS_WIDTH = 3

WORKER_NAME = 'C2:N2'


FORMATS = {
    'OUTER_BORDER': {
        'border': 2
    }
}
