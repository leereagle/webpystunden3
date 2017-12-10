from datetime import timedelta
from decimal import Decimal


def calculate_stunden(startzeit, endzeit):
    """
    Rechnet den Unterschied zwischen einer Startzeit und einer Endzeit aus.
    Dadurch, dass auf zwei Dezimalstellen gerundet wird ist die geringste
    Auflösung ca. 18 Sekunden.
    Returniert wird ein string, der in ein float umgewandelt werden kann.
    """
    startdelta = timedelta(
        hours=int(startzeit.hour),
        minutes=int(startzeit.minute),
        seconds=int(startzeit.second)
    )
    enddelta = timedelta(
        hours=int(endzeit.hour),
        minutes=int(endzeit.minute),
        seconds=int(endzeit.second)
    )
    delta = enddelta - startdelta
    stunden = delta.total_seconds() / 3600
    return "{:.2f}".format(stunden)


def moneyformat(value, places=2, curr="", sep=".", dp=",", pos="", neg="-", trailneg=""):
    """Convert Decimal to a money formatted string.

    places:  required number of places after the decimal point
    curr:    optional currency symbol before the sign (may be blank)
    sep:     optional grouping separator (comma, period, space, or blank)
    dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    pos:     optional sign for positive numbers: "+", space or blank
    neg:     optional sign for negative numbers: "-", "(", space or blank
    trailneg:optional trailing minus indicator:  "-", ")", space or blank

    >>> d = Decimal("-1234567.8901")
    >>> moneyfmt(d, curr="$")
    "-$1,234,567.89"
    >>> moneyfmt(d, places=0, sep=".", dp="", neg="", trailneg="-")
    "1.234.568-"
    >>> moneyfmt(d, curr="$", neg="(", trailneg=")")
    "($1,234,567.89)"
    >>> moneyfmt(Decimal(123456789), sep=" ")
    "123 456 789.00"
    >>> moneyfmt(Decimal("-0.02"), neg="<", trailneg=">")
    "<0.02>"
    """
    q = Decimal(10) ** -places      # 2 places --> "0.01"
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = map(str, digits)
    digits = list(digits)
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else "0")
    build(dp)
    if not digits:
        build("0")
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return "".join(reversed(result))
