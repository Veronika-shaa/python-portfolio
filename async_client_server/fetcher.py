

import argparse
import asyncio
from collections import Counter
import json
import re

import aiofiles
import aiohttp
from bs4 import BeautifulSoup


async def fetch_url(url, session):
    """Обрабытывает url"""
    # Выполняем асинхронный запрос на получение HTTP-запроса по URL
    async with session.get(url) as resp:
        text = await resp.text()  # получаем текст из ответа
        # Создаем поток для обработки HTTP-запроса
        result = await asyncio.to_thread(process_text, text)
        return result


def process_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()

    words = re.findall(r'\w+', text.lower(), flags=re.ASCII)
    counter = Counter(words).most_common(5)

    return json.dumps(dict(counter))


async def reader(urls, que):
    """Выполняет чтение url из файла и добавление их в очередь"""
    async with aiofiles.open(urls, mode='r', encoding='utf-8') as f:
        async for url in f:
            await que.put(url.strip('\n'))


async def fetch_worker(que, session):
    """Обрабатывает url из очереди и выводит ответ"""
    while True:
        url = await que.get()
        try:
            result = await fetch_url(url, session)
            print(result)
        except Exception as err:  # pylint: disable=broad-exception-caught
            print(err)
        finally:
            que.task_done()


async def fetch_batch_urls(urls, n):
    que = asyncio.Queue()  # очередь для url
    sem = asyncio.Semaphore(n)  # семафор, который ограничивает количество параллельных задач
    workers = []  # список задач для обработки url
    async with sem:
        async with aiohttp.ClientSession() as session:
            # Создаем задачу для чтения url из файла
            read_url = asyncio.create_task(reader(urls, que))

            # Создаем рабочие задачи для обработки url
            for _ in range(n):
                workers.append(asyncio.create_task(fetch_worker(que, session)))

            # Ожидаем завершения чтения url
            await read_url

            # Ожидаем обработку всех url
            await que.join()

            # Завершаем работу всех задач
            for wrk in workers:
                wrk.cancel()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=int, help='Количество одновременных запросов.')
    parser.add_argument('urls', type=str, help='Файл с URL-адресами.')
    args = parser.parse_args()
    asyncio.run(fetch_batch_urls(args.urls, args.c))
