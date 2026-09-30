import apiClient from "./api";
import { HealthFacility, DashboardSummaryMetrics, MedicineItem, ResourceTransfer, RiskAlert } from "@/types";

export const metricsService = {
  getSummaryMetrics: () => apiClient.get<DashboardSummaryMetrics>("/metrics/summary"),
  getHospitalOccupancyRate: () => apiClient.get<{ rate: number }>("/metrics/occupancy"),
};

export const phcService = {
  getAllFacilities: (params?: { state?: string; district?: string; type?: string }) =>
    apiClient.get<HealthFacility[]>("/phcs", params),
  getFacilityById: (id: string) => apiClient.get<HealthFacility>(`/phcs/${id}`),
};

export const inventoryService = {
  getMedicines: (params?: { facilityId?: string; status?: string }) =>
    apiClient.get<MedicineItem[]>("/inventory/medicines", params),
  getBeds: (params?: { facilityId?: string }) =>
    apiClient.get<unknown[]>("/inventory/beds", params),
};

export const transferService = {
  getTransfers: (params?: { status?: string }) =>
    apiClient.get<ResourceTransfer[]>("/transfers", params),
  createTransfer: (data: Partial<ResourceTransfer>) =>
    apiClient.post<ResourceTransfer>("/transfers", data),
};

export const riskService = {
  getRiskAlerts: (params?: { severity?: string; isResolved?: boolean }) =>
    apiClient.get<RiskAlert[]>("/risks", params),
};

export * from "./api";
