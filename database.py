import sqlite3
from datetime import datetime

class BibleReadingDB:
    def __init__(self):
        self.conn = sqlite3.connect('bible_reading.db', check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                date TEXT,
                month TEXT,
                at_progress INTEGER,
                nt_progress INTEGER,
                salmos_progress INTEGER,
                proverbios_progress INTEGER,
                daily_completed BOOLEAN,
                PRIMARY KEY (date)
            )
        ''')
        self.conn.commit()

    def save_progress(self, month, at_progress, nt_progress, salmos_progress, proverbios_progress, daily_completed):
        cursor = self.conn.cursor()
        date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT OR REPLACE INTO progress 
            (date, month, at_progress, nt_progress, salmos_progress, proverbios_progress, daily_completed)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (date, month, at_progress, nt_progress, salmos_progress, proverbios_progress, daily_completed))
        self.conn.commit()

    def get_progress(self, month):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT at_progress, nt_progress, salmos_progress, proverbios_progress, daily_completed
            FROM progress
            WHERE month = ?
            ORDER BY date DESC
            LIMIT 1
        ''', (month,))
        result = cursor.fetchone()
        if result:
            return {
                'AT': result[0],
                'NT': result[1],
                'Salmos': result[2],
                'Proverbios': result[3],
                'Daily': result[4]
            }
        return None
