import pandas as pd
import pytest

from src import error_handling

data = pd.read_csv("https://media.geeksforgeeks.org/wp-content/uploads/nba.csv")


def test1(data):
    assert error_handling.head_check(data) == [
        "Name",
        "Team",
        "Number",
        "Position",
        "age",
        "Height",
        "Weight",
        "College",
        "Salary",
    ]
