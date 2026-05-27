import time
import random
import json
from datetime import datetime
import redis

# Подключение к Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

BOOKS = ["1984", "The Hobbit", "Fahrenheit 451", "Dune", "Clean Code"]
USERS = [f"user_{i}" for i in range(1, 20)]

print("🚀 Генератор логов запущен. Нажмите Ctrl+C для остановки.")

try:
    with open("data/raw_logs.txt", "a", encoding="utf-8") as f:
        while True:
            event = {
                "user": random.choice(USERS),
                "book": random.choice(BOOKS),
                "timestamp": datetime.now().isoformat()
            }
            
            # 1. Отправка в Kappa/Lambda Speed (Поток)
            r.xadd("book_views", {"json": json.dumps(event)})
            
            # 2. Запись в файл для Lambda Batch (Пакет)
            f.write(json.dumps(event) + "\n")
            f.flush()
            
            print(f"🔥 Отправлено событие: {event['user']} посмотрел '{event['book']}'")
            time.sleep(random.uniform(0.2, 0.8)) # Случайная задержка до 1 сек
except KeyboardInterrupt:
    print("\n🛑 Генератор остановлен.")
