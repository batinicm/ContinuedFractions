# 1. Determine abbreviated notation for the given number
# 2. Use the abbreviated notation to determine convergents
# 3. Input n and m (n < m), so that n <= q <= m, and calculate p as floor(alpha * q)
# 4. Determine if the fraction is a best rational approximation of I, II or no order
#       * II <=> it's equal to one of the continuous fractions
#       * I <=> it's not equal to one of the continuous fractions, but its absolute difference is smaller than the one of
#           its closest continuous fraction
#       * not I nor II <=> it's not equal to one of the continuous fractions,
#                      and its absolute difference is larger than the one of its closest continuous fraction
# 5. For those which are a best rational approximation, save the absolute difference and calculate continuous digit representation

import math
from fractions import Fraction
from tabulate import tabulate

NOTATION_COUNT = 10
ABS_DIFF = 3


def gather_parameters():
    prompt = "Please input a positive real number with a finite number of decimal digits: "
    alpha = float(input(prompt))
    parameters = list(map(lambda i: int(i), input("Please input n and m, where n < m and n >=0 and m>=0: ").split()))
    return [alpha, parameters]


def generate_abbreviated_notation(alpha):
    i = 0
    values = [alpha]
    notation = [math.floor(alpha)]
    diff = 10

    while diff != 0 and i < NOTATION_COUNT:
        diff = values[i] - notation[i]
        i += 1
        new_value = float(1 / diff)
        values.append(new_value)
        notation.append(math.floor(new_value))

    return notation


def generate_convergents(abbreviated_notation):
    convergents = [Fraction(abbreviated_notation[0], 1),
                   Fraction(abbreviated_notation[0] * abbreviated_notation[1] + 1, abbreviated_notation[1])]

    for i in range(2, NOTATION_COUNT):
        p = convergents[i - 1].numerator * abbreviated_notation[i] + convergents[i - 2].numerator
        q = convergents[i - 1].denominator * abbreviated_notation[i] + convergents[i - 2].denominator
        convergents.append(Fraction(p, q))

    return convergents


# Generate p using n <= q <= m, as floor(alpha * q), check if p/q is a convergent
# yes -> best rational approximation of II order
# no -> calculate absolute difference between fraction and alpha, find closest convergent
# and see if absolute difference is smaller than the one of the convergent
#   -> yes -> best rational approximation of I order
#   -> no -> not of any order, unimportant
# If fraction is a best rational approximation of any order, find notation digits
def find_approximations(alpha, parameters, convergents):
    q = parameters[0]
    approximations = []

    while parameters[0] <= q <= parameters[1]:
        p = round(alpha * q)
        order = None
        fraction = Fraction(p, q)
        abs_diff = abs(alpha - fraction)

        if q in list(map(lambda c: c.denominator, convergents)) and p in list(map(lambda c: c.numerator, convergents)):
            order = 2
        else:
            i = 0
            for i in (0, len(convergents)):
                if convergents[i] > fraction:
                    break
                i += 1
            closest_convergent = convergents[i - 1]
            if abs_diff < abs(alpha - closest_convergent):
                order = 1
            else:
                continue

        approximations.append([q, fraction, generate_abbreviated_notation(fraction), order, abs_diff])
        q += 1

    return approximations


# Prints approximations sorted by absolute difference with alpha
# Approximation details: q, p/q, notation, order, absolute difference
def print_approximations(approximations):
    approximations.sort(key=lambda a: a[ABS_DIFF])
    print(tabulate(approximations, headers=["q, p/q, p/q = [a0;...], order, abs_diff"], tablefmt="fancy_grid"))


if __name__ == '__main__':
    print("Hello, welcome to the Best Rational Approximation Calculator!")
    parameters = gather_parameters()

    abbreviated_notation = generate_abbreviated_notation(parameters[0])
    print("Abbreviated notation of number " + str(parameters[0]) + ": " + str(abbreviated_notation))

    convergents = generate_convergents(abbreviated_notation)
    approximations = find_approximations(parameters[0], parameters[1], convergents)

    print_approximations(approximations)
