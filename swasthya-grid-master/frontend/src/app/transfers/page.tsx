"use client";

import React, { useState } from "react";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { Table, Column } from "@/components/common/Table";
import { Badge } from "@/components/common/Badge";
import { MetricCard } from "@/components/common/MetricCard";
import { ArrowRightLeft, Search, Plus, Clock, MapPin, Truck, CheckCircle2 } from "lucide-react";
import { ResourceTransfer } from "@/types";

const MOCK_ALL_TRANSFERS: ResourceTransfer[] = [
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
    approvedBy: "Directorate of Health Services",
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
    approvedBy: "Chief District Medical Officer (CDMO)",
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
    approvedBy: "District Medical Store Keeper",
  },
  {
    id: "TR-2044",
    transferCode: "TR-OD-2026-9044",
    sourceFacilityName: "State Cold-Chain Central Depot",
    sourceDistrict: "Bhubaneswar",
    targetFacilityName: "Konark Primary Health Centre",
    targetDistrict: "Puri",
    resourceType: "Medicines",
    itemName: "Rabies Immunoglobulin (RIG 300 IU)",
    quantity: 150,
    unit: "Vials",
    urgency: "Urgent",
    status: "Delivered",
    requestedAt: "2026-08-22T14:20:00Z",
    estimatedArrival: "Delivered (Aug 22, 18:45)",
    approvedBy: "State Immunization Officer",
  },
];

export default function TransfersPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");

  const filtered = MOCK_ALL_TRANSFERS.filter((t) => {
    const matchesSearch =
      t.transferCode.toLowerCase().includes(searchTerm.toLowerCase()) ||
      t.itemName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      t.sourceFacilityName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      t.targetFacilityName.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === "ALL" || t.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const columns: Column<ResourceTransfer>[] = [
    {
      header: "Transfer ID",
      cell: (row) => (
        <div>
          <span className="font-mono font-bold text-xs text-slate-800">
            {row.transferCode}
          </span>
          <div className="text-slate-400 text-[11px]">{row.approvedBy}</div>
        </div>
      ),
    },
    {
      header: "Origin → Destination",
      cell: (row) => (
        <div className="text-xs">
          <div className="font-semibold text-slate-900">{row.sourceFacilityName} ({row.sourceDistrict})</div>
          <div className="text-teal-700 font-medium flex items-center gap-1 mt-0.5">
            <Truck className="w-3 h-3 text-teal-600" />
            <span>↳ {row.targetFacilityName} ({row.targetDistrict})</span>
          </div>
        </div>
      ),
    },
    {
      header: "Resource Payload",
      cell: (row) => (
        <div>
          <div className="font-semibold text-slate-900 text-xs">{row.itemName}</div>
          <div className="text-slate-500 text-[11px]">
            {row.quantity} {row.unit} • {row.resourceType}
          </div>
        </div>
      ),
    },
    {
      header: "Urgency",
      cell: (row) => (
        <Badge
          variant={
            row.urgency === "Critical"
              ? "danger"
              : row.urgency === "Urgent"
              ? "warning"
              : "neutral"
          }
          size="sm"
          dot
        >
          {row.urgency}
        </Badge>
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
              : row.status === "Delivered"
              ? "success"
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
      header: "Logistics Timeline",
      cell: (row) => (
        <div className="text-xs text-slate-600 flex items-center gap-1">
          <Clock className="w-3.5 h-3.5 text-slate-400" />
          <span>{row.estimatedArrival}</span>
        </div>
      ),
    },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2.5">
              <ArrowRightLeft className="w-6 h-6 text-teal-600" />
              <span>Inter-Facility Resource Transfers & Balancing</span>
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Automated and authorized redistribution of medicines, medical oxygen, and clinical consumables between surplus and deficit health nodes.
            </p>
          </div>

          <button className="px-4 py-2 bg-teal-600 hover:bg-teal-500 text-white rounded-lg text-xs font-bold flex items-center gap-2 shadow-xs cursor-pointer self-start sm:self-auto">
            <Plus className="w-4 h-4" />
            <span>Initiate Resource Reallocation</span>
          </button>
        </div>

        {/* Top metrics */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <MetricCard
            title="Total Dispatches"
            value="142"
            subtitle="This Month"
            iconName="Truck"
            statusBadge="Active Grid"
            statusVariant="primary"
          />
          <MetricCard
            title="In-Transit Active"
            value="8"
            subtitle="En-route along NH-16"
            iconName="ArrowRightLeft"
            statusBadge="Live GPS"
            statusVariant="teal"
            highlightBorder="teal"
          />
          <MetricCard
            title="Avg Delivery SLA"
            value="3.2 Hours"
            subtitle="Target < 6.0 Hours"
            iconName="Clock"
            statusBadge="On Target"
            statusVariant="success"
          />
          <MetricCard
            title="Surplus Shared"
            value="₹48.6 Lakh"
            subtitle="Prevented Expiry Waste"
            iconName="CheckCircle2"
            statusBadge="Optimized"
            statusVariant="success"
          />
        </div>

        {/* Filters */}
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex flex-col md:flex-row gap-3 items-center justify-between">
          <div className="relative w-full md:w-96">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by transfer code, medicine name, source or target facility..."
              className="w-full pl-9 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-teal-500"
            />
          </div>

          <div className="flex items-center gap-2 w-full md:w-auto">
            {["ALL", "In Transit", "Dispatched", "Approved", "Delivered"].map((st) => (
              <button
                key={st}
                onClick={() => setStatusFilter(st)}
                className={`px-3 py-1 rounded-lg text-xs font-semibold cursor-pointer transition-colors ${
                  statusFilter === st
                    ? "bg-slate-900 text-white"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                }`}
              >
                {st}
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
