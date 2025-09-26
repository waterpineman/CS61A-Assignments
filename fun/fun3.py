def spilt(n):
    return n // 10, n % 10
def sum_digits(n):
    if n < 10:
        return n
    else:
        all_but_last, last = spilt(n)
        return sum_digits(all_but_last) + last
    

def luhn_sum(n):
    if n < 10:
        return n
    else:
         all_but_last, last = spilt(n)
         return luhn_sum_double(all_but_last) + last


def luhn_sum_double(n):
    all_but_last, last = spilt(n)
    luhn_digits = sum_digits(last * 2)
    if n < 10:
        return luhn_digits
    else:
        return luhn_sum(all_but_last) + luhn_digits

def divisor(n):
    return [1] + [x for x in range(2, n) if n % x == 0]


def perfect_num(n):
    return [x for x in range(n) if sum(divisor(x)) == x]


def primeter(width, h):
    return 2 * width + 2 * h


def width(area, h):
    assert area % h == 0
    return area // h


def min_primeter(area):
    height = divisor(area)
    primeters = [primeter(width(area, h), h) for h in height]
    return min(primeters)


