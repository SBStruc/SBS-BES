import pytest
import numpy as np
import pathlib

# import numpy.testing as npt
from sbs_bes.extract.extract_from_staad_syntax import (
    extract_beam_groups,
    extract_beam_dimensions,
)

TEST_FILENAME = pathlib.Path(__file__).parent / "test_staad_syntax.txt"

with open(TEST_FILENAME) as f:
    CONTENT = f.readlines()


def test_extract_beam_groups():
    beam_group_df = extract_beam_groups(CONTENT)
    assert beam_group_df.shape == (380, 2)
    assert beam_group_df.columns.values.tolist() == ["Name", "Beam"]
    assert beam_group_df["Name"].dtype == np.dtype("O")
    assert beam_group_df["Name"] == ["test"]
    assert beam_group_df["Name"].unique().shape == (34,)
    assert beam_group_df["Beam"].iloc[0] == 1
    assert beam_group_df["Name"].iloc[0] == "FTB01"
    # check if COLUMNS and FLOOR beams are not caught
    assert "C01A" not in beam_group_df["Name"].unique()
    assert "2FS1" not in beam_group_df["Name"].unique()


def test_extract_beam_dimensions():
    beam_dim_df = extract_beam_dimensions(CONTENT)
    assert beam_dim_df.shape == (34, 3)
    assert beam_dim_df.columns.values.tolist() == ["Name", "b", "h"]
    assert beam_dim_df["Name"].dtype == np.dtype("O")
    assert beam_dim_df["Name"].unique().shape == (34,)
    assert beam_dim_df["Name"].iloc[33] == "RCB1"
    assert beam_dim_df["b"].iloc[33] == 200
    assert beam_dim_df["h"].iloc[1] == 300
    # check if COLUMNS and FLOOR beams are not caught
    assert "C01A" not in beam_dim_df["Name"].unique()
    assert "2FS1" not in beam_dim_df["Name"].unique()


# should len(names) of both beam group df and beam dim df be equal?
#

if __name__ == "__main__":
    pytest.main()
