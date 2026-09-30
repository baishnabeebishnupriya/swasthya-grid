"use client";

import React, { useState } from "react";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { Table, Column } from "@/components/common/Table";
import { Badge } from "@/components/common/Badge";
import { MetricCard } from "@/components/common/MetricCard";
import { AlertTriangle, ShieldAlert, Sparkles, MapPin, Search, ChevronRight } from "lucide-react";
import { RiskAlert } from "@/types";

const MOCK_EXTENDED_RISKS: RiskAlert[] = [
  {
    id: "ALT-801",
    facilityId: "PHC-CTC-04",
    facilityName: "Tangi Community Health Centre",
    district: "Cuttack",
    state: "Odisha",
    category: "Stockout",
    severity: "Critical",
    headline: "Amoxicillin & IV Saline Stockout Imminent (< 36 hrs)",
    description: "Consumption surge detected due to seasonal gastrointestinal infections. 80 units remaining in buffer.",
    predictedImpactTimeframe: "36 Hours",
    recommendedAction: "Trigger emergency transfer from SCB Medical College Depot",
    confidenceScore: 94.2,
    createdAt: "2026-08-23T06:30:00Z",
    isResolved: false,
  },
  {
    id: "ALT-802",
    facilityId: "PHC-PURI-09",
    facilityName: "Konark Primary Health Centre",
    district: "Puri",
    state: "Odisha",
    category: "Disease Outbreak Surge",
    severity: "High",
    headline: "Vector-Borne Case Cluster Detected in Gop Block",
    description: "Dengue antigen positive rate increased by 42% over previous 7-day baseline.",
    predictedImpactTimeframe: "48-72 Hours",
    recommendedAction: "Pre-position rapid test kits and mosquito bed nets",
    confidenceScore: 89.5,
    createdAt: "2026-08-23T08:15:00Z",
    isResolved: false,
  },
  {
    id: "ALT-803",
    facilityId: "PHC-BLS-02",
    facilityName: "Soro Sub-Divisional Hospital",
    district: "Balasore",
    state: "Odisha",
    category: "Staff Shortage",
    severity: "Moderate",
    headline: "Night Shift Anesthetist & Trauma Nurse Deficit",
    description: "Emergency surgical coverage constrained for upcoming weekend duty roster.",
    predictedImpactTimeframe: "5 Days",
    recommendedAction: "Deploy roster reallocation from District HQ",
    confidenceScore: 82.0,
    createdAt: "2026-08-23T09:00:00Z",
    isResolved: false,
  },
  {
    id: "ALT-804",
    facilityId: "PHC-BBI-01",
    facilityName: "Capital Hospital Peripheral Post",
    district: "Bhubaneswar",
    state: "Odisha",
    category: "Infrastructure",
    severity: "Low",
    headline: "Backup Generator Fuel Level at 28%",
    description: "Cold-chain chiller backup power integrity requires fuel replenishment.",
    predictedImpactTimeframe: "7 Days",
    recommendedAction: "Dispatch routine diesel generator maintenance requisition",
    confidenceScore: 78.4,
    createdAt: "2026-08-23T09:40:00Z",
    isResolved: false,
  },
];

export default function RisksPage() {
  const [searchTerm, setSearchTerm] = useState("");

  const filtered = MOCK_EXTENDED_RISKS.filter((r) =>
    r.headline.toLowerCase().includes(searchTerm.toLowerCase()) ||
    r.facilityName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    r.district.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const columns: Column<RiskAlert>[] = [
    {
      header: "Severity / Category",
      cell: (row) => (
        <div>
          <Badge
            variant={
              row.severity === "Critical"
                ? "danger"
                : row.severity === "High"
                ? "warning"
                : row.severity === "Moderate"
                ? "teal"
                : "neutral"
            }
            size="sm"
            dot
          >
            {row.severity}
          </Badge>
          <div className="text-slate-400 text-[11px] mt-1">{row.category}</div>
        </div>
      ),
    },
    {
      header: "Facility & Location",
      cell: (row) => (
        <div>
          <div className="font-bold text-slate-900 text-sm">{row.facilityName}</div>
          <div className="text-slate-500 text-xs flex items-center gap-1">
            <MapPin className="w-3 h-3 text-slate-400" />
            <span>{row.district}, {row.state}</span>
          </div>
        </div>
      ),
    },
    {
      header: "Risk Prediction Description",
      cell: (row) => (
        <div className="max-w-md">
          <div className="font-semibold text-slate-800 text-xs">{row.headline}</div>
          <div className="text-slate-500 text-[11px] mt-0.5">{row.description}</div>
        </div>
      ),
    },
    {
      header: "Impact Timeframe",
      cell: (row) => (
        <span className="font-mono font-bold text-xs text-rose-600">
          {row.predictedImpactTimeframe}
        </span>
      ),
    },
    {
      header: "AI Recommendation",
      cell: (row) => (
        <div className="text-xs text-teal-800 bg-teal-50 border border-teal-100 p-2 rounded-lg flex items-center gap-1.5 max-w-xs">
          <Sparkles className="w-4 h-4 text-teal-600 shrink-0" />
          <span>{row.recommendedAction}</span>
        </div>
      ),
    },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2.5">
            <AlertTriangle className="w-6 h-6 text-rose-600" />
            <span>Predictive Risk Alerts & Early Warning System</span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            AI-driven anomaly detection identifying medicine stockout threats, sudden disease surges, and resource bottlenecks before they impact patient care.
          </p>
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <MetricCard
            title="Active Risk Warnings"
            value="4"
            subtitle="Across Regional Network"
            iconName="AlertTriangle"
            statusBadge="Active Warnings"
            statusVariant="danger"
            highlightBorder="rose"
          />
          <MetricCard
            title="Critical Stockouts"
            value="1"
            subtitle="< 36h Remaining"
            iconName="ShieldAlert"
            statusBadge="Urgent Action"
            statusVariant="danger"
          />
          <MetricCard
            title="AI Prediction Accuracy"
            value="94.2%"
            subtitle="Validated on Historical Outbreaks"
            iconName="Sparkles"
            statusBadge="Model v2.4"
            statusVariant="teal"
          />
          <MetricCard
            title="Resolved This Month"
            value="38"
            subtitle="Zero Preventable Stockouts"
            iconName="Activity"
            statusBadge="High Resilience"
            statusVariant="success"
          />
        </div>

        {/* Filter */}
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="relative w-full md:w-96">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search risk alerts by facility, district, headline..."
              className="w-full pl-9 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-teal-500"
            />
          </div>
        </div>

        {/* Table */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden p-4">
          <Table columns={columns} data={filtered} keyExtractor={(r) => r.id} />
        </div>
      </div>
    </DashboardLayout>
  );
}
