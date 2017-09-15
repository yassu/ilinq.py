#!/usr/bin/env python
# -*- coding: utf-8 -*-

# We obtain the last primes less than 10^4.

from ilinq.ilinq import Linq


def is_prime(n):
    if n < 2:
        return False

    for j in range(2, n):
        if n % j == 0:
            return False

    return True


if __name__ == '__main__':
    print(
        Linq(range(10**4))
        .where(is_prime)
        .last())
    # => 9973