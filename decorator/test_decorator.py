import unittest
from unittest import mock

from deco import retry_deco


class TestDecorator(unittest.TestCase):

    def test_with_pos_args(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            mock_func = mock.Mock(return_value=7)
            mock_func.__name__ = "mock_func"
            deco_func = retry_deco(2)(mock_func)

            result = deco_func(3, 4)

            mock_print.assert_has_calls([
                mock.call("run mock_func with pos. args = (3, 4), attempt=1, result=7"),
                ], any_order=False)

            self.assertEqual(result, 7)
            # проверяем количество перезапусков функции
            self.assertEqual(mock_func.call_count, 1)

    def test_with_keyword_args(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            mock_func = mock.Mock(return_value=7)
            mock_func.__name__ = "mock_func"
            deco_func = retry_deco(2)(mock_func)

            result = deco_func(x=3, y=4)

            mock_print.assert_has_calls([
                mock.call("run mock_func with keyword kwargs = {'x': 3, 'y': 4}, attempt=1, result=7"),
                ], any_order=False)

            self.assertEqual(result, 7)
            # проверяем количество перезапусков функции
            self.assertEqual(mock_func.call_count, 1)

    def test_with_everyone_arg(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            mock_func = mock.Mock(return_value=7)
            mock_func.__name__ = "mock_func"
            deco_func = retry_deco(2)(mock_func)

            result = deco_func(3, y=4)

            mock_print.assert_has_calls([
                mock.call("run mock_func with pos. args = (3,), keyword kwargs = {'y': 4}, attempt=1, result=7"),
                ], any_order=False)

            self.assertEqual(result, 7)
            # проверяем количество перезапусков функции
            self.assertEqual(mock_func.call_count, 1)

    def test_diff_call_func(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            mock_func = mock.Mock(return_value=7)
            mock_func.__name__ = "mock_func"
            deco_func = retry_deco(2)(mock_func)

            deco_func(3, 4)
            deco_func(3, 4)

            mock_print.assert_has_calls([
                mock.call("run mock_func with pos. args = (3, 4), attempt=1, result=7"),
                mock.call("run mock_func with pos. args = (3, 4), attempt=1, result=7")
                ], any_order=False)

    def test_error(self):
        mock_print = mock.Mock()

        # проверяем работу с исключением без заданного списка
        with mock.patch("builtins.print", mock_print):

            mock_func = mock.Mock(side_effect=ValueError())
            mock_func.__name__ = "mock_func"
            deco_func = retry_deco(2)(mock_func)

            with self.assertRaises(ValueError):
                deco_func(3, 4)

            mock_print.assert_has_calls([
                mock.call("run mock_func with pos. args = (3, 4), attempt=1, err=ValueError()"),
                mock.call("run mock_func with pos. args = (3, 4), attempt=2, err=ValueError()")
                ], any_order=False)

            # проверяем количество перезапусков функции
            self.assertEqual(mock_func.call_count, 2)

        # проверяем работу с исключением не входящим в заданный список
        with mock.patch("builtins.print", mock_print):

            mock_func = mock.Mock(side_effect=TypeError())
            mock_func.__name__ = "mock_func"
            cls_exception = [ValueError]
            deco_func = retry_deco(2, cls_exception)(mock_func)

            with self.assertRaises(TypeError):
                deco_func(3, 4)

            mock_print.assert_has_calls([
                mock.call("run mock_func with pos. args = (3, 4), attempt=1, err=TypeError()"),
                mock.call("run mock_func with pos. args = (3, 4), attempt=2, err=TypeError()")
                ], any_order=False)

            # проверяем количество перезапусков функции
            self.assertEqual(mock_func.call_count, 2)

    def test_error_in_cls_exception(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            mock_func = mock.Mock(side_effect=ValueError())
            mock_func.__name__ = "mock_func"
            cls_exception = [ValueError]
            deco_func = retry_deco(2, cls_exception)(mock_func)

            with self.assertRaises(ValueError):
                deco_func(3, 4)

            mock_print.assert_has_calls([
                mock.call("run mock_func with pos. args = (3, 4), attempt=1, err=ValueError()")
                ], any_order=False)

            # проверяем количество перезапусков функции
            self.assertEqual(mock_func.call_count, 1)

    def test_error_with_keyword_args(self):
        mock_print = mock.Mock()

        # проверяем работу с исключением без заданного списка
        with mock.patch("builtins.print", mock_print):

            mock_func = mock.Mock(side_effect=ValueError())
            mock_func.__name__ = "mock_func"
            deco_func = retry_deco(2)(mock_func)

            with self.assertRaises(ValueError):
                deco_func(x=3, y=4)

            mock_print.assert_has_calls([
                mock.call("run mock_func with keyword kwargs = {'x': 3, 'y': 4}, attempt=1, err=ValueError()"),
                mock.call("run mock_func with keyword kwargs = {'x': 3, 'y': 4}, attempt=2, err=ValueError()")
            ])

            # проверяем количество перезапусков функции
            self.assertEqual(mock_func.call_count, 2)

        # проверяем работу с исключением входящим в заданный список
        with mock.patch("builtins.print", mock_print):

            mock_func = mock.Mock(side_effect=ValueError())
            mock_func.__name__ = "mock_func"
            cls_exception = [ValueError]
            deco_func = retry_deco(2, cls_exception)(mock_func)

            with self.assertRaises(ValueError):
                deco_func(x=3, y=4)

            mock_print.assert_has_calls([
                mock.call("run mock_func with keyword kwargs = {'x': 3, 'y': 4}, attempt=1, err=ValueError()")
            ])

            # проверяем количество перезапусков функции
            self.assertEqual(mock_func.call_count, 1)

    def test_error_with_everyone_arg(self):
        mock_print = mock.Mock()

        # проверяем работу с исключением без заданного списка
        with mock.patch("builtins.print", mock_print):

            mock_func = mock.Mock(side_effect=ValueError())
            mock_func.__name__ = "mock_func"
            deco_func = retry_deco(2)(mock_func)

            with self.assertRaises(ValueError):
                deco_func(3, y=4)

            mock_print.assert_has_calls([
                mock.call("run mock_func with pos. args = (3,), keyword kwargs = {'y': 4}, attempt=1, err=ValueError()"),
                mock.call("run mock_func with pos. args = (3,), keyword kwargs = {'y': 4}, attempt=2, err=ValueError()")
                ])

            # проверяем количество перезапусков функции
            self.assertEqual(mock_func.call_count, 2)

        # проверяем работу с исключением входящим в заданный список
        with mock.patch("builtins.print", mock_print):

            mock_func = mock.Mock(side_effect=ValueError())
            mock_func.__name__ = "mock_func"
            cls_exception = [ValueError]
            deco_func = retry_deco(2, cls_exception)(mock_func)

            with self.assertRaises(ValueError):
                deco_func(3, y=4)

            mock_print.assert_has_calls([
                mock.call("run mock_func with pos. args = (3,), keyword kwargs = {'y': 4}, attempt=1, err=ValueError()"),
                ])

            # проверяем количество перезапусков функции
            self.assertEqual(mock_func.call_count, 1)
