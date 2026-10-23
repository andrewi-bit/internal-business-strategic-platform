# Internal Business Strategic Platform

Fondasi backend/frontend untuk Internal Business Strategic Platform (IBSP), sebuah platform internal perusahaan yang dirancang untuk mengelola portofolio bisnis serta mendukung pengelolaan operasional bisnis secara terstruktur.

Pengembangan platform dilakukan secara bertahap, dimulai dari  **ase 1: Manajemen Portofolio (Portfolio Management).**.

---

## Teknologi Utama

- **Framework:** FastAPI (Python 3.12)
- **Database Relasional:** PostgreSQL 15
- **ORM:** SQLAlchemy 2.0 (Async)
- **Database Driver:** asyncpg
- **Database Migration:** Alembic
- **Configuration Management:** Pydantic Settings
- **ASGI Server:** Uvicorn
- **Containerization:** Docker & Docker Compose
- **Database Management:** pgAdmin

---

## Persyaratan Sistem (Prerequisites)

Pastikan aplikasi berikut sudah terinstal:

1. Git
2. Docker Desktop
3. Docker Compose

Python dan PostgreSQL tidak perlu diinstal secara lokal untuk menjalankan development environment melalui Docker.

---

## Struktur Proyek Utama

```text
internal-business-strategic-platform/
├── deploy/
│   ├── compose/
│   │   └── docker-compose.dev.yml
│   ├── docker/
│   │   └── backend.dev.Dockerfile
│   └── entrypoints/
│       └── api.sh
├── src/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   ├── config/
│   │   │   │   └── env/
│   │   │   ├── connections/
│   │   │   ├── core/
│   │   │   ├── lib/
│   │   │   ├── middleware/
│   │   │   ├── models/
│   │   │   ├── main.py
│   │   │   ├── migrate.py
│   │   │   └── settings.py
│   │   ├── db_migrations/
│   │   ├── tests/
│   │   ├── alembic.ini
│   │   └── pyproject.toml
│   └── frontend/
├── .gitattributes
├── .gitignore
└── README.md
```

---

## Cara Menjalankan Proyek di Lokal

### 1. Clone Repository

```bash
git clone <repository-url>
cd internal-business-strategic-platform
```

### 2. Konfigurasi Environment

Buat file `.env` di root repository untuk konfigurasi Docker Compose.

Gunakan `.env.example` sebagai referensi apabila file tersebut tersedia di root repository.

File konfigurasi aplikasi backend berada di:

```text
src/backend/app/config/env/
```

Salin `env.example` menjadi `development.env`, kemudian sesuaikan nilainya untuk development lokal.

Pastikan konfigurasi database aplikasi sesuai dengan konfigurasi PostgreSQL pada Docker Compose.

**Jangan commit file environment yang berisi credentials atau secrets.**

### 3. Jalankan Docker Environment

Jalankan dari root repository:

```bash
docker compose -f deploy/compose/docker-compose.dev.yml up --build -d
```

Periksa status container:

```bash
docker compose -f deploy/compose/docker-compose.dev.yml ps
```

### 4. Verifikasi Layanan
- **API Documentation (Swagger UI):** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **pgAdmin:** http://localhost:5050

---

## Manajemen Database (Alembic Migrations)

Database migration digunakan untuk mengelola perubahan struktur database secara terkontrol.

### 1. Konfigurasi Migration

File konfigurasi Alembic:

```text
src/backend/alembic.ini
```

Environment migration:

```text
src/backend/db_migrations/env.py
```

### 2. Membuat Migration Baru

Setelah model SQLAlchemy dibuat atau diubah, jalankan:

```bash
docker compose -f deploy/compose/docker-compose.dev.yml exec api alembic revision --autogenerate -m "describe_your_change"
```

Pastikan model sudah diimpor ke metadata Alembic dan periksa isi migration yang dihasilkan sebelum diterapkan.

### 3. Menerapkan Migration

```bash
docker compose -f deploy/compose/docker-compose.dev.yml exec api alembic upgrade head
```

### 4. Rollback Migration Terakhir

```bash
docker compose -f deploy/compose/docker-compose.dev.yml exec api alembic downgrade -1
```

---

## Perintah Operasional Docker

**Melihat log backend:**

```bash
docker compose -f deploy/compose/docker-compose.dev.yml logs -f api
```

**Restart backend:**

```bash
docker compose -f deploy/compose/docker-compose.dev.yml restart api
```

**Menghentikan seluruh container:**

```bash
docker compose -f deploy/compose/docker-compose.dev.yml down
```

**Menghentikan container dan menghapus volume database:**

```bash
docker compose -f deploy/compose/docker-compose.dev.yml down -v
```

> **Peringatan:** Perintah `down -v` menghapus volume persisten yang dikelola oleh Compose, termasuk data PostgreSQL lokal. Gunakan dengan hati-hati.
