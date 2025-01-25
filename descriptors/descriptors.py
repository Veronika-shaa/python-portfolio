import hashlib
import re


class BaseDescriptor:

    def __set_name__(self, class_type, name):
        self._name = name  # pylint: disable=attribute-defined-outside-init

    def __get__(self, obj, objtype):
        if obj is None:
            return None

        return obj.__dict__.get(self._name)

    def __set__(self, obj, val):
        if not self.validate(val):
            raise ValueError

        obj.__dict__[self._name] = val

    def __delete__(self, obj):
        if self._name in obj.__dict__:
            del obj.__dict__[self._name]

    def validate(self, val):
        pass


class Nickname(BaseDescriptor):
    __name_dict = {}  # Создаем словарь для хранения множества никнеймов по классам

    def validate(self, val):
        return isinstance(val, str)

    def __set__(self, obj, val):
        cls = obj.__class__  # Получаем класс объекта
        name_set = self._get_class_name_set(cls)  # Получаем множество никнеймов для класса

        current_nick = obj.__dict__.get(self._name)  # Получаем текущий никнейм

        if current_nick:
            name_set.discard(current_nick)  # Удаляем текущий никнейм с дальнейшей установкой нового

        # Проверяем, существует ли устанавливаемый никнейм
        if val in name_set:
            raise ValueError(f"Никнейм '{val}' уже существует")

        super().__set__(obj, val)

        name_set.add(val)  # Добавляем новый никнейм в множество

    def _get_class_name_set(self, cls):
        """Получает или создает множество никнеймов для каждого класса."""
        if cls not in self.__name_dict:
            self.__name_dict[cls] = set()

        return self.__name_dict[cls]

    def __delete__(self, obj):
        cls = obj.__class__
        name_set = self._get_class_name_set(cls)  # Получаем множество никнеймов для класса
        name_set.discard(self._name)  # Удаляем никнейм из множества

        return super().__delete__(obj)


class Password(BaseDescriptor):

    def __get__(self, obj, objtype):
        raise AttributeError("Пароль можно только установить")

    def __set__(self, obj, val):
        if not self.validate(val):
            raise ValueError

        hash_password = self.hash(val)  # Хэшируем пароль
        obj.__dict__[self._name] = hash_password  # Устанавливаем хэшированный пароль в словаре экземпляра

    def hash(self, password):
        """Хэширует пароль, возвращает хэш-строку"""
        b_password = password.encode('utf-8')  # Кодируем пароль в байты

        return hashlib.sha256(b_password).hexdigest()  # Возвращаем хэш-строку

    def validate(self, val):
        return (isinstance(val, str) and len(val) > 7
                and re.search(r'[A-Z]', val)
                and re.search(r'[a-z]', val)
                and re.search(r'[0-9]', val))


class Age(BaseDescriptor):

    def validate(self, val):
        if isinstance(val, int) and val < 12:
            raise ValueError('Возрастное ограничение 12+')
        return isinstance(val, int)


class User:

    nickname = Nickname()
    password = Password()
    age = Age()

    def __init__(self, nickname, pw="Qwerty345", age=18):
        self.nickname = nickname
        self.password = pw
        self.age = age
