import React, { useState } from "react";
import { NavLink, useLocation } from "react-router-dom";

const NAV_ITEMS = [
  { path: "/cpi", label: "CPI", icon: "📈" },
  { path: "/signs-of-excess", label: "Signs of Excess", shortLabel: "Excess", icon: "⚠️" },
  { path: "/operating-fundamentals", label: "Operating Fundamentals", shortLabel: "Fundamentals", icon: "🏭" },
  { path: "/yield-spreads", label: "Yield Spreads", shortLabel: "Yields", icon: "📊" },
  { path: "/global-growth", label: "Global Growth", shortLabel: "Global", icon: "🌍" },
  { path: "/download", label: "Download", icon: "⬇️" },
];

export default function Layout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  const currentPage = NAV_ITEMS.find((item) => item.path === location.pathname);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Top navbar - desktop */}
      <header className="bg-white shadow-sm border-b border-gray-200 hidden md:block">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center h-14">
            <h1 className="text-lg font-bold text-primary-700 mr-8 whitespace-nowrap">
              Ascentris Research
            </h1>
            <nav className="flex space-x-1">
              {NAV_ITEMS.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    `px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? "bg-primary-100 text-primary-700"
                        : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                    }`
                  }
                >
                  {item.label}
                </NavLink>
              ))}
            </nav>
          </div>
        </div>
      </header>

      {/* Mobile header */}
      <header className="bg-white shadow-sm border-b border-gray-200 md:hidden">
        <div className="flex items-center justify-between h-12 px-4">
          <h1 className="text-base font-bold text-primary-700">Ascentris Research</h1>
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-md text-gray-600 hover:bg-gray-100"
            aria-label="Toggle navigation"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {sidebarOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile dropdown menu */}
        {sidebarOpen && (
          <nav className="border-t border-gray-200 bg-white py-2 px-4 space-y-1">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={() => setSidebarOpen(false)}
                className={({ isActive }) =>
                  `block px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-primary-100 text-primary-700"
                      : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                  }`
                }
              >
                <span className="mr-2">{item.icon}</span>
                {item.label}
              </NavLink>
            ))}
          </nav>
        )}
      </header>

      {/* Main content */}
      <main className="flex-1 w-full max-w-7xl mx-auto px-3 md:px-6 py-4 md:py-6">
        {children}
      </main>

      {/* Bottom tab bar - mobile */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg z-50">
        <div className="flex justify-around items-center h-14">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex flex-col items-center justify-center py-1 px-1 min-w-0 flex-1 ${
                  isActive ? "text-primary-600" : "text-gray-400"
                }`
              }
            >
              <span className="text-lg leading-none">{item.icon}</span>
              <span className="text-[10px] mt-0.5 truncate max-w-full">
                {item.shortLabel || item.label}
              </span>
            </NavLink>
          ))}
        </div>
      </nav>

      {/* Bottom padding spacer for mobile tab bar */}
      <div className="md:hidden h-16" />
    </div>
  );
}
