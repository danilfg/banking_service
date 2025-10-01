'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';

interface RatesResponse {
  base: string;
  rates: Record<string, string>;
  as_of: string;
  source: string;
}

const API_PREFIX = process.env.NEXT_PUBLIC_GATEWAY_URL ?? 'http://localhost:8080/api';

export default function ExchangePage() {
  const [data, setData] = useState<RatesResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function loadRates() {
    try {
      const { data: response } = await axios.get(`${API_PREFIX}/fx/rates/latest`, {
        headers: { Authorization: 'Bearer demo-token' }
      });
      setData(response);
      setError(null);
    } catch (err) {
      setError('Не удалось получить курсы (демо).');
    }
  }

  useEffect(() => {
    loadRates();
  }, []);

  return (
    <main className="px-6 py-10 max-w-4xl mx-auto space-y-6">
      <header>
        <h1 className="text-3xl font-semibold text-secondary">Курсы валют</h1>
        <p className="text-gray-600">Источники — Redis / Frankfurter API. TTL кеша 24 часа.</p>
      </header>

      <section className="bg-white rounded-xl p-6 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <p className="text-sm text-gray-500">Базовая валюта</p>
            <p className="text-xl font-semibold">{data?.base ?? '—'}</p>
          </div>
          <button onClick={loadRates} className="px-4 py-2 rounded-md bg-primary text-white">Обновить</button>
        </div>
        {error && <p className="text-red-600 text-sm mb-3">{error}</p>}
        <table className="w-full text-left">
          <thead>
            <tr>
              <th className="py-2 text-gray-500">Валюта</th>
              <th className="py-2 text-gray-500">Курс</th>
            </tr>
          </thead>
          <tbody>
            {data ? (
              Object.entries(data.rates).map(([currency, rate]) => (
                <tr key={currency} className="border-t">
                  <td className="py-2 font-medium">{currency}</td>
                  <td className="py-2">{rate}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={2} className="py-4 text-center text-gray-500">Загрузка...</td>
              </tr>
            )}
          </tbody>
        </table>
        <p className="text-xs text-gray-500 mt-4">Источник данных: {data?.source ?? '—'} · Обновлено: {data?.as_of ?? '—'}</p>
      </section>
    </main>
  );
}
