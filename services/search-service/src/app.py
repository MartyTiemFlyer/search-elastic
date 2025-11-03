import time
import sys
import os
from elasticsearch import Elasticsearch

print("🚀 Search Service STARTED!", flush=True)

es_url = os.getenv('ELASTICSEARCH_URL', 'http://elasticsearch:9200')
print(f"🔗 Connecting to: {es_url}", flush=True)

max_retries = 10
retry_delay = 5

for attempt in range(max_retries):
    try:
        print(f"🔄 Attempt {attempt + 1}/{max_retries}...", flush=True)
        
        # Пробуем разные настройки клиента
        es = Elasticsearch(
            es_url,
            request_timeout=30,
            max_retries=3,
            retry_on_timeout=True,
            verify_certs=False,  # отключаем проверку SSL
            ssl_show_warn=False
        )
        
        # Пробуем получить информацию вместо ping
        print("📡 Trying to get cluster info...", flush=True)
        info = es.info()
        print(f"🎉 SUCCESS: Connected to Elasticsearch!", flush=True)
        print(f"📊 Cluster: {info['cluster_name']}", flush=True)
        print(f"🔧 Version: {info['version']['number']}", flush=True)
        break
        
    except Exception as e:
        print(f"❌ Attempt {attempt + 1} failed:", flush=True)
        print(f"   Error type: {type(e).__name__}", flush=True)
        print(f"   Error message: {e}", flush=True)
        
        # Детальная диагностика для распространенных ошибок
        if "ConnectionError" in str(type(e).__name__):
            print("   💡 This is a connection error - network issue", flush=True)
        elif "Authentication" in str(e):
            print("   💡 Authentication required - check security", flush=True)
        elif "SSL" in str(e):
            print("   💡 SSL certificate issue", flush=True)
    
    if attempt < max_retries - 1:
        print(f"⏳ Waiting {retry_delay} seconds...", flush=True)
        time.sleep(retry_delay)
else:
    print("💥 FATAL: Could not connect to Elasticsearch", flush=True)
    sys.exit(1)

print("🟢 ALL TESTS PASSED! Starting main loop...", flush=True)

# Основной цикл
counter = 0
while True:
    try:
        info = es.info()
        print(f"💚 Heartbeat #{counter} - Cluster: {info['cluster_name']}", flush=True)
        counter += 1
        time.sleep(5)
        
    except Exception as e:
        print(f"💔 Heartbeat #{counter} - ERROR: {e}", flush=True)
        counter += 1
        time.sleep(5)