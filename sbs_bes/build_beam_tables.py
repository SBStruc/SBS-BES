import os
import shutil
import xlwings as xw
import pandas as pd
from sbs_bes.extract.extract_from_staad_syntax import (
    extract_beam_groups,
    extract_beam_dimensions,
)
from sbs_bes.extract.extract_beam_forces import extract_beam_forces
from sbs_bes.compute.build_MuVuTu_table import build_MuVuTu_table


def main(
    template_path: str,
    beam_group_path: str,
    beam_force_path: str,
    filename: str,
    dst_folder: str,
) -> None:
    if beam_group_path == "" or beam_force_path == "" or filename == "":
        raise Exception("All fields must be filled in. Exiting...")

    BEAM_GROUP_PATH: str = beam_group_path
    BEAM_FORCE_PATH: str = beam_force_path
    BEAM_TABLE_FILENAME: str = f"{filename}.xlsm"
    BEAM_TABLE_FOLDER: str = dst_folder
    TEMPLATE_FILE_PATH: str = template_path

    beam_force_df: pd.DataFrame = extract_beam_forces(BEAM_FORCE_PATH)
    beam_group_df, beam_dim_df = build_beam_group_tables(BEAM_GROUP_PATH)
    beam_group_forces_df: pd.DataFrame = build_beam_group_forces_table(
        beam_group_df, beam_force_df
    )
    MuVuTu_df: pd.DataFrame = build_MuVuTu_table(beam_group_forces_df)
    master_table: pd.DataFrame = build_master_table(MuVuTu_df, beam_dim_df)

    write_to_xlsm(
        TEMPLATE_FILE_PATH, BEAM_TABLE_FILENAME, BEAM_TABLE_FOLDER, master_table
    )


def build_beam_group_tables(file: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    print("extracting beam group from", file)
    try:
        with open(file) as bg:
            lines: list[str] = bg.readlines()
    except Exception as e:
        raise Exception(f"Error opening beam group file: {e}. Exiting...")

    print("extracting beam group done!")
    return extract_beam_groups(lines), extract_beam_dimensions(lines)


def build_beam_group_forces_table(
    beam_group_df: pd.DataFrame, beam_force_df: pd.DataFrame
) -> pd.DataFrame:
    print("merging beam group and beam force dataframes...")
    try:
        # remove "Beam" column; it's useless after the merge
        merged_df: pd.DataFrame = pd.merge(
            beam_group_df, beam_force_df, on="Beam"
        ).drop(["Beam", "L/C"], axis=1)
    except Exception:
        raise Exception(
            "Error merging beam group and beam force dataframes. Exiting..."
        )
    print("merging beam group and beam force dataframes done!")

    return merged_df


def build_master_table(
    MuVuTu_df: pd.DataFrame,
    beam_dimensions_df: pd.DataFrame,
) -> pd.DataFrame:
    master_table: pd.DataFrame = pd.merge(
        MuVuTu_df, beam_dimensions_df, on="Name", sort=False
    )
    if master_table["Name"].str.contains(r"0\d"):
        raise Exception("Beam names cannot contain 0 followed by a number. Exiting...")

    return master_table[
        [
            "Name",
            "b",
            "h",
            "Mu_neg",
            "Mu_pos",
            "Vu",
            "Tu",
        ]
    ]


def write_to_xlsm(
    template_path: str, dst_filename: str, dst_folder: str, master_table: pd.DataFrame
) -> None:
    EXCEL_TEMPLATE: str = template_path
    dst_filepath: str = os.path.join(dst_folder, dst_filename)
    print(
        "copying template xlsm to",
        f"{dst_filename} in folder {dst_folder}",
    )
    try:
        shutil.copy(EXCEL_TEMPLATE, f"{dst_filepath}")

    except FileNotFoundError:
        raise FileNotFoundError(f"{EXCEL_TEMPLATE} not found. exiting...")
    print("copying template xlsm done! ")
    print("writing dataframe to xlsm...")

    wb = xw.Book(f"{dst_filepath}")
    ws = wb.sheets["MASTER"]
    ws["A1"].options(pd.DataFrame, header=1, index=False, expand="table").value = (
        master_table
    )

    wb.save(f"{dst_filepath}")
    print("writing dataframe to xlsm done!")
