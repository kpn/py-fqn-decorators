FQN Decorators
==============

.. image:: https://secure.travis-ci.org/kpn-digital/py-fqn-decorators.svg?branch=master
    :target:  http://travis-ci.org/kpn-digital/py-fqn-decorators?branch=master

.. image:: https://img.shields.io/codecov/c/github/kpn-digital/py-fqn-decorators/master.svg
    :target: http://codecov.io/github/kpn-digital/py-fqn-decorators?branch=master

.. image:: https://img.shields.io/pypi/v/fqn-decorators.svg
    :target: https://pypi.python.org/pypi/fqn-decorators

.. image:: https://readthedocs.org/projects/fqn-decorators/badge/?version=latest
    :target: http://fqn-decorators.readthedocs.org/en/latest/?badge=latest


Installation
------------
.. start_installation

At the command line::

    $ pip install fqn-decorators


.. end_installation

Usage
-----
.. start_usage
.. py:currentmodule:: fqn_decorators.decorators

Introduction
------------

By extending the :class:`~Decorator` class you can create simple decorators.
Implement the :meth:`~Decorator.before` and/or :meth:`~Decorator.after` methods to perform actions before or after execution of the decorated item.
The :meth:`~Decorator.before` method can access the arguments of the decorated item by changing the :attr:`~Decorator.args` and :attr:`~Decorator.kwargs` attributes.
The :meth:`~Decorator.after` method can access or change the result using the :attr:`~Decorator.result` attribute.
The :meth:`~Decorator.exception` method can be used for do something with an Exception that has been raised.
In all three methods the :attr:`~Decorator.fqn` and :attr:`~Decorator.func` attributes are available.

Simple decorator
----------------

Create a simple decorator::

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

    >>>my_function()
    __main__.my_function took 1.00293397903 seconds


Decorator with arguments
------------------------

It is also very easy to create a decorator with arguments.

.. note::
    It is not possible to create decorators with *non-keyworded* arguments.
    To create a decorator that supports non-keyworded arguments see the :ref:`Advanced Usage <usage_advanced_non_keyword_decorators>` section.

Example::

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

    >>> my_function()
    Exception: Execution took longer than the threshold

.. end_usage
