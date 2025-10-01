/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  basePath: '/banking-service',
  experimental: {
    appDir: true
  }
};

export default nextConfig;
