import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Для примера парсим демо-сайт (книжный магазин)
URL = "http://books.toscrape.com/catalogue/page-1.html"

def parse_books():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при подключении к сайту: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ищем все книги на странице
    books = soup.find_all('article', class_='product_pod')
    
    data = []
    
    for book in books:
        title = book.find('h3').find('a')['title']
        
        price_text = book.find('p', class_='price_color').text
        price = float(price_text.replace('£', '').replace('Â', ''))
        
        rating_class = book.find('p', class_='star-rating')['class']
        rating = rating_class[1]
        
        availability = book.find('p', class_='instock availability').text.strip()
        
        data.append({
            'Название': title,
            'Цена (GBP)': price,
            'Рейтинг': rating,
            'Наличие': availability
        })
        
        # Пауза, чтобы не спамить сервер
        time.sleep(0.5)
    
    # Сохраняем в Excel
    df = pd.DataFrame(data)
    df.to_excel('books_parsed.xlsx', index=False)
    
    print(f"Готово! Собрано {len(data)} записей. Данные сохранены в файл 'books_parsed.xlsx'")

if __name__ == '__main__':
    parse_books()
