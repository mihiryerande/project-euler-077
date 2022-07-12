# Problem 77:
#     Prime Summations
#
# Description:
#     It is possible to write ten as the sum of primes in exactly five different ways:
#         7 + 3
#         5 + 5
#         5 + 3 + 2
#         3 + 3 + 2 + 2
#         2 + 2 + 2 + 2 + 2
#
# What is the first value which can be written as the sum of primes in over five thousand different ways?

from math import floor, sqrt
from typing import Tuple

# Store already discovered primes
PRIMES = []
NEXT_PRIME = dict()

# Store already computed counts for later usage:
#   (n, max_p) -> ways
PRIME_SUM_WAYS = dict()


def is_prime(n: int) -> bool:
    """
    Return True iff `n` is prime, using already computed list `PRIMES`.

    Args:
        n (int): Natural number

    Returns:
        (bool): True iff `n` is prime

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(n) == int and n > 0

    global PRIMES

    # Quick check
    if n < 2:
        return False

    # Only check divisibility up to sqrt(n)
    n_mid = floor(sqrt(n)) + 1

    i = 0
    while i < len(PRIMES) and PRIMES[i] < n_mid:
        p = PRIMES[i]
        if n % p == 0:
            return False
        else:
            i += 1
            continue
    return True


def prime_sum_ways(n: int, max_prime: int) -> int:
    """
    Returns the number of (unordered) ways to sum to `n`
      using only prime numbers which are at most `max_prime`.

    Args:
        n         (int): Non-negative integer
        max_prime (int): Prime number

    Returns:
        (int): Number of ways to sum to `n` using primes at most `max_prime`

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(n) == int and n >= 0
    assert type(max_prime) == int and max_prime > 1

    # Idea:
    #     Attempt to use `max_prime` as much as possible to achieve `n`.
    #     Siphon off `max_prime` one-by-one, using smaller coins to fill the remainder.
    #     To avoid redundant counting, maintain computed counts in `PRIME_SUM_WAYS`

    global PRIME_SUM_WAYS

    if (n, max_prime) in PRIME_SUM_WAYS:
        # Already computed this
        return PRIME_SUM_WAYS[(n, max_prime)]
    else:
        # Haven't computed this case yet
        if n < 2:
            # Base cases
            #   * n = 0 -> Vacuous case of empty sum, meaning 1 way
            #   * n = 1 -> Unable to sum to 1 as least prime is 2, meaning 0 ways
            ways = int(n == 0)
        else:
            next_prime = NEXT_PRIME[max_prime]
            if next_prime is None:
                # No lower primes available, so can only sum using `max_prime`, which is 2
                # Return 1 if this is possible
                ways = int(n % max_prime == 0)
            else:
                # Use as much of `max_prime` as possible
                next_prime = NEXT_PRIME[max_prime]
                ways = 0
                max_prime_count_max, remaining_sum = divmod(n, max_prime)
                for _ in range(max_prime_count_max, -1, -1):
                    ways += prime_sum_ways(remaining_sum, next_prime)
                    remaining_sum += max_prime

        # Store for later
        PRIME_SUM_WAYS[(n, max_prime)] = ways
        return ways


def main(min_ways: int) -> Tuple[int, int]:
    """
    Returns the least number which can be expressed as a sum of primes in over `min_ways` ways.

    Args:
        min_ways (int): Natural number

    Returns:
        (Tuple[int, int]):
            Tuple of ...
              * First number that can be summed by primes in over `min_ways` ways
              * Number of ways to sum to that number

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(min_ways) == int and min_ways > 0

    # Keep track of known primes while iterating
    global PRIMES
    global NEXT_PRIME

    # Also map each prime to the next lowest prime for quick access
    # NOTE: 2 will map to None, indicating no further primes below 2

    # Greatest prime <= `n`, which is
    #   the greatest prime that can be part of a summation of `n`
    p_curr = None

    # Iterate upwards, counting number of ways to sum to `n` with primes
    n = 2
    while True:
        # Primality check before counting ways
        if is_prime(n):
            PRIMES.append(n)
            NEXT_PRIME[n] = p_curr
            p_curr = n
        else:
            pass

        # Count ways to sum to `n`, starting with next lowest prime
        ways = prime_sum_ways(n, p_curr)
        if ways > min_ways:
            return n, ways
        else:
            n += 1
            continue


if __name__ == '__main__':
    prime_summation_ways = int(input('Enter a natural number: '))
    summation_ways_number, summation_ways = main(prime_summation_ways)
    print('First number that can be written as a sum of primes in over {} ways:'.format(prime_summation_ways))
    print('  {} in {} ways'.format(summation_ways_number, summation_ways))
