# 📚 Web Scraping & Data Analysis: проект 1000 книг

### Описание проекта
Автоматизированный процесс сбора и анализа данных с сайта-каталога книг. 
Проект реализует полный цикл ETL (Extract, Transform, Load).

### Что было сделано:
1. **Scraping**: Написан парсер на `BeautifulSoup`, собирающий данные с 50 страниц (1000 книг).
2. **Data Cleaning**: Очищены цены от спецсимволов, категориальный рейтинг ("Three", "Four") преобразован в числовой формат.
3. **Storage**: Данные сохранены в реляционную базу данных **SQLite**.
4. **Analysis**: Проведен SQL-анализ (группировки, агрегации) и визуализация распределения цен.

### Стек технологий:
* Python (Requests, BeautifulSoup)
* Pandas (Data Processing)
* SQLite (Database)
* Matplotlib (Visualization)

### Как запустить:
1. `pip install -r requirements.txt`
2. Запустить `parsing1.py`