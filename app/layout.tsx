import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Cachuntu — Ubuntu, más rápido y listo desde el primer arranque",
  description:
    "Cachuntu es una distribución Linux basada en Ubuntu, en desarrollo, enfocada en rendimiento, limpieza y una experiencia lista para usar.",
  openGraph: {
    type: "website",
    locale: "es_MX",
    siteName: "Cachuntu",
    title: "Cachuntu — Ubuntu, más rápido y listo desde el primer arranque",
    description:
      "Una distribución Linux basada en Ubuntu, actualmente en desarrollo.",
  },
  twitter: {
    card: "summary_large_image",
    title: "Cachuntu — Ubuntu, más rápido y listo desde el primer arranque",
    description:
      "Una distribución Linux basada en Ubuntu, actualmente en desarrollo.",
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
