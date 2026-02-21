import React, { useState } from "react";
import { NavLink, useLocation } from "react-router-dom";

const NAV_ITEMS = [
  { path: "/cpi", label: "CPI", shortLabel: "CPI", icon: "📈" },
  { path: "/signs-of-excess", label: "Signs of Excess", shortLabel: "Excess", icon: "⚠️" },
  { path: "/operating-fundamentals", label: "Operating Fundamentals", shortLabel: "Ops", icon: "🏭" },
  { path: "/yield-spreads", label: "Yield Spreads", shortLabel: "Yields", icon: "📊" },
  { path: "/global-growth", label: "Global Growth", shortLabel: "Global", icon: "🌍" },
  { path: "/download", label: "Download", shortLabel: "Data", icon: "⬇️" },
];

export default function Layout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  return (
    <div className="min-h-screen bg-brand-black flex flex-col">
      {/* Top navbar - desktop */}
      <header className="bg-brand-charcoal border-b-2 border-brand-gold hidden md:block">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center h-16">
            <h1 className="text-lg font-bold text-brand-gold mr-10 whitespace-nowrap tracking-widest uppercase">
              Ascentris Research
            </h1>
            <nav className="flex space-x-1">
              {NAV_ITEMS.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    `px-4 py-2 text-sm font-medium transition-all tracking-wider uppercase ${
                      isActive
                        ? "text-brand-gold border-b-2 border-brand-gold"
                        : "text-brand-light hover:text-brand-white border-b-2 border-transparent"
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
      <header className="bg-brand-charcoal border-b-2 border-brand-gold md:hidden">
        <div className="flex items-center justify-between h-13 px-4 py-2">
          <h1 className="text-base font-bold text-brand-gold tracking-widest uppercase">
            Ascentris Research
          </h1>
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-md text-brand-light hover:text-brand-gold hover:bg-brand-dark transition-colors"
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
          <nav className="border-t border-brand-gray bg-brand-charcoal py-2 px-4 space-y-1">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={() => setSidebarOpen(false)}
                className={({ isActive }) =>
                  `block px-3 py-2.5 rounded-md text-sm font-medium transition-colors tracking-wide uppercase ${
                    isActive
                      ? "bg-brand-dark text-brand-gold border-l-4 border-brand-gold pl-2"
                      : "text-brand-light hover:text-brand-white hover:bg-brand-dark"
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

      {/* Footer - desktop only */}
      <footer className="hidden md:block bg-brand-charcoal border-t border-brand-gray">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <span className="text-brand-muted text-xs tracking-wider uppercase">
            Ascentris Research {new Date().getFullYear()}
          </span>
          <div className="w-12 h-0.5 bg-brand-gold" />
        </div>
      </footer>

      {/* Bottom tab bar - mobile */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-brand-charcoal border-t-2 border-brand-gold shadow-lg z-50">
        <div className="flex justify-around items-center h-14">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex flex-col items-center justify-center py-1 px-1 min-w-0 flex-1 transition-colors ${
                  isActive ? "text-brand-gold" : "text-brand-muted"
                }`
              }
            >
              <span className="text-lg leading-none">{item.icon}</span>
              <span className="text-[10px] mt-0.5 truncate max-w-full font-medium">
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
