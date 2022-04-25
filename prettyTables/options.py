"""
OPTIONS

some parameters for the creation of styles
and formatting.
"""

import re


INVISIBLE_SEPARATOR = ' '
MARGIN = 1
ESCAPE_CODES = ['\n', '\r']
MIN_COLUMN_WIDTH = 2
NONE_VALUE_REPLACEMENT = ''
DEFAULT_FILL_CHAR = ' '
DEFAULT_STYLE = 'grid_eheader'
I_COL_TIT = 'i'  # INDEX COLUMN TITLE
DEFAULT_TABLE_ALIGNMENT = 'l'
INT_FILTER = re.compile(r'^[-]?[0-9]*$').match
FLT_FILTER = re.compile(r'^[-]?[0-9]*[.][0-9]*$').match
