from calculator import calculate_expression

def test_calculate_addition():
    assert calculate_expression('1 + 2 + 3') == '6'

def test_calculate_subtraction():
    assert calculate_expression('2 - 3') == '-1'

def test_smoke():
    assert True
