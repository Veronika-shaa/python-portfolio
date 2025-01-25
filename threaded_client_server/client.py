

import argparse
import socket
import threading


# pylint: disable=broad-exception-caught
class Client:
    def __init__(self, urls, m):
        self.m = m
        self.urls = urls
        self.host = '127.0.0.1'
        self.port = 65432
        self.lock = threading.Lock()

    def connect_with_server(self, urls):
        for url in urls:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((self.host, self.port))  # соединение с сервером
                    client_socket.sendall(url.encode())  # отправка запроса на сервер
                    response = client_socket.recv(1024)  # получение ответа с сервера
                    print(response.decode('utf-8'))
            except Exception as e:
                print(f"Произошла ошибка: {e}")

    def read_url(self, m, i_th):
        with open(self.urls, 'r', encoding='utf-8') as f:
            try:
                f.seek(0)
                count_lines = sum(1 for _ in f)  # количетво урлов в файле
                f.seek(0)
                n_urls = count_lines//m  # количетво урлов на поток
                start = i_th * n_urls
                if i_th == m - 1:  # последний поток читает до конца файла
                    end = count_lines
                else:
                    end = (i_th + 1) * n_urls
                urls = []
                for line, url in enumerate(f):
                    if start <= line < end:
                        urls.append(url.strip('\n'))
                return urls
            except Exception as e:
                print(f"Ошибка при чтении URL: {e}")
                return []

    def run(self):
        threads = [
            threading.Thread(
                target=self.connect_with_server,
                args=(self.read_url(self.m, i),)
            )
            for i in range(self.m)
        ]

        for th in threads:
            th.start()

        for th in threads:
            th.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('m', type=int, help='Количество потоков.')
    parser.add_argument('urls', type=str, help='Файл с URL-адресами.')
    args = parser.parse_args()
    client = Client(args.urls, args.m)
    client.run()
