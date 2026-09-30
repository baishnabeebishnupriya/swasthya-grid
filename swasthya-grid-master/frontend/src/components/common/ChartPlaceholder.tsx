import React from "react";
import { cn } from "@/utils/cn";
import { TrendingUp, BarChart3, PieChart, Activity } from "lucide-react";

export interface ChartPlaceholderProps {
  title: string;
  subtitle?: string;
  type?: "bar" | "line" | "donut" | "area";
  height?: string;
  className?: string;
  statsSummary?: { label: string; value: string; color?: string }[];
}

export const ChartPlaceholder: React.FC<ChartPlaceholderProps> = ({
  title,
  subtitle,
  type = "bar",
  height = "h-64",
  className,
  statsSummary,
}) => {
  return (
    <div
      className={cn(
        "bg-white rounded-xl p-5 border border-slate-200 shadow-xs flex flex-col justify-between",
        className
      )}
    >
      <div className="flex items-start justify-between gap-3 mb-4">
        <div>
          <h4 className="text-sm font-bold text-slate-800 tracking-tight flex items-center gap-2">
            {type === "bar" && <BarChart3 className="w-4 h-4 text-teal-600" />}
            {type === "line" && <TrendingUp className="w-4 h-4 text-blue-600" />}
            {type === "donut" && <PieChart className="w-4 h-4 text-amber-600" />}
            {type === "area" && <Activity className="w-4 h-4 text-indigo-600" />}
            {title}
          </h4>
          {subtitle && <p className="text-xs text-slate-500 mt-0.5">{subtitle}</p>}
        </div>

        <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
          Real-time Feed
        </span>
      </div>

      {/* SVG Chart Graphic Illustration */}
      <div className={cn("w-full relative flex items-end justify-between gap-2 px-2 py-4 bg-slate-50/60 rounded-lg border border-dashed border-slate-200 overflow-hidden", height)}>
        {type === "bar" && (
          <div className="w-full h-full flex items-end justify-between gap-3 pt-6 pb-2">
            {[
              { label: "Bhubaneswar", val: 88, color: "bg-teal-600" },
              { label: "Cuttack", val: 72, color: "bg-teal-500" },
              { label: "Puri", val: 65, color: "bg-teal-500" },
              { label: "Balasore", val: 94, color: "bg-amber-500" },
              { label: "Kolkata", val: 82, color: "bg-teal-600" },
              { label: "Howrah", val: 78, color: "bg-teal-500" },
              { label: "Jamshedpur", val: 60, color: "bg-teal-400" },
            ].map((bar, i) => (
              <div key={i} className="flex-1 flex flex-col items-center gap-1.5 h-full justify-end group">
                <span className="text-[10px] font-mono font-bold text-slate-600 group-hover:text-teal-600 transition-colors">
                  {bar.val}%
                </span>
                <div
                  style={{ height: `${bar.val}%` }}
                  className={cn("w-full rounded-t-md transition-all duration-300 group-hover:opacity-90", bar.color)}
                />
                <span className="text-[9px] font-medium text-slate-500 truncate w-full text-center">
                  {bar.label}
                </span>
              </div>
            ))}
          </div>
        )}

        {type === "area" && (
          <div className="w-full h-full flex flex-col justify-between pt-2">
            <svg viewBox="0 0 400 120" className="w-full h-full text-teal-600/20 fill-current">
              <path d="M0,80 Q60,30 120,60 T240,40 T360,70 T400,30 L400,120 L0,120 Z" />
              <path
                d="M0,80 Q60,30 120,60 T240,40 T360,70 T400,30"
                fill="none"
                stroke="#0D9488"
                strokeWidth="2.5"
              />
            </svg>
            <div className="flex items-center justify-between text-[10px] text-slate-400 font-mono pt-1">
              <span>00:00</span>
              <span>06:00</span>
              <span>12:00</span>
              <span>18:00</span>
              <span>24:00</span>
            </div>
          </div>
        )}

        {type === "donut" && (
          <div className="w-full h-full flex items-center justify-center gap-6">
            <div className="relative w-28 h-28 flex items-center justify-center">
              <svg viewBox="0 0 36 36" className="w-full h-full -rotate-90">
                <circle cx="18" cy="18" r="14" fill="none" stroke="#E2E8F0" strokeWidth="4" />
                <circle
                  cx="18" cy="18" r="14" fill="none"
                  stroke="#0D9488" strokeWidth="4"
                  strokeDasharray="60, 100" strokeLinecap="round"
                />
                <circle
                  cx="18" cy="18" r="14" fill="none"
                  stroke="#2563EB" strokeWidth="4"
                  strokeDasharray="25, 100" strokeDashoffset="-60"
                />
                <circle
                  cx="18" cy="18" r="14" fill="none"
                  stroke="#F59E0B" strokeWidth="4"
                  strokeDasharray="15, 100" strokeDashoffset="-85"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
                <span className="text-xs font-bold text-slate-800">1,248</span>
                <span className="text-[8px] uppercase tracking-wider text-slate-400">Total Units</span>
              </div>
            </div>

            <div className="space-y-1.5 text-xs">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-teal-600" />
                <span className="text-slate-600">PHCs (60%)</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-blue-600" />
                <span className="text-slate-600">CHCs (25%)</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
                <span className="text-slate-600">District Hospitals (15%)</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {statsSummary && (
        <div className="grid grid-cols-3 gap-2 mt-4 pt-3 border-t border-slate-100">
          {statsSummary.map((st, i) => (
            <div key={i} className="text-center">
              <p className="text-[10px] uppercase font-semibold text-slate-400 truncate">
                {st.label}
              </p>
              <p className={cn("text-sm font-bold mt-0.5", st.color || "text-slate-800")}>
                {st.value}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
