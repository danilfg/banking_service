FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY services/customer/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY services/customer/app ./app
COPY shared ./shared

EXPOSE 8002

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
