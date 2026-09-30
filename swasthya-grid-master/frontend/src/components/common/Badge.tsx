import React from "react";
import { cn } from "@/utils/cn";

export type BadgeVariant =
  | "primary"
  | "success"
  | "warning"
  | "danger"
  | "neutral"
  | "info"
  | "teal";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant;
  dot?: boolean;
  size?: "sm" | "md" | "lg";
}

const variantStyles: Record<BadgeVariant, string> = {
  primary: "bg-blue-50 text-blue-700 border-blue-200 ring-blue-500/20",
  success: "bg-emerald-50 text-emerald-700 border-emerald-200 ring-emerald-500/20",
  warning: "bg-amber-50 text-amber-800 border-amber-200 ring-amber-500/20",
  danger: "bg-rose-50 text-rose-700 border-rose-200 ring-rose-500/20",
  neutral: "bg-slate-50 text-slate-700 border-slate-200 ring-slate-500/20",
  info: "bg-sky-50 text-sky-700 border-sky-200 ring-sky-500/20",
  teal: "bg-teal-50 text-teal-700 border-teal-200 ring-teal-500/20",
};

const dotColors: Record<BadgeVariant, string> = {
  primary: "bg-blue-600",
  success: "bg-emerald-600",
  warning: "bg-amber-600",
  danger: "bg-rose-600",
  neutral: "bg-slate-600",
  info: "bg-sky-600",
  teal: "bg-teal-600",
};

const sizeStyles = {
  sm: "px-2 py-0.5 text-[11px]",
  md: "px-2.5 py-1 text-xs",
  lg: "px-3 py-1.5 text-sm",
};

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = "neutral",
  dot = false,
  size = "md",
  className,
  ...props
}) => {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 font-medium border rounded-full tracking-wide shadow-xs transition-colors",
        variantStyles[variant],
        sizeStyles[size],
        className
      )}
      {...props}
    >
      {dot && (
        <span
          className={cn("w-1.5 h-1.5 rounded-full shrink-0", dotColors[variant])}
        />
      )}
      {children}
    </span>
  );
};
