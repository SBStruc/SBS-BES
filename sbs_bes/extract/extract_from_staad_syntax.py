import re
import pandas as pd
from typing import Iterator


def extract_beam_groups(doc_lines: list[str]) -> pd.DataFrame:
    try:
        bg_start_index: int = doc_lines.index("MEMBER\n")
        bg_end_index: int = doc_lines.index("END GROUP DEFINITION\n")
        bg_lines: list[str] = clean_bg_lines(doc_lines[bg_start_index:bg_end_index])

    except ValueError:
        raise ValueError(
            "Wrong file. No START GROUP DEFINITION or END GROUP DEFINITION"
        )

    return load_groups_to_df(bg_lines)


def extract_beam_dimensions(doc_lines: list[str]) -> pd.DataFrame:
    try:
        bd_start_index: int = doc_lines.index("MEMBER PROPERTY AMERICAN\n")
        bd_end_index: int = -1
        for idx, bd_line in enumerate(
            doc_lines[bd_start_index + 1 :], start=bd_start_index + 1  # noqa
        ):
            if re.match(r"^[A-Z\s]+\n$", bd_line):
                bd_end_index = idx
                break
        if bd_end_index == -1:
            raise Exception
        bd_lines: list[str] = clean_bd_lines(doc_lines[bd_start_index:bd_end_index])
    except Exception as e:
        raise ValueError(f"{e}\nWrong file. No MEMBER PROPERTY AMERICAN or CONSTANTS")

    return load_dim_to_df(bd_lines)


def clean_bg_lines(document_lines: list[str]) -> list[str]:
    """
    - remove useless header lines (START GROUP DEFINITION, etc)
    - removes underscores and new lines
    - replace `TO` with number series using `extract_member_group_numbers` function
    - append succeeding lines to current lines with dahses using `concatenate_lines` function
    - remove lines that does not contain beam names
    """

    cleaned_lines: list[str] = concatenate_lines(
        [
            extract_member_group_numbers(re.sub(r"\n|_", "", line))
            for line in document_lines
            if not re.match(r"^[A-Z\s\\n]+$", line)
        ]
    )

    # remove lines not starting with beam names
    return [line for line in cleaned_lines if re.match(r"^\d*[A-Z]", line)]


def clean_bd_lines(document_lines: list[str]) -> list[str]:
    """
    - remove useless header lines (START GROUP DEFINITION, FLOOR, etc.)
    - removes underscores and new lines using `clean_line` function,
    - append succeeding lines to current lines with dahses using `concatenate_lines` function
    - remove lines that does not contain beam names
    """

    cleaned_lines: list[str] = concatenate_lines(
        [
            re.sub(r"\n|_", "", line)
            for line in document_lines
            if not re.match(r"^[A-Z\s\\n]+$", line)
        ]
    )

    # remove lines not starting with beam names
    return [line for line in cleaned_lines if re.match(r"^\d*[A-Z]", line)]


def extract_member_group_numbers(line: str) -> str:
    # extracts all beam numbers from beam name lines
    new_line: str = line
    pattern_re: str = r"(?P<A>\d+)\s(?P<B>TO)\s(?P<C>\d+)"
    matches: Iterator[re.Match[str]] = re.finditer(pattern_re, new_line)
    if not matches:
        return line

    for match in matches:
        num_series_list: list[int] = list(
            range(int(match.group("A")) + 1, int(match.group("C")))
        )
        num_series_str: str = " ".join(str(num) for num in num_series_list)
        new_line = re.sub("TO", num_series_str, new_line, count=1)
    return new_line


def concatenate_lines(lines: list[str]) -> list[str]:
    # append succeeding lines to the current line if current line ends with a dash
    index = 0
    cleaned_lines: list[str] = lines
    while index < len(cleaned_lines):
        line = cleaned_lines[index]
        if re.match(r"^[A-Z].*\-$", line):
            # Find the next line that does not end with a dash
            while re.match(r"^[A-Z].*\-$", cleaned_lines[index]) and index + 1 < len(
                cleaned_lines
            ):
                # Remove the dash from the current line and append the next line
                cleaned_lines[index] = (
                    re.sub(r"\-$", "", cleaned_lines[index]) + cleaned_lines[index + 1]
                )
                # Remove the next line from the list
                del cleaned_lines[index + 1]

        index += 1
    return cleaned_lines


def load_groups_to_df(lines: list[str]) -> pd.DataFrame:
    data: list[list[str]] = []

    for line in lines:
        split_line: list[str] = line.split()
        beam_name: str = next((el for el in split_line if re.match(r"^\d*[A-Z]", el)))
        if beam_name:
            data.extend(
                [beam_name, el]
                for el in split_line
                if el != beam_name and el is not None  # type: ignore
            )

    df: pd.DataFrame = pd.DataFrame(data, columns=["Name", "Beam"])
    df.iloc[:, 1:] = df.iloc[:, 1:].astype(int)
    try:
        df = remove_columns_and_floor_groups(df)
    except TypeError:
        raise TypeError("Beam names might have other types than str")

    return df


def load_dim_to_df(lines: list[str]) -> pd.DataFrame:
    if len(lines) == 0:
        raise Exception("File does not contain beam dimensions")

    data: list[tuple] = []

    for line in lines:
        line = re.sub(r"PRIS|YD|ZD", "", line)
        beam_dim: tuple = tuple(line.split())
        if beam_dim:

            beam_dim = (
                beam_dim[0],
                float(beam_dim[2]) * 1000,
                float(beam_dim[1]) * 1000,
            )

        data.append(beam_dim)

    df: pd.DataFrame = pd.DataFrame(data, columns=["Name", "b", "h"])
    df.iloc[:, 1:] = df.iloc[:, 1:].astype(float)
    try:
        df = remove_columns_and_floor_groups(df)
    except TypeError:
        raise TypeError("Beam names might have other types than str")

    return df


def remove_columns_and_floor_groups(df: pd.DataFrame) -> pd.DataFrame:
    del_re: str = r"\d*P*[C|S][\d-]+"
    filter_logic: pd.Series[bool] = df["Name"].str.contains(del_re)

    return df[~filter_logic]
