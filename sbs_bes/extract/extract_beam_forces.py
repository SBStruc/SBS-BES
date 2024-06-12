import pandas as pd


def clean_beam_and_lc_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the "Beam" and "L/C" columns by:
    - filling in missing/NaN values with the previous value
    - remove unecessary characters from the L/C cells

    Parameters:
        df (pd.DataFrame): The DataFrame to be cleaned.

    Returns:
        None
    """

    cleaned_df: pd.DataFrame = df

    cleaned_df["Beam"] = cleaned_df["Beam"].ffill()
    if cleaned_df["L/C"].dtype == "O":  # if it's a string
        cleaned_df["L/C"] = cleaned_df["L/C"].str.split(":", expand=True)[0]
    cleaned_df["L/C"] = cleaned_df["L/C"].ffill()

    return cleaned_df


def extract_beam_forces(bf_file: str) -> pd.DataFrame:
    print("extracting beam forces from", bf_file)
    try:
        df: pd.DataFrame = clean_beam_and_lc_columns(pd.read_excel(bf_file))
        assert df.columns.values.tolist() == [
            "Beam",
            "L/C",
            "Section",
            "Axial Force kN",
            "Shear-Y kN",
            "Shear-Z kN",
            "Torsion kNm",
            "Moment-Y kNm",
            "Moment-Z kNm",
        ]

    except Exception as e:
        raise Exception(f"Error extracting beam forces: {e}")

    print("extracting beam forces done!")
    return df
