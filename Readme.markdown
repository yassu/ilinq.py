ILinq
=======

This project provides the module like linq of C# for Python.

## How To Install

```
$ python setup.py install
```

## First Example

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# We obtain the last prime less than 10^4.

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
```

## Todo

- [ ] check all linq defined c# ([here](https://msdn.microsoft.com/ja-jp/library/system.linq.enumerable(v=vs.110).aspx))
- [ ] use compare function not key function

## LICENSE

Apache 2.0
