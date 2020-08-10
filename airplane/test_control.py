from control import Control


def test_control_degree():
    assert Control(1000, 2000).degree(-5000) == 0, "Should be 0"

    assert Control(1000, 2000).degree(910) == 0, "Should be 0"

    assert Control(1000, 2000).degree(5010) == 180, "Should be 180"

    assert Control().degree(1) == 0, "Should be 0"

    assert Control(-500, 500).degree(0) == 90, "Should be 90"

    assert Control(0, 180).degree(163) == 163, "Should be 163"

    a = Control(1000, 2000)
    assert a.degree(1500) == 90, "Should be 90"

    a = Control(1000, 2000)
    assert a.degree(5000) == 180, "Should be 90"


def test_control_switch():
    a = Control(19000, 20000)
    assert a.switch(19700), "Should be True"

    a = Control(19000, 20000)
    assert a.switch(19699) is None, "Should be False"


def test_control_variator():
    a = Control(1000, 2000)
    assert a.variator(1500, 0.0, 1.0) == 0.5, "Should be 0.5"

    a = Control(1000, 2000)
    assert a.variator(1500, 0.0, 0.1) == 0.05, "Should be 0.05"
