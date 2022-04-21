from .cells import (
    _center_cell, 
    _ljust_cell, 
    _rjust_cell, 
    _add_cell_spacing
)
from .style_compositions import TableComposition
from .utils import (
    is_some_instance,
    IndexCounter,
    ValuePlacer
)
from .options import DEFAULT_FILL_CHAR

from typing import List
from collections import namedtuple


TypeNames = namedtuple(
    'TypeNames',
    [
        'bool_',
        'str_',
        'int_',
        'float_',
        'bytes_',
        'none_type_',
        'index_counter_',
        'value_placer_',
    ]
) 


TYPE_NAMES = TypeNames(
    bool_=bool.__name__,
    str_=str.__name__,
    int_=int.__name__,
    float_=float.__name__,
    bytes_=bytes.__name__,
    none_type_=type(None).__name__,
    index_counter_=IndexCounter.__name__,
    value_placer_=ValuePlacer.__name__,
)


def __check_for_types_in_column(column_types: list, 
                                accepted_types: list):
    for type_ in column_types:
        if type_ not in accepted_types:
            return False
                
    return True


def __is_str_column(column_types: list):
    comprobation = __check_for_types_in_column(
        column_types=column_types,
        accepted_types=list(TYPE_NAMES)
    )
    return comprobation


def __is_byte_column(column_types: list):
    comprobation = __check_for_types_in_column(
        column_types=column_types,
        accepted_types=[
            TYPE_NAMES.bytes_,
            TYPE_NAMES.value_placer_
        ]
    )
    return comprobation


def __is_int_column(column_types: list):
    comprobation = __check_for_types_in_column(
        column_types=column_types,
        accepted_types=[
            TYPE_NAMES.int_,
            TYPE_NAMES.bool_,
            TYPE_NAMES.value_placer_,
            TYPE_NAMES.index_counter_
        ]
    )
    return comprobation
    
    
def __is_float_column(column_types: list):
    comprobation = __check_for_types_in_column(
        column_types=column_types,
        accepted_types=[
            TYPE_NAMES.float_,
            TYPE_NAMES.int_,
        ]
    )
    return comprobation


def __is_bool_column(column_types: bool):
    comprobation = __check_for_types_in_column(
        column_types=column_types,
        accepted_types=[
            TYPE_NAMES.bool_,
            TYPE_NAMES.value_placer_
        ]
    )
    return comprobation


def __is_none_type(column_types: list):
    comprobation = __check_for_types_in_column(
        column_types=column_types,
        accepted_types=[
            TYPE_NAMES.none_type_,
            TYPE_NAMES.value_placer_
        ]
    )
    return comprobation


def __get_column_type(column_types):
    if __is_none_type(column_types):
        return TYPE_NAMES.none_type_
    if __is_byte_column(column_types):
        return TYPE_NAMES.bytes_
    if __is_int_column(column_types):
        return TYPE_NAMES.int_
    if __is_float_column(column_types):
        return TYPE_NAMES.float_
    if __is_bool_column(column_types):
        return TYPE_NAMES.bool_
    if __is_str_column(column_types):
        return TYPE_NAMES.str_
    else:
        return TYPE_NAMES.none_type_


ALIGNMENST_PER_TYPE = {
    'bool': 'r',
    'str': 'l',
    'int': 'r',
    'float': 'f',
    'bytes': 'b',
    'NoneType': 'l',
}


def _column_sizes(columns: dict, show_headers: bool):
    # TODO add support for colouring codes

    if show_headers:
        head_sizes = [
            max([len(str(row)) for row in column['header']]) if (
                is_some_instance(column['header'], tuple, list)
            ) else len(str(column['header']))
            for _, column in columns.items()
        ]
    body_sizes = [
        max([
            max([len(str(sbRow)) for sbRow in row]) if (
                is_some_instance(row, tuple, list)
            ) else len(str(row))
            for row in column['data']
        ])
        for _, column in columns.items()
    ]

    if show_headers:
        sizes = list(map(lambda x, y: max(x, y), head_sizes, body_sizes))
    else:    
        sizes = body_sizes

    return sizes


def _typify_column(column, index_column=False):  # TODO make typify work with missing val to not alter column type
    """
    Get the types of the column and it's alignments
    """
    # create = False
    # if column_alignment is not None:
    #     return colSizes
    # else:
    #     create = True

    identified_types = []

    for row in column:
        if index_column:
            identified_types.append(int.__name__)
        elif row != '':
            identified_types.append(type(row).__name__)
        else:
            identified_types.append(type(None).__name__)

    column_type = __get_column_type(identified_types)
    column_alignment = ALIGNMENST_PER_TYPE[column_type]

    return identified_types, column_type, column_alignment


def __align_single_cell(cell, col_width, to_where, margin):
    new_cell = cell
    if to_where == 'l':
        new_cell = _ljust_cell(cell, col_width, DEFAULT_FILL_CHAR)
    elif to_where == 'c':
        new_cell = _center_cell(cell, col_width, DEFAULT_FILL_CHAR)
    elif to_where in ['r']:
        new_cell = _rjust_cell(cell, col_width, DEFAULT_FILL_CHAR)
    new_cell = _add_cell_spacing(new_cell, margin, margin, 0)
    return new_cell


def __align_one_column_row(cell, col_width, to_where, margin):
    new_cell = __align_single_cell(cell, col_width, to_where, margin)
    if is_some_instance(new_cell, tuple, list):
        return tuple(new_cell)
    else:
        return new_cell


def __align_one_column(column, column_i, col_alignments, col_widths,
                       margin, show_empty, empty_row_i):
    aligned_column = list()
    to_where = col_alignments[column_i]
    col_width = col_widths[column_i]
    for row_i, cell in enumerate(column):
        if not show_empty and row_i not in empty_row_i:
            aligned_column.append(
                __align_one_column_row(cell, col_width, to_where, margin)
            )
        elif show_empty:
            aligned_column.append(
                __align_one_column_row(cell, col_width, to_where, margin)
            )
        else:
            continue

    yield tuple(aligned_column)


def _align_columns(style_composition: TableComposition, columns,
                   col_alignments: List[str], col_widths: List[int],
                   empty_columns_i: List[int], empty_rows_i: List[int],
                   show_empty: bool):
    margin = style_composition.margin
    for column_i, column in enumerate(columns):
        if not show_empty and column_i not in empty_columns_i:
            yield from __align_one_column(
                column, 
                column_i, 
                col_alignments, 
                col_widths, 
                margin,
                show_empty,
                empty_rows_i
            )
        elif show_empty:
            yield from __align_one_column(
                column, 
                column_i, 
                col_alignments, 
                col_widths, 
                margin,
                show_empty,
                empty_rows_i
            )
        else:
            continue
    
        
def __align_one_header(column, col_width, to_where, margin):
    if is_some_instance(column, tuple, list):
        yield tuple(map(
            lambda cell: __align_single_cell(
                cell, 
                col_width, 
                to_where, 
                margin),
            column
        ))
    else:
        yield __align_single_cell(column, col_width, to_where, margin)


def _align_headers(style_composition: TableComposition, headers,
                   col_alignments: List[str], col_widths: List[int],
                   empty_columns_i: List[int], show_empty: bool):
    margin = style_composition.margin

    for column_i, column in enumerate(headers):
        to_where = col_alignments[column_i]
        col_width = col_widths[column_i]
        if not show_empty and column_i not in empty_columns_i:
            yield from __align_one_header(column, col_width, to_where, margin)
        elif show_empty:
            yield from __align_one_header(column, col_width, to_where, margin)
        else:
            continue
             


if __name__ == '__main__':
    print('Hey! This is not to be executed.')
