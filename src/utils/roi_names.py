# This file contains utility functions to convert the ROI labels and indexes in different formats

def roi_indexes_to_compact_label(x: int, y: int):
    return f"({x}; {y})"


def roi_compact_label_to_indexes(label: str):
    without_parentheses = label.replace('(', '').replace(')', '')
    x_str, y_str = without_parentheses.split(';')
    x, y = int(x_str), int(y_str)
    return x, y


def roi_indexes_to_filename(x: int, y: int, max_digits: int):
    x_formatted = f'{x:0{max_digits}d}'
    y_formatted = f'{y:0{max_digits}d}'
    file_name = f'({x_formatted}; {y_formatted}).roi'
    return file_name


def roi_filename_to_indexes():
    raise NotImplementedError()


def roi_indexes_to_imagej_label(x: int, y: int):
    return f'Mean(({x}; {y}))'


def roi_imagej_label_to_indexes():
    raise NotImplementedError()


def roi_indexes_to_linear_index(x: int, y: int, n_horizontal: int):
    """Takes in an index pair (x, y) and converts it to a linear index z"""
    return x * n_horizontal + y


def roi_linear_index_to_indexes(idx: int, n_horizontal: int):
    """Takes in a linear index z and converts it to a pair of indexes (x, y)"""
    y = idx % n_horizontal
    x = idx // n_horizontal
    return x, y


def roi_linear_index_to_compact_label(idx: int, n_horizontal: int):
    x, y = roi_linear_index_to_indexes(idx, n_horizontal)
    return roi_indexes_to_compact_label(x, y)
