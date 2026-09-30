"use client";

import React from "react";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { Table, Column } from "@/components/common/Table";
import { Badge } from "@/components/common/Badge";
import { MetricCard } from "@/components/common/MetricCard";
import { Map, Building2, CheckCircle2, TrendingUp } from "lucide-react";

interface StateOverviewData {
  id: string;
  name: string;
  districtsCount: number;
  totalFacilities: number;
  medicineAvailability: number;
  bedOccupancy: number;
  riskStatus: "Optimal" | "Surge Alert" | "Stockout Risk";
}

const MOCK_STATES: StateOverviewData[] = [
  {
    id: "ST-01",
    name: "Odisha",
    districtsCount: 30,
    totalFacilities: 1248,
    medicineAvailability: 92.4,
    bedOccupancy: 74.8,
    riskStatus: "Optimal",
  },
  {
    id: "ST-02",
    name: "West Bengal",
    districtsCount: 23,
    totalFacilities: 1840,
    medicineAvailability: 89.2,
    bedOccupancy: 81.5,
    riskStatus: "Surge Alert",
  },
  {
    id: "ST-03",
    name: "Jharkhand",
    districtsCount: 24,
    totalFacilities: 960,
    medicineAvailability: 86.8,
    bedOccupancy: 68.2,
    riskStatus: "Optimal",
  },
  {
    id: "ST-04",
    name: "Andhra Pradesh",
    districtsCount: 26,
    totalFacilities: 1420,
    medicineAvailability: 94.0,
    bedOccupancy: 72.0,
    riskStatus: "Optimal",
  },
];

export default function StatesPage() {
  const columns: Column<StateOverviewData>[] = [
    {
      header: "State Name",
      cell: (row) => (
        <span className="font-bold text-slate-900 text-sm">{row.name}</span>
      ),
    },
    {
      header: "Districts Mapped",
      cell: (row) => <span>{row.districtsCount} Districts</span>,
    },
    {
      header: "Total Facilities",
      cell: (row) => <span className="font-semibold">{row.totalFacilities} Units</span>,
    },
    {
      header: "Medicine Availability",
      cell: (row) => (
        <span className="font-mono text-teal-700 font-bold">
          {row.medicineAvailability}%
        </span>
      ),
    },
    {
      header: "Bed Occupancy",
      cell: (row) => (
        <span className="font-mono text-slate-700 font-bold">
          {row.bedOccupancy}%
        </span>
      ),
    },
    {
      header: "Grid Status",
      cell: (row) => (
        <Badge
          variant={
            row.riskStatus === "Optimal"
              ? "success"
              : row.riskStatus === "Surge Alert"
              ? "warning"
              : "danger"
          }
          size="sm"
          dot
        >
          {row.riskStatus}
        </Badge>
      ),
    },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2.5">
            <Map className="w-6 h-6 text-teal-600" />
            <span>State-Level Health Grid Aggregation</span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Macro public health indicators, inter-state corridor health readiness, and national healthcare balancing.
          </p>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden p-4">
          <Table columns={columns} data={MOCK_STATES} keyExtractor={(r) => r.id} />
        </div>
      </div>
    </DashboardLayout>
  );
}
