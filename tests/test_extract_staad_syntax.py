import pytest
import pandas as pd
import numpy as np
import pathlib

# import numpy.testing as npt
from sbs_bes.extract.extract_from_staad_syntax import (
    extract_beam_groups,
    extract_beam_dimensions,
)

TEST_FILENAME = pathlib.Path(__file__).parent / "test_file_staad_syntax.txt"

with open(TEST_FILENAME) as f:
    CONTENT = f.readlines()


def test_extract_beam_groups():
    beam_group_df = extract_beam_groups(CONTENT)
    assert beam_group_df.shape == (277, 2)
    assert beam_group_df["Name"].dtype == np.dtype("O")
    assert beam_group_df["Name"].unique().shape == (60,)
    assert beam_group_df["Beam"].iloc[0] == 45
    assert beam_group_df["Name"].iloc[0] == "FTB01"
    # check if COLUMNS and FLOOR beams are not caught
    assert "C02-1" not in beam_group_df["Name"].unique()
    assert "PC02" not in beam_group_df["Name"].unique()


def test_extract_beam_dimensions():
    beam_dim_df = extract_beam_dimensions(CONTENT)
    assert beam_dim_df.shape == (60, 3)
    assert beam_dim_df["Name"].dtype == np.dtype("O")
    assert beam_dim_df["Name"].unique().shape == (60,)
    assert beam_dim_df["Name"].iloc[59] == "RCB04"
    assert beam_dim_df["b"].iloc[59] == 250
    assert beam_dim_df["h"].iloc[59] == 450
    # check if COLUMNS and FLOOR beams are not caught
    assert "C02-1" not in beam_dim_df["Name"].unique()
    assert "PC02" not in beam_dim_df["Name"].unique()


# should len(names) of both beam group df and beam dim df be equal?
#

if __name__ == "__main__":
    pytest.main()
