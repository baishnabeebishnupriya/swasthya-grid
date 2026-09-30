"use client";

import React, { useState } from "react";
import Link from "next/link";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { MetricCard } from "@/components/common/MetricCard";
import { Badge } from "@/components/common/Badge";
import { Table, Column } from "@/components/common/Table";
import { ChartPlaceholder } from "@/components/common/ChartPlaceholder";
import {
  Building2,
  Activity,
  AlertTriangle,
  ArrowRightLeft,
  ArrowUpRight,
  ShieldAlert,
  Calendar,
  CheckCircle2,
  Clock,
  MapPin,
  RefreshCw,
  SlidersHorizontal,
  ChevronRight,
  Layers,
  Sparkles,
} from "lucide-react";
import { ResourceTransfer, RiskAlert } from "@/types";
import { formatNumber, formatDate } from "@/utils/formatters";

// Mock data for initial realistic government healthcare presentation
const MOCK_CRITICAL_ALERTS: RiskAlert[] = [
  {
    id: "ALT-801",
    facilityId: "PHC-CTC-04",
    facilityName: "Tangi Community Health Centre",
    district: "Cuttack",
    state: "Odisha",
    category: "Stockout",
    severity: "Critical",
    headline: "Amoxicillin & IV Saline Stockout Imminent (< 36 hrs)",
    description: "Consumption surge detected due to seasonal gastrointestinal infections. 80 units remaining.",
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
];

const MOCK_TRANSFERS: ResourceTransfer[] = [
  {
    id: "TR-2041",
    transferCode: "TR-OD-2026-9041",
    sourceFacilityName: "Capital Hospital Depot",
    sourceDistrict: "Bhubaneswar",
    targetFacilityName: "Pipili Primary Health Centre",
    targetDistrict: "Puri",
    resourceType: "Medicines",
    itemName: "Amoxicillin 500mg (1,000 vials)",
    quantity: 1000,
    unit: "Vials",
    urgency: "Urgent",
    status: "In Transit",
    requestedAt: "2026-08-23T07:10:00Z",
    estimatedArrival: "Today, 15:30 IST",
  },
  {
    id: "TR-2042",
    transferCode: "TR-OD-2026-9042",
    sourceFacilityName: "SCB Medical College Store",
    sourceDistrict: "Cuttack",
    targetFacilityName: "Tangi CHC",
    targetDistrict: "Cuttack",
    resourceType: "Oxygen Cylinders",
    itemName: "Type-D High Pressure O2 Cylinders",
    quantity: 25,
    unit: "Cylinders",
    urgency: "Critical",
    status: "Dispatched",
    requestedAt: "2026-08-23T09:45:00Z",
    estimatedArrival: "Today, 14:00 IST",
  },
  {
    id: "TR-2043",
    transferCode: "TR-OD-2026-9043",
    sourceFacilityName: "District Reserve Depot",
    sourceDistrict: "Balasore",
    targetFacilityName: "Jaleswar CHC",
    targetDistrict: "Balasore",
    resourceType: "Medical Consumables",
    itemName: "Sterile Surgical Kits & Gloves",
    quantity: 450,
    unit: "Kits",
    urgency: "Routine",
    status: "Approved",
    requestedAt: "2026-08-23T10:00:00Z",
    estimatedArrival: "Tomorrow, 11:00 IST",
  },
];

export default function DashboardPage() {
  const [selectedState, setSelectedState] = useState("Odisha (NH-16 Corridor)");
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 600);
  };

  // Columns for Critical Risk Alerts Table
  const alertColumns: Column<RiskAlert>[] = [
    {
      header: "Severity / Time",
      cell: (row) => (
        <div className="flex items-center gap-2">
          <Badge
            variant={
              row.severity === "Critical"
                ? "danger"
                : row.severity === "High"
                ? "warning"
                : "neutral"
            }
            size="sm"
            dot
          >
            {row.severity}
          </Badge>
          <span className="text-slate-400 font-mono text-[11px]">
            {row.predictedImpactTimeframe}
          </span>
        </div>
      ),
    },
    {
      header: "Facility & Location",
      cell: (row) => (
        <div>
          <div className="font-semibold text-slate-800">{row.facilityName}</div>
          <div className="text-slate-400 text-xs flex items-center gap-1">
            <MapPin className="w-3 h-3 text-slate-400" />
            <span>{row.district}, {row.state}</span>
          </div>
        </div>
      ),
    },
    {
      header: "Diagnosis / Risk Headline",
      cell: (row) => (
        <div className="max-w-md">
          <div className="font-medium text-slate-800 text-xs truncate">{row.headline}</div>
          <div className="text-slate-500 text-[11px] truncate mt-0.5">{row.description}</div>
        </div>
      ),
    },
    {
      header: "AI Recommendation",
      cell: (row) => (
        <div className="flex items-center gap-1.5 text-xs text-teal-700 bg-teal-50 px-2.5 py-1 rounded-md border border-teal-100 max-w-xs truncate">
          <Sparkles className="w-3.5 h-3.5 shrink-0 text-teal-600" />
          <span className="truncate">{row.recommendedAction}</span>
        </div>
      ),
    },
    {
      header: "Action",
      cell: (row) => (
        <Link
          href={`/risks`}
          className="inline-flex items-center gap-1 text-xs font-semibold text-teal-700 hover:text-teal-900 bg-white hover:bg-slate-50 border border-slate-200 px-2.5 py-1 rounded-md shadow-2xs transition-colors"
        >
          <span>Respond</span>
          <ChevronRight className="w-3 h-3" />
        </Link>
      ),
    },
  ];

  // Columns for Resource Transfers Table
  const transferColumns: Column<ResourceTransfer>[] = [
    {
      header: "Transfer Code",
      cell: (row) => (
        <span className="font-mono font-bold text-xs text-slate-700">
          {row.transferCode}
        </span>
      ),
    },
    {
      header: "Source → Destination",
      cell: (row) => (
        <div className="text-xs">
          <div className="font-semibold text-slate-800">{row.sourceFacilityName} ({row.sourceDistrict})</div>
          <div className="text-teal-700 font-medium flex items-center gap-1 mt-0.5">
            <span>↳ {row.targetFacilityName} ({row.targetDistrict})</span>
          </div>
        </div>
      ),
    },
    {
      header: "Resource Item",
      cell: (row) => (
        <div>
          <div className="font-medium text-slate-800 text-xs">{row.itemName}</div>
          <div className="text-slate-500 text-[11px]">{row.resourceType}</div>
        </div>
      ),
    },
    {
      header: "Status",
      cell: (row) => (
        <Badge
          variant={
            row.status === "In Transit"
              ? "info"
              : row.status === "Dispatched"
              ? "teal"
              : row.status === "Approved"
              ? "primary"
              : "neutral"
          }
          size="sm"
          dot
        >
          {row.status}
        </Badge>
      ),
    },
    {
      header: "ETA",
      cell: (row) => (
        <div className="text-xs text-slate-600 font-medium flex items-center gap-1">
          <Clock className="w-3.5 h-3.5 text-slate-400" />
          <span>{row.estimatedArrival || "Pending"}</span>
        </div>
      ),
    },
  ];

  return (
    <DashboardLayout>
      {/* ── TOP EXECUTIVE BANNER ── */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-teal-950 text-white rounded-2xl p-6 shadow-sm border border-slate-800 relative overflow-hidden">
        {/* Background Network Graphic Overlay */}
        <div className="absolute right-0 top-0 bottom-0 w-96 opacity-10 pointer-events-none hidden md:block">
          <svg viewBox="0 0 200 200" className="w-full h-full text-white fill-current">
            <circle cx="40" cy="40" r="8" />
            <circle cx="120" cy="60" r="12" />
            <circle cx="160" cy="140" r="10" />
            <circle cx="60" cy="160" r="6" />
            <line x1="40" y1="40" x2="120" y2="60" stroke="white" strokeWidth="2" />
            <line x1="120" y1="60" x2="160" y2="140" stroke="white" strokeWidth="2" />
            <line x1="160" y1="140" x2="60" y2="160" stroke="white" strokeWidth="2" />
          </svg>
        </div>

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-teal-900/60 border border-teal-500/30 text-teal-300 text-[11px] font-mono font-semibold uppercase tracking-wider">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              <span>National Health Infrastructure Command</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              SwasthyaGrid Operational Telemetry
            </h1>
            <p className="text-xs sm:text-sm text-slate-300 max-w-2xl">
              Real-time monitoring of Primary Health Centres, critical drug availability, emergency bed surges, and automated inter-facility resource balancing.
            </p>
          </div>

          <div className="flex items-center gap-3 self-start md:self-auto">
            <button
              onClick={handleRefresh}
              className="px-3.5 py-2 bg-slate-800/90 hover:bg-slate-700 border border-slate-700 text-white rounded-lg text-xs font-semibold flex items-center gap-2 transition-all cursor-pointer shadow-xs active:scale-95"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? "animate-spin text-teal-400" : ""}`} />
              <span>Refresh Telemetry</span>
            </button>

            <Link
              href="/transfers"
              className="px-4 py-2 bg-teal-600 hover:bg-teal-500 text-white rounded-lg text-xs font-bold flex items-center gap-2 transition-all shadow-xs cursor-pointer active:scale-95"
            >
              <ArrowRightLeft className="w-3.5 h-3.5" />
              <span>New Resource Transfer</span>
            </Link>
          </div>
        </div>
      </div>

      {/* ── 7 PRIMARY HEALTHCARE METRIC CARDS ── */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-600 font-mono">
            Core Infrastructure Indicators
          </h2>
          <span className="text-xs text-slate-500 font-medium">
            Active Region: <strong>{selectedState}</strong>
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* 1. Total Health Facilities */}
          <MetricCard
            title="Total Health Facilities"
            value="1,248"
            subtitle="Across 30 Districts"
            change="+12 this quarter"
            changeType="positive"
            iconName="Building2"
            statusBadge="100% Mapped"
            statusVariant="primary"
            highlightBorder="blue"
          />

          {/* 2. Active PHCs */}
          <MetricCard
            title="Active PHCs"
            value="892"
            subtitle="88 CHCs + 42 Dist. Hospitals"
            change="98.6% Operational"
            changeType="positive"
            iconName="Activity"
            statusBadge="Online"
            statusVariant="success"
            highlightBorder="teal"
          />

          {/* 3. Medicine Availability */}
          <MetricCard
            title="Medicine Availability"
            value="92.4%"
            subtitle="Essential Drug List (EDL)"
            change="-1.2% buffer risk"
            changeType="warning"
            iconName="Pill"
            statusBadge="Stable Buffer"
            statusVariant="teal"
            highlightBorder="none"
          />

          {/* 4. Bed Availability */}
          <MetricCard
            title="Bed Availability"
            value="74.8%"
            subtitle="14,280 / 19,100 Occupied"
            change="4,820 Ready Beds"
            changeType="positive"
            iconName="BedDouble"
            statusBadge="Surge Ready"
            statusVariant="info"
            highlightBorder="none"
          />

          {/* 5. Staff Strength */}
          <MetricCard
            title="Staff Strength"
            value="6,420"
            subtitle="Doctors, Nurses, MOs & ANMs"
            change="91.4% Attendance"
            changeType="positive"
            iconName="Users"
            statusBadge="On Duty"
            statusVariant="success"
            highlightBorder="none"
          />

          {/* 6. Critical Alerts */}
          <MetricCard
            title="Critical Alerts"
            value="3"
            subtitle="Action required within 48h"
            change="2 Stockouts, 1 Outbreak"
            changeType="negative"
            iconName="AlertTriangle"
            statusBadge="Urgent Action"
            statusVariant="danger"
            highlightBorder="rose"
          />

          {/* 7. Pending Resource Transfers */}
          <MetricCard
            title="Pending Transfers"
            value="8"
            subtitle="4 Dispatched, 4 Approved"
            change="Avg transit 3.4 hrs"
            changeType="neutral"
            iconName="ArrowRightLeft"
            statusBadge="Balancing Active"
            statusVariant="warning"
            highlightBorder="amber"
          />

          {/* 8. Predictive Risk Index (Bonus Healthcare Resilience Metric) */}
          <MetricCard
            title="Resilience Score"
            value="88.2"
            subtitle="AI Corridor Readiness Score"
            change="High Network Resilience"
            changeType="positive"
            iconName="ShieldAlert"
            statusBadge="Tier 1 Grade"
            statusVariant="teal"
            highlightBorder="teal"
          />
        </div>
      </div>

      {/* ── VISUAL ANALYTICS & CHARTS SECTION ── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Corridor Bed Capacity Distribution */}
        <ChartPlaceholder
          title="Regional Bed Occupancy & Surge Capacity"
          subtitle="Real-time bed utilization across major district healthcare clusters"
          type="bar"
          height="h-56"
          statsSummary={[
            { label: "Total Bed Pool", value: "19,100", color: "text-slate-900" },
            { label: "ICU Available", value: "482 Beds", color: "text-teal-600" },
            { label: "Peak Cluster", value: "Balasore (94%)", color: "text-amber-600" },
          ]}
        />

        {/* Essential Medicine Stock Distribution */}
        <ChartPlaceholder
          title="Primary Facility Tier Breakdown"
          subtitle="Distribution of registered healthcare units across the public grid"
          type="donut"
          height="h-56"
          statsSummary={[
            { label: "PHCs", value: "892 Units", color: "text-teal-600" },
            { label: "CHCs", value: "268 Units", color: "text-blue-600" },
            { label: "Hospitals", value: "88 Units", color: "text-amber-600" },
          ]}
        />
      </div>

      {/* ── CRITICAL RISK ALERTS TABLE ── */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h3 className="text-sm font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-rose-600" />
              <span>Critical Health Resource Vulnerabilities & Early Warnings</span>
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Automated AI risk detection evaluating stockout risks, surge demands, and staffing deficits.
            </p>
          </div>

          <Link
            href="/risks"
            className="text-xs font-semibold text-teal-700 hover:text-teal-800 flex items-center gap-1 self-start sm:self-auto"
          >
            <span>View All Risk Forecasts</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="p-4">
          <Table
            columns={alertColumns}
            data={MOCK_CRITICAL_ALERTS}
            keyExtractor={(row) => row.id}
          />
        </div>
      </div>

      {/* ── PENDING RESOURCE TRANSFERS TABLE ── */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h3 className="text-sm font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <ArrowRightLeft className="w-4 h-4 text-teal-600" />
              <span>Active Inter-Facility Resource Transfers</span>
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Live logistics tracking of dispatched medicines, oxygen supplies, and critical consumables.
            </p>
          </div>

          <Link
            href="/transfers"
            className="text-xs font-semibold text-teal-700 hover:text-teal-800 flex items-center gap-1 self-start sm:self-auto"
          >
            <span>Transfer Management Ledger</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="p-4">
          <Table
            columns={transferColumns}
            data={MOCK_TRANSFERS}
            keyExtractor={(row) => row.id}
          />
        </div>
      </div>
    </DashboardLayout>
  );
}
