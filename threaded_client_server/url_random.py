import requests
from bs4 import BeautifulSoup


def scrape_links(url, limit=100):
    urls = set()  # Используем set, чтобы избежать дубликатов
    to_visit = [url]  # Начальная очередь для посещения страниц

    while to_visit and len(urls) < limit:
        current_url = to_visit.pop(0)  # Берем первую ссылку из очереди

        try:
            response = requests.get(current_url)
            response.raise_for_status()  # Проверяем наличие ошибок
        except requests.RequestException as e:
            print(f"Ошибка при запросе {current_url}: {e}")
            continue  # Переходим к следующей ссылке в очереди

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ищем все теги <a> с атрибутом href
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Проверяем, что это абсолютный URL
            if href.startswith("http") and href not in urls:
                urls.add(href)
                to_visit.append(href)  # Добавляем новую ссылку в очередь
            # Если достигли лимита, прекращаем сбор
            if len(urls) >= limit:
                break

    return urls

# Пример использования функции
start_url = "https://en.wikipedia.org/"  # Укажите начальную страницу для сбора ссылок
collected_urls = scrape_links(start_url)

# Сохраняем в файл
with open("urls3.txt", "w") as f:
    for url in collected_urls:
        f.write(url + "\n")

print(f"Собрано ссылок: {len(collected_urls)}")

