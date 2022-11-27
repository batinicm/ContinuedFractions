# 1. Determine abbreviated notation for the given number
# 2. Use the abbreviated notation to determine single continued fraction values
# 3. Input n and m (n < m), so that n <= q <= m, and calculate convergents
# 4. Determine if the convergent is a best rational approximation of I, II or no order
#       * II <=> it's equal to one of the continuous fractions
#       * I <=> it's not equal to one of the continuous fractions, but its absolute difference is smaller than the one of
#           its closest continuous fraction
#       * not I nor II <=> it's not equal to one of the continuous fractions,
#                      and its absolute difference is larger than the one of its closest continuous fraction
# 5. For those which are a best rational approximaition, save the absolute difference and calculate continuous digit representation

import math

def gather_parameters():
    prompt = "Please input a positive real number with a finite number of decimal digits: "
    alpha = input(prompt)

    while alpha < 0:
        input(prompt)

    parameters = input("Please input n and m, where n < m and n >=0 and m>=0").split()
    return [alpha, parameters]


def generate_abbreviated_notation(alpha):
    i = 0
    values = [alpha]
    notation = [math.floor(alpha)]
    diff = 10

    while diff != 0 and i < 10:
        diff = values[i] - notation[i]
        i += 1
        values[i] = 1/diff
        notation[i] = math.floor(values[i])

    return notation


if __name__ == '__main__':
    print("Hello, welcome to the Best Rational Approximation Calculator!")
    parameters = gather_parameters()

    abbreviated_notation = generate_abbreviated_notation(parameters[0])
    print("Abbreviated notation of number " + str(parameters[0]) + ": " + str(abbreviated_notation))

