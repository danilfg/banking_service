# Banking Service — Архитектурная схема

Документ описывает учебную архитектуру из 9 доменных микросервисов, API Gateway и SPA-интерфейса.

## 1. Компоненты

- **Gateway** — FastAPI, JWT, проксирование `/api/{service}/*` в доменные сервисы, rate-limit (заглушка).
- **Auth** — управление пользователями, ролями, токенами. События Kafka `user.*`.
- **Customer** — сценарии клиента: дашборд, переводы, обмен валют, ЖКХ. События `payment.*`, `utility.*`, `fx.*`.
- **Office** — back-office сотрудников, открытие счетов, выпуск карт, создание клиентов.
- **Accounts** — данные счетов и карт, идемпотентность при создании, привязка к продуктам.
- **Ledger** — двойная запись транзакций, идемпотентность `Idempotency-Key`. События `payment.executed`.
- **FX** — интеграция с Frankfurter, кеш в Redis, TTL 24 часа.
- **Utilities** — справочники провайдеров, платежи ЖКХ.
- **Contracts** — договоры обслуживания, версии, статусы.
- **Notifications** — заглушка e-mail/webpush.
- **Frontend** — Next.js (SSR + SPA), маршруты `/banking-service`, `/lk`, `/office`, `/exchange`.
- **Infrastructure** — PostgreSQL per service, Redis, Kafka, Splunk (через Kafka Connect), Redis Commander.

## 2. API-группы

| Сервис    | Префикс            | Ключевые методы                                                    |
|-----------|--------------------|---------------------------------------------------------------------|
| Auth      | `/api/auth`        | register, activate, login, me                                      |
| Customer  | `/api/customer`    | dashboard, transfer, fx/exchange, utilities/pay                     |
| Office    | `/api/office`      | employees, users, accounts open/close                              |
| Accounts  | `/api/accounts`    | my, {id}                                                            |
| Ledger    | `/api/ledger`      | topup, transfer, transactions                                       |
| FX        | `/api/fx`          | rates/latest, exchange                                              |
| Utilities | `/api/utilities`   | providers, pay                                                      |
| Contracts | `/api/contracts`   | templates, create, activate                                         |
| Notifications | `/api/notifications` | send                                                        |

## 3. Потоки данных

- **Регистрация**: Auth → Kafka (`user.registered`) → Notifications.
- **Перевод (P2P)**: Customer API → Orchestrator (будущий) → Ledger двойная запись → Kafka `payment.executed`.
- **FX**: Customer → FX (Redis кеш) → Ledger → Accounts balances.
- **ЖКХ**: Customer → Utilities → Ledger → Kafka `utility.paid`.
- **Back-office**: Office → Accounts/Contracts/Notifications → Kafka `account.*`.

## 4. Интеграции

- **Frankfurter** — HTTP API, пример: `GET https://api.frankfurter.dev/latest?base=USD&symbols=EUR,GBP`.
- **Kafka → Splunk** — topic `logs.app`, HEC-коннектор.
- **Redis** — ключи `fx:latest:{base}:{symbols}` TTL 86400.

## 5. Тестирование

- **API**: pytest + httpx (заготовки).
- **E2E**: Playwright для UI (план).
- **Нагрузка**: Locust (план).

## 6. Дорожная карта

1. Реализация персистентного слоя (SQLModel + Alembic).
2. Настоящая авторизация, refresh-токены, MFA (opc.).
3. Event-driven взаимодействие (Kafka producers/consumers).
4. Сценарии саг и компенсирующих операций.
5. Тесты (API + UI), CI/CD pipeline.
