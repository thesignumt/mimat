from fractions import Fraction


def tok_to_frac(s: str) -> Fraction:
    if "." not in s:
        return Fraction(int(s))

    ip, fp = s.split(".")  # Integer and fractional parts
    ip = ip or "0"
    fp = fp or "0"

    return Fraction(int(ip + fp), 10 ** len(fp))
