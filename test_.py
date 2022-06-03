import pytest
from src import funcs, material_options


def test1():
    assert funcs.rebar("rebar", 1000)[0] == 1733


def test2():
    assert funcs.rebar("rebar", 1000)[1] == "Over 65% Recycled Content"


def test3():
    assert funcs.rebar("rebar", 1000)[2] == 2900


def test4():
    assert funcs.rebar("rebar", 1000)[3] == "Steel reinforcement bar "


def test5():
    assert funcs.rebar("rebar", 1000)[4] == 1990


def test6():
    assert funcs.rebar("rebar", 1000)[5] == "Steel Rebar recycled "
