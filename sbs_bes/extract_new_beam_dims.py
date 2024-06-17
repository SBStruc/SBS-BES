import xlwings as xw
import pathlib
import pandas as pd
import re


def extract_beam_dims(staad_file: str, xl_filename: str, xl_folder: str) -> None:
    SUMMARY_SHEET_NAME: str = "SUMMARY"
    new_staad_syntax_path: pathlib.Path = pathlib.Path(xl_folder) / xl_filename
    wb: xw.Book = xw.Book(new_staad_syntax_path)

    if SUMMARY_SHEET_NAME not in wb.sheet_names:
        raise Exception(f"{SUMMARY_SHEET_NAME} not found in {xl_filename}. Exiting...")


# def extract_beam_dimensions(doc_lines: list[str]) -> pd.DataFrame:
#     try:
#         bd_start_index: int = doc_lines.index("MEMBER PROPERTY AMERICAN\n")
#         bd_end_index: int = -1
#         for idx, bd_line in enumerate(
#             doc_lines[bd_start_index + 1 :], start=bd_start_index + 1  # noqa
#         ):
#             if re.match(r"^[A-Z\s]+\n$", bd_line):
#                 bd_end_index = idx
#                 break
#         if bd_end_index == -1:
#             raise Exception
#         bd_lines: list[str] = clean_bd_lines(doc_lines[bd_start_index:bd_end_index])
#     except Exception as e:
#         raise ValueError(f"{e}\nWrong file. No MEMBER PROPERTY AMERICAN or CONSTANTS")

#     return load_dim_to_df(bd_lines)


extract_beam_dims(
    "../tests/test_staad_syntax.txt",
    "test_data.xlsm",
    "/Users/regutierrez/repos/SBS-BES/",
)
