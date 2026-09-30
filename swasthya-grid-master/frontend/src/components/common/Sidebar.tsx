"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/utils/cn";
import {
  LayoutDashboard,
  Building2,
  Map,
  Compass,
  Boxes,
  Pill,
  BedDouble,
  Users,
  CalendarCheck,
  TrendingUp,
  AlertTriangle,
  ArrowRightLeft,
  ShieldCheck,
  LucideIcon,
} from "lucide-react";
import { NAVIGATION_ITEMS, NavItem } from "@/utils/constants";
import { Badge } from "./Badge";

const ICON_MAP: Record<string, LucideIcon> = {
  LayoutDashboard,
  Building2,
  Map,
  Compass,
  Boxes,
  Pill,
  BedDouble,
  Users,
  CalendarCheck,
  TrendingUp,
  AlertTriangle,
  ArrowRightLeft,
  ShieldCheck,
};

interface SidebarProps {
  isMobileOpen?: boolean;
  onCloseMobile?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  isMobileOpen = false,
  onCloseMobile,
}) => {
  const pathname = usePathname();

  const coreNav = NAVIGATION_ITEMS.filter((i) => i.section === "core");
  const resourceNav = NAVIGATION_ITEMS.filter((i) => i.section === "resources");
  const intelligenceNav = NAVIGATION_ITEMS.filter((i) => i.section === "intelligence");
  const systemNav = NAVIGATION_ITEMS.filter((i) => i.section === "system");

  const renderSection = (title: string, items: NavItem[]) => (
    <div className="space-y-1 mb-5">
      <h4 className="px-3 text-[10px] font-bold uppercase tracking-wider text-slate-400 font-mono mb-2">
        {title}
      </h4>
      {items.map((item) => {
        const IconComponent = ICON_MAP[item.iconName] || LayoutDashboard;
        const isActive =
          pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));

        return (
          <Link
            key={item.href}
            href={item.href}
            onClick={onCloseMobile}
            className={cn(
              "flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium transition-all group",
              isActive
                ? "bg-teal-700 text-white font-semibold shadow-xs"
                : "text-slate-300 hover:text-white hover:bg-slate-800"
            )}
          >
            <div className="flex items-center gap-2.5">
              <IconComponent
                className={cn(
                  "w-4 h-4 shrink-0 transition-colors",
                  isActive ? "text-white" : "text-slate-400 group-hover:text-teal-400"
                )}
              />
              <span className="truncate">{item.title}</span>
            </div>

            {item.badge && (
              <Badge
                variant={item.badgeVariant || "neutral"}
                size="sm"
                className={cn(
                  "text-[9px] px-1.5 py-0.2",
                  isActive && "bg-teal-800/90 text-teal-100 border-teal-600 ring-0"
                )}
              >
                {item.badge}
              </Badge>
            )}
          </Link>
        );
      })}
    </div>
  );

  return (
    <>
      {/* Mobile Backdrop */}
      {isMobileOpen && (
        <div
          onClick={onCloseMobile}
          className="fixed inset-0 bg-slate-950/60 backdrop-blur-xs z-40 lg:hidden"
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={cn(
          "fixed top-16 bottom-0 left-0 z-40 w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between transition-transform duration-200 lg:translate-x-0 overflow-y-auto",
          isMobileOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        <div className="p-4">
          {renderSection("Executive Overview", coreNav)}
          {renderSection("Resource Management", resourceNav)}
          {renderSection("Predictive Intelligence", intelligenceNav)}
          {renderSection("Governance & Compliance", systemNav)}
        </div>

        {/* Bottom Status Card */}
        <div className="p-4 border-t border-slate-800 bg-slate-950/50 m-3 rounded-xl">
          <div className="flex items-center justify-between text-xs mb-1">
            <span className="text-slate-400 font-mono text-[10px] uppercase">Grid Node</span>
            <span className="text-emerald-400 font-bold text-[10px]">OD-BBI-CENTRAL</span>
          </div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden mb-2">
            <div className="bg-teal-500 h-full w-[94%]" />
          </div>
          <div className="flex justify-between text-[10px] text-slate-400 font-mono">
            <span>Sync Latency</span>
            <span className="text-slate-200">18ms (Fast)</span>
          </div>
        </div>
      </aside>
    </>
  );
};
