'use client';

import { useState } from 'react';
import axios from 'axios';

const API_PREFIX = process.env.NEXT_PUBLIC_GATEWAY_URL ?? 'http://localhost:8080/api';

export default function OfficePortal() {
  const [message, setMessage] = useState<string | null>(null);

  async function handleCreateCustomer() {
    try {
      const { data } = await axios.post(
        `${API_PREFIX}/office/users`,
        { email: 'demo.customer@bank.local', phone: '+79991234567' },
        { headers: { Authorization: 'Bearer demo-admin' } }
      );
      setMessage(`Создан клиент с id ${data.id}`);
    } catch (error) {
      setMessage('Не удалось создать клиента (демо)');
    }
  }

  return (
    <main className="px-6 py-10 max-w-5xl mx-auto space-y-8">
      <header>
        <h1 className="text-3xl font-semibold text-secondary">Личный кабинет сотрудника</h1>
        <p className="text-gray-600">Открытие счетов, выпуск карт, администрирование сотрудников.</p>
      </header>

      <section className="grid gap-6 md:grid-cols-2">
        <div className="bg-white rounded-xl p-6 shadow-sm">
          <h2 className="text-xl font-semibold mb-3">Быстрые операции</h2>
          <ul className="space-y-3">
            <li className="border rounded-lg p-4">
              <p className="font-medium">Создать клиента</p>
              <p className="text-sm text-gray-500 mb-3">Регистрация нового клиента для оформления продуктов.</p>
              <button onClick={handleCreateCustomer} className="px-4 py-2 rounded-md bg-primary text-white">Создать</button>
            </li>
            <li className="border rounded-lg p-4">
              <p className="font-medium">Открыть счет</p>
              <p className="text-sm text-gray-500">Форма открытия счета клиенту с выбором продукта.</p>
            </li>
            <li className="border rounded-lg p-4">
              <p className="font-medium">Выпустить карту</p>
              <p className="text-sm text-gray-500">Привязка карты к выбранному счету, управление статусами.</p>
            </li>
          </ul>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm">
          <h2 className="text-xl font-semibold mb-3">Дашборд статусов</h2>
          <p className="text-sm text-gray-600">Здесь будут отображаться события Kafka (account.opened, card.issued, payment.executed) с фильтрами по счету и сотруднику.</p>
        </div>
      </section>

      {message && <div className="p-4 border rounded-lg bg-green-50 text-green-700">{message}</div>}
    </main>
  );
}
