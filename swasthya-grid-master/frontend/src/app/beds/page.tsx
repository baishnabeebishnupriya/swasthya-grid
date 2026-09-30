"use client";

import React, { useState } from "react";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { Table, Column } from "@/components/common/Table";
import { Badge } from "@/components/common/Badge";
import { MetricCard } from "@/components/common/MetricCard";
import { BedDouble, Search, Activity, ShieldCheck, HeartPulse, Plus } from "lucide-react";
import { BedAllocation } from "@/types";

const MOCK_BEDS: BedAllocation[] = [
  {
    id: "BED-01",
    facilityId: "PHC-104",
    facilityName: "Soro Sub-Divisional Hospital",
    totalBeds: 120,
    occupiedBeds: 112,
    availableBeds: 8,
    icuBedsTotal: 12,
    icuBedsOccupied: 11,
    oxygenSupportedBeds: 45,
    occupancyRate: 93.3,
    status: "Near Capacity",
  },
  {
    id: "BED-02",
    facilityId: "PHC-102",
    facilityName: "Tangi Community Health Centre",
    totalBeds: 60,
    occupiedBeds: 48,
    availableBeds: 12,
    icuBedsTotal: 4,
    icuBedsOccupied: 3,
    oxygenSupportedBeds: 20,
    occupancyRate: 80.0,
    status: "High Occupancy",
  },
  {
    id: "BED-03",
    facilityId: "PHC-103",
    facilityName: "Konark Primary Health Centre",
    totalBeds: 30,
    occupiedBeds: 28,
    availableBeds: 2,
    icuBedsTotal: 0,
    icuBedsOccupied: 0,
    oxygenSupportedBeds: 8,
    occupancyRate: 93.3,
    status: "Near Capacity",
  },
  {
    id: "BED-04",
    facilityId: "PHC-101",
    facilityName: "Pipili Primary Health Centre",
    totalBeds: 24,
    occupiedBeds: 14,
    availableBeds: 10,
    icuBedsTotal: 0,
    icuBedsOccupied: 0,
    oxygenSupportedBeds: 6,
    occupancyRate: 58.3,
    status: "Normal",
  },
  {
    id: "BED-05",
    facilityId: "PHC-105",
    facilityName: "Jatni Urban Primary Health Centre",
    totalBeds: 20,
    occupiedBeds: 11,
    availableBeds: 9,
    icuBedsTotal: 0,
    icuBedsOccupied: 0,
    oxygenSupportedBeds: 4,
    occupancyRate: 55.0,
    status: "Normal",
  },
];

export default function BedsPage() {
  const [searchTerm, setSearchTerm] = useState("");

  const filtered = MOCK_BEDS.filter((b) =>
    b.facilityName.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const columns: Column<BedAllocation>[] = [
    {
      header: "Healthcare Facility",
      cell: (row) => (
        <div>
          <div className="font-bold text-slate-900 text-sm">{row.facilityName}</div>
          <div className="text-slate-400 text-xs font-mono">{row.facilityId}</div>
        </div>
      ),
    },
    {
      header: "General Bed Pool",
      cell: (row) => (
        <div className="w-32">
          <div className="flex justify-between text-xs mb-1">
            <span className="font-semibold text-slate-800">{row.occupiedBeds}/{row.totalBeds}</span>
            <span className="text-slate-500">{row.occupancyRate}%</span>
          </div>
          <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
            <div
              style={{ width: `${row.occupancyRate}%` }}
              className={`h-full ${
                row.occupancyRate > 90
                  ? "bg-rose-500"
                  : row.occupancyRate > 75
                  ? "bg-amber-500"
                  : "bg-teal-600"
              }`}
            />
          </div>
        </div>
      ),
    },
    {
      header: "Available Beds",
      cell: (row) => (
        <span className="font-bold text-teal-700 text-sm">
          {row.availableBeds} Ready
        </span>
      ),
    },
    {
      header: "ICU Beds",
      cell: (row) => (
        <span className="text-xs font-medium text-slate-700">
          {row.icuBedsTotal > 0 ? `${row.icuBedsOccupied}/${row.icuBedsTotal} Occupied` : "N/A (Referral)"}
        </span>
      ),
    },
    {
      header: "O2 Supported Beds",
      cell: (row) => (
        <span className="text-xs font-semibold text-slate-800">
          {row.oxygenSupportedBeds} Active
        </span>
      ),
    },
    {
      header: "Capacity Status",
      cell: (row) => (
        <Badge
          variant={
            row.status === "Normal"
              ? "success"
              : row.status === "High Occupancy"
              ? "teal"
              : row.status === "Near Capacity"
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
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2.5">
              <BedDouble className="w-6 h-6 text-teal-600" />
              <span>Bed Availability & Emergency Surge Management</span>
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Live census of general ward beds, ICU units, and oxygen-supported beds across the public health grid.
            </p>
          </div>

          <button className="px-4 py-2 bg-teal-600 hover:bg-teal-500 text-white rounded-lg text-xs font-bold flex items-center gap-2 shadow-xs cursor-pointer self-start sm:self-auto">
            <Plus className="w-4 h-4" />
            <span>Update Facility Census</span>
          </button>
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <MetricCard
            title="Total Bed Capacity"
            value="19,100"
            subtitle="Mapped Public Beds"
            iconName="BedDouble"
            statusBadge="Active Pool"
            statusVariant="primary"
          />
          <MetricCard
            title="Currently Occupied"
            value="14,280"
            subtitle="74.8% Average Occupancy"
            iconName="Activity"
            statusBadge="Normal Load"
            statusVariant="teal"
          />
          <MetricCard
            title="Available Vacancies"
            value="4,820"
            subtitle="Immediate Admission Ready"
            iconName="ShieldCheck"
            statusBadge="Ready"
            statusVariant="success"
          />
          <MetricCard
            title="Surge Critical Units"
            value="3 Facilities"
            subtitle="> 90% Occupancy"
            iconName="HeartPulse"
            statusBadge="Surge Risk"
            statusVariant="danger"
            highlightBorder="rose"
          />
        </div>

        {/* Filter */}
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="relative w-full md:w-80">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search facility name..."
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
