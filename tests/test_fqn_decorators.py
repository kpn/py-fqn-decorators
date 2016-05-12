#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
import unittest

import fqn_decorators
import mock


@fqn_decorators.Decorator
def my_test_func(a):
    return a


@fqn_decorators.Decorator()
class A(object):

    @fqn_decorators.Decorator
    def method(self, a):
        return a


class TestFqn(unittest.TestCase):

    def test_function(self):
        self.assertEqual(fqn_decorators.get_fqn(fqn_decorators.get_fqn), 'fqn_decorators.decorators.get_fqn')

    def test_decorated_function(self):
        self.assertEqual(fqn_decorators.get_fqn(my_test_func), 'tests.test_fqn_decorators.my_test_func')

    def test_class(self):
        self.assertEqual(fqn_decorators.get_fqn(fqn_decorators.Decorator), 'fqn_decorators.decorators.Decorator')

    def test_method(self):
        self.assertEqual(
            fqn_decorators.get_fqn(fqn_decorators.Decorator().before), 'fqn_decorators.decorators.Decorator.before'
        )

    def test_decorated_method(self):
        self.assertEqual(fqn_decorators.get_fqn(A().method), 'tests.test_fqn_decorators.A.method')

    def test_decorated_class(self):
        self.assertEqual(fqn_decorators.get_fqn(A), 'tests.test_fqn_decorators.A')


class TestDecorator(unittest.TestCase):

    def test_getattr(self):
        class Decorator(fqn_decorators.Decorator):
            pass

        @Decorator
        def my_method():
            pass

        with self.assertRaises(AttributeError):
            self.fail(my_method.doesnotexists)

    def test_class_decoration(self):
        class Decorator(fqn_decorators.Decorator):
            def before(self):
                self.kwargs['username'] = 'root'

        @Decorator
        class User(object):
            def __init__(self, username):
                self.username = username

        user = User(username='admin')
        self.assertEqual(user.username, 'root')

    def test_advanced_class_decoration(self):
        class Decorator(fqn_decorators.Decorator):
            def before(self):
                self.kwargs['username'] = self.params['username']

        @Decorator(username='root')
        class User(object):
            def __init__(self, username):
                self.username = username

        user = User(username='admin')
        self.assertEqual(user.username, 'root')

    def test_function_decoration(self):
        class Decorator(fqn_decorators.Decorator):
            def after(self):
                self.result = True

        @Decorator
        def return_false():
            return False

        self.assertTrue(return_false())

    def test_advanced_function_decoration(self):
        class Decorator(fqn_decorators.Decorator):
            def after(self):
                self.result = self.params['result']

        @Decorator(result=None)
        def return_false():
            return False

        self.assertIsNone(return_false())

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

        self.assertEqual(User(username='root').get_username(), 'root')
        with self.assertRaises(Exception):
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

        self.assertFalse(User().staticmethod())

    def test_class_method_instance_decoration(self):
        class Decorator(fqn_decorators.Decorator):
            def after(self):
                self.result = False

        class User(object):
            @classmethod
            @Decorator
            def classmethod(cls):
                return True

        self.assertFalse(User().classmethod())

    def test_static_method_decoration(self):
        class Decorator(fqn_decorators.Decorator):
            def after(self):
                self.result = False

        class User(object):
            @staticmethod
            @Decorator
            def staticmethod():
                return True

        self.assertFalse(User.staticmethod())

    def test_class_method_decoration(self):
        class Decorator(fqn_decorators.Decorator):
            def after(self):
                self.result = False

        class User(object):
            @classmethod
            @Decorator
            def classmethod(cls):
                return True

        self.assertFalse(User.classmethod())

    def test_exception(self):
        class User(object):
            @fqn_decorators.Decorator
            def check_permission(self):
                raise Exception('Permission denied')

        with mock.patch('fqn_decorators.Decorator.exception') as mocked_method:
            with self.assertRaises(Exception):
                User().check_permission()
            self.assertTrue(mocked_method.called)
        with self.assertRaises(Exception):
            User().check_permission()


class TestChainedDecorator(unittest.TestCase):

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

        self.assertTrue(MyClass().my_method().endswith('MyClass.my_method'))


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
