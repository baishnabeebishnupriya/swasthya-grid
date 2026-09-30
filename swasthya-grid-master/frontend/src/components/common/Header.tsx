"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Bell,
  Search,
  Shield,
  Activity,
  Menu,
  X,
  ExternalLink,
} from "lucide-react";
import { APP_NAME, APP_TAGLINE } from "@/utils/constants";
import { Badge } from "./Badge";

interface HeaderProps {
  onToggleMobileSidebar?: () => void;
  isMobileSidebarOpen?: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  onToggleMobileSidebar,
  isMobileSidebarOpen = false,
}) => {
  const [hasUnreadAlerts, setHasUnreadAlerts] = useState(true);

  return (
    <header className="sticky top-0 z-40 h-16 bg-slate-900 text-white border-b border-slate-800 shadow-sm flex items-center justify-between px-4 lg:px-8 select-none">
      {/* LEFT: Branding & National Health Program Identity */}
      <div className="flex items-center gap-4">
        {onToggleMobileSidebar && (
          <button
            type="button"
            onClick={onToggleMobileSidebar}
            className="lg:hidden p-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 transition-colors"
            aria-label="Toggle navigation menu"
          >
            {isMobileSidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        )}

        <Link href="/" className="flex items-center gap-3 group">
          {/* Emblem / Cross Icon */}
          <div className="w-9 h-9 rounded-lg bg-teal-600 border border-teal-400 text-white flex items-center justify-center font-black text-base shadow-sm group-hover:scale-105 transition-transform">
            <Activity className="w-5 h-5" />
          </div>

          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-base tracking-tight text-white uppercase">
                {APP_NAME}
              </span>
              <span className="hidden sm:inline-flex px-1.5 py-0.5 rounded bg-teal-950/80 border border-teal-600/40 text-[9px] font-mono uppercase tracking-widest text-teal-300 font-bold">
                NATIONAL GRID
              </span>
            </div>
            <p className="text-[11px] text-slate-400 font-medium tracking-wide">
              {APP_TAGLINE}
            </p>
          </div>
        </Link>
      </div>

      {/* MIDDLE: Search & National Health System Status */}
      <div className="hidden md:flex items-center gap-3 max-w-md w-full mx-4">
        <div className="relative w-full">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search PHC, district, medicine stock, bed availability..."
            className="w-full pl-10 pr-4 py-1.5 bg-slate-800/80 border border-slate-700 rounded-lg text-xs text-white placeholder-slate-400 focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500 transition-all font-sans"
          />
        </div>
      </div>

      {/* RIGHT: Notifications, Telemetry, and User Profile */}
      <div className="flex items-center gap-3 sm:gap-4">
        {/* Network Health Status Dot */}
        <div className="hidden xl:flex items-center gap-2 px-3 py-1 bg-slate-800/80 border border-slate-700 rounded-lg text-xs text-slate-300">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="font-medium text-[11px] text-slate-200">
            Grid Telemetry: <strong className="text-emerald-400 font-semibold">Active (99.8%)</strong>
          </span>
        </div>

        {/* Notifications Icon with Badge */}
        <div className="relative">
          <button
            type="button"
            onClick={() => setHasUnreadAlerts(!hasUnreadAlerts)}
            className="p-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 transition-colors relative"
            title="System alerts and transfer requests"
          >
            <Bell className="w-5 h-5" />
            {hasUnreadAlerts && (
              <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-amber-500 ring-2 ring-slate-900 animate-pulse" />
            )}
          </button>
        </div>

        {/* User Placeholder */}
        <div className="flex items-center gap-2.5 pl-2 sm:pl-3 border-l border-slate-800">
          <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-teal-400 font-bold text-xs">
            <Shield className="w-4 h-4 text-teal-400" />
          </div>
          <div className="hidden lg:block text-left">
            <div className="text-xs font-semibold text-white leading-tight">
              Dr. Priya Sharma
            </div>
            <div className="text-[10px] text-slate-400 uppercase tracking-wider font-mono">
              State Health Director
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};
