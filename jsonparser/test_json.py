import unittest
from unittest import mock

from processjson import process_json


class TestProcessJson(unittest.TestCase):

    def test_empty_keys(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = []
        tokens = ["WORD1", "word2"]

        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            process_json(json_str, required_keys, tokens)

            mock_print.assert_has_calls([
                mock.call("")
                ], any_order=False)

    def test_empty_tokens(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "key2"]
        tokens = []

        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            process_json(json_str, required_keys, tokens)

            mock_print.assert_has_calls([
                mock.call("")
                ], any_order=False)

    def test_default_keys(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        tokens = ["WORD1", "word2"]

        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            process_json(json_str, tokens=tokens)

            mock_print.assert_has_calls([
                mock.call("")
                ], any_order=False)

    def test_default_tokens(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "key2"]

        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            process_json(json_str, required_keys)

            mock_print.assert_has_calls([
                mock.call("")
                ], any_order=False)

    def test_mismatch_keys(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["KEy1", "KEy2"]
        tokens = ["WORD1", "word2"]

        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            process_json(json_str, required_keys, tokens)

            mock_print.assert_has_calls([
                mock.call("Совпадений не найдено")
                ], any_order=False)

    def test_mismatch_tokens(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "key2"]
        tokens = ["Tom", "Jerry"]

        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            process_json(json_str, required_keys, tokens)

            mock_print.assert_has_calls([
                mock.call("Совпадений не найдено")
                ], any_order=False)

    def test_given_func(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "KEY2"]
        tokens = ["WORD1", "word2"]

        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            process_json(json_str, required_keys, tokens, lambda key, token: f"ключ: {key}, токен: {token}")

            mock_print.assert_has_calls([
                mock.call("ключ: key1, токен: WORD1"),
                mock.call("ключ: key1, токен: word2")
                ], any_order=False)

    def test_all_keys(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "key2"]
        tokens = ["WORD1", "word2"]

        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            process_json(json_str, required_keys, tokens)

            mock_print.assert_has_calls([
                mock.call("key='key1', token='WORD1'"),
                mock.call("key='key1', token='word2'"),
                mock.call("key='key2', token='word2'")
                ], any_order=False)

    def test_all_tokens(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key2"]
        tokens = ["WORD1", "word2", "woRd3"]

        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            process_json(json_str, required_keys, tokens)

            mock_print.assert_has_calls([
                mock.call("key='key2', token='word2'"),
                mock.call("key='key2', token='woRd3'")
                ], any_order=False)

    def test_all_lists(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "key2"]
        tokens = ["WORD1", "word2", "woRd3"]

        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            process_json(json_str, required_keys, tokens)

            mock_print.assert_has_calls([
                mock.call("key='key1', token='WORD1'"),
                mock.call("key='key1', token='word2'"),
                mock.call("key='key2', token='word2'"),
                mock.call("key='key2', token='woRd3'")
                ], any_order=False)

    def test_repeating_keys(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "key2", "key1"]
        tokens = ["WORD1", "word2"]

        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            process_json(json_str, required_keys, tokens)

            mock_print.assert_has_calls([
                mock.call("key='key1', token='WORD1'"),
                mock.call("key='key1', token='word2'"),
                mock.call("key='key2', token='word2'")
                ], any_order=False)

    def test_repeating_tokens(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "key2"]
        tokens = ["WORD1", "word2", "WORD1"]

        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            process_json(json_str, required_keys, tokens)

            mock_print.assert_has_calls([
                mock.call("key='key1', token='WORD1'"),
                mock.call("key='key1', token='word2'"),
                mock.call("key='key1', token='WORD1'"),
                mock.call("key='key2', token='word2'")
                ], any_order=False)

    def test_register_keys(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "KEY2"]
        tokens = ["WORD1", "word2"]

        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            process_json(json_str, required_keys, tokens)

            mock_print.assert_has_calls([
                mock.call("key='key1', token='WORD1'"),
                mock.call("key='key1', token='word2'")
                ], any_order=False)

    def test_register_tokens(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "key2"]
        tokens = ["WORD1", "woRD2"]

        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            process_json(json_str, required_keys, tokens)

            mock_print.assert_has_calls([
                mock.call("key='key1', token='WORD1'"),
                mock.call("key='key1', token='woRD2'"),
                mock.call("key='key2', token='woRD2'")
                ], any_order=False)

    def test_overlap_lists(self):
        json_str = '{"key1": "keY1 KEY2", "key2": "KEy2 kEy1"}'
        required_keys = ["key1", "key2"]
        tokens = ["key1", "key2"]

        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):

            process_json(json_str, required_keys, tokens)

            mock_print.assert_has_calls([
                mock.call("key='key1', token='key1'"),
                mock.call("key='key1', token='key2'"),
                mock.call("key='key2', token='key1'"),
                mock.call("key='key2', token='key2'")
                ], any_order=False)
