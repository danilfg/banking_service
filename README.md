# Banking Service Platform

Учебная реализация микросервисного банковского комплекса. Проект демонстрирует архитектуру "banking-as-a-service" с модульным backend на FastAPI, SPA-интерфейсом на Next.js и инфраструктурой из PostgreSQL, Redis, Kafka и Splunk.

## Архитектура

- **Gateway** — единая точка входа, JWT-аутентификация, маршрутизация и проксирование REST-запросов к доменным сервисам.
- **Auth, Customer, Office, Accounts, Ledger, FX, Utilities, Contracts, Notifications** — изолированные FastAPI-сервисы с собственными схемами БД.
- **Frontend** — SSR/SPA на Next.js, маршруты `/banking-service/*` для лендинга, клиентского и офисного кабинетов, витрины курсов.
- **Infra** — PostgreSQL (per-service), Redis (кеш курсов, rate-limit), Kafka (event-driven интеграции и логи), Splunk (через Kafka topic `logs.app`).

Подробное описание компонентов и потоков: `docs/ARCHITECTURE.md`.

## Статус

- [x] Каркасы FastAPI-сервисов, API Gateway с проксированием
- [x] Заглушечные REST-эндпоинты и схемы данных
- [x] Next.js UI с основными экранами (лендинг, ЛК клиента, ЛК офиса, курсы валют)
- [x] Docker Compose инфраструктура (PostgreSQL, Redis, Kafka, Splunk, Redis Commander)
- [ ] Реальный persistence/ORM и миграции
- [ ] Интеграция Kafka, Redis, Frankfurter API
- [ ] Аутентификация, refresh, MFA
- [ ] Тесты (pytest, Playwright), CI/CD

## Развёртывание

### Вариант 1. Docker Compose (полное окружение)

1. Установите Docker Desktop ≥ 4.0 с поддержкой Compose v2 (`docker compose version`).
2. При необходимости скорректируйте переменные в `infra/env/*.env` (учебные секреты `dev-secret`, подключения к Postgres/Redis/Kafka и т.д.).
3. Соберите и поднимите инфраструктуру:
   ```bash
   cd infra
   docker compose up --build
   ```
   Добавьте ключ `-d`, чтобы запускать в фоне.
4. Дождитесь готовности контейнеров и проверьте health-check'и:
   ```bash
   docker compose ps
   curl http://localhost:8080/api/health
   curl http://localhost:8080/api/customer/health
   ```
5. Для просмотра логов используйте:
   ```bash
   docker compose logs -f gateway
   ```
6. После старта окружение доступно по адресам:
   - Frontend: `http://localhost:3000/banking-service`
   - Nginx (единая точка входа): `http://localhost/banking-service`
   - Gateway API: `http://localhost:8080/api`
   - Redis Commander: `http://localhost:8081`
   - Splunk UI: `http://localhost:8000` (логин `admin`, пароль `changeme123`)

Gateway автоматически проксирует все запросы `/api/{service}/...` к соответствующим контейнерам (`auth`, `customer`, `office`, `accounts`, `ledger`, `fx`, `utilities`, `contracts`, `notifications`). Каждый сервис публикует `GET /api/<service>/health` для мониторинга.

### Вариант 2. Локальный запуск без Docker

```bash
# 1. Python-зависимости (можно использовать uv/poetry/pip)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Backend-сервисы по отдельности (пример)
uvicorn services.auth.app.main:app --reload --port 8001
uvicorn services.gateway.app.main:app --reload --port 8080

# 3. Frontend (Node 20+)
cd frontend
npm install
npm run dev
```

Все сервисы при локальном запуске также доступны через gateway: `http://localhost:8080/api/<service>/...` (например, `/api/customer/dashboard`). Для полной функциональности можно поднять внешние зависимости из Docker Compose выборочно (`docker compose up redis kafka accounts_db ...`).

### Полезные команды

```bash
# Пересборка только backend-сервисов после изменений
cd infra
docker compose build gateway auth customer office accounts ledger fx utilities contracts notifications

# Перезапуск выбранного сервиса
docker compose up --build gateway

# Остановка и удаление контейнеров + томов БД
docker compose down -v
```

> ⚠️ Учебные секреты и пароли (`dev-secret`, `changeme123`) заданы в открытом виде. Перед использованием вне демо-окружения обязательно заменить их и провести hardening.

## Структура репозитория

```text
services/
  gateway/            # API Gateway (reverse proxy + auth)
  auth/               # Управление пользователями и ролями
  customer/           # Клиентский кабинет
  office/             # Кабинет сотрудника
  accounts/           # Счета и карты
  ledger/             # Платежи и проводки (двойная запись)
  fx/                 # Курсы валют и обмен
  utilities/          # ЖКХ
  contracts/          # Договоры обслуживания
  notifications/      # Рассылка уведомлений
frontend/             # Next.js приложение (SSR/SPA)
infra/                # docker-compose, nginx.conf, env-файлы
shared/               # Общие библиотеки (config, security, logging)
docs/                 # Архитектурные документы, тестовые планы
```

## Следующие шаги

1. Подключить реальные БД и миграции (Alembic/SQLModel).
2. Реализовать Kafka producer/consumer и интеграцию со Splunk.
3. Интегрировать Redis и внешнее API Frankfurter в FX-сервисе.
4. Настроить полноценную аутентификацию (password+refresh, MFA для офиса).
5. Покрыть тестами (pytest + httpx, Playwright E2E) и собрать CI/CD pipeline.
