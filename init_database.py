import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

load_dotenv()


def create_database():
    """Создает базу данных если она не существует"""
    try:
        print("🔄 Попытка создания базы данных...")

        # Подключение к дефолтной БД postgres
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASS', '1234'),
            database='postgres'
        )
        conn.autocommit = True
        cursor = conn.cursor()

        db_name = os.getenv('DB_NAME', 'fastapi_db')

        # Проверяем существование БД
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))

        if not cursor.fetchone():
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"✅ База данных '{db_name}' создана успешно")
        else:
            print(f"✅ База данных '{db_name}' уже существует")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Ошибка при создании базы данных: {e}")
        print("\n💡 Возможные решения:")
        print("1. Убедитесь, что PostgreSQL запущен")
        print("2. Проверьте правильность пароля в .env файле")
        print("3. Попробуйте пустой пароль если использовали Homebrew")
        return False


if __name__ == "__main__":
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден! Создайте его с настройками БД")
        sys.exit(1)

    create_database()
    print("\n🎉 Инициализация завершена! Запускайте сервер:")
    print("uvicorn app.main:app --reload")