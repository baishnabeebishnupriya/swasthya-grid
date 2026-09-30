"use client";

import React, { useState } from "react";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { Table, Column } from "@/components/common/Table";
import { Badge } from "@/components/common/Badge";
import { ShieldCheck, Search, Lock, User, Clock, FileText } from "lucide-react";

interface AuditLogEntry {
  id: string;
  timestamp: string;
  actor: string;
  actorRole: string;
  action: string;
  resource: string;
  status: "Success" | "Flagged" | "Failed";
  ipAddress: string;
}

const MOCK_AUDIT_LOGS: AuditLogEntry[] = [
  {
    id: "LOG-9001",
    timestamp: "2026-08-23T10:14:22Z",
    actor: "Dr. Priya Sharma",
    actorRole: "State Health Director",
    action: "Authorize Resource Transfer",
    resource: "TR-OD-2026-9041 (Amoxicillin 1,000 vials)",
    status: "Success",
    ipAddress: "10.14.20.104 (NIC VPN)",
  },
  {
    id: "LOG-9002",
    timestamp: "2026-08-23T09:48:10Z",
    actor: "Dr. Manoj Das",
    actorRole: "Medical Officer (PHC)",
    action: "Update Census & Bed Occupancy",
    resource: "Konark PHC (28/30 Beds Occupied)",
    status: "Success",
    ipAddress: "10.14.32.88 (NIC VPN)",
  },
  {
    id: "LOG-9003",
    timestamp: "2026-08-23T09:12:05Z",
    actor: "System AI Risk Engine",
    actorRole: "Automated Service",
    action: "Emit Early Warning Alert",
    resource: "ALT-801 (Tangi CHC Stockout Threat)",
    status: "Success",
    ipAddress: "127.0.0.1 (Local Core Daemon)",
  },
  {
    id: "LOG-9004",
    timestamp: "2026-08-23T08:30:00Z",
    actor: "District Store Officer",
    actorRole: "Logistics Manager",
    action: "Medicine Batch Stock Inward",
    resource: "Batch PCM-2026-104 (1,450 Units)",
    status: "Success",
    ipAddress: "10.14.18.52 (NIC VPN)",
  },
];

export default function AuditLogsPage() {
  const [searchTerm, setSearchTerm] = useState("");

  const filtered = MOCK_AUDIT_LOGS.filter((l) =>
    l.actor.toLowerCase().includes(searchTerm.toLowerCase()) ||
    l.action.toLowerCase().includes(searchTerm.toLowerCase()) ||
    l.resource.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const columns: Column<AuditLogEntry>[] = [
    {
      header: "Timestamp",
      cell: (row) => (
        <span className="font-mono text-xs text-slate-500">
          {new Date(row.timestamp).toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit", second: "2-digit" })} IST
        </span>
      ),
    },
    {
      header: "Authorized Actor",
      cell: (row) => (
        <div>
          <div className="font-bold text-slate-900 text-xs">{row.actor}</div>
          <div className="text-slate-400 text-[11px] font-mono">{row.actorRole}</div>
        </div>
      ),
    },
    {
      header: "Action Performed",
      cell: (row) => (
        <span className="font-semibold text-slate-800 text-xs">{row.action}</span>
      ),
    },
    {
      header: "Target Resource",
      cell: (row) => (
        <span className="text-xs text-teal-800 font-mono bg-teal-50 px-2 py-0.5 rounded border border-teal-100">
          {row.resource}
        </span>
      ),
    },
    {
      header: "Status",
      cell: (row) => (
        <Badge variant={row.status === "Success" ? "success" : "danger"} size="sm" dot>
          {row.status}
        </Badge>
      ),
    },
    {
      header: "Network Origin",
      cell: (row) => (
        <span className="font-mono text-[11px] text-slate-400">
          {row.ipAddress}
        </span>
      ),
    },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2.5">
            <ShieldCheck className="w-6 h-6 text-teal-600" />
            <span>Governance Audit Trail & System Activity Logs</span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Immutable regulatory audit log of clinical resource allocations, emergency authorizations, and system operations.
          </p>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="relative w-full md:w-80">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search audit trail..."
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
