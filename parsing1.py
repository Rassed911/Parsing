import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

rating_map = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}

all_data = []
for page in range(1, 51):
    url = f"http://books.toscrape.com/catalogue/page-{page}.html" 
    print(f"Парсим страницу: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    print(f"Найдено книг: {len(books)}")

    for book in books:
        title = book.h3.a['title']
        price_raw = book.find('p', class_='price_color').text
        price_clean = float(price_raw.replace('Â£', '').replace('£', ''))
        rating_tag = book.find('p', class_='star-rating')
        current_rating = rating_tag['class'][1] 
        all_data.append({'title': title, 'price': price_clean, 'rating_word': current_rating})
    time.sleep(1)


df = pd.DataFrame(all_data)
df['rating_num'] = df['rating_word'].map(rating_map)
print(f"Всего собрано книг: {len(df)}")

## Визуализация данных
import matplotlib.pyplot as plt

# Рисуем гистограмму цен
plt.figure(figsize=(10, 6)) # Размер картинки
plt.hist(df['price'], bins=20, color='skyblue', edgecolor='black')

plt.title('Распределение цен на книги')
plt.xlabel('Цена (£)')
plt.ylabel('Количество книг')
plt.grid(axis='y', alpha=0.75)
plt.show()

import sqlite3
#подключаемся к нашей базе
conn = sqlite3.connect('books_store.db')

query1 = """
SELECT rating_num, AVG(price) as average_price 
FROM books
GROUP BY rating_num
ORDER BY rating_num DESC
"""
res1 = pd.read_sql(query1, conn)
print("\n1. Средняя цена по рейтингам:")
print(res1)

# ЗАДАЧА 2: Сколько книг имеют рейтинг 5 звезд?
query2 = "SELECT COUNT(*) as count_5_stars FROM books WHERE rating_num = 5"
res2 = pd.read_sql(query2, conn)
print("\n2. Количество книг с рейтингом 5:")
print(res2)

# ЗАДАЧА 3: Самые элитные книги (Цена > 55 и Рейтинг = 5)
query3 = "SELECT title, price FROM books WHERE price > 55 AND rating_num = 5"
res3 = pd.read_sql(query3, conn)
print("\n3. Элитные книги (Цена > 55 и 5 звезд):")
print(res3)

conn.close()