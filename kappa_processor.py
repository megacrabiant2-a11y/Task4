import time
import json
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.delete("kappa_realtime_counts")

# Читаем стрим С САМОГО НАЧАЛА (ID: 0-0), симулируя полнуюKappa-архивацию
last_id = "0-0"

print("🌊 Единый конвейер KAPPA запущен (обрабатывает поток с нуля)...")

try:
    while True:
        events = r.xread({"book_views": last_id}, count=10, block=1000)
        
        for stream, messages in events:
            for msg_id, data in messages:
                event = json.loads(data["json"])
                book = event["book"]
                
                # Налету обновляет глобальный стейт
                r.hincrby("kappa_realtime_counts", book, 1)
                
                last_id = msg_id
                
        # Выводим текущее состояние Каппы в консоль
        current_state = r.hgetall("kappa_realtime_counts")
        if current_state:
            print(f"[Kappa Realtime State]: {current_state}")
            
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\n🛑 Kappa процессор остановлен.")
