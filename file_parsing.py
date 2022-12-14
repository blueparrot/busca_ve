import os
import csv
from typing import Union, Iterator

import chardet
from dbfread import DBF


def get_csv_separator(file: Union[str, os.PathLike]) -> str:
    with open(file, "r") as csvfile:
        return csv.Sniffer().sniff(csvfile.readline()).delimiter


def get_csv_encoding(file: Union[str, os.PathLike]) -> str:
    with open(file, "rb") as rawdata:
        result = chardet.detect(rawdata.read(5000))
        return result["encoding"]


def get_csv_columns(file: Union[str, os.PathLike]) -> list[str]:
    column_names = []
    with open(file, encoding=get_csv_encoding(file)) as csvfile:
        reader = csv.reader(csvfile, delimiter=get_csv_separator(file))
        for row in reader:
            column_names.append(row)
            break
        return column_names[0]


def get_dbf_columns(file: Union[str, os.PathLike]) -> list[str]:
    with DBF(file) as table:
        return table.field_names


def get_columns(file: Union[str, os.PathLike]) -> list[str]:
    _, file_extension = os.path.splitext(file)
    if file_extension.upper() == ".CSV":
        file_cols = get_csv_columns(file)
    if file_extension.upper() == ".DBF":
        file_cols = get_dbf_columns(file)
    return file_cols


def csv_streamer(file: Union[str, os.PathLike]) -> Iterator[dict[str, str]]:
    with open(file, encoding=get_csv_encoding(file)) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=get_csv_separator(file))
        for row in reader:
            yield (row)


def dbf_streamer(file: Union[str, os.PathLike]) -> Iterator[dict[str, str]]:
    with DBF(file, encoding="cp850") as table:
        for record in table:
            yield (dict(record))


def file_streamer(file: Union[str, os.PathLike]) -> Iterator[dict[str, str]]:
    _, file_extension = os.path.splitext(file)
    if file_extension.upper() == ".CSV":
        streamer = csv_streamer
    if file_extension.upper() == ".DBF":
        streamer = dbf_streamer
    return streamer(file)
