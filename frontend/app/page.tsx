import Link from 'next/link';

const tiles = [
  { href: '/banking-service/lk', title: 'Личный кабинет клиента', description: 'Счета, переводы, обмен валют и платежи ЖКХ.' },
  { href: '/banking-service/office', title: 'Личный кабинет сотрудника', description: 'Открытие счетов, выпуск карт, управление договорами.' },
  { href: '/banking-service/exchange', title: 'Курсы валют', description: 'Свежие курсы из Redis, обновление из Frankfurter.' }
];

export default function HomePage() {
  return (
    <main className="px-6 py-14 max-w-5xl mx-auto">
      <section className="mb-12 text-center">
        <h1 className="text-4xl font-bold mb-4 text-secondary">Banking Service</h1>
        <p className="text-lg text-gray-600">Учебная платформа для моделирования банковских сценариев через UI и API.</p>
      </section>
      <section className="grid gap-6 md:grid-cols-3">
        {tiles.map((tile) => (
          <Link key={tile.href} href={tile.href} className="border rounded-xl p-6 shadow-sm hover:shadow-lg transition">
            <h2 className="text-xl font-semibold mb-2 text-primary">{tile.title}</h2>
            <p className="text-sm text-gray-600">{tile.description}</p>
          </Link>
        ))}
      </section>
    </main>
  );
}
