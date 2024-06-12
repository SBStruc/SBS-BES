import pandas as pd
from functools import reduce


def build_MuVuTu_table(df: pd.DataFrame) -> pd.DataFrame:
    assert df.columns.values.tolist() == [
        "Name",
        "Axial Force kN",
        "Shear-Y kN",
        "Shear-Z kN",
        "Torsion kNm",
        "Moment-Y kNm",
        "Moment-Z kNm",
    ]
    # df is the merged beam forces and group table
    df_to_merge: list[pd.DataFrame] = [
        compute_Muneg(df),
        compute_Mupos(df),
        compute_Vu(df),
        compute_Tu(df),
    ]
    merged_df: pd.DataFrame = reduce(
        lambda x, y: pd.merge(x, y, on="Name", sort=False),
        df_to_merge,
    )
    merged_df.columns = ["Mu_neg", "Mu_pos", "Vu", "Tu"]

    return merged_df


# takes the beam forces table as input
def compute_Muneg(df: pd.DataFrame) -> pd.DataFrame:
    return df[["Name", "Moment-Z kNm"]].groupby("Name", sort=False).max().abs()


def compute_Mupos(df: pd.DataFrame) -> pd.DataFrame:
    return df[["Name", "Moment-Z kNm"]].groupby("Name", sort=False).min().abs()


def compute_Vu(df: pd.DataFrame) -> pd.DataFrame:
    Vu_df: pd.DataFrame = df[["Name", "Shear-Y kN"]]
    Vu_df.loc[:, "Shear-Y kN"] = Vu_df["Shear-Y kN"].abs()
    return Vu_df.groupby("Name", sort=False).max()


def compute_Tu(df: pd.DataFrame):
    Tu_df: pd.DataFrame = df[["Name", "Torsion kNm"]]
    Tu_df.loc[:, "Torsion kNm"] = Tu_df["Torsion kNm"].abs()
    return Tu_df.groupby("Name", sort=False).max()
