import io

from backports import csv

COMMENT_CHAR = u'#'

DEFAULT_DELIMITER = u';'
DEFAULT_LINETERMINATOR = u'\n'


def strip_comments_and_empty_lines(lines):
    for line in lines:
        if not line.startswith(COMMENT_CHAR) and line.strip():
            yield line.strip()


def _read_csv(file_path, delimiter=DEFAULT_DELIMITER):
    return csv.reader(
        read_lines(file_path),
        delimiter=delimiter
    )


def _write_csv(
        file_path,
        data,
        delimiter=DEFAULT_DELIMITER,
        lineterminator=DEFAULT_LINETERMINATOR):
    with io.open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(
            f,
            delimiter=delimiter,
            lineterminator=lineterminator
        )
        writer.writerows(data)


def read_lines(file_path):
    with io.open(file_path, 'r', newline='', encoding='utf-8') as f:
        for line in strip_comments_and_empty_lines(f):
            yield line


read_map = _read_csv

write_map = _write_csv


def read_list(file_path):
    return [item[0] for item in _read_csv(file_path)]


def write_list(file_path, data):
    _write_csv(
        file_path,
        [[item] for item in data]
    )
