# date formats
YEAR_FORMAT = '%Y'
MONTH_YEAR_FORMAT = '%m-%Y'

# help messages
MONTH_ARG_HELP = """Date for generate working time.
Supported date formats:
    * MM-YYY
    * M-YYYY
    * MM (default current year)
    * M (default current year)
Default:
    * current month and year
Example:
    01-2019

"""

FURLOUGH_ARG_HELP = """Absent days in the month, separated by comma.
Example:
    1,5,10

"""

WORK_ARG_HELP = """Additional worked days in saturdays/sundays/holidays in the month, separated by comma.
Example:
    1,5,10

"""
