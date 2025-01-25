

import argparse
import json
import queue
import re
import socket
import threading
from collections import Counter

from bs4 import BeautifulSoup
import requests


# pylint: disable=too-many-instance-attributes, broad-exception-caught
class Server:
    def __init__(self, worker, k):
        self.w = worker
        self.k = k
        self.host = '127.0.0.1'
        self.port = 65432
        self.url_count = 0  # счетчик обработанных урлов
        self.lock = threading.Lock()
        self.flag = True  # флаг для остановки работы сервера
        self.que = queue.Queue()  # очередь для хранения и выдачи запросов воркерам
        self.server_socket = None

    def master(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            self.server_socket = server_socket
            server_socket.bind((self.host, self.port))
            server_socket.listen()  # мастер слушает порт

            # создание потоков воркеров
            workers = [
                threading.Thread(
                    target=self.worker,
                    args=(self.que,)
                )
                for _ in range(self.w)
            ]

            for worker in workers:
                worker.start()

            try:
                # пока сервер запущен, запросы принимаются
                while self.flag:
                    client_socket = server_socket.accept()[0]
                    data = client_socket.recv(1024)  # получение запроса от клиента
                    url = data.decode()
                    if url:
                        self.que.put((client_socket, url))  # добавление запроса в очередь
            except Exception as e:
                print(f"Произошла ошибка: {e}")
            finally:
                self.que.put((None, None))

                for worker in workers:
                    worker.join()

    def worker(self, que):
        while True:
            client_socket, url = que.get()  # вытягивание запроса из очереди
            if url is None:
                que.put((None, None))
                break

            try:
                response = requests.get(url, timeout=10)  # получение HTTP-запроса по урлу

                soup = BeautifulSoup(response.text, 'html.parser')  # извлечение текста из HTML-кода
                text = soup.get_text()  # извлечение текста из HTML-кода и удаление тегов

                words = re.findall(r'\w+', text.lower(), flags=re.ASCII)  # извлечение слов из текста
                counter = Counter(words).most_common(self.k)  # кортежи наиболее часто встречающихся слов и их количество
                result = json.dumps(dict(counter))  # преобразование в JSON строку
                client_socket.sendall(result.encode())

            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"Ошибка обработки URL {url}: {e}")
                client_socket.sendall(f"Ошибка обработки URL: {url}".encode())

            finally:
                client_socket.close()  # закрытие сокета после обработки урла

                with self.lock:
                    self.url_count += 1
                    print(f'Обработано {self.url_count} URL')

    def run(self):
        master = threading.Thread(
                    target=self.master
                )
        master.start()
        master.join()

    def stop(self):
        self.flag = False

        if self.server_socket:
            self.server_socket.close()  # остановка сервера


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', type=int, help='Количество воркеров')
    parser.add_argument('-k', type=int, help='Топ самых частых слов')
    args = parser.parse_args()

    server = Server(worker=args.w, k=args.k)
    server.run()
