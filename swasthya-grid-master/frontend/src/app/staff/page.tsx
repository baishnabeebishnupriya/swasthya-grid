"use client";

import React, { useState } from "react";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { Table, Column } from "@/components/common/Table";
import { Badge } from "@/components/common/Badge";
import { MetricCard } from "@/components/common/MetricCard";
import { Users, Search, Plus, UserCheck, CalendarCheck, Shield } from "lucide-react";

interface StaffMember {
  id: string;
  name: string;
  role: "Medical Officer (Doctor)" | "Staff Nurse" | "Pharmacist" | "Lab Technician" | "ANM / Health Worker";
  facilityName: string;
  district: string;
  contactNumber: string;
  status: "On Duty" | "Available" | "On Leave" | "Deployed";
  shift: "Morning (08:00 - 14:00)" | "Evening (14:00 - 20:00)" | "Night (20:00 - 08:00)";
}

const MOCK_STAFF: StaffMember[] = [
  {
    id: "STF-01",
    name: "Dr. Alok Pattnaik (MBBS, MD)",
    role: "Medical Officer (Doctor)",
    facilityName: "Pipili Primary Health Centre",
    district: "Puri",
    contactNumber: "+91 94370 12345",
    status: "On Duty",
    shift: "Morning (08:00 - 14:00)",
  },
  {
    id: "STF-02",
    name: "Sister Snehalata Nayak (B.Sc Nursing)",
    role: "Staff Nurse",
    facilityName: "Tangi Community Health Centre",
    district: "Cuttack",
    contactNumber: "+91 94371 67890",
    status: "On Duty",
    shift: "Morning (08:00 - 14:00)",
  },
  {
    id: "STF-03",
    name: "Ramesh Chandra Mohapatra",
    role: "Pharmacist",
    facilityName: "Konark Primary Health Centre",
    district: "Puri",
    contactNumber: "+91 94372 11223",
    status: "On Duty",
    shift: "Morning (08:00 - 14:00)",
  },
  {
    id: "STF-04",
    name: "Dr. Subhasree Routray",
    role: "Medical Officer (Doctor)",
    facilityName: "Soro Sub-Divisional Hospital",
    district: "Balasore",
    contactNumber: "+91 94373 44556",
    status: "On Duty",
    shift: "Night (20:00 - 08:00)",
  },
  {
    id: "STF-05",
    name: "Kalyani Jena",
    role: "ANM / Health Worker",
    facilityName: "Jatni Urban PHC",
    district: "Khordha",
    contactNumber: "+91 94374 99887",
    status: "On Duty",
    shift: "Morning (08:00 - 14:00)",
  },
];

export default function StaffPage() {
  const [searchTerm, setSearchTerm] = useState("");

  const filtered = MOCK_STAFF.filter((s) =>
    s.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    s.role.toLowerCase().includes(searchTerm.toLowerCase()) ||
    s.facilityName.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const columns: Column<StaffMember>[] = [
    {
      header: "Staff Member Name",
      cell: (row) => (
        <div>
          <div className="font-bold text-slate-900 text-sm">{row.name}</div>
          <div className="text-slate-400 text-xs font-mono">{row.id}</div>
        </div>
      ),
    },
    {
      header: "Clinical Role",
      cell: (row) => (
        <Badge
          variant={
            row.role.includes("Doctor")
              ? "primary"
              : row.role.includes("Nurse")
              ? "teal"
              : "neutral"
          }
          size="sm"
        >
          {row.role}
        </Badge>
      ),
    },
    {
      header: "Assigned Facility",
      cell: (row) => (
        <div className="text-xs">
          <div className="font-semibold text-slate-800">{row.facilityName}</div>
          <div className="text-slate-400">{row.district} District</div>
        </div>
      ),
    },
    {
      header: "Shift Schedule",
      cell: (row) => (
        <span className="text-xs text-slate-700 font-medium">
          {row.shift}
        </span>
      ),
    },
    {
      header: "Duty Status",
      cell: (row) => (
        <Badge
          variant={
            row.status === "On Duty"
              ? "success"
              : row.status === "Available"
              ? "primary"
              : "warning"
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
              <Users className="w-6 h-6 text-teal-600" />
              <span>Healthcare Human Resources & Clinical Staffing</span>
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Roster management, clinical duty assignments, and emergency medical personnel reallocation.
            </p>
          </div>

          <button className="px-4 py-2 bg-teal-600 hover:bg-teal-500 text-white rounded-lg text-xs font-bold flex items-center gap-2 shadow-xs cursor-pointer self-start sm:self-auto">
            <Plus className="w-4 h-4" />
            <span>Add Clinical Staff</span>
          </button>
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <MetricCard
            title="Total Staff Registered"
            value="6,420"
            subtitle="Across All Facilities"
            iconName="Users"
            statusBadge="Full Roster"
            statusVariant="primary"
          />
          <MetricCard
            title="Currently On Duty"
            value="5,870"
            subtitle="91.4% Attendance Rate"
            iconName="UserCheck"
            statusBadge="Active Duty"
            statusVariant="success"
          />
          <MetricCard
            title="Medical Officers"
            value="892 Doctors"
            subtitle="100% PHC Doctor Coverage"
            iconName="Shield"
            statusBadge="Full Coverage"
            statusVariant="teal"
          />
          <MetricCard
            title="Surge Reserves"
            value="140 Specialists"
            subtitle="Ready for Rapid Reallocation"
            iconName="CalendarCheck"
            statusBadge="Reserve Active"
            statusVariant="teal"
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
              placeholder="Search by name, role, facility..."
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
