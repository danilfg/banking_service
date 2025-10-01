FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY services/contracts/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY services/contracts/app ./app
COPY shared ./shared

EXPOSE 8008

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8008"]
