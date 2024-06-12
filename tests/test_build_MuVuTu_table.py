import pytest
import pandas as pd

# import numpy.testing as npt
from sbs_bes.compute.build_MuVuTu_table import (
    compute_Muneg,
    compute_Mupos,
    compute_Vu,
    compute_Tu,
)

test_df = pd.DataFrame(
    {
        "Name": ["A", "A", "A", "B", "B", "B", "B", "C"],
        "Moment-Z kNm": [-10, 0, 3, -2, 2, 0, 2, 3],
        "Shear-Y kN": [-7, 0, 3, -2, 2, 0, 2, 3],
        "Torsion kNm": [-5, 0, 3, -2, 2, 0, 2, 3],
    }
)


def test_compute_Muneg():
    assert compute_Muneg(test_df).loc["A", "Moment-Z kNm"] == 3
    assert compute_Muneg(test_df).loc["B", "Moment-Z kNm"] == 2
    assert compute_Muneg(test_df).loc["C", "Moment-Z kNm"] == 3


def test_compute_Mupos():
    assert compute_Mupos(test_df).loc["A", "Moment-Z kNm"] == 10
    assert compute_Mupos(test_df).loc["B", "Moment-Z kNm"] == 2
    assert compute_Mupos(test_df).loc["C", "Moment-Z kNm"] == 3


def test_compute_Vu():
    assert compute_Vu(test_df).loc["A", "Shear-Y kN"] == 7
    assert compute_Vu(test_df).loc["B", "Shear-Y kN"] == 2
    assert compute_Vu(test_df).loc["C", "Shear-Y kN"] == 3


def test_compute_Tu():
    assert compute_Tu(test_df).loc["A", "Torsion kNm"] == 5
    assert compute_Tu(test_df).loc["B", "Torsion kNm"] == 2
    assert compute_Tu(test_df).loc["C", "Torsion kNm"] == 3


if __name__ == "__main__":
    pytest.main()
