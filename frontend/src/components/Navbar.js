'use client'

import Link from 'next/link';
import { useState } from 'react';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="flex items-center justify-between flex-wrap bg-primary p-6">
      {/* Left Side: Logo and App Name */}
      <div className="flex items-center flex-shrink-0 text-white mr-6">
        {/* Replace with your logo image */}
        <img src="/acsed.jpeg" alt="Logo" className="h-8 w-8 mr-2" />
        <span className="font-semibold text-xl tracking-tight">MeAyudAI</span>
      </div>

      {/* Right Side: Navigation Links */}
      <div className="block lg:hidden">
        <button 
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          className="flex items-center px-3 py-2 border rounded text-white border-white hover:text-neutral hover:border-neutral"
        >
          <svg className="fill-current h-3 w-3" viewBox="0 0 20 20">
            <title>Menu</title>
            <path d="M0 3h20v2H0z" />
            <path d="M0 9h20v2H0z" />
            <path d="M0 15h20v2H0z" />
          </svg>
        </button>
      </div>
      <div className={`w-full block flex-grow lg:flex lg:items-center lg:w-auto ${!isMenuOpen && 'hidden'} lg:block`}>
        <div className="text-sm lg:flex-grow lg:flex lg:justify-end ml-6">
          <Link className="block mt-4 lg:inline-block lg:mt-0 text-white hover:text-neutral mr-4" href="/">
            Home
          </Link>
          <Link className="block mt-4 lg:inline-block lg:mt-0 text-white hover:text-neutral mr-4" href="/guidelines">
            Pautas
          </Link>
          <Link className="block mt-4 lg:inline-block lg:mt-0 text-white hover:text-neutral mr-4" href="/uiResources">
            UI Resources
          </Link>
        </div>
      </div>
    </nav>
  );
};

export {
  Navbar
}
