export type FacilityType = "PHC" | "CHC" | "DH" | "SDH" | "SubCentre";

export type FacilityStatus = "Operational" | "Surge Capacity" | "Stockout Risk" | "Critical Alert" | "Maintenance";

export interface HealthFacility {
  id: string;
  name: string;
  code: string;
  type: FacilityType;
  state: string;
  district: string;
  block?: string;
  pincode: string;
  latitude: number;
  longitude: number;
  contactPerson: string;
  phone: string;
  totalBeds: number;
  occupiedBeds: number;
  staffCount: number;
  status: FacilityStatus;
  lastUpdated: string;
}
