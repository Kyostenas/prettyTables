"""
Print formatted tabular data in different styles
"""

# FORMATION OF THE TABLE
#
# Main Class.
# Here the whole table is formed

from .style_compositions import (
    __style_compositions as style_catalogue, 
    HorizontalComposition, 
    SeparatorLine,
    TableComposition
)
from .columns import (
    _column_widths, 
    _typify_column, 
    _align_columns, 
    _align_headers,
    TYPE_NAMES,
    CAN_WRAP_TYPES,
    ALIGNMENTS_PER_TYPE as type_alignments
)
from .table_strings import (
    _get_separators, 
    _get_data_rows, 
    DataRows
)
from .utils import (
    delete_repetitions,
    get_window_size, 
    is_multi_row,
    ValuePlacer,
    IndexCounter,
    read_file
)
from .options import (
    NONE_VALUE_REPLACEMENT, 
    DEFAULT_STYLE, 
    I_COL_TIT, 
    DEFAULT_TABLE_ALIGNMENT,
    DEFAULT_TRIMMING_SIGN,
    MIN_COLUMN_SIZE
)
from .cells import (
    _wrap_rows,
    _zip_wrapped_rows
)

from copy import deepcopy
from textwrap import wrap
from typing import (
    Any,
    Generator,
    List,
    Optional,
    Tuple,
    Union
)


class Table(object):
    """
    TABLE
    =====

    Makes a table out of tabular data

    ---------------
    POSSIBLE STYLES
    ---------------
    ### PLAIN
    >>> from prettyTables import Table
    >>> new_table = Table()
    >>> new_table.missing_val = 'n/a'
    >>> new_table.add_row(data=[1])
    >>> new_table.add_column(data=['Kg', 'ml'])
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'plain'
    ... column 1 column 2
    ...
    ... 1        Kg
    ... n/a      ml
    >>> new_table.show_headers = False
    >>> new_table
    ... 1   Kg
    ... n/a ml

    ---------------
    ### PRETTY_GRID
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'pretty_grid'
    ... ╒══════════╤══════════╕
    ... │ column 1 │ column 2 │
    ... ╞══════════╪══════════╡
    ... │ 1        │ Kg       │
    ... ├──────────┼──────────┤
    ... │ n/a      │ ml       │
    ... ╘══════════╧══════════╛
    >>> new_table.show_headers = False
    >>> new_table
    ... ╒═════╤════╕
    ... │ 1   │ Kg │
    ... ├─────┼────┤
    ... │ n/a │ ml │
    ... ╘═════╧════╛

    ---------------
    ### PRETTY_COLUMNS
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'pretty_columns'
    ... ╒══════════╤══════════╕
    ... │ column 1 │ column 2 │
    ... ╞══════════╪══════════╡
    ... │ 1        │ Kg       │
    ... │ n/a      │ ml       │
    ... ╘══════════╧══════════╛
    >>> new_table.show_headers = False
    >>> new_table
    ... ╒═════╤════╕
    ... │ 1   │ Kg │
    ... │ n/a │ ml │
    ... ╘═════╧════╛

    ---------------
    ### BOLD_HEADER
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'bold_header'
    ... ╔══════════╦══════════╗
    ... ║ column 1 ║ column 2 ║
    ... ╚══════════╩══════════╝
    ... │ 1        │ Kg       │
    ... ├──────────┼──────────┤
    ... │ n/a      │ ml       │
    ... └──────────┴──────────┘
    >>> new_table.show_headers = False
    >>> new_table
    ... ┌─────┬────┐
    ... │ 1   │ Kg │
    ... ├─────┼────┤
    ... │ n/a │ ml │
    ... └─────┴────┘

    ---------------
    ### BHEADER_COLUMNS
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'bheader_columns'
    ... ╔══════════╦══════════╗
    ... ║ column 1 ║ column 2 ║
    ... ╚══════════╩══════════╝
    ... │ 1        │ Kg       │
    ... │ n/a      │ ml       │
    ... └──────────┴──────────┘
    >>> new_table.show_headers = False
    >>> new_table
    ... ┌─────┬────┐
    ... │ 1   │ Kg │
    ... │ n/a │ ml │
    ... └─────┴────┘

    ---------------
    ### BOLD_EHEADER
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'bold_eheader'
    ... ╔═════════════════════╗
    ... ║ column 1   column 2 ║
    ... ╚═════════════════════╝
    ... │ 1        │ Kg       │
    ... ├──────────┼──────────┤
    ... │ n/a      │ ml       │
    ... └──────────┴──────────┘
    >>> new_table.show_headers = False
    >>> new_table
    ... ┌─────┬────┐
    ... │ 1   │ Kg │
    ... ├─────┼────┤
    ... │ n/a │ ml │
    ... └─────┴────┘

    ---------------
    ### BEHEADER_COLUMNS
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'beheader_columns'
    ... ╔═════════════════════╗
    ... ║ column 1   column 2 ║
    ... ╚═════════════════════╝
    ... │ 1        │ Kg       │
    ... │ n/a      │ ml       │
    ... └──────────┴──────────┘
    >>> new_table.show_headers = False
    >>> new_table
    ... ┌─────┬────┐
    ... │ 1   │ Kg │
    ... │ n/a │ ml │
    ... └─────┴────┘

    ---------------
    ### BHEADER_EBODY
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'bheader_ebody'
    ... ╔═════════════════════╗
    ... ║ column 1   column 2 ║
    ... ╚═════════════════════╝
    ... │ 1          Kg       │
    ... │ n/a        ml       │
    ... └─────────────────────┘
    >>> new_table.show_headers = False
    >>> new_table
    ... ┌──────────┐
    ... │ 1     Kg │
    ... │ n/a   ml │
    ... └──────────┘

    ---------------
    ### ROUND_EDGES
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'round_edges'
    ... ╭──────────┬──────────╮
    ... │ column 1 │ column 2 │
    ... ╞══════════╪══════════╡
    ... │ 1        │ Kg       │
    ... │ n/a      │ ml       │
    ... ╰──────────┴──────────╯
    >>> new_table.show_headers = False
    >>> new_table
    ... ╭─────┬────╮
    ... │ 1   │ Kg │
    ... │ n/a │ ml │
    ... ╰─────┴────╯

    ---------------
    ### RE_EHEADER
    >>> new_table.show_headers = True
    >>> new_table.style_name = 're_eheader'
    ... ╭─────────────────────╮
    ... │ column 1   column 2 │
    ... ╞══════════╤══════════╡
    ... │ 1        │ Kg       │
    ... │ n/a      │ ml       │
    ... ╰──────────┴──────────╯
    >>> new_table.show_headers = False
    >>> new_table
    ... ╭─────┬────╮
    ... │ 1   │ Kg │
    ... │ n/a │ ml │
    ... ╰─────┴────╯

    ---------------
    ### RE_EBODY
    >>> new_table.show_headers = True
    >>> new_table.style_name = 're_ebody'
    ... ╭─────────────────────╮
    ... │ column 1   column 2 │
    ... ╞═════════════════════╡
    ... │ 1          Kg       │
    ... │ n/a        ml       │
    ... ╰─────────────────────╯
    >>> new_table.show_headers = False
    >>> new_table
    ... ╭──────────╮
    ... │ 1     Kg │
    ... │ n/a   ml │
    ... ╰──────────╯

    ---------------
    ### THIN_BORDERLINE
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'thin_borderline'
    ... ┌──────────┬──────────┐
    ... │ column 1 │ column 2 │
    ... ╞══════════╪══════════╡
    ... │ 1        │ Kg       │
    ... ├──────────┼──────────┤
    ... │ n/a      │ ml       │
    ... └──────────┴──────────┘
    >>> new_table.show_headers = False
    >>> new_table
    ... ┌─────┬────┐
    ... │ 1   │ Kg │
    ... ├─────┼────┤
    ... │ n/a │ ml │
    ... └─────┴────┘

    ---------------
    ### TH_BD_EHEADER
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'th_bd_eheader'
    ... ┌─────────────────────┐
    ... │ column 1   column 2 │
    ... ╞══════════╤══════════╡
    ... │ 1        │ Kg       │
    ... ├──────────┼──────────┤
    ... │ n/a      │ ml       │
    ... └──────────┴──────────┘
    >>> new_table.show_headers = False
    >>> new_table
    ... ┌─────┬────┐
    ... │ 1   │ Kg │
    ... ├─────┼────┤
    ... │ n/a │ ml │
    ... └─────┴────┘

    ---------------
    ### TH_BD_EBODY
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'th_bd_ebody'
    ... ┌──────────┬──────────┐
    ... │ column 1 │ column 2 │
    ... ╞══════════╧══════════╡
    ... │ 1          Kg       │
    ... │ n/a        ml       │
    ... └─────────────────────┘
    >>> new_table.show_headers = False
    >>> new_table
    ... ┌──────────┐
    ... │ 1     Kg │
    ... │ n/a   ml │
    ... └──────────┘

    ---------------
    ### TH_BD_EMPTY
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'th_bd_empty'
    ... ┌─────────────────────┐
    ... │ column 1   column 2 │
    ... ╞═════════════════════╡
    ... │ 1          Kg       │
    ... │ n/a        ml       │
    ... └─────────────────────┘
    >>> new_table.show_headers = False
    >>> new_table
    ... ┌──────────┐
    ... │ 1     Kg │
    ... │ n/a   ml │
    ... └──────────┘

    ---------------
    ### BOLD_BORDERLINE
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'bold_borderline'
    ... ╔══════════╤══════════╗
    ... ║ column 1 │ column 2 ║
    ... ╠══════════╪══════════╣
    ... ║ 1        │ Kg       ║
    ... ╟──────────┼──────────╢
    ... ║ n/a      │ ml       ║
    ... ╚══════════╧══════════╝
    >>> new_table.show_headers = False
    >>> new_table
    ... ╔═════╤════╗
    ... ║ 1   │ Kg ║
    ... ╟─────┼────╢
    ... ║ n/a │ ml ║
    ... ╚═════╧════╝

    ---------------
    ### BD_BL_EHEADER
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'bd_bl_eheader'
    ... ╔═════════════════════╗
    ... ║ column 1   column 2 ║
    ... ╠══════════╤══════════╣
    ... ║ 1        │ Kg       ║
    ... ╟──────────┼──────────╢
    ... ║ n/a      │ ml       ║
    ... ╚══════════╧══════════╝
    >>> new_table.show_headers = False
    >>> new_table
    ... ╔═════╤════╗
    ... ║ 1   │ Kg ║
    ... ╟─────┼────╢
    ... ║ n/a │ ml ║
    ... ╚═════╧════╝

    ---------------
    ### BD_BL_EBODY
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'bd_bl_ebody'
    ... ╔══════════╤══════════╗
    ... ║ column 1 │ column 2 ║
    ... ╠══════════╧══════════╣
    ... ║ 1          Kg       ║
    ... ║ n/a        ml       ║
    ... ╚═════════════════════╝
    >>> new_table.show_headers = False
    >>> new_table
    ... ╔══════════╗
    ... ║ 1     Kg ║
    ... ║ n/a   ml ║
    ... ╚══════════╝

    ---------------
    ### BD_BL_EMPTY
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'bd_bl_empty'
    ... ╔═════════════════════╗
    ... ║ column 1   column 2 ║
    ... ╠═════════════════════╣
    ... ║ 1          Kg       ║
    ... ║ n/a        ml       ║
    ... ╚═════════════════════╝
    >>> new_table.show_headers = False
    >>> new_table
    ... ╔══════════╗
    ... ║ 1     Kg ║
    ... ║ n/a   ml ║
    ... ╚══════════╝

    ---------------
    ### PWRSHLL_ALIKE
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'pwrshll_alike'
    ... column 1 column 2
    ... -------- --------
    ... 1        Kg
    ... n/a      ml
    >>> new_table.show_headers = False
    >>> new_table
    ... 1   Kg
    ... n/a ml

    ---------------
    ### PRESTO
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'presto'
    ...  column 1 | column 2
    ... ----------+----------
    ...  1        | Kg
    ...  n/a      | ml
    >>> new_table.show_headers = False
    >>> new_table
    ...  1   | Kg
    ...  n/a | ml

    ---------------
    ### GRID
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'grid'
    ... +----------+----------+
    ... | column 1 | column 2 |
    ... +==========+==========+
    ... | 1        | Kg       |
    ... +----------+----------+
    ... | n/a      | ml       |
    ... +----------+----------+
    >>> new_table.show_headers = False
    >>> new_table
    ... +-----+----+
    ... | 1   | Kg |
    ... +-----+----+
    ... | n/a | ml |
    ... +-----+----+

    ---------------
    ### GRID_EHEADER
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'grid_eheader'
    ... +---------------------+
    ... | column 1   column 2 |
    ... +==========+==========+
    ... | 1        | Kg       |
    ... | n/a      | ml       |
    ... +----------+----------+
    >>> new_table.show_headers = False
    >>> new_table
    ... +-----+----+
    ... | 1   | Kg |
    ... | n/a | ml |
    ... +-----+----+

    ---------------
    ### GRID_EBODY
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'grid_ebody'
    ... +----------+----------+
    ... | column 1 | column 2 |
    ... +==========+==========+
    ... | 1          Kg       |
    ... | n/a        ml       |
    ... +---------------------+
    >>> new_table.show_headers = False
    >>> new_table
    ... +----------+
    ... | 1     Kg |
    ... | n/a   ml |
    ... +----------+

    ---------------
    ### GRID_EMPTY
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'grid_empty'
    ... +---------------------+
    ... | column 1   column 2 |
    ... +=====================+
    ... | 1          Kg       |
    ... | n/a        ml       |
    ... +---------------------+
    >>> new_table.show_headers = False
    >>> new_table
    ... +----------+
    ... | 1     Kg |
    ... | n/a   ml |
    ... +----------+

    ---------------
    ### PIPES
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'pipes'
    ... | column 1 | column 2 |
    ... |----------|----------|
    ... | 1        | Kg       |
    ... | n/a      | ml       |
    >>> new_table.show_headers = False
    >>> new_table
    ... |-----|----|
    ... | 1   | Kg |
    ... | n/a | ml |

    ---------------
    ### TILDE_GRID
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'tilde_grid'
    ... +----------+----------+
    ... | column 1 | column 2 |
    ... O~~~~~~~~~~O~~~~~~~~~~O
    ... | 1        | Kg       |
    ... +----------+----------+
    ... | n/a      | ml       |
    ... O~~~~~~~~~~O~~~~~~~~~~O
    >>> new_table.show_headers = False
    >>> new_table
    ... O~~~~~O~~~~O
    ... | 1   | Kg |
    ... +-----+----+
    ... | n/a | ml |
    ... O~~~~~O~~~~O

    ---------------
    ### TILG_EHEADER
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'tilg_eheader'
    ... +---------------------+
    ... | column 1   column 2 |
    ... O~~~~~~~~~~O~~~~~~~~~~O
    ... | 1        | Kg       |
    ... +----------+----------+
    ... | n/a      | ml       |
    ... O~~~~~~~~~~O~~~~~~~~~~O
    >>> new_table.show_headers = False
    >>> new_table
    ... O~~~~~O~~~~O
    ... | 1   | Kg |
    ... +-----+----+
    ... | n/a | ml |
    ... O~~~~~O~~~~O

    ---------------
    ### TILG_COLUMNS
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'tilg_columns'
    ... +----------+----------+
    ... | column 1 | column 2 |
    ... O~~~~~~~~~~O~~~~~~~~~~O
    ... | 1        | Kg       |
    ... | n/a      | ml       |
    ... O~~~~~~~~~~O~~~~~~~~~~O
    >>> new_table.show_headers = False
    >>> new_table
    ... O~~~~~O~~~~O
    ... | 1   | Kg |
    ... | n/a | ml |
    ... O~~~~~O~~~~O

    ---------------
    ### TILG_EMPTY
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'tilg_empty'
    ... +---------------------+
    ... | column 1   column 2 |
    ... O~~~~~~~~~~~~~~~~~~~~~O
    ... | 1          Kg       |
    ... | n/a        ml       |
    ... O~~~~~~~~~~~~~~~~~~~~~O
    >>> new_table.show_headers = False
    >>> new_table
    ... O~~~~~~~~~~O
    ... | 1     Kg |
    ... | n/a   ml |
    ... O~~~~~~~~~~O

    ---------------
    ### ORGTBL
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'orgtbl'
    ... | column 1 | column 2 |
    ... |----------+----------|
    ... | 1        | Kg       |
    ... | n/a      | ml       |
    >>> new_table.show_headers = False
    >>> new_table
    ... | 1   | Kg |
    ... | n/a | ml |

    ---------------
    ### CLEAN
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'clean'
    ... column 1 column 2
    ... ──────── ────────
    ... 1        Kg
    ... n/a      ml
    ... ──────── ────────
    >>> new_table.show_headers = False
    >>> new_table
    ... ─── ──
    ... 1   Kg
    ... n/a ml
    ... ─── ──

    ---------------
    ### SIMPLE
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'simple'
    ... ---------------------
    ...  column 1   column 2
    ... ---------------------
    ...  1          Kg
    ...  n/a        ml
    ... ---------------------
    >>> new_table.show_headers = False
    >>> new_table
    ... ----------
    ...  1     Kg
    ...  n/a   ml
    ... ----------

    ---------------
    ### SIMPLE_BOLD
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'simple_bold'
    ... =====================
    ...  column 1   column 2
    ... =====================
    ...  1          Kg
    ...  n/a        ml
    ... =====================
    >>> new_table.show_headers = False
    >>> new_table
    ... ==========
    ...  1     Kg
    ...  n/a   ml
    ... ==========

    ---------------
    ### SIMPLE_HEAD
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'simple_head'
    ...  column 1   column 2
    ... ---------------------
    ...  1          Kg
    ...  n/a        ml
    >>> new_table.show_headers = False
    >>> new_table
    ...  1     Kg
    ...  n/a   ml

    ---------------
    ### SIMPLE_HEAD_BOLD
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'simple_head_bold'
    ...  column 1   column 2
    ... =====================
    ...  1          Kg
    ...  n/a        ml
    >>> new_table.show_headers = False
    >>> new_table
    ...  1     Kg
    ...  n/a   ml

    ---------------
    ### SIM_TH_BL
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'sim_th_bl'
    ... ─────────────────────
    ...  column 1   column 2
    ... ─────────────────────
    ...  1          Kg
    ...  n/a        ml
    ... ─────────────────────
    >>> new_table.show_headers = False
    >>> new_table
    ... ──────────
    ...  1     Kg
    ...  n/a   ml
    ... ──────────

    ---------------
    ### SIM_BD_BL
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'sim_bd_bl'
    ... ═════════════════════
    ...  column 1   column 2
    ... ═════════════════════
    ...  1          Kg
    ...  n/a        ml
    ... ═════════════════════
    >>> new_table.show_headers = False
    >>> new_table
    ... ══════════
    ...  1     Kg
    ...  n/a   ml
    ... ══════════

    ---------------
    ### SIM_HEAD_TH_BL
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'sim_head_th_bl'
    ...  column 1   column 2
    ... ─────────────────────
    ...  1          Kg
    ...  n/a        ml
    >>> new_table.show_headers = False
    >>> new_table
    ...  1     Kg
    ...  n/a   ml

    ---------------
    ### SIM_HEAD_BD_BL
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'sim_head_bd_bl'
    ...  column 1   column 2
    ... ═════════════════════
    ...  1          Kg
    ...  n/a        ml
    >>> new_table.show_headers = False
    >>> new_table
    ...  1     Kg
    ...  n/a   ml

    ---------------
    ### DASHES
    >>> new_table.show_headers = True
    >>> new_table.style_name = 'dashes'
    ... ┌┄┄┄┄┄┄┄┄┄┄┬┄┄┄┄┄┄┄┄┄┄┐
    ... ┊ column 1 ┊ column 2 ┊
    ... ┝╍╍╍╍╍╍╍╍╍╍┿╍╍╍╍╍╍╍╍╍╍┥
    ... ┊ 1        ┊ Kg       ┊
    ... ┊ n/a      ┊ ml       ┊
    ... └┄┄┄┄┄┄┄┄┄┄┴┄┄┄┄┄┄┄┄┄┄┘
    >>> new_table.show_headers = False
    >>> new_table
    ... ┌┄┄┄┄┄┬┄┄┄┄┐
    ... ┊ 1   ┊ Kg ┊
    ... ┊ n/a ┊ ml ┊
    ... └┄┄┄┄┄┴┄┄┄┄┘

    ---------------
    """

    def __init__(self, rows=None, columns=None, headers=None, style_name='',
                 missing_val='', header_style=None) -> None:
        # +------------------------+ PARAMETERS +------------------------+
        self.__missing_value = missing_val
        self.__value_placer = ValuePlacer()
        self.__str_align = None
        self.__int_align = None
        self.__float_align = None
        self.__bool_align = None
        self.__table_align = None
        self.__column_align = None
        self.__show_index = False
        self.__roman_index = False
        self.__i_start = 0
        self.__i_step = 1
        self.__index_counter = IndexCounter()
        self.__parse_numbers = True
        self.__parse_str_numbers = False
        self.__auto_wrap_table = False
        self.__expand_to_window = False  # TODO implement expand_to_window
        self.__auto_wrap_text = False
        self.__expand_body_to = 'r'
        self.__expand_header_to = 'r'
        self.__leading_zeros = None
        self.__float_spaces = 2
        self.__format_exponential = True
        # +--------------------------+ STYLE +---------------------------+
        # HEADER STYLES: None, l, u, t, c
        #   None: unmodified
        #   l: lower case
        #   u: upper case
        #   t: title
        #   c: capitalized
        self.__header_style = header_style
        self.__show_margin = True
        self.__show_empty_columns = True
        self.__show_empty_rows = True
        self.__generic_column_name = 'column'
        self.__style_name = style_name
        # +------------------+ TABLE CHARACTERISTICS +-------------------+
        self.__show_headers = True
        self.__table_height = 0
        self.__table_height_with_i = 0
        self.__table_width = 0
        self.__table_width_with_i = 0
        self.__real_row_count = 0
        self.__real_column_count = 0
        self.__line_spacing = 0
        self.__cell_types = {}
        self.__cell_types_with_i = {I_COL_TIT: []}
        self.__column_types = {}
        self.__column_types_with_i = {
            I_COL_TIT: TYPE_NAMES.int_
        }
        self.__column_types_as_list = []
        self.__column_types_as_list_with_i = []
        self.__column_i_per_type = {}
        self.__column_i_per_type_with_i = {}
        self.__float_columns_widths = {}
        self.__float_columns_widths_with_i = {}
        self.__column_widths = {}
        self.__column_widths_with_i = {}
        self.__column_widths_as_list = []
        self.__column_widths_as_list_with_i = []
        self.__table_alignment = 'l'
        self.__column_alignments = {}
        self.__column_alignments_with_i = {
            I_COL_TIT: type_alignments[TYPE_NAMES.int_]
        }
        self.__column_alignments_as_list = []
        self.__column_alignments_as_list_with_i = []
        self.__row_alignments = {}
        self.__row_alignments_as_list = []
        self.__cells_alignment = []
        # +------------------------+ TABLE BODY +------------------------+
        self.__columns = {}
        self.__columns_with_i = {I_COL_TIT: []}
        self.__headers = []
        self.__headers_with_i = [I_COL_TIT]
        self.__rows = []
        self.__rows_with_i = []
        self.__processed_columns = {}
        self.__processed_columns_with_i = {I_COL_TIT: []}
        self.__semi_processed_columns = {}
        self.__semi_processed_columns_with_i = {I_COL_TIT: []}
        self.__processed_headers = []
        self.__processed_headers_with_i = []
        self.__processed_rows = []
        self.__processed_rows_with_i = []
        # +-----------------------+ INIT ACTIONS +-----------------------+
        try:
            for header, column in columns.items():
                try:
                    column.__iter__
                    self.add_column(header=header, data=list(column))
                except AttributeError:
                    pass
            return None
        except (AttributeError, TypeError):
            pass
        try:
            for header in headers:
                self.__check_add_header_on_init(header)
        except TypeError:
            pass
        try:
            for row in rows:
                try:
                    row.__iter__
                    self.add_row(data=list(row))
                except AttributeError:
                    pass
            empty_to_add = len(headers) - len(rows[0])
            for _ in range(empty_to_add):
                self.add_column()
            return None
        except (TypeError, IndexError):
            pass
        try:
            for column in columns:
                try:
                    column.__iter__
                    self.add_column(data=list(column))
                except AttributeError:
                    pass
            empty_to_add = len(headers) - len(columns)
            for _ in range(empty_to_add):
                self.add_column()
        except TypeError:
            pass

    # +-----------------------------------------------------------------------------+
    # start +---------------------------+ METHODS +---------------------------+ start

    def __str__(self) -> str:
        return self.compose()
    
    
    def __repr__(self) -> str:
        return self.compose()

    # end +-----------------------------+ METHODS +-----------------------------+ end
    # +-----------------------------------------------------------------------------+


    # +-----------------------------------------------------------------------------+
    # start +-----------------------+ STATIC METHODS +------------------------+ start
    
    @staticmethod
    def __apply_wrap(piece: str, new_width: int) -> str:
        try:
            return '\n'.join(wrap(piece, new_width))
        except TypeError:
            return '\n'.join(wrap(str(piece), new_width))
    
    @staticmethod
    def __trim_with_sign(piece: str, new_widht: int) -> str:
        try:
            return ''.join([
                piece[:new_widht],
                DEFAULT_TRIMMING_SIGN
            ])
        except TypeError:
            return ''.join([
                str(piece)[:new_widht],
                DEFAULT_TRIMMING_SIGN
            ])
        
    @staticmethod
    def __check_if_none_and_get_len(value: Union[str, None]) -> int:
        """
        Checks if a value is::

            None | string
        
        Returns::
        
            None    # The len of the default value for None
            string  # The len of the string
        """
        if value is None:
            value_len = len(NONE_VALUE_REPLACEMENT)
        else:
            value_len = len(value)
        return value_len
    
    @staticmethod
    def __zip_columns(columns: Union[List[Union[list, tuple]], Tuple[Union[list, tuple]]], 
                      headers: Union[list, tuple]=False
                     ) -> Tuple[Union[Tuple[str], Tuple[Tuple[str]]]]:
        """
        Transforms columns into rows by zipping them.
        """
        if headers:
            row = tuple(map(lambda x: x, columns))
            if is_multi_row(row):
                zipped = tuple(zip(*row))
                return zipped
            else:
                zipped = row
        else:
            half_zipped = zip(*columns)
            
            # Map trough the half zipped columns.
            zipped = tuple(map(
                lambda s_row: tuple(
                    zip(*s_row)  # Zip if it's wrapped.
                ) if is_multi_row(
                    s_row  # Don't do anything on contrary.
                ) else s_row,
                half_zipped
            ))

        return zipped

    # @staticmethod
    # def __new_dict(key, value):
    #     """
    #     Simply a new dict out of key and value
    #     """
    #     new_dict = {}
    #     new_dict[key] = value
    #     return new_dict
    
    # end +-------------------------+ STATIC METHODS +--------------------------+ end
    # +-----------------------------------------------------------------------------+


    # TODO add the rest of getters
    # +-----------------------------------------------------------------------------+
    # start +---------------------------+ GETTERS +---------------------------+ start

    @property
    def columns(self) -> dict:
        """
        The data of the table by columns.
        
        Comes arranged in a dictionary with the 
        following structure::
        
            {
                'header': (data, data, ...),
                ...
            }
        """
        return self.__columns

    @property
    def headers(self) -> list:
        """
        The titles or headers of each column.
        A generic name appears if no name was provided
        for the column.
        """
        return self.__headers
    
    @property
    def internal_columns(self) -> dict:
        """
        Includes columns that the class adds internally,
        for now only the index column (when shown). 
        
        Uses the same format as the columns property.
        """
        if self.__show_index:
            return self.__columns_with_i
        else:
            return self.__columns
        
    
    @property
    def internal_headers(self) -> list:
        """
        Headers that includes the index column (when shown).
        """
        if self.__show_index:
            return self.__headers_with_i
        else:
            return self.__headers
        
    @property
    def rows(self) -> List[list]:
        """
        The data of the table as rows.
        """
        return self.__rows
    
    @property
    def internal_rows(self) -> List[list]:
        """
        The data of the table as rows, including the 
        index column (when shown).
        """
        if self.__show_index:
            return self.__rows_with_i
        else:
            return self.__rows

    @property
    def style_name(self) -> str:
        """
        The name of the style used to print the table.
        
        Default style is::
        
            'grid_eheader'
            
        The default style is selected if the provided
        one is incorrect (not one of the following)::
        
            'plain'            'pretty_grid' 
            'pretty_columns'   'bold_header' 
            'bheader_columns'  'bold_eheader' 
            'beheader_columns' 'bheader_ebody' 
            'round_edges'      're_eheader' 
            're_ebody'         'thin_borderline' 
            'th_bd_eheader'    'th_bd_ebody' 
            'th_bd_empty'      'bold_borderline' 
            'bd_bl_eheader'    'bd_bl_ebody' 
            'bd_bl_empty'      'pwrshll_alike' 
            'presto'           'grid' 
            'grid_eheader'     'grid_ebody' 
            'grid_empty'       'pipes' 
            'tilde_grid'       'tilg_eheader' 
            'tilg_columns'     'tilg_empty' 
            'orgtbl'           'clean' 
            'simple'           'simple_bold' 
            'simple_head'      'simple_head_bold' 
            'sim_th_bl'        'sim_bd_bl' 
            'sim_head_th_bl'   'sim_head_bd_bl' 
            'dashes'
            
        """
        return self.__checked_style_name

    @property
    def missing_value(self) -> Any:
        """
        A placeholder for empty cells.
        
        Default is::
        
            ''
        """
        return self.__missing_value

    @property
    def str_align(self): 
        return self.__str_align

    @property
    def int_align(self):
        return self.__int_align

    @property
    def float_align(self):
        return self.__float_align

    @property
    def bool_align(self):
        return self.__float_align

    @property
    def table_align(self):
        return self.__table_align

    @property
    def col_alignment(self):
        return self.__column_align

    @property
    def leading_zeros(self):
        return self.__leading_zeros

    @property
    def style_composition(self) -> TableComposition:
        """
        A named tuple that indicates the characters used
        for each line of the table.
        """
        return self.__style_composition

    @property
    def empty_rows_i(self) -> list:
        """
        A list with the indexes of the empty rows.
        """
        return self.__empty_row_indexes

    @property
    def empty_columns_i(self) -> list:
        """
        A list with the indexes of the empty columns.
        """
        if self.__show_index:
            
            # If the index column is shown, subtract 1 from the empty
            # columns indexes because it's only meant for visual
            # representation or internal count.
            return list(map(
                lambda empty_col_i: empty_col_i - 1,
                self.__empty_column_indexes
            ))
            
        return self.__empty_column_indexes

    @property
    def possible_styles(self):
        """
        Returns a tuple with the admitted style names.
        """
        return self.__possible_styles

    @property
    def row_count(self):
        """
        Returns the count of rows conditioned byt the
        ``show_empty_rows`` property.
        """
        return self.__row_count

    @property
    def column_count(self):
        """
        Returns the count of columns conditioned byt the
        ``show_empty_columns`` property.
        """
        if self.__show_index:
            return self.__column_count - 1
        return self.__column_count

    @property
    def internal_row_count(self):
        """
        Returns the count of rows including the index column
        and the empty rows (even if hidden).
        """
        return self.__real_row_count

    @property
    def internal_column_count(self):
        """
        Returns the count of rows including the index column
        and the empty rows (even if hidden).
        """
        return self.__checked_real_column_count
    
    @property
    def show_index(self) -> bool:
        """
        If set to::
        
            True  # An index column is added to the left.
            False # No index column is added (default).
        """
        return self.__show_index
    
    @property
    def index_start(self) -> int:
        """
        The starting number of the index count.
        """
        return self.__i_start
    
    @property
    def index_step(self):
        """
        Amount between each index number.
        """
        return self.__i_step
    
    @property
    def auto_wrap(self):
        """
        If set to::
        
            True  # The cells are wrapped if needed.
            False # They are trimmed instead (default).
        """
        return self.__auto_wrap_table
    
    # +----------------------+ SHOW GETTERS +------------------------+

    @property
    def show_headers(self):
        """
        If set to::
        
            True  # The headers are shown (default).
            False # The headers are hidden.
            
        The widths of the columns are adjusted to fit the headers,
        so if they are hidden the widths of the columns could
        change.
        """
        return self.__show_headers
    
    @property    
    def show_margin(self):
        return self.__show_margin

    @property
    def show_empty_rows(self):
        """
        If set to::
        
            True  # The empty rows are shown (default).
            False # The empty rows are hidden.
        """
        return self.__show_empty_rows

    @property
    def show_empty_columns(self):
        """
        If set to::
        
            True  # The empty columns are shown (default).
            False # The empty columns are hidden.
        """
        return self.__show_empty_columns

    # end +-----------------------------+ GETTERS +-----------------------------+ end
    # +-----------------------------------------------------------------------------+
    
    
    # TODO add the rest of setters
    # +-----------------------------------------------------------------------------+
    # start +---------------------------+ SETTERS +---------------- -----------+ start

    # @columns.setter
    # def columns(self, value: dict):
    #     self.__columns = {} if value is None else value

    # @headers.setter
    # def headers(self, value: list):
    #     self.__headers = [] if value is None else value
    #     self.__headers_with_i = [] if value is None else [I_COL_TIT, *value]

    @style_name.setter
    def style_name(self, value):
        __doc__ = read_file('style_examples.md')
        self.__style_name = value

    @missing_value.setter
    def missing_value(self, value):
        self.__missing_value = value

    @str_align.setter
    def str_align(self, value):
        self.__str_align = value

    @int_align.setter
    def int_align(self, value):
        self.__int_align = value

    @float_align.setter
    def float_align(self, value):
        self.__float_align = value

    @bool_align.setter
    def bool_align(self, value):
        self.__float_align = value

    @table_align.setter
    def table_align(self, value):
        self.__table_align = value

    @col_alignment.setter
    def col_alignment(self, value):
        self.__column_align = value

    @leading_zeros.setter
    def leading_zeros(self, value):
        self.__leading_zeros = value
        
    @show_index.setter
    def show_index(self, value: bool):
        self.__show_index = bool(value)
    
    @index_start.setter
    def index_start(self, value: int):
        try:
            self.__i_start = int(value)
        except ValueError:
            self.__i_start = 0
    
    @index_step.setter
    def index_step(self, value: int):
        try:
            self.__i_step = int(value)
        except ValueError:
            self.__i_step = 1
        
    @auto_wrap.setter
    def auto_wrap(self, value: bool):
        self.__auto_wrap_table = bool(value)

    # +----------------------+ SHOW SETTERS +------------------------+

    @show_headers.setter
    def show_headers(self, value: bool):
        self.__show_headers = bool(value)

    @show_margin.setter
    def show_margin(self, value: bool):
        self.__show_margin = bool(value)

    @show_empty_rows.setter
    def show_empty_rows(self, value: bool):
        self.__show_empty_rows = bool(value)

    @show_empty_columns.setter
    def show_empty_columns(self, value: bool):
        self.__show_empty_columns = value

    # end +-----------------------------+ SETTERS +-----------------------------+ end
    # +-----------------------------------------------------------------------------+


    # +-----------------------------------------------------------------------------+
    # start +---------------------+ PRIVATE PROPERTIES +----------------------+ start

    @property
    def __style_composition(self) -> TableComposition:
        """
        Gets the style composition using a checked name.
        """
        return style_catalogue.__getattribute__(self.__checked_style_name)

    @property
    def __checked_style_name(self) -> str:
        """
        Returns the used style name if it exists, 
        otherwise the default style name.
        """
        if self.__style_name in self.__possible_styles:
            return self.__style_name
        else:
            return DEFAULT_STYLE

    @property
    def __empty_row_indexes(self) -> list:
        """
        Search for empty columns using the ``__value_placer``
        
        If the count of those is the same as the length of the row,
        it's empty.
        """
        empty_rows = []
        for i, row in enumerate(self.__rows):
            if row.count(self.__value_placer) == len(row):
                empty_rows.append(i)
        return empty_rows

    @property
    def __empty_column_indexes(self) -> list:
        """
        Search for empty columns using the column types.
        
        A ``NoneType`` is considered empty.
        """
        none_type_columns = []
        for i, type_name in enumerate(self.__column_types_as_list):
            if type_name == TYPE_NAMES.none_type_:
                if self.__show_index:
                    none_type_columns.append(i + 1)
                else:
                    none_type_columns.append(i)
        return none_type_columns

    @property
    def __possible_styles(self) -> tuple:
        """
        The names of all the implemented styles.
        """
        return style_catalogue._fields

    @property
    def __row_count(self) -> int:
        """
        Returns the number of rows. 
        
        Affected by the ``show_empty_rows`` property.
        """
        checked_real_row_count = self.__real_row_count
        if self.__show_empty_rows:
            return checked_real_row_count
        else:
            updated_row_count = sum([
                checked_real_row_count,
                -len(self.__empty_row_indexes)
            ])
            return updated_row_count

    @property
    def __column_count(self) -> int:
        """
        Returns the number of columns.
        
        Affected by the ``show_empty_columns`` property.
        """
        if self.__show_empty_columns:
            return self.__checked_real_column_count
        else:
            updated_column_count = sum([
                self.__checked_real_column_count,
                -len(self.__empty_column_indexes)
            ])
            return updated_column_count
        
    @property
    def __checked_real_column_count(self) -> int:
        """
        Adds one to the real column count if the index 
        column is shown.
        """
        if self.__show_index:
            return self.__real_column_count + 1
        else:
            return self.__real_column_count
                
    # end +-----------------------+ PRIVATE PROPERTIES +------------------------+ end
    # +-----------------------------------------------------------------------------+


    # +-----------------------------------------------------------------------------+
    # start +------------------------+ COLUMN ADDING +------------------------+ start

    def add_column(self, 
                   header=None, 
                   data: Union[list, tuple]=None
                  ) -> None:
        """
        Add a column to the table.
        Can be left empty to add an empty column.

        ``header``: The title of the column. If not provided, 
        gets filled with a generic name.
        
        ``data``: Data provided in a list. If not 
        provided, column gets filled with the missing value.
        The Table class adjusts the columns when one or more
        are smaller or larger.
        
        Example::
        
            table = Table()
            table.add_column('Name', ['John', 'Jane'])
            table.add_column('Age', [20])
            table.add_column('Height', [1.75, 1.60, 1.75])
            table.add_column()
            table.missing_value = '?'
            
        Results in:
        
        >>> +--------------------------------+
        ... | Name   Age   Height   column 4 |
        ... +======+=====+========+==========+
        ... | John |  20 |   1.75 | ?        |
        ... | Jane |   ? |   1.6  | ?        |
        ... | ?    |   ? |   1.75 | ?        |
        ... +------+-----+--------+----------+
        
        """
        checked_header = self.__check_header(header)
        if checked_header not in self.__headers:
            self.__add_header(checked_header)
        self.__add_column_data(
            data=data, 
            column_header=checked_header
        )
        if checked_header not in self.__headers:  # This repeated if statement is needed.
            self.__adjust_columns_to_row_count()
        self.__check_existent_rows_vs_row_count()
        self.__transpose_column_to_rows(data)
        self.__adjust_rows_to_column_count(
            there_are_headers_to_add=False, 
            count_of_new_headers=1, 
            columns_added_before=True
        )
        
    def __get_auto_header(self) -> str:
        """
        Returns a generic name for a column.
        """
        return f'{self.__generic_column_name} {len(self.__headers) + 1}'
    
    def __name_duplicated_header(self, header: str) -> str:
        """
        Returns a name for a column if the name is already in use.
        """
        return f'{header} {self.__headers.count(header) + 1}'
        
    def __process_header(self, header: str) -> str:
        """
        Checks if header is None.
        
        If it is, will be replaced with a generic name.
        
        If the header already exists, a number matching
        the column count (starting from 1) will be added.
        """
        if header is None:
            checked = self.__get_auto_header()
        else:
            checked = str(header)
            if checked in self.__headers:
                checked = self.__name_duplicated_header(checked)
        
        return checked
    
    def __add_header(self, checked_header: str) -> None:
        self.__headers.append(checked_header)
        self.__headers_with_i.append(checked_header)
        self.__column_widths[checked_header] = 0
        self.__column_types[checked_header] = None
        self.__column_alignments[checked_header] = ''
        self.__cell_types[checked_header] = []
        self.__columns[checked_header] = []
        self.__columns_with_i[checked_header] = []
    
    def __check_add_header_on_init(self, header: str) -> str:
        checked_header = self.__process_header(header)
        self.__add_header(checked_header)
        
        return checked_header

    def  __check_header(self, header: Union[str, None]) -> str:
        try:
            column_count_from_rows = len(self.__rows[0])
        except IndexError:
            column_count_from_rows = 0
        header_count = len(self.__headers)
        if column_count_from_rows == header_count:
            # The header gets checked here because the add_row
            # method uses the __add_column_header too.
            checked_header = self.__process_header(header)
        else:
            checked_header = self.__headers[column_count_from_rows]
            
        return checked_header
    

    def __add_column_data(self, data: Union[list, tuple], column_header: str) -> None:
        """
        Add the data of the column.
        """
        self.__real_column_count += 1
        if data is not None:
            if len(data) > self.__real_row_count:
                
            # If the new column is bigger than the existing columns,
            # add the difference to the real row count.
                difference = len(data) - self.__real_row_count
                self.__real_row_count += difference
                
                for _ in range(difference):
                    # Add index counter to the table with index.
                    # This table is used when the index is shown.
                    self.__columns_with_i[I_COL_TIT].append(self.__index_counter)

            # Add to the table with and without index
            self.__columns[column_header] += data
            self.__columns_with_i[column_header] += data
            

    def __adjust_columns_to_row_count(self, rows_added_before: bool=False) -> None:
        """
        Make all the columns the same size.
        
        The point of reference is ``__real_row_count`` because
        the height of a column is determined by how many rows
        it has.
        """
        for header, column_body in self.__columns.items():
            
            # Check if the new column is bigger than the existing columns.
            # Once again, the point of reference is __real_row_count.
            difference = self.__real_row_count - len(column_body)
            
            for _ in range(difference):
                if rows_added_before:
                    # If there is rows added already, use insert, to put the
                    # value placer before them.
                    self.__columns[header].insert(0, self.__value_placer) 
                    self.__columns_with_i[header].insert(0, self.__value_placer)
                else:
                    # If there is no rows added yet, use append.
                    self.__columns[header].append(self.__value_placer)
                    self.__columns_with_i[header].append(self.__value_placer)
            
    def __transpose_column_to_rows(self, data: Union[list, tuple]) -> None:
        """
        Pass the column to the rows list.
        """
        for row_i in range(self.__real_row_count):
            self.__distribute_column_to_rows(
                row_i,
                data
            )

    def __distribute_column_to_rows(self, row_i: int, data: Union[list, tuple]) -> None:
        """
        Grab values from the column to put in the row.
        """
        try:
            # Try to get the piece of data from the column.
            value_to_add = data[row_i]
        except (IndexError, TypeError):
            # If there is no data, use the missing value (value placer).
            value_to_add = self.__value_placer
        
        # Add the value to the row.
        self.__rows[row_i].append(value_to_add)
        self.__rows_with_i[row_i].append(value_to_add)
        
    # end +--------------------------+ COLUMN ADDING +--------------------------+ end
    # +-----------------------------------------------------------------------------+


    # +-----------------------------------------------------------------------------+
    # start +-------------------------+ ROW ADDING +--------------------------+ start

    def add_row(self, data: Union[list, tuple]=None) -> None:
        """
        Add a row to the table. Can be left empty to add
        an empty row.

        ``data``: Data provided as any iterable.
        
        Example::
        
            table = Table()
            table.add_row(['size 1', 12.4325])
            table.add_row(['size 2', 111.22])
            table.add_row(['size 3', 0.4])
            table.add_row()
            table.add_row(['size 5', 39865])
            table.missing_value = '?'
        
        Results in:
        
        >>> +-----------------------+
        ... | column 1     column 2 |
        ... +==========+============+
        ... | size 1   |    12.4325 |
        ... | size 2   |   111.22   |
        ... | size 3   |     0.4    |
        ... | ?        |          ? |
        ... | size 5   | 39865      |
        ... +----------+------------+
        """
        self.__columns_with_i[I_COL_TIT].append(self.__index_counter)
        added_to_column_count = self.__add_row_data(data)
        add_headers = True if added_to_column_count is not None else False
        self.__adjust_rows_to_column_count(add_headers, added_to_column_count)
        self.__adjust_headers_to_data_length(data)
        self.__transpose_row_to_columns(data)
        self.__adjust_columns_to_row_count(rows_added_before=True)
        
    def __adjust_headers_to_data_length(self, data: Union[list, tuple]) -> None:
        if data is None:
            headers_to_add = 0
        else:
            headers_to_add = len(data) - len(self.__headers)
        for _ in range(headers_to_add):
            auto_named_header = self.__get_auto_header()
            self.__add_header(auto_named_header)
        
    def __add_row_data(self, data: Union[list, tuple]) -> Optional[int]:
        """
        Add the data of the new row.
        
        If data is ``None``, value placers are added.
        """
        # Create a new list in the rows list for the new row.
        self.__rows.append([])
        # For the index table, the new list gets added with an
        # index counter first (the index columns it's always first).
        self.__rows_with_i.append([self.__index_counter])
        
        self.__real_row_count += 1
        if data is None:
            # Add value placers if the row is empty.
            for _ in range(self.__checked_real_column_count):
                self.__rows[-1].append(self.__value_placer)
                self.__rows_with_i[-1].append(self.__value_placer)
        else:
            return self.__check_data_and_fill_last_row(data)

    def __adjust_rows_to_column_count(self, 
                                      there_are_headers_to_add: bool, 
                                      count_of_new_headers: int,
                                      columns_added_before: bool=False
                                     ) -> None:
        """
        Make all the rows the same size.
        
        The point of reference is ``__real_column_count`` because
        the width of a row is determined by how many columns
        has.
        """
        if there_are_headers_to_add:
            for _ in range(count_of_new_headers):
                auto_named_header = self.__get_auto_header()
                self.__add_header(auto_named_header)
        for row_i in range(self.__real_row_count):
            # Check if there is a difference between the column count
            # and the length of the new row (the length of the row is the
            # is how many columns it has).
            difference = self.__real_column_count - len(self.__rows[row_i])
            for _ in range(difference):
                if columns_added_before:
                    # If there is columns added already, use insert, to put the
                    # value placer before them.
                    self.__rows[row_i].insert(0, self.__value_placer)
                    self.__rows_with_i[row_i].insert(1, self.__value_placer)
                else:
                    # If there is no columns added yet, use append.
                    self.__rows[row_i].append(self.__value_placer)
                    self.__rows_with_i[row_i].append(self.__value_placer)

    def __transpose_row_to_columns(self, data: list) -> None:
        """
        Grab values from the row to put in the column.
        """
        for column_i in range(self.__checked_real_column_count):
            if data is None:
                self.__fil_column_from_empty_row(column_i)
            else:
                self.__fill_column_from_row(column_i, data)

    def __check_existent_rows_vs_row_count(self) -> None:
        """
        Check if the quantity of rows is less than the real count.
        
        If so, add the necessary rows (new lists).
        """
        if len(self.__rows) < self.__real_row_count:
            rows_to_add = self.__real_row_count - len(self.__rows)
            for _ in range(rows_to_add):
                # Single list for the table without index.
                self.__rows.append([])
                # Lis with index counter for the table with index.
                self.__rows_with_i.append([self.__index_counter])

    def __check_data_and_fill_last_row(self, data: list) -> Optional[int]:
        """
        Add the data to the rows.
        """
        added_columns_to_count = None
        if len(data) > self.__checked_real_column_count:
            if self.column_count < len(self.__headers):
                added_columns_to_count = 0
                self.__real_column_count += len(data) - self.column_count
            else:
                added_columns_to_count = len(data) - self.column_count
                self.__real_column_count += added_columns_to_count
        for column_i in range(self.__checked_real_column_count):
            try:
                self.__rows[-1].append(data[column_i])
                self.__rows_with_i[-1].append(data[column_i])
            except IndexError:
                self.__rows_with_i[-1].append(self.__value_placer)
        return added_columns_to_count

    def __fil_column_from_empty_row(self, column_i: int) -> None:
        """
        Put value placers on the column, because the row is empty.
        """
        try:
            self.__columns[self.__headers[column_i]].append(self.__value_placer)
            self.__columns_with_i[self.__headers[column_i]].append(self.__value_placer)
        except IndexError:
            pass

    def __fill_column_from_row(self, column_i: int, data: list) -> None:
        """
        Put the value from the row in the column.
        """
        try:
            self.__columns[self.__headers[column_i]].append(data[column_i])
            self.__columns_with_i[self.__headers[column_i]].append(data[column_i])
        except IndexError:
            self.__fil_column_from_empty_row(column_i)

    # end +---------------------------+ ROW ADDING +----------------------------+ end
    # +-----------------------------------------------------------------------------+

    # +-----------------------------------------------------------------------------+
    # start +-------------------+ STRING TABLE COMPOSITION +------------------+ start

    # +----------------------+ NUMBER PARSING +----------------------+
    
    # def __parse_numbers(self):
    #     pass

    # def __parse_float(self):
    #     pass

    # def __parse_int_boolean(self):
    #     pass

    # def __parse_exponentials(self):
    #     pass

    # def __parse_bytes(self):
    #     pass

    # def __parse_escape_codes(self):
    #     pass

    # +------------------------+ TABLE BODY +------------------------+

    def compose(self) -> str:
        """
        Crafts the table and returns it as a string.
        """
        if len(self.__columns) != 0:
            # self.__parse_data()  # TODO add parsing
            rows, rows_with_i = self.__call_table_objects()
            self.__typify_table()
            self.__wrap_data(
                rows, 
                rows_with_i, 
                semi=True
            )
            self.__get_column_widths(semi=True)
            table_width = self.__get_string_table_width()
            headers, rows, rows_with_i = self.__check_columns_size(
                table_width, 
                rows, 
                rows_with_i
            )
            self.__wrap_data(
                rows, 
                rows_with_i, 
                semi=False,
                headers_after_semi=headers
            )
            self.__get_column_widths(semi=False)

        return self.__form_string(
            table_with_i=self.__show_index
        )

    def __get_string_table_width(self) -> int:
        """
        Gets the horizontal width of the table::
        
            |---------- 25 ---------|
        
            +-----------------------+
            | column 1     column 2 |
            +==========+============+
            | size 1   |    12.4325 |
            | size 2   |   111.22   |
            | size 3   |     0.4    |
            | ?        |          ? |
            | size 5   | 39865      |
            +----------+------------+
        """
        one_column_margin = self.__style_composition.margin * 2
        all_columns_margin = one_column_margin * self.column_count
        vertical_body_lines: SeparatorLine = (
            self.__style_composition.vertical_table_body_lines
        )
        separator_count = self.__column_count - 1
        left_len = self.__check_if_none_and_get_len(vertical_body_lines.left)
        right_len = self.__check_if_none_and_get_len(vertical_body_lines.right)
        middle_len = self.__check_if_none_and_get_len(vertical_body_lines.middle)   
        if not self.__show_index:     
            separators_of_table = sum([
                left_len,
                (middle_len * separator_count),
                right_len
            ])
            table_width = sum([
                *self.__column_widths_as_list,
                all_columns_margin,
                separators_of_table
            ])
            return table_width
        else:
            separators_of_table_with_i = sum([
                left_len,
                middle_len * separator_count,
                right_len
            ])
            table_width_with_i = sum([
                *self.__column_widths_as_list_with_i,
                all_columns_margin + one_column_margin,
                separators_of_table_with_i
            ])
            return table_width_with_i
        
    def __check_columns_size(self, 
                             table_width: int, 
                             rows: list, 
                             rows_with_i: list
                            ) -> Tuple[list, list]:
        """
        Checks the difference between the width of the table and the 
        width of the terminal.
        
        It adjusts the column widths if necessary.
        """
        adjust = False
        difference = 0
        console_cols, console_lines = get_window_size()
        if console_cols < table_width:
            difference = (table_width - console_cols) + 1
            adjust = True
        if adjust:
            headers, rows, rows_with_i = self.__adjust_column_widths(
                difference,
                rows, 
                rows_with_i
            )
        else:
            if self.show_index:
                headers = self.__headers_with_i
            else:
                headers = self.__headers
        return headers, rows, rows_with_i
    
    def __get_amounts_to_reduce(self, difference: int) -> list:
        """
        Determines the amount of space to reduce to each column.
        
        Index column will never get its space reduced.
        """
        if self.__show_index:
            sums_of_widths = sum(self.__column_widths_as_list_with_i)
            widths = self.__column_widths_as_list_with_i
            widths.pop(0)
        else:
            sums_of_widths = sum(self.__column_widths_as_list)
            widths = self.__column_alignments_as_list
        proportions = [
            col_width / sums_of_widths 
            for col_width in widths
        ]
        trimm_sign_len = len(DEFAULT_TRIMMING_SIGN)
        amnt_to_reduce_per_column = [
            round(prop * difference) + (trimm_sign_len if (
                not self.__auto_wrap_table
            ) else 0)
            for prop in proportions
        ]
        if self.show_index:
            amnt_to_reduce_per_column.insert(0, 0)
        
        return amnt_to_reduce_per_column
    
    def __adjust_column_widths(self, 
                               difference: int, 
                               rows: List[list], 
                               rows_with_i: List[list]
                              ) -> Tuple[list, List[list], List[list]]:
        """
        Reduces the difference provided to each column.
        """
        if self.__show_index:
            columns_with_i = list(map(list, zip(*rows_with_i)))
            columns = rows  # will remain untouched
        else:
            columns_with_i = rows_with_i  # will remain untouched
            columns = list(map(list, zip(*rows)))
        to_reduce_per_col = self.__get_amounts_to_reduce(difference)
        adjusted_headers = []
        adjusted_columns = []
        for col_i , to_reduce in enumerate(to_reduce_per_col):
            if self.__show_index:
                wpped_header, wpped_body = self.__adjust_column_to_new_width(
                    col_i, 
                    to_reduce,
                    columns_with_i,
                )
            else:
                wpped_header, wpped_body = self.__adjust_column_to_new_width(
                    col_i, 
                    to_reduce,
                    columns,
                )
            adjusted_headers.append(wpped_header)
            adjusted_columns.append(wpped_body)
        if self.__show_index:
            return adjusted_headers, rows, zip(*adjusted_columns)
        else:
            return adjusted_headers, zip(*adjusted_columns), rows_with_i
    
    def __wrap_columns(self, 
                       column_i: int, 
                       columns: List[list], 
                       new_width: int, 
                       index: int
                      ) -> Tuple[str, List[list]]:
        """
        Wraps the column with the provided width::
        
            'Wrapped\\ndata'
        """
        col_to_wrap = columns[column_i]
        if self.show_index:
            header_to_wrap = self.__headers_with_i[column_i]
        else:            
            header_to_wrap = self.__headers[column_i]
        header_to_wrap = self.__apply_wrap(
            header_to_wrap, 
            new_width
        )
        for row_i, row in enumerate(col_to_wrap):
            wrapped = self.__apply_wrap(row, new_width)
            col_to_wrap[row_i] = wrapped
            
        return header_to_wrap, col_to_wrap
    
    def __trim_column(self, 
                      column_i: int, 
                      columns: List[list], 
                      new_width: int, 
                      index: int
                     ) -> Tuple[str, List[list]]:
        """
        Trims the column with the provided width::
        
            'Trimmed d...'
        """
        col_to_trim = columns[column_i]
        if self.show_index:
            header_to_trim = self.__headers_with_i[column_i]
        else:
            header_to_trim = self.__headers[column_i]
        if len(str(header_to_trim)) > new_width:
            header_to_trim = self.__trim_with_sign(
                header_to_trim, 
                new_width
            )
        for row_i, row in enumerate(col_to_trim):
            if len(str(row)) > new_width:
                trimmed = self.__trim_with_sign(
                    row,
                    new_width
                )
                col_to_trim[row_i] = trimmed
        
        return header_to_trim, col_to_trim
    
    def __wrap_or_trim_data(self, 
                            column_i: int, 
                            new_width: int, 
                            columns: List[list], 
                            index: bool,
                            col_type_name: str, 
                            column_title: str
                           ) -> Tuple[str, List[list]]:
        """
        Wraps or trims the data of a column, depending on the type
        and the ``__auto_wrap_table`` setting.
        """
        trim_alignment = type_alignments[TYPE_NAMES.str_]
        can_wrap = col_type_name in CAN_WRAP_TYPES and self.__auto_wrap_table
        if can_wrap:
            return self.__wrap_columns(
                column_i=column_i,
                columns=columns,
                new_width=new_width,
                index=True
            )
        else:
            if index:
                self.__column_alignments[
                    column_title
                ] = trim_alignment
                self.__column_alignments_as_list[
                    column_i
                ] = trim_alignment
            else:
                self.__column_alignments_with_i[
                    column_title
                ] = trim_alignment
                self.__column_alignments_as_list_with_i[
                    column_i
                ] = trim_alignment
            return self.__trim_column(
                column_i=column_i,
                columns=columns,
                new_width=new_width,
                index=True
            )
        
    def __adjust_column_to_new_width(self, 
                                     column_i: int, 
                                     to_reduce: int, 
                                     columns: List[list]
                                    ) -> Tuple[str, List[list]]:
        """
        Will adjust a column to the provided width.
        """
        if self.__show_index:
            col_title = self.__headers_with_i[column_i]
            col_type = self.__column_types_as_list_with_i[column_i]
            new_width = sum([
                self.__column_widths_with_i[col_title],
                -to_reduce
            ])
        else:
            col_title = self.__headers[column_i]
            col_type = self.__column_types_as_list[column_i]
            new_width = sum([
                self.__column_widths[col_title],
                -to_reduce
            ])
        return self.__wrap_or_trim_data(
            column_i,
            new_width,
            columns,
            index=False,
            col_type_name=col_type,
            column_title=col_title
        )
            
    
    def __call_table_objects(self):
        """
        This is to call the ``__call__`` method of the 
        stored objects in the table.

        returns:: 
            
            rows, rows_with_i 
        """
        # For adding the index. The index is in the first column
        # or the index 0.
        rows_with_i = deepcopy(self.__rows_with_i)
        for row_i, row in enumerate(rows_with_i):
            if self.__show_empty_rows:
                rows_with_i[row_i][0] = row[0](
                    self.__i_start,
                    self.__i_step,
                )
            else:
                rows_with_i[row_i][0] = row[0](
                    self.__i_start,
                    self.__i_step,
                    row_i not in self.__empty_row_indexes
                )
            # For adding the missing value where the ValuePlacer
            # is used (in the rows with index).
            for column_i, column in enumerate(row):
                if isinstance(column, ValuePlacer):
                    rows_with_i[row_i][column_i] = column(
                        self.__missing_value
                    )
                
        # For adding the missing value where the ValuePlacer
        # is used.
        rows = deepcopy(self.__rows)
        for row_i, row in enumerate(rows):
            for column_i, column in enumerate(row):
                if isinstance(column, ValuePlacer):
                    rows[row_i][column_i] = column(
                        self.__missing_value
                    )
        
        return rows, rows_with_i
    
    def __typify_table(self):
        for column_i, column in enumerate(self.__columns.items()):
            self.__typify_single_column(column, column_i)
        for column_i, column in enumerate(self.__columns_with_i.items()):
            self.__typify_single_column_with_i(column, column_i)
                
    def __typify_single_column(self, column, column_i):
        header, column_content = column
        cell_types, column_type, column_alignment = _typify_column(column_content)
        try:
            self.__column_i_per_type[column_type].append(column_i)
        except KeyError:
            self.__column_i_per_type[column_type] = []
            self.__column_i_per_type[column_type].append(column_i)
        self.__column_types[header] = column_type
        self.__cell_types[header] = cell_types
        self.__column_alignments[header] = column_alignment
        try:
            self.__column_alignments_as_list[column_i] = column_alignment
            self.__column_types_as_list[column_i] = column_type
        except IndexError:
            self.__column_alignments_as_list.append(column_alignment)
            self.__column_types_as_list.append(column_type)
        
    def __typify_single_column_with_i(self, column, column_i):
        header, column_content = column
        if column_i == 0:
            is_index = True
        else:
            is_index = False
        cell_types, column_type, column_alignment = _typify_column(
            column_content,
            index_column=is_index
        )
        try:
            self.__column_i_per_type_with_i[column_type].append(column_i)
        except KeyError:
            self.__column_i_per_type_with_i[column_type] = []
            self.__column_i_per_type_with_i[column_type].append(column_i)
        self.__column_types_with_i[header] = column_type
        self.__cell_types_with_i[header] = cell_types
        self.__column_alignments_with_i[header] = column_alignment
        try:
            self.__column_alignments_as_list_with_i[column_i] = column_alignment
            self.__column_types_as_list_with_i[column_i] = column_type
        except IndexError:
            self.__column_alignments_as_list_with_i.append(column_alignment)
            self.__column_types_as_list_with_i.append(column_type)

    def __wrap_data(self, 
                    rows, 
                    rows_with_i, 
                    semi,
                    headers_after_semi = []
                   ) -> None:
        if semi:
            headers_with_i = self.__headers_with_i
            headers = self.__headers
        else:
            headers_with_i = headers_after_semi
            headers = headers_after_semi
            
        if self.show_index:
            headers = headers_with_i
            rows = rows_with_i
            semi_processed_columns = self.__semi_processed_columns_with_i
            processed_columns = self.__processed_columns_with_i
        else:
            semi_processed_columns = self.__semi_processed_columns
            processed_columns = self.__processed_columns
            
        wrapped_headers, wrapped_rows = _wrap_rows(
            headers, 
            rows
        )
        transformed_columns, transformed_headers = _zip_wrapped_rows(
            wrapped_headers, 
            wrapped_rows, 
        )
        
        if self.show_index:
            columns_to_iterate = {I_COL_TIT: [], **self.__columns}.items()
        else:
            columns_to_iterate = self.__columns.items()
        for i, column in enumerate(columns_to_iterate):
            header, _ = column
            if semi:
                semi_processed_columns[header] = {
                    'header': transformed_headers[i],
                    'data': transformed_columns[i]
                }
            else:
                processed_columns[header] = {
                    'header': transformed_headers[i],
                    'data': transformed_columns[i]
                }

                
    def __get_column_widths(self, semi):
        if self.show_index:
            sizes_with_i, float_sizes_with_i = _column_widths(
                processed_columns=(
                    self.__semi_processed_columns_with_i
                ) if semi else (
                    self.__processed_columns_with_i
                ),
                column_type_names=self.__column_types_with_i,
                show_headers=self.__show_headers
            )
            self.__column_widths_as_list_with_i = sizes_with_i
            if float_sizes_with_i is not None:
                self.__float_columns_widths_with_i = {
                    **self.__float_columns_widths_with_i,
                    **float_sizes_with_i
                }
            for column_i, column in enumerate(self.__columns_with_i.items()):
                header, _ = column
                self.__column_widths_with_i[header] = sizes_with_i[column_i]
        else:
            sizes, float_sizes = _column_widths(
                processed_columns=(
                    self.__semi_processed_columns
                ) if semi else (
                    self.__processed_columns
                ),
                column_type_names=self.__column_types,
                show_headers=self.__show_headers
            )
            self.__column_widths_as_list = sizes
            if float_sizes is not None:
                self.__float_columns_widths = {
                    **self.__float_columns_widths,
                    **float_sizes
                }
            for column_i, column in enumerate(self.__columns.items()):
                header, _ = column
                self.__column_widths[header] = sizes[column_i]
        

    def __parse_data(self):
        pass

    def __form_string(self, table_with_i=False):
        # Data from column dict is put in tuples
        unaligned_columns = self.__get_processed_columns_data(
            columns_with_i=table_with_i
        )
        unaligned_header = self.__get_processed_columns_data(
            header=True,
            columns_with_i=table_with_i
        )
        if table_with_i:
            column_titles = self.__headers_with_i
            column_alignments_list = self.__column_alignments_as_list_with_i
            column_widths_list = self.__column_widths_as_list_with_i
            column_widths = self.__column_widths_with_i
            float_column_widths = self.__float_columns_widths_with_i
        else:
            column_titles = self.__headers
            column_alignments_list = self.__column_alignments_as_list
            column_widths_list = self.__column_widths_as_list
            column_widths = self.__column_widths
            float_column_widths = self.__float_columns_widths
        # Header and body rows get aligned
        aligned_header = _align_headers(
            self.__style_composition,
            unaligned_header,
            column_alignments_list,
            column_widths_list,
            self.__empty_column_indexes,
            self.__show_empty_columns,
            float_column_widths
        )
        aligned_header = self.__zip_columns(aligned_header, headers=True)
        aligned_columns = _align_columns(
            self.__style_composition,
            unaligned_columns,
            column_titles,  # here the header is used to know the title of the column
            column_alignments_list,
            column_widths_list,
            self.__empty_column_indexes,
            self.__show_empty_columns,
            float_column_widths
        )
        aligned_columns = self.__zip_columns(aligned_columns)
        # String separators and data rows are joined
        separators: HorizontalComposition = _get_separators(
            self.__style_composition,
            tuple(column_widths.values()),
            self.__empty_column_indexes,
            self.__show_empty_columns
        )
        data_rows: DataRows = _get_data_rows(
            self.__style_composition, 
            aligned_header, 
            aligned_columns,
            self.__show_headers,
            self.__empty_row_indexes,
            self.__show_empty_rows,
        )

        # Table string is formed
        header_superior = ''.join([separators.superior_header_line, '\n']) if (
                separators.superior_header_line is not None
        ) else NONE_VALUE_REPLACEMENT
        no_header_superior = separators.superior_header_line_no_header
        header_inferior = ''.join(['\n', separators.inferior_header_line]) if (
                separators.inferior_header_line is not None
        ) else NONE_VALUE_REPLACEMENT
        body_line = ''.join(['\n', separators.table_body_line]) if (
                separators.table_body_line is not None
        ) else NONE_VALUE_REPLACEMENT
        end_line = separators.table_end_line

        header_row = data_rows.header_row
        body_rows = data_rows.body_rows

        if self.__show_headers:
            superior_row = ''.join([header_superior, header_row, header_inferior])
        else:
            superior_row = no_header_superior

        if superior_row is None and end_line is not None:
            table_string = '\n'.join([f'{body_line}\n'.join(body_rows), end_line])
        elif end_line is None and superior_row is not None:
            table_string = '\n'.join([superior_row, f'{body_line}\n'.join(body_rows)])
        elif superior_row is None and end_line is None:
            table_string = f'{body_line}\n'.join(body_rows)
        else:
            table_string = '\n'.join([superior_row, f'{body_line}\n'.join(body_rows), end_line])

        return table_string

    def __get_processed_columns_data(self, header=False, columns_with_i=False):
        if columns_with_i:
            columns_with_headers = self.__processed_columns_with_i.values()
        else:
            columns_with_headers = self.__processed_columns.values()
        for column_w_h in columns_with_headers:
            get = 'header' if header else 'data'
            yield column_w_h[get]

    # +------------------------+ TABLE BODY +------------------------+

    # end +---------------------+ STRING TABLE COMPOSITION +--------------------+ end
    # +-----------------------------------------------------------------------------+

    # +-----------------------------------------------------------------------------+
    # start +------------------------+ DATA READING +-------------------------+ start

    def __read_pandas_dataframe(self):
        pass

    def __read_csv_file(self):
        pass

    def __read_html_table(self):
        pass

    def __read_text_file(self):
        pass

    # end +--------------------------+ DATA READING +---------------------------+ end
    # +-----------------------------------------------------------------------------+


if __name__ == '__main__':
    print('This is not supposed to be shown!')
