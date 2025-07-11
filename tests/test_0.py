import pytest
import numpy as np
from definition_4b4c489895aa463197b9c4d941dcb981 import calculate_ks_distance

@pytest.mark.parametrize("data1, data2, expected", [
    ([1, 2, 3], [4, 5, 6], 0.0),
    ([1, 2, 3], [1, 2, 3], 0.0),
    ([1, 2, 3], [1, 2, 4], 1/6),
    ([1, 2, 3, 4, 5], [6, 7, 8, 9, 10], 0.0),
    ([1, 1, 1, 1, 1], [2, 2, 2, 2, 2], 1.0),
])
def test_calculate_ks_distance(data1, data2, expected):
    assert calculate_ks_distance(data1, data2) == expected
