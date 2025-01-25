import unittest
import hashlib
from descriptors import User


class TestDescriptors(unittest.TestCase):

    def test_set_nickname(self):

        user_1 = User("wow")
        self.assertEqual(user_1.nickname, "wow")

        # изменение никнейма
        user_1.nickname = "WOW"
        self.assertEqual(user_1.nickname, "WOW")

        # попытка установки невалидного никнейма
        with self.assertRaises(ValueError):
            user_1.nickname = 8

        self.assertEqual(user_1.nickname, "WOW")

    def test_del_nickname(self):

        user_2 = User("ww")
        del user_2.nickname

        self.assertEqual(user_2.nickname, None)

    def test_set_same_nickname(self):
        User('Hello, World')
        with self.assertRaises(ValueError) as err:
            User("Hello, World")

            self.assertEqual(str(err.exception), "Никнейм 'Hello, World' уже существует")

    def test_set_invalid_nickname(self):

        with self.assertRaises(ValueError):
            User(23)

    def test_set_password(self):

        user_1 = User("wow", 'WalterWhite50')

        with self.assertRaises(AttributeError) as err:
            print(user_1.password)

        self.assertEqual(str(err.exception), "Пароль можно только установить")

    def test_set_invalid_password(self):

        # отсутствуют заглавные буквы
        with self.assertRaises(ValueError):
            User("Hello", 'walterwhite50')

        # отсутствуют цифры
        with self.assertRaises(ValueError):
            User("Hello", 'WalterWhite')

        # отсутствуют заглавные и строчные буквы
        with self.assertRaises(ValueError):
            User("Hello", '12345678')

        # меньше 8 знаков
        with self.assertRaises(ValueError):
            User("Hello", 'Pv3')

    def test_del_password(self):

        user_1 = User("wow1", 'WalterWhite50')
        del user_1.password

        self.assertNotIn('password', user_1.__dict__)

    def test_hash_password(self):

        user_1 = User("wow2", 'WalterWhite50')
        self.assertEqual(user_1.__dict__['password'], hashlib.sha256('WalterWhite50'.encode('utf-8')).hexdigest())

        # изменение пароля
        user_1.password = 'WalterWhite55'
        self.assertEqual(user_1.__dict__['password'], hashlib.sha256('WalterWhite55'.encode('utf-8')).hexdigest())

        # попытка установки невалидного пароля
        with self.assertRaises(ValueError):
            user_1.password = '55'

        self.assertEqual(user_1.__dict__['password'], hashlib.sha256('WalterWhite55'.encode('utf-8')).hexdigest())

    def test_set_invalid_age(self):

        with self.assertRaises(ValueError) as err:
            User("Walt", 'WalterWhite50', 11)

            self.assertEqual(str(err.exception), "Возрастное ограничение 12+")

    def test_set_age(self):

        user_1 = User("Walt", 'WalterWhite50', 50)
        self.assertEqual(user_1.age, 50)

        # изменение возраста
        user_1.age = 32
        self.assertEqual(user_1.age, 32)

        # попытка установки невалидного возраста
        with self.assertRaises(ValueError):
            user_1.age = 9

        self.assertEqual(user_1.age, 32)

    def test_del_age(self):

        user_2 = User("WaltW", 'WalterWhite50', 50)
        del user_2.age

        self.assertEqual(user_2.age, None)

    def test_users_dependency(self):
        # создание второго экземпляра
        user_1 = User("Pinkman", "JPn27272727", 27)
        user_2 = User("White", "Wwt50505050", 50)

        self.assertEqual(user_1.nickname, "Pinkman")
        self.assertEqual(user_2.nickname, "White")

        self.assertEqual(user_1.age, 27)
        self.assertEqual(user_2.age, 50)

        # изменение второго экземпляра
        user_2.nickname = "Flynn"
        user_2.age = 16

        self.assertEqual(user_1.nickname, "Pinkman")
        self.assertEqual(user_2.nickname, "Flynn")

        self.assertEqual(user_1.age, 27)
        self.assertEqual(user_2.age, 16)
