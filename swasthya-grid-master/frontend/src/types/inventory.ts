export type MedicineCategory =
  | "Antibiotics"
  | "Analgesics"
  | "Cardiovascular"
  | "Maternal & Child Health"
  | "Emergency & Trauma"
  | "Vaccines"
  | "IV Fluids & Electrolytes";

export type StockStatus = "Adequate" | "Low Stock" | "Critical Stockout" | "Excess";

export interface MedicineItem {
  id: string;
  name: string;
  genericName: string;
  category: MedicineCategory;
  batchNumber: string;
  unit: string;
  quantityOnHand: number;
  thresholdMinimum: number;
  expiryDate: string;
  facilityId: string;
  facilityName: string;
  status: StockStatus;
  daysOfSupplyRemaining: number;
}

export interface BedAllocation {
  id: string;
  facilityId: string;
  facilityName: string;
  totalBeds: number;
  occupiedBeds: number;
  availableBeds: number;
  icuBedsTotal: number;
  icuBedsOccupied: number;
  oxygenSupportedBeds: number;
  occupancyRate: number;
  status: "Normal" | "High Occupancy" | "Near Capacity" | "Overwhelmed";
}
