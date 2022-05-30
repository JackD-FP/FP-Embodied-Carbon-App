import pytest
from pages.analysis import epic_db, ice_db


# {"label": "Concrete 40 MPa", "value": 413.4943}
def test_concrete():
    assert ice_db.concrete(413.4943, 1000) == ("Concrete 40 MPa", 413494.3)


print(ice_db.concrete(413.4943, 1000))
