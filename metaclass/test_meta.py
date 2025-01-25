import unittest
from unittest import mock

from custommeta import CustomClass, MyClass


# pylint: disable=no-member, protected-access
class TestCustomMeta(unittest.TestCase):

    def test_public_cls_attr(self):

        self.assertEqual(CustomClass.custom_x, 50)

        with self.assertRaises(AttributeError):
            print(CustomClass.x)

    def test_protected_cls_attr(self):

        self.assertEqual(MyClass.custom__protect, 'cls_protect')

        with self.assertRaises(AttributeError):
            print(CustomClass._protect)

    def test_private_cls_attr(self):

        self.assertEqual(MyClass.custom__MyClass__private, 'cls_private')

        with self.assertRaises(AttributeError):
            print(CustomClass._MyClass__private)

    def test_dynamic_cls_attr(self):
        # public
        CustomClass.new_attr = 'new'

        self.assertEqual(CustomClass.custom_new_attr, 'new')

        with self.assertRaises(AttributeError):
            print(CustomClass.new_attr)

        # protected
        CustomClass._new_attr = '_new'

        self.assertEqual(CustomClass.custom__new_attr, '_new')

        with self.assertRaises(AttributeError):
            print(CustomClass._new_attr)

        # private
        CustomClass._CustomClass__new_attr = '__new'

        self.assertEqual(CustomClass.custom__CustomClass__new_attr, '__new')

        with self.assertRaises(AttributeError):
            print(CustomClass._CustomClass__new_attr)

    def test_public_obj_attr(self):

        inst = CustomClass()
        self.assertEqual(inst.custom_val, 99)

        with self.assertRaises(AttributeError):
            print(inst.val)

        inst = CustomClass('wow')
        self.assertEqual(inst.custom_val, 'wow')

        with self.assertRaises(AttributeError):
            print(inst.val)

    def test_protected_obj_attr(self):

        inst = MyClass()

        self.assertEqual(inst.custom__obj_protect, 'obj_protect')

        with self.assertRaises(AttributeError):
            print(inst._obj_protect)

    def test_private_obj_attr(self):

        inst = MyClass()

        self.assertEqual(inst.custom__MyClass__obj_private, 'obj_private')

        with self.assertRaises(AttributeError):
            print(inst._MyClass__obj_private)

    def test_dynamic_obj_attr(self):

        inst = CustomClass()
        # public
        inst.dynamic_attr = 'I am new'

        self.assertEqual(inst.custom_dynamic_attr, 'I am new')

        with self.assertRaises(AttributeError):
            print(inst.dynamic_attr)

        # protected
        inst._dynamic_attr = '_I am new'

        self.assertEqual(inst.custom__dynamic_attr, '_I am new')

        with self.assertRaises(AttributeError):
            print(inst._dynamic_attr)

    def test_dynamic_method(self):
        mock_func = mock.Mock(return_value=7)

        setattr(MyClass, 'dynamic_method', mock_func)

        inst = MyClass()
        self.assertEqual(inst.custom_dynamic_method(), 7)

        with self.assertRaises(AttributeError):
            inst.dynamic_method()

    def test_dynamic_protected_method(self):
        mock_func = mock.Mock(return_value=7)

        setattr(MyClass, '_dynamic_protected_method', mock_func)

        inst = MyClass()
        self.assertEqual(inst.custom__dynamic_protected_method(), 7)

        with self.assertRaises(AttributeError):
            inst._dynamic_protected_method()

    def test_method(self):

        inst = CustomClass()
        self.assertEqual(inst.custom_line(), 100)

        with self.assertRaises(AttributeError):
            inst.line()

    def test_protected_method(self):

        inst = MyClass()
        self.assertEqual(inst.custom__protected_method(), "_protected_method")

        with self.assertRaises(AttributeError):
            inst._protected_method()

    def test_magic_method(self):

        inst = CustomClass()
        self.assertEqual(str(inst), "Custom_by_metaclass")

    def test_error(self):

        inst = CustomClass()

        with self.assertRaises(AttributeError):
            print(inst.yyy)
