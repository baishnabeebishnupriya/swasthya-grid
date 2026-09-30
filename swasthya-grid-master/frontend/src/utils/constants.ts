export const APP_NAME = "SwasthyaGrid";
export const APP_TAGLINE = "Health Resource Resilience Network";
export const APP_ORGANIZATION = "National Health Infrastructure Division";
export const APP_VERSION = "v1.4.0-Production";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";

export interface NavItem {
  title: string;
  href: string;
  iconName: string;
  badge?: string;
  badgeVariant?: "primary" | "warning" | "danger" | "success" | "neutral";
  section?: "core" | "resources" | "intelligence" | "system";
}

export const NAVIGATION_ITEMS: NavItem[] = [
  // Core
  {
    title: "Dashboard",
    href: "/",
    iconName: "LayoutDashboard",
    section: "core",
  },
  {
    title: "PHC Network",
    href: "/phcs",
    iconName: "Building2",
    badge: "1,248 Active",
    badgeVariant: "primary",
    section: "core",
  },
  {
    title: "State Overview",
    href: "/states",
    iconName: "Map",
    section: "core",
  },
  {
    title: "District Overview",
    href: "/districts",
    iconName: "Compass",
    section: "core",
  },

  // Resource Management
  {
    title: "Inventory",
    href: "/inventory",
    iconName: "Boxes",
    section: "resources",
  },
  {
    title: "Medicines",
    href: "/medicines",
    iconName: "Pill",
    badge: "92% In-Stock",
    badgeVariant: "success",
    section: "resources",
  },
  {
    title: "Beds",
    href: "/beds",
    iconName: "BedDouble",
    section: "resources",
  },
  {
    title: "Staff Management",
    href: "/staff",
    iconName: "Users",
    section: "resources",
  },
  {
    title: "Attendance",
    href: "/attendance",
    iconName: "CalendarCheck",
    section: "resources",
  },

  // Intelligence & Operations
  {
    title: "Forecasts",
    href: "/forecasts",
    iconName: "TrendingUp",
    badge: "AI Predictive",
    badgeVariant: "primary",
    section: "intelligence",
  },
  {
    title: "Risk Alerts",
    href: "/risks",
    iconName: "AlertTriangle",
    badge: "3 Critical",
    badgeVariant: "danger",
    section: "intelligence",
  },
  {
    title: "Resource Transfers",
    href: "/transfers",
    iconName: "ArrowRightLeft",
    badge: "8 Pending",
    badgeVariant: "warning",
    section: "intelligence",
  },

  // System
  {
    title: "Audit Logs",
    href: "/audit-logs",
    iconName: "ShieldCheck",
    section: "system",
  },
];
