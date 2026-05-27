import json
import os
import pandas as pd
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

print("💾 Lambda BATCH джоб запущен (Имитация периодического запуска)...")

if not os.path.exists("data/raw_logs.txt"):
    print("❌ Лог-файл пуст или не найден. Сначала запустите generator.py")
    exit()

# Читаем накопленные логи через Pandas
with open("data/raw_logs.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

records = [json.loads(line) for line in lines]
df = pd.DataFrame(records)

if df.empty:
    print("💤 Нет данных для обработки.")
else:
    # Группируем и агрегируем ВСЮ историю с абсолютной точностью
    batch_counts = df.groupby("book").size().to_dict()
    
    # Записываем эталонные результаты в финальный Serving Layer
    r.delete("lambda_serving_batch")
    for book, count in batch_counts.items():
        r.hset("lambda_serving_batch", book, count)
        
    print("\n📊 --- РЕЗУЛЬТАТЫ BATCH СЛОЯ (Эталонная точность) ---")
    print(batch_counts)
    print("---------------------------------------------------\n")
