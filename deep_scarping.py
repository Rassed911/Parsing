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
for page in range(1, 6):
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

        # --- НОВЫЙ БЛОК ГЛУБОКОГО ПАРСИНГА ---
        link = book.h3.a['href']
        clean_link = link.replace('../../../', '').replace('catalogue/', '')
        book_url = f"http://books.toscrape.com/catalogue/{clean_link}"
        
        print(f"  Заходим внутрь: {book_url}")
        
        book_resp = requests.get(book_url)
        book_soup = BeautifulSoup(book_resp.text, 'html.parser')
        
        # Ищем описание
        # Оно обычно находится в первом теге <p>, у которого НЕТ никаких классов, 
        # внутри блока с описанием товара.
        description_tag = book_soup.find('article', class_='product_page').find('p', recursive=False)
        # Если find не сработал так, попробуем через поиск заголовка:
        if not description_tag:
             description_tag = book_soup.find('div', id='product_description').find_next_sibling('p')
        
        description = description_tag.text if description_tag else "No description"
        all_data.append({
            'title': title, 
            'price': price_clean, 
            'rating_word': current_rating,
            'description': description 
        })
   
    time.sleep(1)

df = pd.DataFrame(all_data)
df['rating_num'] = df['rating_word'].map(rating_map)
print(f"Всего собрано книг: {len(df)}")

##Работа с sql
import sqlite3
conn = sqlite3.connect('books_store.db')
df.to_sql('books', conn, if_exists='replace', index=False)
print("--- АНАЛИЗ ДАННЫХ ЧЕРЕЗ SQL ЗАПРОСЫ ---")

# ЗАДАЧА 1: Средняя цена книг для каждого рейтинга
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
#Задача 4 находим книги в описании которых есть слово world 
query4 = "SELECT title FROM books WHERE description LIKE '%world%'"
res4 = pd.read_sql(query4,conn)
print("\n4. Книги в которых есть слово world: ")
print(res4)

conn.close()