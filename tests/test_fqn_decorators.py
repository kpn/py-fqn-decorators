#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
import sys

import fqn_decorators
import mock
import pytest

from . import examples


class InheritedExample(examples.B):
    pass


class TestFqn(object):

    def test_function(self):
        assert fqn_decorators.get_fqn(fqn_decorators.get_fqn) == \
            'fqn_decorators.decorators.get_fqn'

    def test_decorated_function(self):
        assert fqn_decorators.get_fqn(examples.my_test_func) == \
            'tests.examples.my_test_func'

    def test_class(self):
        assert fqn_decorators.get_fqn(fqn_decorators.Decorator) == \
            'fqn_decorators.decorators.Decorator'

    def test_method(self):
        assert fqn_decorators.get_fqn(fqn_decorators.Decorator().before) == \
            'fqn_decorators.decorators.Decorator.before'

    def test_decorated_method(self):
        assert fqn_decorators.get_fqn(examples.A().method) == \
            'tests.examples.A.method'

    def test_decorated_inherited_method(self):
        assert fqn_decorators.get_fqn(InheritedExample().method) == \
            'tests.test_fqn_decorators.InheritedExample.method'

    def test_decorated_class(self):
        assert fqn_decorators.get_fqn(examples.A) == 'tests.examples.A'


class TestGetCallerFqn:
    def test_function(self):
        def inline_method():
            return fqn_decorators.get_caller_fqn()

        assert inline_method() == 'tests.test_fqn_decorators.TestGetCallerFqn.test_function'

    def test_method(self):
        class Inline:
            def inline(self):
                return fqn_decorators.get_caller_fqn()

        assert Inline().inline() == 'tests.test_fqn_decorators.TestGetCallerFqn.test_method'

    @pytest.mark.skipif(sys.version_info < (3, 0), reason='requires python3')
    def test_caller_is_method(self):
        def inline_method():
            return fqn_decorators.get_caller_fqn()

        class Caller:
            def parent(self):
                return inline_method()

        assert Caller().parent() == (
            'tests.test_fqn_decorators.TestGetCallerFqn.test_caller_is_method.Caller.parent'
        )

    def test_caller_is_inner(self):
        def child_method():
            return fqn_decorators.get_caller_fqn()

        def parent_method():
            return child_method()

        assert parent_method() == (
            'tests.test_fqn_decorators.TestGetCallerFqn.test_caller_is_inner.parent_method'
        )

    @pytest.mark.skipif(sys.version_info < (3, 0), reason='requires python3')
    def test_caller_is_complex(self):
        def child_method():
            return fqn_decorators.get_caller_fqn()

        def outer_method():
            return child_method()

        class Caller:
            def parent(self):
                return outer_method()

            def parent_with_inner(self):
                def inner_parent():
                    return outer_method()
                return inner_parent()

        assert Caller().parent() == (
            'tests.test_fqn_decorators.TestGetCallerFqn.test_caller_is_complex.Caller.parent.outer_method'
        )

        assert Caller().parent_with_inner() == (
            'tests.test_fqn_decorators.TestGetCallerFqn.test_caller_is_complex.'
            'Caller.parent_with_inner.inner_parent.outer_method'
        )


class TestDecorator(object):

    def test_getattr(self):
        class Decorator(fqn_decorators.Decorator):
            pass

        @Decorator
        def my_method():
            pass

        with pytest.raises(AttributeError):
            assert my_method.doesnotexists is False

    def test_class_decoration(self):
        class Decorator(fqn_decorators.Decorator):
            def before(self):
                self.kwargs['username'] = 'root'

        @Decorator
        class User(object):
            def __init__(self, username):
                self.username = username

        user = User(username='admin')
        assert user.username == 'root'

    def test_advanced_class_decoration(self):
        class Decorator(fqn_decorators.Decorator):
            def before(self):
                self.kwargs['username'] = self.params['username']

        @Decorator(username='root')
        class User(object):
            def __init__(self, username):
                self.username = username

        user = User(username='admin')
        assert user.username == 'root'

    def test_function_decoration(self):
        class Decorator(fqn_decorators.Decorator):
            def after(self):
                self.result = True

        @Decorator
        def return_false():
            return False

        assert return_false() is True

    def test_advanced_function_decoration(self):
        class Decorator(fqn_decorators.Decorator):
            def after(self):
                self.result = self.params['result']

        @Decorator(result=None)
        def return_false():
            return False

        assert return_false() is None

    def test_method_decoration(self):
        class Decorator(fqn_decorators.Decorator):
            def after(self):
                if self.result != 'root':
                    raise Exception('Not root')

        class User(object):
            def __init__(self, username):
                self.username = username

            @Decorator
            def get_username(self):
                return self.username

        assert User(username='root').get_username() == 'root'
        with pytest.raises(Exception):
            User(username='admin').get_username()

    def test_static_method_instance_decoration(self):
        class Decorator(fqn_decorators.Decorator):
            def after(self):
                self.result = False

        class User(object):

            @staticmethod
            @Decorator
            def staticmethod():
                return True

        assert User().staticmethod() is False

    def test_class_method_instance_decoration(self):
        class Decorator(fqn_decorators.Decorator):
            def after(self):
                self.result = False

        class User(object):
            @classmethod
            @Decorator
            def classmethod(cls):
                return True

        assert User().classmethod() is False

    def test_static_method_decoration(self):
        class Decorator(fqn_decorators.Decorator):
            def after(self):
                self.result = False

        class User(object):
            @staticmethod
            @Decorator
            def staticmethod():
                return True

        assert User.staticmethod() is False

    def test_class_method_decoration(self):
        class Decorator(fqn_decorators.Decorator):
            def after(self):
                self.result = False

        class User(object):
            @classmethod
            @Decorator
            def classmethod(cls):
                return True

        assert User.classmethod() is False

    def test_exception(self):
        class User(object):
            @fqn_decorators.Decorator
            def check_permission(self):
                raise Exception('Permission denied')

        with mock.patch('fqn_decorators.Decorator.exception') as mocked_method:
            with pytest.raises(Exception):
                User().check_permission()
            assert mocked_method.called is True
        with pytest.raises(Exception):
            User().check_permission()


class TestChainedDecorator(object):

    def test_chaining(self):
        def simple_decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        def simple_keyword_decorator(func=None, result=True):
            def func_wrapper(func):
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    return func(*args, **kwargs)
                return wrapper

            if func:
                return func_wrapper(func)
            return func_wrapper

        class SimpleDecorator(fqn_decorators.Decorator):
            def after(self):
                self.result = self.fqn

        class MyClass(object):
            @fqn_decorators.chained_decorator(decorators=[
                SimpleDecorator, simple_decorator, simple_keyword_decorator(result=False)
            ])
            def my_method(self):
                pass

        assert MyClass().my_method().endswith('MyClass.my_method')
