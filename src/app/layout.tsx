import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navigation from "../components/Navigation";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "MuscleVision - Analyze Your Flex. Improve Your Form.",
  description: "Real-time muscle detection and form feedback using computer vision",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gray-900 text-white min-h-screen flex flex-col`}>
        <Navigation />
        <main className="flex-1 w-full max-w-7xl mx-auto px-4 py-8">{children}</main>
        <footer className="w-full py-6 text-center text-gray-400 border-t border-gray-800 text-sm">
          &copy; {new Date().getFullYear()} MuscleVision. All rights reserved.
        </footer>
      </body>
    </html>
  );
}
