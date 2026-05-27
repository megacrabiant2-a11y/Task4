import time
import json
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Сбрасываем старый ключ скоростного слоя
r.delete("lambda_speed_counts")
last_id = '$'  # Читать только новые сообщения, пришедшие после старта

print("⏱️ Lambda SPEED слой запущен и слушает поток...")

try:
    while True:
        # Блокирующее чтение новых элементов из стрима (ожидание до 1 сек)
        events = r.xread({"book_views": last_id}, count=10, block=1000)
        
        for stream, messages in events:
            for msg_id, data in messages:
                event = json.loads(data["json"])
                book = event["book"]
                
                # Инкрементируем просмотры в быстром in-memory хранилище Redis
                r.hincrby("lambda_speed_counts", book, 1)
                print(f"[Speed Layer] Мгновенно учтен просмотр книги: {book}")
                
                last_id = msg_id
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n🛑 Speed слой остановлен.")
