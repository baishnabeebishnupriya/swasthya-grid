export type TransferStatus =
  | "Requested"
  | "Approved"
  | "Dispatched"
  | "In Transit"
  | "Delivered"
  | "Rejected";

export type ResourceType = "Medicines" | "Oxygen Cylinders" | "Medical Consumables" | "Equipment" | "Staff Deployment";

export interface ResourceTransfer {
  id: string;
  transferCode: string;
  sourceFacilityName: string;
  sourceDistrict: string;
  targetFacilityName: string;
  targetDistrict: string;
  resourceType: ResourceType;
  itemName: string;
  quantity: number;
  unit: string;
  urgency: "Routine" | "Urgent" | "Critical";
  status: TransferStatus;
  requestedAt: string;
  estimatedArrival?: string;
  approvedBy?: string;
}
