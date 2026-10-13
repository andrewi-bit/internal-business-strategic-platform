
#!/bin/sh
set -e

MAX_RETRIES=30
RETRY_INTERVAL=2
retries=0

echo "Waiting for database..."

until python -c "
import socket
import sys

try:
    with socket.create_connection(('db', 5432), timeout=1):
        sys.exit(0)
except OSError:
    sys.exit(1)
" 2>/dev/null; do
    retries=$((retries + 1))

    if [ "$retries" -ge "$MAX_RETRIES" ]; then
        echo "ERROR: Database belum siap setelah ${MAX_RETRIES} percobaan."
        exit 1
    fi

    echo "Database belum siap, mencoba lagi (${retries}/${MAX_RETRIES})..."
    sleep "$RETRY_INTERVAL"
done

echo "Database ready!"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
