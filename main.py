import requests
from bs4 import BeautifulSoup

# Список ключевых слов для поиска
KEYWORDS = ['google', '1911']

# URL страницы со свежими статьями
URL = "https://habr.com/ru/articles/"

# Получаем страницу
response = requests.get(URL)
response.raise_for_status()

# Парсим страницу
soup = BeautifulSoup(response.text, 'html.parser')

# Находим все статьи на странице
articles = soup.find_all('article')

# Проходимся по всем статьям
for article in articles:
    # Ищем заголовок и ссылку на статью
    title_element = article.find('h2')
    if title_element:
        title = title_element.text.strip()
        href = title_element.find('a')['href']
        link = f"https://habr.com{href}"
    else:
        continue

    # Загружаем страницу статьи
    article_response = requests.get(link)
    article_response.raise_for_status()

    # Парсим страницу статьи
    article_soup = BeautifulSoup(article_response.text, 'html.parser')

    # Получаем весь текст статьи
    article_text = article_soup.get_text().lower()

    # Проверяем наличие любого из ключевых слов в тексте статьи
    if any(keyword.lower() in article_text for keyword in KEYWORDS):
        # Извлекаем дату публикации
        date_element = article.find('time')
        if date_element:
            date = date_element['title']
        else:
            date = "Дата не найдена"

        # Выводим результат в формате <дата> – <заголовок> – <ссылка>
        print(f"{date} – {title} – {link}")
