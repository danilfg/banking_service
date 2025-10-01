'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';

interface AccountSummary {
  id: string;
  currency: string;
  balance: string;
}

interface DashboardResponse {
  accounts: AccountSummary[];
  recent_transactions: any[];
}

const API_PREFIX = process.env.NEXT_PUBLIC_GATEWAY_URL ?? 'http://localhost:8080/api';

export default function ClientPortal() {
  const [dashboard, setDashboard] = useState<DashboardResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchDashboard() {
      try {
        const { data } = await axios.get(`${API_PREFIX}/customer/dashboard`, {
          headers: { Authorization: 'Bearer demo-token' }
        });
        setDashboard(data);
      } catch (err) {
        setError('Не удалось загрузить данные дашборда (демо-режим).');
      }
    }

    fetchDashboard();
  }, []);

  return (
    <main className="px-6 py-10 max-w-6xl mx-auto">
      <header className="mb-10">
        <h1 className="text-3xl font-semibold text-secondary">Личный кабинет клиента</h1>
        <p className="text-gray-600">Просматривайте счета, совершайте переводы, обмен валют и оплачивайте услуги ЖКХ.</p>
      </header>

      <section className="grid gap-6 md:grid-cols-3">
        <div className="md:col-span-2 bg-white rounded-xl p-6 shadow-sm">
          <h2 className="text-xl font-semibold mb-4">Счета и балансы</h2>
          {dashboard?.accounts?.length ? (
            <ul className="space-y-3">
              {dashboard.accounts.map((account) => (
                <li key={account.id} className="flex justify-between border rounded-lg p-4">
                  <div>
                    <p className="font-medium text-secondary">{account.id}</p>
                    <p className="text-sm text-gray-500">{account.currency}</p>
                  </div>
                  <span className="text-lg font-semibold">{account.balance}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-gray-500">{error ?? 'Загрузка...'}</p>
          )}
        </div>
        <div className="bg-white rounded-xl p-6 shadow-sm space-y-4">
          <h2 className="text-xl font-semibold">Быстрые действия</h2>
          <button className="w-full py-2 border rounded-lg hover:bg-primary hover:text-white">Пополнить</button>
          <button className="w-full py-2 border rounded-lg hover:bg-primary hover:text-white">Перевести</button>
          <button className="w-full py-2 border rounded-lg hover:bg-primary hover:text-white">Обмен валют</button>
          <button className="w-full py-2 border rounded-lg hover:bg-primary hover:text-white">Оплатить ЖКХ</button>
        </div>
      </section>
    </main>
  );
}
