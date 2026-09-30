"use client";

import React, { useState } from "react";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { Table, Column } from "@/components/common/Table";
import { Badge } from "@/components/common/Badge";
import { MetricCard } from "@/components/common/MetricCard";
import { Boxes, Pill, Search, AlertCircle, CheckCircle, Clock, Plus } from "lucide-react";
import { MedicineItem } from "@/types";

const MOCK_MEDICINES: MedicineItem[] = [
  {
    id: "MED-001",
    name: "Amoxicillin + Clavulanic Acid 625mg",
    genericName: "Amoxicillin / Clavulanate",
    category: "Antibiotics",
    batchNumber: "AMX-2026-881",
    unit: "Strips (10 tabs)",
    quantityOnHand: 180,
    thresholdMinimum: 500,
    expiryDate: "2027-04-30",
    facilityId: "PHC-102",
    facilityName: "Tangi CHC",
    status: "Critical Stockout",
    daysOfSupplyRemaining: 2.4,
  },
  {
    id: "MED-002",
    name: "Paracetamol 500mg Tablets",
    genericName: "Acetaminophen",
    category: "Analgesics",
    batchNumber: "PCM-2026-104",
    unit: "Boxes (1,000 tabs)",
    quantityOnHand: 1450,
    thresholdMinimum: 300,
    expiryDate: "2028-01-15",
    facilityId: "PHC-101",
    facilityName: "Pipili PHC",
    status: "Adequate",
    daysOfSupplyRemaining: 34.0,
  },
  {
    id: "MED-003",
    name: "Normal Saline (0.9% NaCl 500ml)",
    genericName: "Sodium Chloride IV Solution",
    category: "IV Fluids & Electrolytes",
    batchNumber: "NS-2026-442",
    unit: "Bottles",
    quantityOnHand: 220,
    thresholdMinimum: 400,
    expiryDate: "2027-11-20",
    facilityId: "PHC-103",
    facilityName: "Konark PHC",
    status: "Low Stock",
    daysOfSupplyRemaining: 5.8,
  },
  {
    id: "MED-004",
    name: "Tetanus Toxoid Vaccine (0.5ml)",
    genericName: "Tetanus Vaccine (Adsorbed)",
    category: "Vaccines",
    batchNumber: "TT-2026-902",
    unit: "Ampoules",
    quantityOnHand: 680,
    thresholdMinimum: 200,
    expiryDate: "2026-12-31",
    facilityId: "PHC-104",
    facilityName: "Soro SDH",
    status: "Adequate",
    daysOfSupplyRemaining: 28.5,
  },
  {
    id: "MED-005",
    name: "Oxytocin Injection 10 IU/ml",
    genericName: "Oxytocin Synthetic",
    category: "Maternal & Child Health",
    batchNumber: "OXY-2026-319",
    unit: "Ampoules (Cold-Chain 2-8°C)",
    quantityOnHand: 95,
    thresholdMinimum: 250,
    expiryDate: "2027-02-28",
    facilityId: "PHC-102",
    facilityName: "Tangi CHC",
    status: "Low Stock",
    daysOfSupplyRemaining: 4.1,
  },
];

export default function InventoryPage() {
  const [searchTerm, setSearchTerm] = useState("");

  const filtered = MOCK_MEDICINES.filter((m) =>
    m.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    m.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
    m.facilityName.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const columns: Column<MedicineItem>[] = [
    {
      header: "Medicine & Formulation",
      cell: (row) => (
        <div>
          <div className="font-bold text-slate-900 text-sm">{row.name}</div>
          <div className="text-slate-400 text-xs">{row.genericName}</div>
        </div>
      ),
    },
    {
      header: "Category",
      cell: (row) => (
        <Badge variant="teal" size="sm">
          {row.category}
        </Badge>
      ),
    },
    {
      header: "Facility",
      cell: (row) => (
        <span className="text-xs font-semibold text-slate-700">
          {row.facilityName}
        </span>
      ),
    },
    {
      header: "Stock On-Hand",
      cell: (row) => (
        <div>
          <div className="font-bold text-slate-900 text-xs">
            {row.quantityOnHand} {row.unit}
          </div>
          <div className="text-slate-400 text-[11px]">
            Min Buffer: {row.thresholdMinimum}
          </div>
        </div>
      ),
    },
    {
      header: "Supply Runway",
      cell: (row) => (
        <span
          className={`font-mono text-xs font-bold ${
            row.daysOfSupplyRemaining < 3
              ? "text-rose-600"
              : row.daysOfSupplyRemaining < 7
              ? "text-amber-600"
              : "text-emerald-600"
          }`}
        >
          {row.daysOfSupplyRemaining} Days
        </span>
      ),
    },
    {
      header: "Status",
      cell: (row) => (
        <Badge
          variant={
            row.status === "Adequate"
              ? "success"
              : row.status === "Low Stock"
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
              <Boxes className="w-6 h-6 text-teal-600" />
              <span>Essential Drugs & Medical Consumables Inventory</span>
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              National Essential Drugs List (EDL) compliance, batch expiry monitoring, and stockout risk mitigation.
            </p>
          </div>

          <button className="px-4 py-2 bg-teal-600 hover:bg-teal-500 text-white rounded-lg text-xs font-bold flex items-center gap-2 shadow-xs cursor-pointer self-start sm:self-auto">
            <Plus className="w-4 h-4" />
            <span>Add Stock Inward</span>
          </button>
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <MetricCard
            title="EDL Compliance"
            value="92.4%"
            subtitle="National Formulary Target 90%"
            iconName="Pill"
            statusBadge="Compliant"
            statusVariant="success"
          />
          <MetricCard
            title="Active SKUs"
            value="240"
            subtitle="Essential Drug Items"
            iconName="Boxes"
            statusBadge="Categorized"
            statusVariant="primary"
          />
          <MetricCard
            title="Stockout Risk"
            value="14 Facilities"
            subtitle="< 3 Days Runway"
            iconName="AlertTriangle"
            statusBadge="Action Needed"
            statusVariant="danger"
            highlightBorder="rose"
          />
          <MetricCard
            title="Cold-Chain Drugs"
            value="42 SKUs"
            subtitle="2°C - 8°C Monitored"
            iconName="Activity"
            statusBadge="Active Chiller"
            statusVariant="teal"
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
              placeholder="Search medicine name, generic name, category, facility..."
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
