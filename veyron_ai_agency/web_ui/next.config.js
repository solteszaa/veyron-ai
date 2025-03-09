/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    // Engedélyezzük a szerver komponenseket
    serverComponents: true,
    // Engedélyezzük az App Router funkciót
    appDir: true,
  },
  // API Route-ok engedélyezése
  rewrites: async () => {
    return [
      {
        source: '/api/:path*',
        destination: '/api/:path*',
      },
    ];
  },
};

module.exports = nextConfig; 