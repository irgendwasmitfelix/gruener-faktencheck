import requests, logging
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime

def get_date_from_meta(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Prüfen auf alternative Meta-Tags
        meta_tags = [
            {"property": "og:updated_time"},
            {"property": "article:published_time"},
            {"name": "date"},
            {"name": "publish-date"},
            {"name": "dcterms.date"},
        ]
        
        for tag in meta_tags:
            meta = soup.find("meta", tag)
            if meta and meta.get("content"):
                return meta.get("content")
            
        time_tag = soup.find("time")
        if time_tag and time_tag.get("datetime"):
            return time_tag.get("datetime")
        elif time_tag:
            return time_tag.text.strip()
        
        logging.warning("Kein Datum gefunden in Meta-Tags.")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Fehler beim Abrufen der URL: {e}")
        return None

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gruener_faktencheck"
    )

def get_articles():
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.name, a.title, a.url, a.published_date 
            FROM categories c 
            LEFT JOIN articles a ON c.id = a.category_id 
            ORDER BY c.name, a.published_date DESC
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def add_article(category_id, title, url):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        published_date = get_date_from_meta(url)
        
        sql = """
        INSERT INTO articles (category_id, title, url, published_date) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (category_id, title, url, published_date))
        conn.commit()
        
        logging.info(f"Added article: {title}")
    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

def add_category(name):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO categories (name) VALUES (%s)"
        cursor.execute(sql, (name,))
        conn.commit()
        
        logging.info(f"Added category: {name}")
        return cursor.lastrowid
    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_categories():
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM categories ORDER BY name")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
