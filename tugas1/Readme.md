# Meme viewer app
Jadi ini merupakan service lucu lucuan yang bisa menampilkan meme secara random yang akan di refresh setiap 10 detik.

<img width="1917" height="957" alt="image" src="https://github.com/user-attachments/assets/29096d61-2281-4d26-a90c-09fa190830ce" />


## Penjelasan Endpoint Health

Jadi untuk mengakses endpoint health, hanya tinggal mengetikkan path /health dibelakang url

<img width="757" height="240" alt="image" src="https://github.com/user-attachments/assets/06b951ee-e863-452b-ac76-e205d2ef8889" />


## Setup

```
  git clone https://github.com/yatopppi/lab-ncc.git
  cd lab-ncc/tugas1
  sudo docker compose up -d --build 
```

## Penjelasan proses build dan run Docker

Ketika menjalankan ` docker compose up -d --build ` maka file docker compose akan dijalankan, membuat sebuah image dan membuat container baru. File yang digunakan saat build image adalah file `Dockerfile`, `requirements.txt`, `app.py`, folder `templates`, dan `static`.

Disini saya membuat 2 stage.
Stage Builder dan stage final, walau sebenarnya dalam aplikasi yang saya buat multi stage ini tidak terlalu dibutuhkan karena aplikasi saya sederhana. Namun tetap saya buat untuk best practice.

### Stage Builder
```
FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

```
Disini menggunakan base image dari python. Setelah itu, working directory diatur ke `/app` agar semua proses berikutnya dijalankan dari folder tersebut.

Kemudian saya menambahkan environment variable `PYTHONDONTWRITEBYTECODE=1` agar Python tidak membuat file cache seperti .pyc, serta `PYTHONUNBUFFERED=1` agar output log Python langsung muncul tanpa buffering. saya membuat virtual environment di `/opt/venv`, kemudian menginstall dependency yang digunakan dalam projek tersebut, dependency didapat dari `requirements.txt`. 

### Stage Final

```
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY app.py .
COPY templates ./templates
COPY static ./static

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')" || exit 1


CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

```

Kemudian untuk stage final, menggunakan base image python lalu menambahkan environtment variable. Selanjutnya saya menyalin virtual environment hasil builder ke final stage menambahkanya ke environtment. Setelah itu mengcopy file yang diperlukan untuk menjalankan web seperti `app.py` isi template -> `index.html` dan isi static -> `style.css`.

Expose 5000 untuk mendeklarasikan port yang digunakan container dan melakukan `Healthcheck`. terakhir menjalankanya degnan gunicorn

### cek endpoint 
```
  http://103.93.129.221:5000/
  http://103.93.129.221:5000/health
```

### matiin

```
  sudo docker compose down
```
