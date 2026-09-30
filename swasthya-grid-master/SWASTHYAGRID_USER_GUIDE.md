# SwasthyaGrid User Guide
## AI-Powered Health Resource Resilience Network

**Document Reference:** SG-UG-V1.4-2026  
**Target Audience:** Government Health Administrators, State Health Officers, District Medical Officers (CDMOs), PHC Medical Officers, and Healthcare Operations Teams  
**Governing Context:** National Public Health Logistics & Primary Healthcare Resilience  

---

## 1. Introduction

### 1.1 What is SwasthyaGrid?
**SwasthyaGrid** is a digital health operations and resilience platform designed for India's public healthcare ecosystem. It provides real-time visibility, predictive analytics, and automated decision-support across Primary Health Centres (PHCs), Community Health Centres (CHCs), Sub-Divisional Hospitals (SDHs), and District Hospitals (DHs).

By connecting health facilities into a coordinated data network, SwasthyaGrid transforms fragmented facility-level data into actionable intelligence for health administrators at the national, state, district, and grassroots levels.

```
┌──────────────────────────────────────────────────────────────────┐
│                   SWASTHYAGRID NATIONAL GRID                     │
├─────────────────┬─────────────────┬──────────────────────────────┤
│  NATIONAL LEVEL │ STATE DIRECTORS │ DISTRICT HEALTH OFFICERS     │
│  Macro Policy & │ Regional Buffer │ Local Allocation, Census,    │
│  Funding View   │ & Cold Chains   │ & Emergency Transfers        │
├─────────────────┴─────────────────┴──────────────────────────────┤
│                PRIMARY HEALTH CENTRES (PHCs)                     │
│    Daily Patient Footfall, Drug Dispensary & Ward Occupancy      │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 Why SwasthyaGrid was Created
India's public healthcare delivery is powered by over 30,000 rural and urban Primary Health Centres. However, regional health administration frequently encounters structural bottlenecks:

1. **Information Silos:** Health departments often learn about local medicine stockouts or oxygen shortages only after supplies have been depleted.
2. **Surplus-Deficit Mismatch:** While one health centre experiences a critical drug shortage, a neighbouring facility 25 km away may hold excess stock nearing expiration.
3. **Reactive Emergency Response:** Seasonal disease outbreaks (such as monsoon dengue, malaria, or diarrhoeal surges) overwhelm local facilities before buffer supplies can be dispatched.
4. **Administrative Delays:** Manual paperwork and phone coordination slow down inter-facility sharing of life-saving medical supplies.

### 1.3 The Problems SwasthyaGrid Solves

| Traditional Healthcare Operations | SwasthyaGrid Integrated Platform |
| :--- | :--- |
| **Delayed Stockout Reporting:** Shortages discovered during patient consultations. | **Predictive Early Warnings:** AI forecasts stockouts 3 to 7 days in advance. |
| **Isolated Facility Management:** Each PHC operates independently. | **Grid Resource Sharing:** Surplus stock is dynamically balanced across facilities. |
| **Manual Bed Census:** Bed vacancies communicated via ad-hoc phone calls. | **Live Corridor Census:** Real-time occupancy tracking for general and ICU beds. |
| **Uncoordinated Drug Disposal:** Significant medicine wastage due to expiry. | **Zero-Waste Redistribution:** Expiring stock routed to high-consumption facilities. |

### 1.4 How it Improves Visibility and Decision-Making
* **Unified Dashboard:** Delivers end-to-end visibility of health facilities across states, districts, and blocks.
* **Proactive Resource Balancing:** Recommends exact transfer quantities and routing between surplus and deficit centres.
* **Cold-Chain & EDL Compliance:** Automatically tracks Essential Drug List (EDL) compliance and temperature-sensitive biologicals (2°C–8°C).

---

## 2. System Overview & Core Modules

```
                    ┌────────────────────────────────┐
                    │     SWASTHYAGRID MODULES       │
                    └───────────────┬────────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │                          │                          │
┌────────┴─────────┐       ┌────────┴─────────┐       ┌────────┴─────────┐
│   CORE NETWORK   │       │ RESOURCE CONTROL │       │ PREDICTIVE INTEL │
├──────────────────┤       ├──────────────────┤       ├──────────────────┤
│ • Dashboard      │       │ • Inventory      │       │ • AI Forecasts   │
│ • PHC Network    │       │ • Medicines      │       │ • Risk Alerts    │
│ • State Overview │       │ • Bed Capacity   │       │ • Transfers      │
│ • District Grid  │       │ • Clinical Staff │       │ • Audit Trail    │
└──────────────────┘       └──────────────────┘       └──────────────────┘
```

### 2.1 Executive Dashboard
The central operational cockpit for health directors and administrators. Displays vital health indicators, live facility status, capacity heatmaps, urgent risk alerts, and active inter-facility supply transfers.

### 2.2 PHC Network Registry
Maintains an exhaustive, mapped digital directory of all connected Primary Health Centres, Community Health Centres, and Sub-Divisional Hospitals.
* **Facility Information:** View facility code, contact person, GPS coordinates, pincode, and operational classification.
* **Operational Performance:** Monitor facility-specific bed fill-rates, active doctor coverage, and supply status.

### 2.3 Inventory Management
Tracks the complete catalog of medical supplies, surgical consumables, rapid diagnostic test kits, and emergency equipment across district storage depots and individual health posts.

### 2.4 Medicine Management
Dedicated monitoring of the **National Essential Drugs List (EDL)**:
* **Real-time Stock Levels:** Continuous visibility of available tablets, syrups, injectables, and IV fluids.
* **Supply Runway (Days):** Automatically computes how many days of supply remain based on average daily consumption.
* **Batch & Expiry Surveillance:** Alerts storekeepers to batches approaching expiry within 90 days.

### 2.5 Bed Management
Provides live ward census and emergency surge tracking:
* **General Ward Beds:** Total vs. occupied vs. available beds.
* **ICU & Oxygen-Supported Beds:** High-dependency capacity across secondary and tertiary referral nodes.
* **Surge Status:** Highlights facilities exceeding 85% occupancy for proactive patient divert planning.

### 2.6 Staff Management & Human Resources
Maintains public healthcare human resource rosters:
* **Workforce Categories:** Medical Officers (Doctors), Specialists, Staff Nurses, Pharmacists, Lab Technicians, and ANMs/ASHAs.
* **Roster Allocation:** Duty shifts (Morning, Evening, Night) and facility deployments.

### 2.7 Attendance Tracking
Monitors health staff presence and clinical availability across remote and rural health posts, ensuring 100% doctor coverage during operational OPD and emergency hours.

### 2.8 AI Forecasting Engine
Applies epidemiological machine learning models to historical patient footfall and seasonal patterns:
* **Footfall Projections:** Estimates outpatient surge 14 days in advance.
* **Drug Consumption Velocity:** Forecasts rapid depletion of anti-venom, ORS, IV saline, and antibiotics.

### 2.9 Risk Alerts & Early Warning System
Automated anomaly detection that categorizes operational risks into **Critical**, **High**, **Moderate**, and **Low** tiers with prescriptive AI recommendations.

### 2.10 Resource Transfers & Balancing Ledger
The operational logistics engine that coordinates the redistribution of medicines and medical supplies between facilities:
* **Transfer Requisitions:** Step-by-step dispatch creation and approval.
* **Live In-Transit Tracking:** Monitor shipment status from dispatch to verified delivery receipt.

### 2.11 Audit Logs & Governance
An immutable compliance ledger recording every administrative action, user login, emergency override, and stock transfer for transparency and accountability.

---

## 3. User Roles & Access Hierarchy

SwasthyaGrid features role-based access control tailored to public health administrative structures:

```
                  ┌───────────────────────────────┐
                  │    NATIONAL ADMINISTRATOR     │
                  │ Nationwide policy & macro KPIs│
                  └───────────────┬───────────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  │      STATE ADMINISTRATOR      │
                  │ State buffer & regional hubs  │
                  └───────────────┬───────────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  │     DISTRICT ADMINISTRATOR    │
                  │ CDMOs, transfer authorizations│
                  └───────────────┬───────────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  │       PHC ADMINISTRATOR       │
                  │ Local OPD, pharmacy & census  │
                  └───────────────────────────────┘
```

### 3.1 National Administrator (Ministry / Central Health Mission)
* **Scope:** Nationwide health grid.
* **Responsibilities:**
  - Review national healthcare infrastructure metrics and state comparisons.
  - Monitor national emergency reserves and disease outbreak corridors.
  - Allocate central health mission budgets and large-scale bulk procurement.

### 3.2 State Administrator (Director of Health Services / State Health Mission)
* **Scope:** State-wide facilities across all districts.
* **Responsibilities:**
  - Oversee district-to-district resource sharing along state logistics corridors.
  - Monitor state cold-chain depots and vaccine buffer stocks.
  - Reallocate clinical specialists during regional healthcare emergencies.

### 3.3 District Administrator (Chief District Medical Officer - CDMO)
* **Scope:** All PHCs, CHCs, and hospitals within the designated district.
* **Responsibilities:**
  - Review daily district health indicators, bed capacities, and medicine runways.
  - Authorize and dispatch inter-facility resource transfer requisitions.
  - Resolve critical stockout alerts and staffing deficits in remote blocks.

### 3.4 PHC Administrator (Medical Officer In-Charge / Storekeeper)
* **Scope:** Assigned Primary Health Centre or Community Health Centre.
* **Responsibilities:**
  - Record daily outpatient census, bed occupancy, and drug dispensations.
  - Verify receipt of inward medicine shipments and update batch numbers.
  - Request emergency supplies from the district depot when stock drops below minimum buffer.

---

## 4. How To Use SwasthyaGrid: Step-by-Step Guide

Follow this standard operating routine for daily public health administration:

```
  ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
  │    STEP 1     │      │    STEP 2     │      │    STEP 3     │
  │ Login to the  │ ───> │ Open Executive│ ───> │ Review Core   │
  │   Platform    │      │   Dashboard   │      │Health Metrics │
  └───────────────┘      └───────────────┘      └───────────────┘
                                                        │
  ┌───────────────┐      ┌───────────────┐      ┌───────┴───────┐
  │    STEP 6     │      │    STEP 5     │      │    STEP 4     │
  │ Analyze Gaps  │ <─── │Check Inventory│ <─── │ Check Critical│
  │  & Solutions  │      │  & Drug Stock │      │  Risk Alerts  │
  └───────┬───────┘      └───────────────┘      └───────────────┘
          │
  ┌───────┴───────┐
  │    STEP 7     │
  │  Execute Auto │
  │ Stock Transfer│
  └───────────────┘
```

### Step 1: Login to the Platform
1. Open your authorized browser and navigate to `http://localhost:3000` (or your state's SwasthyaGrid web portal URL).
2. Enter your authorized government email and password.
3. Upon authentication, you will be redirected to your role-specific dashboard view.

### Step 2: Open Executive Dashboard
Navigate to the **Dashboard** link located at the top of the left sidebar. The dashboard provides an instant high-level overview of your administrative jurisdiction.

### Step 3: Review Health Indicators
Examine the 7 primary KPI cards displayed along the top:
* Total Health Facilities mapped.
* Active PHCs currently operational.
* Essential Drug Availability (%) against the 90% benchmark.
* Bed Availability (%) and ready bed pool.
* Healthcare Staff Strength and attendance.
* Total Critical Alerts requiring attention.
* Pending Resource Transfers in progress.

### Step 4: Check Risk Alerts
Scroll to the **Critical Resource Vulnerabilities & Early Warnings** table.
* Inspect facilities flagged with **Critical** (Red) or **High** (Amber) badges.
* Note the predicted impact timeframe (e.g., *Stockout expected in < 36 hours*).
* Read the prescriptive AI recommendation.

### Step 5: Review Inventory & Medicine Availability
Click **Medicines** or **Inventory** in the sidebar.
* Sort medicines by **Supply Runway (Days)** to identify items below the 7-day safety threshold.
* Review cold-chain medicines (e.g., Insulin, Oxytocin, Antivenom) requiring 2°C–8°C storage.

### Step 6: Analyze Resource Gaps
When a deficit is identified, click on the affected facility to view its consumption trend and look up nearby health centres holding surplus stock of the same item.

### Step 7: Take Corrective Action via Resource Transfers
1. Click **Resource Transfers** in the sidebar $\rightarrow$ Click **New Resource Transfer**.
2. Select the **Source Facility** (holding surplus) and **Target Facility** (in deficit).
3. Specify the item, quantity, and urgency tier (**Routine**, **Urgent**, or **Critical**).
4. Click **Authorize & Dispatch Transfer**. The system updates the transfer ledger and notifies logistics drivers.

---

## 5. Dashboard Elements & Indicator Guide

### 5.1 Primary Metric Cards

| Card Title | Metric Displayed | Operational Meaning | Action Threshold |
| :--- | :--- | :--- | :--- |
| **Total Facilities** | `1,248` | Total mapped public health institutions in region. | Ensure 100% telemetry connection. |
| **Active PHCs** | `892` | Functioning primary centres currently reporting OPD. | Investigate if active rate drops below 95%. |
| **Medicine Availability** | `92.4%` | Percentage of Essential Drugs in stock. | Target is $\ge 90\%$. Flag below $85\%$. |
| **Bed Availability** | `74.8%` | General bed pool occupancy percentage. | Prepare surge divert when occupancy $> 85\%$. |
| **Staff Strength** | `6,420` | Registered doctors, nurses, and clinical staff. | Monitor attendance rates below $90\%$. |
| **Critical Alerts** | `3` | Imminent stockouts or outbreak surges. | Must be actioned within 24 hours. |
| **Pending Transfers** | `8` | Inter-facility shipments currently en-route. | Monitor delivery SLAs exceeding 6 hours. |

### 5.2 Visual Status Badges

* <span style="color:#059669; font-weight:bold;">● Operational (Green):</span> Facility operating within normal parameters; inventory buffers intact.
* <span style="color:#D97706; font-weight:bold;">● Low Stock / Stockout Risk (Amber):</span> Medicine supply runway between 3 and 7 days.
* <span style="color:#DC2626; font-weight:bold;">● Critical Alert (Red):</span> Immediate threat; stock runway under 48 hours or bed occupancy over 92%.
* <span style="color:#2563EB; font-weight:bold;">● In Transit (Blue):</span> Authorized resource transfer dispatched and on the road.

---

## 6. Common User Workflows

### Workflow 1: Responding to a Critical Medicine Stockout

```
  ┌─────────────────────────────────────────────────────────────┐
  │ 1. Alert Triggered: Tangi CHC has only 80 vials Amoxicillin │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
  ┌──────────────────────────────┴──────────────────────────────┐
  │ 2. System Suggests: SCB Medical Depot has 4,200 vials       │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
  ┌──────────────────────────────┴──────────────────────────────┐
  │ 3. CDMO Approves: 1,000 vials transfer via NH-16 highway    │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
  ┌──────────────────────────────┴──────────────────────────────┐
  │ 4. Delivered: Tangi CHC buffer restored; alert auto-cleared │
  └─────────────────────────────────────────────────────────────┘
```

1. **Detection:** An alert appears on the District Dashboard: *"Tangi CHC Amoxicillin stockout in < 36 hrs"*.
2. **Identification:** The District Officer clicks the alert. The system displays surrounding facilities within a 35 km radius with surplus Amoxicillin.
3. **Requisition:** The officer clicks **Initiate Transfer**. The source is set to *SCB Medical College Depot* (holding 4,200 surplus vials) and target to *Tangi CHC* for 1,000 vials.
4. **Dispatch:** The warehouse keeper confirms packaging; status shifts to **In Transit**.
5. **Receipt:** Tangi CHC receives the shipment, verifies the batch in SwasthyaGrid, and the alert automatically resolves.

---

### Workflow 2: Managing Emergency Bed Surge During Outbreak

1. **Surge Warning:** An epidemic alert flags a dengue cluster in Gop Block; *Konark PHC* reaches 93.3% bed occupancy.
2. **Capacity Review:** The District Health Officer opens **Bed Management** and reviews nearby facility occupancies.
3. **Surge Balancing:** The officer identifies that *Pipili PHC* (22 km away) has 10 vacant beds with available medical staff.
4. **Referral Protocol:** Emergency 108 ambulance routing is updated to divert non-critical admissions to Pipili PHC, preventing Konark PHC from becoming overwhelmed.

---

### Workflow 3: Resolving Weekend Clinical Staff Deficits

1. **Roster Audit:** The **Staff Management** module detects zero on-duty anesthetist coverage for the upcoming Saturday night shift at *Soro Sub-Divisional Hospital*.
2. **Gap Analysis:** The system identifies 2 available specialists on reserve duty in the Balasore District Headquarters pool.
3. **Roster Deployment:** The administrator assigns a temporary weekend duty roster, updating the digital schedule and issuing an automated SMS notification to the medical officer.

---

## 7. Administrative Best Practices

```
┌────────────────────────────────────────────────────────────────────────┐
│                   DAILY BEST PRACTICE CHECKLIST                        │
├───────────────────────────────────┬────────────────────────────────────┤
│ 08:30 IST — Morning Inspection    │ 14:00 IST — Mid-Day Review         │
│ • Review top KPI metric cards     │ • Authorize morning transfer slips │
│ • Triage Red Critical Alerts      │ • Audit medicine inward dispatches │
├───────────────────────────────────┼────────────────────────────────────┤
│ 17:30 IST — Evening Census        │ Weekly Operations Audit            │
│ • Verify bed occupancy updates    │ • Review 14-day AI demand forecasts│
│ • Confirm completed transfers     │ • Inspect batch expiry schedules   │
└───────────────────────────────────┴────────────────────────────────────┘
```

1. **Perform Twice-Daily Dashboard Reviews:** Check the dashboard at the start (08:30) and close (17:30) of administrative shifts.
2. **Prioritize Red Critical Alerts:** Resolve all stockout warnings with less than 48 hours runway before routine tasks.
3. **Enforce Daily Facility Census Updates:** Ensure PHC data operators submit daily OPD footfall and bed counts before 16:00 IST.
4. **Maintain Accurate Batch Numbers:** Always enter manufacturing batch codes and expiry dates during stock inward receipt.
5. **Minimize Emergency Idle Time:** Aim to approve urgent inter-facility transfer requests within 60 minutes of submission.

---

## 8. Frequently Asked Questions (FAQ)

### Q1: What is SwasthyaGrid?
**A:** SwasthyaGrid is an AI-powered public health resilience platform that unifies Primary Health Centres, Community Health Centres, and District Hospitals into a single real-time resource tracking and sharing network.

### Q2: Who is authorized to use SwasthyaGrid?
**A:** SwasthyaGrid is designed for authorized public health personnel including National Health Mission directors, State Health Secretaries, Chief District Medical Officers (CDMOs), PHC Medical Officers, Hospital Superintendents, and medical storekeepers.

### Q3: What categories of data does SwasthyaGrid manage?
**A:** The platform manages essential medicine inventory, batch expiries, cold-chain temperature telemetry, general and ICU bed occupancy, medical staff duty rosters, epidemiological disease patterns, and inter-facility logistics.

### Q4: How does SwasthyaGrid support clinical and administrative decision-making?
**A:** Instead of relying on manual reports, administrators receive real-time visibility, automated risk alerts, and AI-driven recommendations that suggest exactly how many resources to transfer from surplus centres to avert stockouts.

### Q5: Can SwasthyaGrid scale across multiple states and corridors?
**A:** Yes. SwasthyaGrid is built on a high-concurrency microservice architecture supporting national-scale deployment across all 28 states and 8 union territories, connecting over 30,000 health facilities on standard open APIs.

---

**SwasthyaGrid Technical Support & Helpdesk:**  
*Email:* `support@swasthya-grid.gov.in` | *Toll-Free Helpline:* `1800-11-HEALTH`  
*National Health Mission Integrated Systems Command*
