import logging
from datetime import datetime
import pytz  # Import the pytz library
import psutil
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

# Inisialisasi koneksi ke Elasticsearch dengan SSL/HTTPS dan autentikasi
es = Elasticsearch(
    ['https://elk.adamrizqi.my.id:9200'],  # Ganti dengan alamat host dan port Elasticsearch Anda
    http_auth=('elastic', 'Indo@123'),  # Ganti dengan kredensial yang benar
    verify_certs=True,
)

# Inisialisasi logger
logger = logging.getLogger('port_status_logger')
logger.setLevel(logging.INFO)

# Membuat handler untuk menulis ke file log
log_file_path = 'port_status.log'
file_handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Membuat handler untuk menulis ke konsol
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Mendapatkan daftar port yang sedang aktif dalam rentang 1-65000
def get_active_ports():
    active_ports = []
    for conn in psutil.net_connections(kind='inet'):
        port = conn.laddr.port
        if 1 <= port <= 65000:
            active_ports.append(port)
    return active_ports

# Membuat log dan mengirimnya ke Elasticsearch serta menulis ke file log
def log_active_ports():
    active_ports = get_active_ports()
    
    # Set the timezone to Asia/Jakarta
    jakarta_timezone = pytz.timezone('Asia/Jakarta')
    timestamp = datetime.now(jakarta_timezone).strftime("%Y-%m-%dT%H:%M:%S%z")
    
    for port in active_ports:
        log_entry = {
            "@timestamp": timestamp,
            "port": port,
            "status": "active"
        }
        try:
            es.index(index='port_status', body=log_entry)
        except Exception as e:
            log_message = f"Failed to index data for port {port}: {e}"
            logger.error(log_message)

        # Menulis log ke file .log
        log_message = f"Port {port} is active at {timestamp}"
        logger.info(log_message)

# Mengecek log dari Elasticsearch
def check_elasticsearch_logs():
    query = {
        "query": {
            "match_all": {}
        }
    }
    try:
        results = scan(es, query=query, index="port_status")
        for result in results:
            print(result['_source'])
    except Exception as e:
        log_message = f"Failed to retrieve Elasticsearch logs: {e}"
        logger.error(log_message)

# Menjalankan fungsi untuk membuat log dan mengirimnya ke Elasticsearch serta menulis ke file log
log_active_ports()

# Menjalankan fungsi untuk memeriksa log dari Elasticsearch
check_elasticsearch_logs()

