

class LRUCache:
    def __init__(self, limit=42):
        self.limit = limit
        self._value = {}

    def get(self, key):
        # ключ не был установлен
        if key not in self._value:
            return None

        # получаем значение и перезаписываем ключ в конец словаря
        get_val = self._value.pop(key)
        self._value[key] = get_val

        return get_val

    def set(self, key, value):
        # удаляем ключ при перезаписи значения
        if key in self._value:
            self._value.pop(key)

        self._value[key] = value

        # превышение лимита
        if len(self._value) > self.limit:
            # получение и удаление неиспользуемого (первого) элемента
            unused_key = next(iter(self._value))
            self._value.pop(unused_key)
