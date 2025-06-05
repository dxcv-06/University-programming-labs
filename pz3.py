import sqlite3
import datetime
from typing import List, Dict, Optional

# Адаптери для datetime для сумісності з Python 3.12+
def adapt_datetime(dt):
    """Конвертує datetime в строку для SQLite"""
    return dt.isoformat()

def convert_datetime(val):
    """Конвертує строку з SQLite назад в datetime"""
    return datetime.datetime.fromisoformat(val.decode())

# Реєстрація адаптерів
sqlite3.register_adapter(datetime.datetime, adapt_datetime)
sqlite3.register_converter("DATETIME", convert_datetime)

class SecurityEventLogger:
    """Система логування подій безпеки з SQLite базою даних"""
    
    def __init__(self, db_path: str = "security_events.db"):
        self.db_path = db_path
        self.init_database()
        self.populate_initial_data()
    
    def init_database(self):
        """Ініціалізація бази даних та створення таблиць"""
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        
        # Увімкнення підтримки зовнішніх ключів
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Створення таблиці EventSources
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS EventSources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                location TEXT NOT NULL,
                type TEXT NOT NULL
            )
        """)
        
        # Створення таблиці EventTypes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS EventTypes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_name TEXT UNIQUE NOT NULL,
                severity TEXT NOT NULL
            )
        """)
        
        # Створення таблиці SecurityEvents
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS SecurityEvents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                source_id INTEGER NOT NULL,
                event_type_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                ip_address TEXT,
                username TEXT,
                FOREIGN KEY (source_id) REFERENCES EventSources(id),
                FOREIGN KEY (event_type_id) REFERENCES EventTypes(id)
            )
        """)
        
        conn.commit()
        conn.close()
        print("База даних ініціалізована успішно!")
    
    def populate_initial_data(self):
        """Заповнення початкових даних"""
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        
        # Перевіряємо, чи вже є дані
        cursor.execute("SELECT COUNT(*) FROM EventTypes")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Додавання типів подій
        event_types = [
            ("Login Success", "Informational"),
            ("Login Failed", "Warning"),
            ("Port Scan Detected", "Warning"),
            ("Malware Alert", "Critical")
        ]
        
        cursor.executemany("""
            INSERT INTO EventTypes (type_name, severity) VALUES (?, ?)
        """, event_types)
        
        # Додавання джерел подій
        event_sources = [
            ("Firewall_A", "192.168.1.1", "Firewall"),
            ("Web_Server_Logs", "192.168.1.10", "Web Server"),
            ("IDS_Sensor_B", "192.168.1.5", "IDS"),
            ("Domain_Controller", "192.168.1.100", "Active Directory"),
            ("Mail_Server", "192.168.1.20", "Email Server")
        ]
        
        cursor.executemany("""
            INSERT INTO EventSources (name, location, type) VALUES (?, ?, ?)
        """, event_sources)
        
        # Додавання тестових подій
        test_events = [
            (datetime.datetime.now() - datetime.timedelta(hours=2), 1, 2, "Failed login attempt from suspicious IP", "10.0.0.100", "admin"),
            (datetime.datetime.now() - datetime.timedelta(hours=1), 2, 1, "User successfully logged in", "192.168.1.50", "user1"),
            (datetime.datetime.now() - datetime.timedelta(minutes=30), 3, 3, "Port scan detected from external IP", "203.0.113.10", None),
            (datetime.datetime.now() - datetime.timedelta(minutes=15), 1, 2, "Multiple failed login attempts", "10.0.0.100", "admin"),
            (datetime.datetime.now() - datetime.timedelta(minutes=10), 4, 4, "Malware detected in email attachment", "192.168.1.30", "user2"),
            (datetime.datetime.now() - datetime.timedelta(hours=3), 1, 2, "Brute force attack detected", "10.0.0.100", "root"),
            (datetime.datetime.now() - datetime.timedelta(hours=4), 1, 2, "Failed login attempt", "10.0.0.100", "admin"),
            (datetime.datetime.now() - datetime.timedelta(hours=5), 1, 2, "Authentication failure", "10.0.0.100", "administrator"),
            (datetime.datetime.now() - datetime.timedelta(hours=6), 1, 2, "Invalid credentials provided", "10.0.0.100", "admin"),
            (datetime.datetime.now() - datetime.timedelta(days=1), 3, 4, "Critical vulnerability exploit attempt", "198.51.100.5", None),
            (datetime.datetime.now() - datetime.timedelta(days=2), 5, 4, "Suspicious email activity detected", "192.168.1.25", "user3"),
            (datetime.datetime.now() - datetime.timedelta(days=3), 2, 1, "User logout successful", "192.168.1.60", "user4")
        ]
        
        cursor.executemany("""
            INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, test_events)
        
        conn.commit()
        conn.close()
        print("Початкові дані додані успішно!")
    
    def register_event_source(self, name: str, location: str, type: str) -> bool:
        """Функція для реєстрації нового джерела подій"""
        try:
            conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO EventSources (name, location, type) VALUES (?, ?, ?)
            """, (name, location, type))
            
            conn.commit()
            conn.close()
            print(f"Джерело подій '{name}' зареєстровано успішно!")
            return True
        except sqlite3.IntegrityError:
            print(f"Помилка: Джерело '{name}' вже існує!")
            return False
        except Exception as e:
            print(f"Помилка при реєстрації джерела: {e}")
            return False
    
    def register_event_type(self, type_name: str, severity: str) -> bool:
        """Функція для реєстрації нового типу подій"""
        try:
            conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO EventTypes (type_name, severity) VALUES (?, ?)
            """, (type_name, severity))
            
            conn.commit()
            conn.close()
            print(f"Тип події '{type_name}' зареєстровано успішно!")
            return True
        except sqlite3.IntegrityError:
            print(f"Помилка: Тип події '{type_name}' вже існує!")
            return False
        except Exception as e:
            print(f"Помилка при реєстрації типу події: {e}")
            return False
    
    def log_security_event(self, source_name: str, event_type_name: str, 
                          message: str, ip_address: str = None, username: str = None) -> bool:
        """Функція для запису нової події безпеки"""
        try:
            conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
            cursor = conn.cursor()
            
            # Отримання ID джерела
            cursor.execute("SELECT id FROM EventSources WHERE name = ?", (source_name,))
            source_result = cursor.fetchone()
            if not source_result:
                print(f"Помилка: Джерело '{source_name}' не знайдено!")
                return False
            source_id = source_result[0]
            
            # Отримання ID типу події
            cursor.execute("SELECT id FROM EventTypes WHERE type_name = ?", (event_type_name,))
            type_result = cursor.fetchone()
            if not type_result:
                print(f"Помилка: Тип події '{event_type_name}' не знайдено!")
                return False
            event_type_id = type_result[0]
            
            # Запис події з поточним часом
            timestamp = datetime.datetime.now()
            cursor.execute("""
                INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (timestamp, source_id, event_type_id, message, ip_address, username))
            
            conn.commit()
            conn.close()
            print(f"Подія безпеки записана успішно! ID: {cursor.lastrowid}")
            return True
        except Exception as e:
            print(f"Помилка при записі події: {e}")
            return False
    
    def get_failed_logins_24h(self) -> List[Dict]:
        """Отримати всі події 'Login Failed' за останні 24 години"""
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        
        twenty_four_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=24)
        
        cursor.execute("""
            SELECT se.timestamp, es.name, se.message, se.ip_address, se.username
            FROM SecurityEvents se
            JOIN EventSources es ON se.source_id = es.id
            JOIN EventTypes et ON se.event_type_id = et.id
            WHERE et.type_name = 'Login Failed' AND se.timestamp >= ?
            ORDER BY se.timestamp DESC
        """, (twenty_four_hours_ago,))
        
        results = cursor.fetchall()
        conn.close()
        
        events = []
        for row in results:
            events.append({
                'timestamp': row[0],
                'source': row[1],
                'message': row[2],
                'ip_address': row[3],
                'username': row[4]
            })
        
        return events
    
    def detect_brute_force_attacks(self) -> List[Dict]:
        """Виявити IP-адреси з більше ніж 5 невдалих спроб входу за 1 годину"""
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        
        one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
        
        cursor.execute("""
            SELECT se.ip_address, COUNT(*) as failed_attempts
            FROM SecurityEvents se
            JOIN EventTypes et ON se.event_type_id = et.id
            WHERE et.type_name = 'Login Failed' 
            AND se.timestamp >= ? 
            AND se.ip_address IS NOT NULL
            GROUP BY se.ip_address
            HAVING COUNT(*) > 5
            ORDER BY failed_attempts DESC
        """, (one_hour_ago,))
        
        results = cursor.fetchall()
        conn.close()
        
        attacks = []
        for row in results:
            attacks.append({
                'ip_address': row[0],
                'failed_attempts': row[1]
            })
        
        return attacks
    
    def get_critical_events_week(self) -> List[Dict]:
        """Отримати всі події з рівнем серйозності 'Critical' за останній тиждень"""
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        
        week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        
        cursor.execute("""
            SELECT es.name as source_name, se.timestamp, se.message, se.ip_address, se.username
            FROM SecurityEvents se
            JOIN EventSources es ON se.source_id = es.id
            JOIN EventTypes et ON se.event_type_id = et.id
            WHERE et.severity = 'Critical' AND se.timestamp >= ?
            ORDER BY es.name, se.timestamp DESC
        """, (week_ago,))
        
        results = cursor.fetchall()
        conn.close()
        
        events = []
        for row in results:
            events.append({
                'source_name': row[0],
                'timestamp': row[1],
                'message': row[2],
                'ip_address': row[3],
                'username': row[4]
            })
        
        return events
    
    def search_events_by_keyword(self, keyword: str) -> List[Dict]:
        """Знайти всі події, що містять певне ключове слово у повідомленні"""
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT se.timestamp, es.name, et.type_name, se.message, se.ip_address, se.username
            FROM SecurityEvents se
            JOIN EventSources es ON se.source_id = es.id
            JOIN EventTypes et ON se.event_type_id = et.id
            WHERE se.message LIKE ?
            ORDER BY se.timestamp DESC
        """, (f'%{keyword}%',))
        
        results = cursor.fetchall()
        conn.close()
        
        events = []
        for row in results:
            events.append({
                'timestamp': row[0],
                'source_name': row[1],
                'event_type': row[2],
                'message': row[3],
                'ip_address': row[4],
                'username': row[5]
            })
        
        return events
    
    def display_statistics(self):
        """Відображення загальної статистики"""
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        
        # Загальна кількість подій
        cursor.execute("SELECT COUNT(*) FROM SecurityEvents")
        total_events = cursor.fetchone()[0]
        
        # Події за типами
        cursor.execute("""
            SELECT et.type_name, COUNT(*) as count
            FROM SecurityEvents se
            JOIN EventTypes et ON se.event_type_id = et.id
            GROUP BY et.type_name
            ORDER BY count DESC
        """)
        events_by_type = cursor.fetchall()
        
        # Події за джерелами
        cursor.execute("""
            SELECT es.name, COUNT(*) as count
            FROM SecurityEvents se
            JOIN EventSources es ON se.source_id = es.id
            GROUP BY es.name
            ORDER BY count DESC
        """)
        events_by_source = cursor.fetchall()
        
        conn.close()
        
        print("\n" + "="*50)
        print("СТАТИСТИКА ПОДІЙ БЕЗПЕКИ")
        print("="*50)
        print(f"Загальна кількість подій: {total_events}")
        
        print("\nПодії за типами:")
        print("-" * 30)
        for event_type, count in events_by_type:
            print(f"{event_type:<20}: {count}")
        
        print("\nПодії за джерелами:")
        print("-" * 30)
        for source, count in events_by_source:
            print(f"{source:<20}: {count}")

def interactive_menu():
    """Інтерактивне меню для роботи з системою логування"""
    logger = SecurityEventLogger()
    
    while True:
        print("\n" + "="*60)
        print("СИСТЕМА ЛОГУВАННЯ ПОДІЙ БЕЗПЕКИ")
        print("="*60)
        print("1. Зареєструвати нове джерело подій")
        print("2. Зареєструвати новий тип події")
        print("3. Записати нову подію безпеки")
        print("4. Переглянути невдалі входи за 24 години")
        print("5. Виявити атаки підбору пароля")
        print("6. Критичні події за тиждень")
        print("7. Пошук подій за ключовим словом")
        print("8. Статистика системи")
        print("9. Вихід")
        
        choice = input("\nОберіть опцію (1-9): ")
        
        if choice == "1":
            print("\nРеєстрація нового джерела подій:")
            name = input("Назва джерела: ")
            location = input("Місце розташування/IP: ")
            type_source = input("Тип джерела: ")
            logger.register_event_source(name, location, type_source)
            
        elif choice == "2":
            print("\nРеєстрація нового типу події:")
            type_name = input("Назва типу події: ")
            severity = input("Рівень серйозності (Informational/Warning/Critical): ")
            logger.register_event_type(type_name, severity)
            
        elif choice == "3":
            print("\nЗапис нової події безпеки:")
            source_name = input("Назва джерела: ")
            event_type_name = input("Тип події: ")
            message = input("Повідомлення: ")
            ip_address = input("IP-адреса (необов'язково): ") or None
            username = input("Ім'я користувача (необов'язково): ") or None
            logger.log_security_event(source_name, event_type_name, message, ip_address, username)
            
        elif choice == "4":
            events = logger.get_failed_logins_24h()
            print(f"\nНевдалі входи за останні 24 години ({len(events)} подій):")
            print("-" * 80)
            for event in events:
                print(f"{event['timestamp']} | {event['source']} | {event['ip_address']} | {event['username']}")
                
        elif choice == "5":
            attacks = logger.detect_brute_force_attacks()
            print(f"\nВиявлені атаки підбору пароля ({len(attacks)} IP-адрес):")
            print("-" * 40)
            for attack in attacks:
                print(f"IP: {attack['ip_address']} | Спроб: {attack['failed_attempts']}")
                
        elif choice == "6":
            events = logger.get_critical_events_week()
            print(f"\nКритичні події за тиждень ({len(events)} подій):")
            print("-" * 80)
            for event in events:
                print(f"{event['timestamp']} | {event['source_name']} | {event['message']}")
                
        elif choice == "7":
            keyword = input("\nВведіть ключове слово для пошуку: ")
            events = logger.search_events_by_keyword(keyword)
            print(f"\nЗнайдено подій з '{keyword}': {len(events)}")
            print("-" * 80)
            for event in events:
                print(f"{event['timestamp']} | {event['source_name']} | {event['event_type']}")
                print(f"   {event['message']}")
                
        elif choice == "8":
            logger.display_statistics()
            
        elif choice == "9":
            print("До побачення!")
            break
            
        else:
            print("Невірний вибір! Спробуйте ще раз.")

if __name__ == "__main__":
    print("Ініціалізація системи логування подій безпеки...")
    interactive_menu()
