from functools import wraps


# pylint: disable=line-too-long, inconsistent-return-statements
def retry_deco(
        n: int,
        cls_exception: list | None = None
):
    # пустой список в случае, если он не передан в качестве аргумента
    if not cls_exception:
        cls_exception = []

    def deco(fn):

        @wraps(fn)
        def inner(*args, **kwargs):
            attempt = 1
            # перезапуск
            while attempt <= n:
                try:
                    arg = (args, tuple(kwargs.items()))
                    result = fn(*args, **kwargs)
                    match arg:
                        case (p_arg, kw_arg) if p_arg and kw_arg:
                            print(f'run {fn.__name__} with pos. args = {args}, keyword kwargs = {kwargs}, {attempt=}, {result=}')
                        case (p_arg, kw_arg) if p_arg:
                            print(f'run {fn.__name__} with pos. args = {args}, {attempt=}, {result=}')
                        case _:
                            print(f'run {fn.__name__} with keyword kwargs = {kwargs}, {attempt=}, {result=}')
                    return result

                # ловим исключения из списка и игнорируем сообщение pylint, т.к. cls_exception не всегда будет пуст
                except tuple(cls_exception) as err:  # pylint: disable=catching-non-exception
                    match arg:
                        case (p_arg, kw_arg) if p_arg and kw_arg:
                            print(f'run {fn.__name__} with pos. args = {args}, keyword kwargs = {kwargs}, {attempt=}, {err=}')
                        case (p_arg, kw_arg) if p_arg:
                            print(f'run {fn.__name__} with pos. args = {args}, {attempt=}, {err=}')
                        case _:
                            print(f'run {fn.__name__} with keyword kwargs = {kwargs}, {attempt=}, {err=}')
                    raise err  # pylint: disable=raising-non-exception

                # ловим исключения не входящие в список и игнорируем сообщение pylint, т.к. ошибка далее логируется
                except Exception as err:  # pylint: disable=broad-exception-caught
                    match arg:
                        case (p_arg, kw_arg) if p_arg and kw_arg:
                            print(f'run {fn.__name__} with pos. args = {args}, keyword kwargs = {kwargs}, {attempt=}, {err=}')
                        case (p_arg, kw_arg) if p_arg:
                            print(f'run {fn.__name__} with pos. args = {args}, {attempt=}, {err=}')
                        case _:
                            print(f'run {fn.__name__} with keyword kwargs = {kwargs}, {attempt=}, {err=}')
                    attempt += 1
                    if attempt > n:
                        raise err
        return inner
    return deco
