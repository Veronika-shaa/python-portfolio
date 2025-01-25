import json

from typing import Callable


def formatter(key: str, token: str):
    return f"{key=}, {token=}"


def process_json(
    json_str: str,
    required_keys: list[str] | None = None,
    tokens: list[str] | None = None,
    callback: Callable[[str, str], None] | None = None,
) -> None:
    if not callback:
        callback = formatter
    if not required_keys:
        print('')
        return
    if not tokens:
        print('')
        return
    json_str = json.loads(json_str)
    low_tokens = list(map(lambda i: i.lower(), tokens))

    flag_key, flag_token = True, True

    for key, value in json_str.items():
        if key in required_keys:
            value_list = list(map(lambda i: i.lower(), value.split()))
            flag_key = False

            for ind, token in enumerate(low_tokens):
                if token in value_list:
                    print(callback(key, tokens[ind]))
                    flag_token = False

    if flag_key or flag_token:
        print('Совпадений не найдено')
    return
