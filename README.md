FQN Decorators
==============

[![](https://secure.travis-ci.org/kpn-digital/py-fqn-decorators.svg?branch=master)](http://travis-ci.org/kpn-digital/py-fqn-decorators?branch=master)
[![](https://img.shields.io/codecov/c/github/kpn-digital/py-fqn-decorators/master.svg)](http://codecov.io/github/kpn-digital/py-fqn-decorators?branch=master)
[![](https://img.shields.io/pypi/v/fqn-decorators.svg)](https://pypi.python.org/pypi/fqn-decorators)
[![](https://readthedocs.org/projects/fqn-decorators/badge/?version=latest)](http://fqn-decorators.readthedocs.org/en/latest/?badge=latest)


Installation
------------
At the command line::

```bash
$ pip install fqn-decorators
```

Usage
-----
```python
import fqn_decorators.decorators
```

Introduction
------------

By extending the `Decorator` class you can create simple decorators.
Implement the `Decorator.before` and/or `Decorator.after` methods to perform actions before or after execution of the decorated item.
The `Decorator.before` method can access the arguments of the decorated item by changing the `Decorator.args` and `Decorator.kwargs` attributes.
The `Decorator.after` method can access or change the result using the `Decorator.result` attribute.
The `Decorator.exception` method can be used for do something with an Exception that has been raised.
In all three methods the `Decorator.fqn` and `Decorator.func` attributes are available.

Simple decorator
----------------

Create a simple decorator:

```python
import fqn_decorators
import time

class time_it(fqn_decorators.Decorator):

    def before(self):
        self.start = time.time()

    def after(self):
        duration = time.time() - self.start
        print("{0} took {1} seconds".format(self.fqn, duration))


@time_it
def my_function():
    time.sleep(1)

my_function()
# __main__.my_function took 1.00293397903 seconds
```

Decorator with arguments
------------------------

It is also very easy to create a decorator with arguments.
It is not possible to create decorators with *non-keyworded* arguments.

Example:

```python
import fqn_decorators
import time

class threshold(fqn_decorators.Decorator):

    def before(self):
        self.start = time.time()

    def after(self):
        duration = time.time() - self.start
        treshold = self.params.get('threshold')
        if threshold and duration > threshold:
            raise Exception('Execution took longer than the threshold')


@threshold(threshold=2)
def my_function():
    time.sleep(3)

my_function()
# Exception: Execution took longer than the threshold
```

Async Decorator
---------------

There's also support for decorating coroutines (or any awaitable), for Python >=3.5 only.

The implementation is the same as with the sync version, just inherit from
`fqn_decorators.asynchronous.AsyncDecorator` instead.

Example:
```python
import asyncio
import time
from fqn_decorators.asynchronous import AsyncDecorator

class time_it_async(AsyncDecorator):

    def before(self):
        self.start = time.time()

    def after(self):
        duration = time.time() - self.start
        print("{0} took {1} seconds".format(self.fqn, duration))

@time_it_async
async def coro():
    await asyncio.sleep(1)

asyncio.run(coro())
# __main__.coro took 1.001493215560913 seconds
```
