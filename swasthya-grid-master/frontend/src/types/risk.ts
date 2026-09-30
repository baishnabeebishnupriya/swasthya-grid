export type RiskSeverity = "Low" | "Moderate" | "High" | "Critical";

export type RiskCategory = "Stockout" | "Staff Shortage" | "Disease Outbreak Surge" | "Infrastructure" | "Weather Disruption";

export interface RiskAlert {
  id: string;
  facilityId: string;
  facilityName: string;
  district: string;
  state: string;
  category: RiskCategory;
  severity: RiskSeverity;
  headline: string;
  description: string;
  predictedImpactTimeframe: string;
  recommendedAction: string;
  confidenceScore: number;
  createdAt: string;
  isResolved: boolean;
}
