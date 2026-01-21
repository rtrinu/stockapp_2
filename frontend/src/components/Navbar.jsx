"use client";

import { useState } from "react";

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="navbar bg-base-100/80 backdrop-blur-md fixed top-0 z-50 border-b border-base-300 px-4 lg:px-8">
      <div className="navbar-start">
        <div className="dropdown">
          <button
            tabIndex={0}
            className="btn btn-ghost lg:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h8m-8 6h16"
              />
            </svg>
          </button>
          {mobileMenuOpen && (
            <ul
              tabIndex={0}
              className="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow-lg bg-base-200 rounded-box w-52"
            >
              <li>
                <a href="#features">Features</a>
              </li>
              <li>
                <a href="#pricing">Pricing</a>
              </li>
              <li>
                <a href="#testimonials">Testimonials</a>
              </li>
              <li>
                <details>
                  <summary>Resources</summary>
                  <ul className="p-2 bg-base-300 rounded-box">
                    <li>
                      <a>Documentation</a>
                    </li>
                    <li>
                      <a>API Reference</a>
                    </li>
                    <li>
                      <a>Blog</a>
                    </li>
                  </ul>
                </details>
              </li>
            </ul>
          )}
        </div>
        <a className="btn btn-ghost text-xl font-bold">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6 text-primary"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm0-8h2V7H3v2zm4 4h14v-2H7v2zm0 4h14v-2H7v2zM7 7v2h14V7H7z" />
          </svg>
          <span className="text-primary">Stock</span>AI
        </a>
      </div>

      <div className="navbar-center hidden lg:flex">
        <ul className="menu menu-horizontal px-1 gap-1">
          <li>
            <a
              href="#features"
              className="hover:text-primary transition-colors"
            >
              Features
            </a>
          </li>
          <li>
            <a href="#pricing" className="hover:text-primary transition-colors">
              Pricing
            </a>
          </li>
          <li>
            <a
              href="#testimonials"
              className="hover:text-primary transition-colors"
            >
              Testimonials
            </a>
          </li>
          <li>
            <details>
              <summary className="hover:text-primary transition-colors">
                Resources
              </summary>
              <ul className="p-2 bg-base-200 rounded-box w-48 shadow-xl">
                <li>
                  <a>Documentation</a>
                </li>
                <li>
                  <a>API Reference</a>
                </li>
                <li>
                  <a>Blog</a>
                </li>
                <li>
                  <a>Community</a>
                </li>
              </ul>
            </details>
          </li>
        </ul>
      </div>

      <div className="navbar-end gap-2">
        <a className="btn btn-ghost btn-sm hidden sm:flex">Log In</a>
        <a className="btn btn-primary btn-sm">Get Started</a>
      </div>
    </div>
  );
}
