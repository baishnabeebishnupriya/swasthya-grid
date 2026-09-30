import { useState, useEffect } from "react";
import { DashboardSummaryMetrics } from "@/types";

export function useDashboardMetrics() {
  const [metrics, setMetrics] = useState<DashboardSummaryMetrics>({
    totalHealthFacilities: 1248,
    activePhcs: 892,
    medicineAvailabilityPercent: 92.4,
    totalBeds: 19100,
    occupiedBeds: 14280,
    bedAvailabilityPercent: 74.8,
    totalStaffStrength: 6420,
    activeStaffOnDuty: 5870,
    criticalAlertsCount: 3,
    pendingResourceTransfersCount: 8,
    activeEmergenciesCount: 1,
    lastUpdated: new Date().toISOString(),
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refreshMetrics = async () => {
    setLoading(true);
    try {
      // Prepared for real API service integration
      setMetrics((prev) => ({
        ...prev,
        lastUpdated: new Date().toISOString(),
      }));
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load metrics");
    } finally {
      setLoading(false);
    }
  };

  return { metrics, loading, error, refreshMetrics };
}
