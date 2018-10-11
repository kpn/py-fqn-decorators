import warnings

warnings.warn(
    'This module was renamed to `asynchronous` due to adding `async`'
    ' keyword in python 3.7',
    PendingDeprecationWarning
)

from .asynchronous import *  # isort:skip
