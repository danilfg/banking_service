'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const links = [
  { href: '/banking-service', label: 'Главная' },
  { href: '/banking-service/lk', label: 'ЛК клиента' },
  { href: '/banking-service/office', label: 'ЛК офиса' },
  { href: '/banking-service/exchange', label: 'Курсы валют' }
];

export function NavBar() {
  const pathname = usePathname();

  return (
    <nav className="bg-white border-b">
      <div className="max-w-6xl mx-auto flex items-center justify-between px-6 py-4">
        <Link href="/banking-service" className="text-xl font-semibold text-primary">
          Banking Service
        </Link>
        <ul className="flex gap-4 text-sm">
          {links.map((link) => {
            const active = pathname === link.href;
            return (
              <li key={link.href}>
                <Link
                  href={link.href}
                  className={`px-3 py-2 rounded-md ${active ? 'bg-primary text-white' : 'text-gray-600 hover:text-secondary'}`}
                >
                  {link.label}
                </Link>
              </li>
            );
          })}
        </ul>
      </div>
    </nav>
  );
}
