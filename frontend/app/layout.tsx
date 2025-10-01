import type { Metadata } from 'next';
import './global.css';
import { NavBar } from '../components/NavBar';

export const metadata: Metadata = {
  title: 'Banking Service Portal',
  description: 'Учебный банковский сервис с микросервисной архитектурой'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru">
      <body className="bg-gray-50">
        <NavBar />
        {children}
      </body>
    </html>
  );
}
