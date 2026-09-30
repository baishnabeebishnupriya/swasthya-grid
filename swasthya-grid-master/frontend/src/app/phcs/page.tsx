"use client";

import React, { useState } from "react";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { Table, Column } from "@/components/common/Table";
import { Badge } from "@/components/common/Badge";
import { MetricCard } from "@/components/common/MetricCard";
import { Building2, Search, Filter, Plus, MapPin, Phone, User, CheckCircle2 } from "lucide-react";
import { HealthFacility } from "@/types";

const MOCK_PHCS: HealthFacility[] = [
  {
    id: "PHC-101",
    name: "Pipili Primary Health Centre",
    code: "PHC-OD-PURI-001",
    type: "PHC",
    state: "Odisha",
    district: "Puri",
    block: "Pipili",
    pincode: "752104",
    latitude: 20.1172,
    longitude: 85.8319,
    contactPerson: "Dr. Alok Pattnaik",
    phone: "+91 94370 12345",
    totalBeds: 24,
    occupiedBeds: 18,
    staffCount: 14,
    status: "Operational",
    lastUpdated: "2026-08-23T08:00:00Z",
  },
  {
    id: "PHC-102",
    name: "Tangi Community Health Centre",
    code: "CHC-OD-CTC-004",
    type: "CHC",
    state: "Odisha",
    district: "Cuttack",
    block: "Tangi-Choudwar",
    pincode: "754022",
    latitude: 20.5934,
    longitude: 85.9612,
    contactPerson: "Dr. Sunita Behera",
    phone: "+91 94371 67890",
    totalBeds: 60,
    occupiedBeds: 54,
    staffCount: 38,
    status: "Stockout Risk",
    lastUpdated: "2026-08-23T08:30:00Z",
  },
  {
    id: "PHC-103",
    name: "Konark Primary Health Centre",
    code: "PHC-OD-PURI-009",
    type: "PHC",
    state: "Odisha",
    district: "Puri",
    block: "Gop",
    pincode: "752111",
    latitude: 19.8876,
    longitude: 86.0945,
    contactPerson: "Dr. Manoj Das",
    phone: "+91 94372 11223",
    totalBeds: 30,
    occupiedBeds: 28,
    staffCount: 16,
    status: "Critical Alert",
    lastUpdated: "2026-08-23T09:15:00Z",
  },
  {
    id: "PHC-104",
    name: "Soro Sub-Divisional Hospital",
    code: "SDH-OD-BLS-002",
    type: "SDH",
    state: "Odisha",
    district: "Balasore",
    block: "Soro",
    pincode: "756045",
    latitude: 21.2891,
    longitude: 86.6892,
    contactPerson: "Dr. R. K. Nayak",
    phone: "+91 94373 44556",
    totalBeds: 120,
    occupiedBeds: 112,
    staffCount: 64,
    status: "Surge Capacity",
    lastUpdated: "2026-08-23T07:45:00Z",
  },
  {
    id: "PHC-105",
    name: "Jatni Urban Primary Health Centre",
    code: "UPHC-OD-KRD-012",
    type: "PHC",
    state: "Odisha",
    district: "Khordha",
    block: "Jatni",
    pincode: "752050",
    latitude: 20.1611,
    longitude: 85.7088,
    contactPerson: "Dr. Geeta Rath",
    phone: "+91 94374 99887",
    totalBeds: 20,
    occupiedBeds: 12,
    staffCount: 12,
    status: "Operational",
    lastUpdated: "2026-08-23T09:30:00Z",
  },
];

export default function PhcNetworkPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [facilityFilter, setFacilityFilter] = useState("ALL");

  const filtered = MOCK_PHCS.filter((f) => {
    const matchSearch =
      f.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      f.district.toLowerCase().includes(searchTerm.toLowerCase()) ||
      f.code.toLowerCase().includes(searchTerm.toLowerCase());
    const matchType = facilityFilter === "ALL" || f.type === facilityFilter;
    return matchSearch && matchType;
  });

  const columns: Column<HealthFacility>[] = [
    {
      header: "Facility Code & Name",
      cell: (row) => (
        <div>
          <div className="font-bold text-slate-900 text-sm">{row.name}</div>
          <div className="text-slate-400 font-mono text-[11px]">{row.code}</div>
        </div>
      ),
    },
    {
      header: "Type",
      cell: (row) => (
        <Badge variant={row.type === "PHC" ? "teal" : row.type === "CHC" ? "primary" : "info"} size="sm">
          {row.type}
        </Badge>
      ),
    },
    {
      header: "District / State",
      cell: (row) => (
        <div className="text-xs text-slate-700">
          <div className="font-medium">{row.district}, {row.state}</div>
          <div className="text-slate-400 text-[11px]">PIN: {row.pincode}</div>
        </div>
      ),
    },
    {
      header: "Bed Capacity",
      cell: (row) => {
        const pct = Math.round((row.occupiedBeds / row.totalBeds) * 100);
        return (
          <div className="w-28 text-xs">
            <div className="flex justify-between text-slate-600 mb-1">
              <span>{row.occupiedBeds}/{row.totalBeds}</span>
              <span className="font-semibold">{pct}%</span>
            </div>
            <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
              <div
                style={{ width: `${pct}%` }}
                className={pct > 90 ? "bg-rose-500 h-full" : pct > 75 ? "bg-amber-500 h-full" : "bg-teal-600 h-full"}
              />
            </div>
          </div>
        );
      },
    },
    {
      header: "Staff Count",
      cell: (row) => (
        <span className="text-xs font-semibold text-slate-800">
          {row.staffCount} Active
        </span>
      ),
    },
    {
      header: "Status",
      cell: (row) => (
        <Badge
          variant={
            row.status === "Operational"
              ? "success"
              : row.status === "Stockout Risk"
              ? "warning"
              : row.status === "Critical Alert"
              ? "danger"
              : "info"
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
              <Building2 className="w-6 h-6 text-teal-600" />
              <span>Primary Healthcare Network (PHC & CHC Grid)</span>
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Comprehensive inventory of mapped public health facilities across districts and highway logistics corridors.
            </p>
          </div>

          <button className="px-4 py-2 bg-teal-600 hover:bg-teal-500 text-white rounded-lg text-xs font-bold flex items-center gap-2 shadow-xs cursor-pointer self-start sm:self-auto">
            <Plus className="w-4 h-4" />
            <span>Register Facility</span>
          </button>
        </div>

        {/* Top Summary Metrics */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <MetricCard
            title="Total Registered PHCs"
            value="892"
            subtitle="National Health Grid Mapped"
            iconName="Building2"
            statusBadge="Active Roster"
            statusVariant="success"
          />
          <MetricCard
            title="Community Health Centres"
            value="268"
            subtitle="Secondary Referral Nodes"
            iconName="Activity"
            statusBadge="Online"
            statusVariant="primary"
          />
          <MetricCard
            title="Surge Capacity Units"
            value="42"
            subtitle="Emergency Buffer Ready"
            iconName="ShieldAlert"
            statusBadge="Surge Active"
            statusVariant="teal"
          />
        </div>

        {/* Filter Bar */}
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex flex-col md:flex-row gap-3 items-center justify-between">
          <div className="relative w-full md:w-80">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by facility name, block, code..."
              className="w-full pl-9 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-teal-500"
            />
          </div>

          <div className="flex items-center gap-2 w-full md:w-auto">
            {["ALL", "PHC", "CHC", "SDH"].map((t) => (
              <button
                key={t}
                onClick={() => setFacilityFilter(t)}
                className={`px-3 py-1 rounded-lg text-xs font-semibold cursor-pointer transition-colors ${
                  facilityFilter === t
                    ? "bg-slate-900 text-white"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                }`}
              >
                {t}
              </button>
            ))}
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
