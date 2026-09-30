"use client";

import React from "react";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { ChartPlaceholder } from "@/components/common/ChartPlaceholder";
import { MetricCard } from "@/components/common/MetricCard";
import { TrendingUp, Sparkles, AlertCircle, CheckCircle2 } from "lucide-react";

export default function ForecastsPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2.5">
            <TrendingUp className="w-6 h-6 text-teal-600" />
            <span>AI Predictive Demand & Epidemiological Forecasts</span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Machine learning forecast models predicting 14-day patient footfall surges, anti-venom and antibiotic consumption spikes, and bed demand.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <MetricCard
            title="14-Day Demand Forecast"
            value="+18.4%"
            subtitle="Monsoon Infection Cycle"
            iconName="TrendingUp"
            statusBadge="Active Model"
            statusVariant="primary"
          />
          <MetricCard
            title="Forecast Confidence"
            value="91.8%"
            subtitle="ARIMA + LightGBM Ensemble"
            iconName="Sparkles"
            statusBadge="High Confidence"
            statusVariant="teal"
          />
          <MetricCard
            title="Proactive Transfers Suggested"
            value="12"
            subtitle="To avert anticipated stockouts"
            iconName="ArrowRightLeft"
            statusBadge="Suggested"
            statusVariant="warning"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ChartPlaceholder
            title="Predicted Patient Outpatient Footfall (Next 14 Days)"
            subtitle="Aggregated baseline vs AI projected patient volume across coastal districts"
            type="area"
            height="h-64"
            statsSummary={[
              { label: "Current Footfall", value: "28,400 / day", color: "text-slate-800" },
              { label: "Predicted Peak", value: "33,600 / day", color: "text-teal-600" },
              { label: "Peak Date", value: "Aug 29, 2026", color: "text-amber-600" },
            ]}
          />

          <ChartPlaceholder
            title="Critical Medicine Consumption Velocity"
            subtitle="Projected depletion rates for essential anti-infective medications"
            type="bar"
            height="h-64"
            statsSummary={[
              { label: "Amoxicillin", value: "94% velocity", color: "text-rose-600" },
              { label: "Oral Rehydration (ORS)", value: "78% velocity", color: "text-amber-600" },
              { label: "Paracetamol", value: "45% velocity", color: "text-teal-600" },
            ]}
          />
        </div>
      </div>
    </DashboardLayout>
  );
}
