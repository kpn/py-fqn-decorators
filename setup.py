
from setuptools import setup
setup(**{'author': 'Mattias Sluis',
 'author_email': 'mattias.sluis@kpn.com',
 'classifiers': ['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Topic :: Internet :: WWW/HTTP'],
 'description': 'Easily create multi-purpose decorators that have access to the FQN of the original function.',
 'include_package_data': True,
 'install_requires': ['pkgversion'],
 'long_description': 'FQN Decorators\n==============\n\n.. image:: https://secure.travis-ci.org/kpn-digital/py-fqn-decorators.svg?branch=master\n    :target:  http://travis-ci.org/kpn-digital/py-fqn-decorators?branch=master\n\n.. image:: https://img.shields.io/codecov/c/github/kpn-digital/py-fqn-decorators/master.svg\n    :target: http://codecov.io/github/kpn-digital/py-fqn-decorators?branch=master\n\n.. image:: https://img.shields.io/pypi/v/fqn-decorators.svg\n    :target: https://pypi.python.org/pypi/fqn-decorators\n\n.. image:: https://readthedocs.org/projects/fqn-decorators/badge/?version=latest\n    :target: http://fqn-decorators.readthedocs.org/en/latest/?badge=latest\n\n\nInstallation\n------------\n.. start_installation\n\nAt the command line::\n\n    $ pip install fqn-decorators\n\n\n.. end_installation\n\nUsage\n-----\n.. start_usage\n.. py:currentmodule:: decorators.decorators\n\nIntroduction\n------------\n\nBy extending the :class:`~Decorator` class you can create simple decorators.\nImplement the :meth:`~Decorator.before` and/or :meth:`~Decorator.after` methods to perform actions before or after execution of the decorated item.\nThe :meth:`~Decorator.before` method can access the arguments of the decorated item by changing the :attr:`~Decorator.args` and :attr:`~Decorator.kwargs` attributes.\nThe :meth:`~Decorator.after` method can access or change the result using the :attr:`~Decorator.result` attribute.\nThe :meth:`~Decorator.exception` method can be used for do something with an Exception that has been raised.\nIn all three methods the :attr:`~Decorator.fqn` and :attr:`~Decorator.func` attributes are available.\n\nSimple decorator\n----------------\n\nCreate a simple decorator::\n\n    import decorators\n    import time\n\n    class time_it(decorators.Decorator):\n\n        def before(self):\n            self.start = time.time()\n\n        def after(self):\n            duration = time.time() - self.start\n            print("{0} took {1} seconds".format(self.fqn, duration))\n\n\n    @time_it\n    def my_function():\n        time.sleep(1)\n\n    >>>my_function()\n    __main__.my_function took 1.00293397903 seconds\n\n\nDecorator with arguments\n------------------------\n\nIt is also very easy to create a decorator with arguments.\n\n.. note::\n    It is not possible to create decorators with *non-keyworded* arguments.\n    To create a decorator that supports non-keyworded arguments see the :ref:`Advanced Usage <usage_advanced_non_keyword_decorators>` section.\n\nExample::\n\n    import decorators\n    import time\n\n    class threshold(decorators.Decorator):\n\n        def before(self):\n            self.start = time.time()\n\n        def after(self):\n            duration = time.time() - self.start\n            treshold = self.params.get(\'threshold\')\n            if threshold and duration > threshold:\n                raise Exception(\'Execution took longer than the threshold\')\n\n\n    @threshold(threshold=2)\n    def my_function():\n        time.sleep(3)\n\n    >>> my_function()\n    Exception: Execution took longer than the threshold\n\n.. end_usage\n',
 'name': 'fqn-decorators',
 'packages': ['decorators', 'tests'],
 'tests_require': ['tox'],
 'url': 'ssh://git@github.com:kpn-digital/py-fqn-decorators.git',
 'version': None,
 'zip_safe': False})