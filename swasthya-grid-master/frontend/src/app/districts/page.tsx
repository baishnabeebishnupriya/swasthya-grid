"use client";

import React, { useState } from "react";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { Table, Column } from "@/components/common/Table";
import { Badge } from "@/components/common/Badge";
import { MetricCard } from "@/components/common/MetricCard";
import { Compass, Search, MapPin } from "lucide-react";

interface DistrictOverviewData {
  id: string;
  name: string;
  state: string;
  phcs: number;
  chcs: number;
  bedsTotal: number;
  medicineAvailability: number;
  status: "Optimal" | "Surge Alert" | "Stockout Risk";
}

const MOCK_DISTRICTS: DistrictOverviewData[] = [
  {
    id: "DST-01",
    name: "Khordha (Bhubaneswar)",
    state: "Odisha",
    phcs: 48,
    chcs: 12,
    bedsTotal: 2400,
    medicineAvailability: 95.2,
    status: "Optimal",
  },
  {
    id: "DST-02",
    name: "Cuttack",
    state: "Odisha",
    phcs: 42,
    chcs: 10,
    bedsTotal: 2800,
    medicineAvailability: 88.4,
    status: "Stockout Risk",
  },
  {
    id: "DST-03",
    name: "Puri",
    state: "Odisha",
    phcs: 36,
    chcs: 8,
    bedsTotal: 1200,
    medicineAvailability: 90.1,
    status: "Surge Alert",
  },
  {
    id: "DST-04",
    name: "Balasore",
    state: "Odisha",
    phcs: 38,
    chcs: 9,
    bedsTotal: 1500,
    medicineAvailability: 91.5,
    status: "Surge Alert",
  },
  {
    id: "DST-05",
    name: "Ganjam",
    state: "Odisha",
    phcs: 54,
    chcs: 14,
    bedsTotal: 2200,
    medicineAvailability: 93.8,
    status: "Optimal",
  },
];

export default function DistrictsPage() {
  const [searchTerm, setSearchTerm] = useState("");

  const filtered = MOCK_DISTRICTS.filter((d) =>
    d.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    d.state.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const columns: Column<DistrictOverviewData>[] = [
    {
      header: "District Name",
      cell: (row) => (
        <div>
          <div className="font-bold text-slate-900 text-sm">{row.name}</div>
          <div className="text-slate-400 text-xs">{row.state}</div>
        </div>
      ),
    },
    {
      header: "Facilities",
      cell: (row) => (
        <span className="text-xs font-medium text-slate-700">
          {row.phcs} PHCs • {row.chcs} CHCs
        </span>
      ),
    },
    {
      header: "Total Beds",
      cell: (row) => <span className="font-semibold text-xs">{row.bedsTotal} Beds</span>,
    },
    {
      header: "Medicine Availability",
      cell: (row) => (
        <span className="font-mono text-teal-700 font-bold text-xs">
          {row.medicineAvailability}%
        </span>
      ),
    },
    {
      header: "District Health Status",
      cell: (row) => (
        <Badge
          variant={
            row.status === "Optimal"
              ? "success"
              : row.status === "Surge Alert"
              ? "warning"
              : "danger"
          }
          size="sm"
          dot
        >
          {row.status}
        </Badge>
      ),
    },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2.5">
            <Compass className="w-6 h-6 text-teal-600" />
            <span>District Health Infrastructure & Allocation</span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Granular district-level oversight of healthcare resource densities and supply chain responsiveness.
          </p>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="relative w-full md:w-80">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search district name..."
              className="w-full pl-9 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-teal-500"
            />
          </div>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden p-4">
          <Table columns={columns} data={filtered} keyExtractor={(r) => r.id} />
        </div>
      </div>
    </DashboardLayout>
  );
}
