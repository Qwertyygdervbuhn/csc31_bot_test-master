def count_text_stats(text: str) -> dict:
    digits = letters = upper = lower = symbols = 0
    for ch in text or "":
        if ch.isdigit():
            digits += 1
        elif ch.isalpha():
            letters += 1
            if ch.isupper():
                upper += 1
            elif ch.islower():
                lower += 1
        elif not ch.isspace():
            symbols += 1
    return {
        "digits": digits,
        "letters": letters,
        "upper": upper,
        "lower": lower,
        "symbols": symbols,
    }
