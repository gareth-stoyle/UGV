import pytest

from src.utils import *

# 1. Test `normalise_to_range` Function
def test_normalise_to_range():
    """Test normalization of values within a range."""
    assert round(normalise_to_range(0, 0, 255, 0, 100), 3) == 0
    assert round(normalise_to_range(255, 0, 255, 0, 100), 3) == 100
    assert round(normalise_to_range(128, 0, 255, 0, 100), 3) == 50.196
    assert round(normalise_to_range(-128, -128, 127, -1, 1), 3) == -1
    assert round(normalise_to_range(127, -128, 127, -1, 1), 3) == 1
    assert round(normalise_to_range(0, -128, 127, -1, 1), 2) == 0
    assert round(normalise_to_range(5, 0, 10, 10, 20), 3) == 15
    assert round(normalise_to_range(3, 0, 6, 0, 12), 3) == 6

    # Collapsed old range
    with pytest.raises(ValueError):
        normalise_to_range(50, 50, 50, 0, 100)
    
    # Collapsed new range
    with pytest.raises(ValueError):
        normalise_to_range(50, 0, 100, 10, 10)
    
    # Both ranges collapsed
    with pytest.raises(ValueError):
        normalise_to_range(50, 50, 50, 10, 10)
