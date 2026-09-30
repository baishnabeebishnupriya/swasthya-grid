import React from "react";
import { cn } from "@/utils/cn";
import {
  Building2,
  Activity,
  Pill,
  BedDouble,
  Users,
  AlertTriangle,
  ArrowRightLeft,
  ShieldAlert,
  TrendingUp,
  TrendingDown,
  LucideIcon,
} from "lucide-react";
import { Badge, BadgeVariant } from "./Badge";

const ICON_MAP: Record<string, LucideIcon> = {
  Building2,
  Activity,
  Pill,
  BedDouble,
  Users,
  AlertTriangle,
  ArrowRightLeft,
  ShieldAlert,
};

export interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  change?: string;
  changeType?: "positive" | "negative" | "neutral" | "warning";
  iconName: string;
  statusBadge?: string;
  statusVariant?: BadgeVariant;
  className?: string;
  highlightBorder?: "none" | "teal" | "amber" | "rose" | "blue";
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  change,
  changeType = "neutral",
  iconName,
  statusBadge,
  statusVariant = "neutral",
  className,
  highlightBorder = "none",
}) => {
  const IconComponent = ICON_MAP[iconName] || Activity;

  const borderStyles = {
    none: "border-slate-200/80",
    teal: "border-teal-300 ring-1 ring-teal-500/10",
    amber: "border-amber-300 ring-1 ring-amber-500/10",
    rose: "border-rose-300 ring-1 ring-rose-500/10",
    blue: "border-blue-300 ring-1 ring-blue-500/10",
  };

  const iconBgStyles = {
    none: "bg-slate-100 text-slate-700",
    teal: "bg-teal-50 text-teal-600 border border-teal-100",
    amber: "bg-amber-50 text-amber-600 border border-amber-100",
    rose: "bg-rose-50 text-rose-600 border border-rose-100",
    blue: "bg-blue-50 text-blue-600 border border-blue-100",
  };

  return (
    <div
      className={cn(
        "bg-white rounded-xl p-5 border shadow-xs transition-all duration-200 hover:shadow-md",
        borderStyles[highlightBorder],
        className
      )}
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="space-y-0.5">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
            {title}
          </p>
          <div className="flex items-baseline gap-2">
            <h3 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              {value}
            </h3>
          </div>
        </div>

        <div className={cn("p-2.5 rounded-lg shrink-0", iconBgStyles[highlightBorder])}>
          <IconComponent className="w-5 h-5" />
        </div>
      </div>

      <div className="flex items-center justify-between gap-2 pt-2 border-t border-slate-100 text-xs">
        <div className="text-slate-500 truncate">
          {subtitle && <span>{subtitle}</span>}
          {change && (
            <span
              className={cn(
                "inline-flex items-center gap-1 font-semibold ml-1",
                changeType === "positive" && "text-emerald-600",
                changeType === "negative" && "text-rose-600",
                changeType === "warning" && "text-amber-600",
                changeType === "neutral" && "text-slate-600"
              )}
            >
              {changeType === "positive" && <TrendingUp className="w-3.5 h-3.5" />}
              {changeType === "negative" && <TrendingDown className="w-3.5 h-3.5" />}
              {change}
            </span>
          )}
        </div>

        {statusBadge && (
          <Badge variant={statusVariant} size="sm" dot>
            {statusBadge}
          </Badge>
        )}
      </div>
    </div>
  );
};
