export interface DashboardSummaryMetrics {
  totalHealthFacilities: number;
  activePhcs: number;
  medicineAvailabilityPercent: number;
  totalBeds: number;
  occupiedBeds: number;
  bedAvailabilityPercent: number;
  totalStaffStrength: number;
  activeStaffOnDuty: number;
  criticalAlertsCount: number;
  pendingResourceTransfersCount: number;
  activeEmergenciesCount: number;
  lastUpdated: string;
}

export interface MetricCardData {
  title: string;
  value: string | number;
  subtitle?: string;
  change?: string;
  changeType?: "positive" | "negative" | "neutral" | "warning";
  iconName: string;
  statusBadge?: string;
  statusVariant?: "primary" | "warning" | "danger" | "success" | "neutral";
}
