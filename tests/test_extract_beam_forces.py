import pytest
import pandas as pd
import numpy as np

# import numpy.testing as npt
from sbs_bes.extract.extract_beam_forces import (
    clean_beam_and_lc_columns,
)


def test_clean_beam_and_lc_columns():
    # Test case 1: DataFrame with missing values
    df1 = pd.DataFrame({"Beam": [1.0, np.nan, 3.0], "L/C": ["A", "B:C", np.nan]})
    expected1 = pd.DataFrame({"Beam": [1.0, 1.0, 3.0], "L/C": ["A", "B", "B"]})
    clean_beam_and_lc_columns(df1)
    assert df1.equals(expected1)

    # Test case 2: DataFrame without missing values
    df2 = pd.DataFrame({"Beam": [1.0, 2.0, 3.0], "L/C": ["A", "B", "C"]})
    expected2 = df2.copy()
    clean_beam_and_lc_columns(df2)
    assert df2.equals(expected2)

    # Test case 3: DataFrame with missing values at the beginning
    df3 = pd.DataFrame({"Beam": [np.nan, 2, 3], "L/C": [":A", "B:C", "D:E"]})
    expected3 = pd.DataFrame({"Beam": [np.nan, 2, 3], "L/C": ["", "B", "D"]})
    clean_beam_and_lc_columns(df3)
    assert df3.equals(expected3)


if __name__ == "__main__":
    pytest.main()
