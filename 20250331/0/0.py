"""This is module."""

from math import *
import sys


def f(a, b):
    """function."""
    return a + b + sin(b)

print(sin(int(sys.argv[1])))
print(f(1, 2))
