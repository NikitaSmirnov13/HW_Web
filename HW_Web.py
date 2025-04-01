import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# URL страницы с новыми статьями
url = 'https://habr.com/ru/articles/'

# Выполняем GET-запрос к странице
response = requests.get(url)

# Проверяем, что запрос успешен
if response.status_code == 200:
    # Парсим HTML-код страницы
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все статьи на странице
    articles = soup.find_all('article')

    # Проходим по каждой статье
    for article in articles:
        # Извлекаем заголовок статьи
        title_element = article.find('h2')
        if not title_element:
            continue  # Пропускаем, если нет заголовка
        title_link = title_element.find('a')
        if not title_link:
            continue  # Пропускаем, если нет ссылки
        title = title_link.text.strip()
        link = title_link['href']
        if not link.startswith('http'):
            link = 'https://habr.com' + link

        # Извлекаем дату публикации статьи
        time_element = article.find('time')
        if not time_element:
            continue  # Пропускаем, если нет даты
        date_str = time_element['datetime']
        date = datetime.fromisoformat(date_str)

        # Извлекаем текст превью статьи (может быть в разных местах)
        preview = ""
        preview_element = article.find('div', class_='article-formatted-body')  # Новый формат
        if preview_element:
            preview = preview_element.text.strip()
        else:
            # Если нет нового формата, пробуем старый (article-formatted-body_version-2)
            preview_element = article.find('div', class_='article-formatted-body_version-2')
            if preview_element:
                preview = preview_element.text.strip()
            else:
                # Если превью нет, можно проверить заголовок или пропустить статью
                continue  # Пропускаем, если нет превью

        # Проверяем, содержит ли превью или заголовок хотя бы одно из ключевых слов
        if any(
                keyword.lower() in (preview.lower() + title.lower())
                for keyword in KEYWORDS
        ):
            # Выводим информацию о статье в указанном формате
            print(f"{date.strftime('%Y-%m-%d')} – {title} – {link}")
else:
    print(f"Ошибка при запросе страницы: {response.status_code}")