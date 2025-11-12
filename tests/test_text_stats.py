from text_stats import count_text_stats

def test_empty():
    assert count_text_stats("") == {"digits": 0, "letters": 0, "upper": 0, "lower": 0, "symbols": 0}

def test_only_digits():
    s = "123456"
    r = count_text_stats(s)
    assert r["digits"] == 6 and r["letters"] == 0 and r["symbols"] == 0

def test_only_letters_lower():
    s = "python"
    r = count_text_stats(s)
    assert r["letters"] == 6 and r["lower"] == 6 and r["upper"] == 0

def test_only_letters_upper():
    s = "PYTHON"
    r = count_text_stats(s)
    assert r["letters"] == 6 and r["upper"] == 6 and r["lower"] == 0

def test_mixed_letters():
    s = "PyThOn"
    r = count_text_stats(s)
    assert r["letters"] == 6 and r["upper"] == 3 and r["lower"] == 3

def test_mixed_letters_digits():
    s = "Py123"
    r = count_text_stats(s)
    assert r["letters"] == 2 and r["digits"] == 3

def test_with_symbols():
    s = "Hi!"
    r = count_text_stats(s)
    assert r["letters"] == 2 and r["symbols"] == 1

def test_spaces_not_symbols():
    s = "A B C"
    r = count_text_stats(s)
    assert r["letters"] == 3 and r["symbols"] == 0

def test_cyrillic_letters():
    s = "ПрИвЕт"
    r = count_text_stats(s)
    assert r["letters"] == 6 and r["upper"] == 3 and r["lower"] == 3

def test_digits_letters_symbols_mix():
    s = "A1b2@!"
    r = count_text_stats(s)
    assert r["letters"] == 2 and r["digits"] == 2 and r["symbols"] == 2
