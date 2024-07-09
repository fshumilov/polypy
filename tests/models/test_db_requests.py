import pandas as pd
from models.db_requests import get_polymer_catalog, get_property_value, get_property_type


def test_test():
    # Step 1 - test environment: objects, settings, envs
    # Step 2 - request of a tested unit (only one)
    # Step 3 - Asserts (as much as wanted)
    assert "True" == "True"


def test_get_polymer_catalog():
    result = get_polymer_catalog()
    assert isinstance(result, pd.DataFrame)


def test_get_property_type():
    result = get_property_type()
    assert isinstance(result, pd.DataFrame)


def test_get_property_value():
    result = get_property_value()
    assert isinstance(result, pd.DataFrame)
