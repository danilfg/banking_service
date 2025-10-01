# Testing Strategy (Roadmap)

## 1. Unit / Component tests
- FastAPI routers → pytest + httpx AsyncClient, фикстуры для временной БД (sqlite или postgres контейнер).
- Shared утилиты (security, logging) → покрыть edge-cases (истекший токен, неверная роль).

## 2. Contract tests
- Consumer-driven contracts (Pact) для взаимодействий: Gateway ↔ Auth/Accounts/Ledger, Accounts ↔ Ledger, Customer ↔ FX.
- Зафиксировать схемы событий Kafka (`payment.executed`, `fx.rate_refreshed`).

## 3. End-to-End
- Playwright: регистрация, активация, логин, перевод, обмен валют, оплата ЖКХ, сценарии офиса.
- Сеансы с использованием тестовых токенов или заглушек.

## 4. Нагрузочные
- Locust/Vegeta: интенсивные API `/api/ledger/transfer`, `/api/fx/exchange`, `/api/utilities/pay`.
- SLA: P95 < 250 мс при 100 RPS (демо цель).

## 5. Observability
- Проверка логов в Splunk по `X-Request-Id`.
- Метрики latency, error-rate, throughput.
