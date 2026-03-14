# 📚 Web Scraping & Data Analysis.

### Описание проекта
Автоматизированный процесс сбора и анализа данных с сайта-каталога книг. 
Проект реализует полный цикл ETL (Extract, Transform, Load).

### Что было сделано:
1. **Scraping**: Написан парсер на `BeautifulSoup`, собирающий данные с 50 страниц (1000 книг).
2. **Data Cleaning**: Очищены цены от спецсимволов, категориальный рейтинг ("Three", "Four") преобразован в числовой формат.
3. **Storage**: Данные сохранены в реляционную базу данных **SQLite**.
4. **Analysis**: Проведен SQL-анализ (группировки, агрегации) и визуализация распределения цен.
5. **Догружен `deep_scarping.py`**: реализованы сложные запросы `requests` внутри `requests`.

### Стек технологий:
* Python (Requests, BeautifulSoup)
* Pandas (Data Processing)
* SQLite (Database)
* Matplotlib (Visualization)

### Как запустить:
1. `pip install -r requirements.txt`
2. Запустить 'parsing1.py' либо запустить `deep_scarping.py`

### Вложенные файлы:
1. Прилагается файл `plot.png` - распределение цен на книги для файла `parsing.py`
2. Прилагается файл `sql.png` - первые несколько строк из базый данных файла `deep_scarpinh.py`
