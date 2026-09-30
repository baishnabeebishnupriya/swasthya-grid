import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Header on pages 2+
        if self._pageNumber > 1:
            self.drawString(40, 802, "SWASTHYAGRID // USER GUIDE & OPERATIONAL MANUAL")
            self.drawRightString(555, 802, "GOI PUBLIC HEALTH RESILIENCE NETWORK")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(40, 796, 555, 796)

        # Running Footer on all pages
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(40, 42, 555, 42)
        self.drawString(40, 30, "CONFIDENTIAL // SWASTHYAGRID USER GUIDE — FOR AUTHORIZED HEALTH PERSONNEL ONLY")
        self.drawRightString(555, 30, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(filename="SwasthyaGrid_User_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=46,
        bottomMargin=48,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=2,
    )

    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0D9488"),
        spaceAfter=8,
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#0F766E"),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=11.2,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4,
    )

    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.0,
        leading=10.8,
        textColor=colors.HexColor("#334155"),
        leftIndent=12,
        spaceAfter=2,
    )

    callout_style = ParagraphStyle(
        "Callout_Text",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.0,
        leading=11.0,
        textColor=colors.HexColor("#1E293B"),
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.8,
        leading=9.5,
        textColor=colors.white,
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.4,
        leading=9.5,
        textColor=colors.HexColor("#1E293B"),
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.4,
        leading=9.5,
        textColor=colors.HexColor("#0F172A"),
    )

    story = []

    # ── HEADER & TITLE ──
    story.append(Paragraph("SWASTHYAGRID", title_style))
    story.append(Paragraph("AI-Powered Health Resource Resilience Network // User Walkthrough Guide", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=6))

    # Executive Overview Box
    exec_summary_html = "<b>Executive Purpose:</b> SwasthyaGrid is a unified public health intelligence and logistics resilience platform designed for India's Primary Health Centres (PHCs), Community Health Centres (CHCs), and District Hospitals. It delivers real-time visibility into medicine stocks, bed occupancy, and healthcare workforce availability, automating inter-facility resource balancing to prevent stockouts and manage emergency health surges."
    exec_table = Table([[Paragraph(exec_summary_html, callout_style)]], colWidths=[515])
    exec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0FDFA")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#99F6E4")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(exec_table)
    story.append(Spacer(1, 6))

    # ── SECTION 1: INTRODUCTION ──
    story.append(Paragraph("1. Introduction & Operational Rationale", h1_style))
    story.append(Paragraph("India's public healthcare delivery is anchored by over 30,000 rural and urban health centres. SwasthyaGrid solves critical structural operational bottlenecks:", body_style))
    story.append(Paragraph("• <b>Information Silos:</b> Health authorities historically detect stockouts only after facilities exhaust essential drugs. SwasthyaGrid establishes real-time telemetry across all tiers.", bullet_style))
    story.append(Paragraph("• <b>Surplus-Deficit Mismatch:</b> Resolves localized shortages by detecting neighbouring centres with surplus inventory and routing buffer stock dynamically.", bullet_style))
    story.append(Paragraph("• <b>Proactive Surge Preparedness:</b> Applies machine learning to forecast monsoon disease surges (e.g. Dengue, Malaria, Diarrhoea) 14 days in advance.", bullet_style))
    story.append(Paragraph("• <b>Zero Expiry Waste:</b> Automatically flags batches nearing expiration within 90 days, facilitating prompt redistribution to high-consumption hubs.", bullet_style))

    # Comparison Matrix Table
    comp_data = [
        [Paragraph("OPERATIONAL CHALLENGE", table_header_style), Paragraph("TRADITIONAL WORKFLOW", table_header_style), Paragraph("SWASTHYAGRID INTEGRATED PLATFORM", table_header_style)],
        [Paragraph("Stockout Identification", table_cell_bold), Paragraph("Discovered during patient consultation", table_cell_style), Paragraph("AI early warning 3-7 days in advance", table_cell_style)],
        [Paragraph("Facility Coordination", table_cell_bold), Paragraph("Isolated, independent local management", table_cell_style), Paragraph("Unified grid sharing surplus stocks", table_cell_style)],
        [Paragraph("Bed Census & Surge", table_cell_bold), Paragraph("Manual phone calls and paper logs", table_cell_style), Paragraph("Real-time general, ICU and O2 bed tracking", table_cell_style)],
        [Paragraph("Logistics Dispatch", table_cell_bold), Paragraph("Slow administrative approvals (days)", table_cell_style), Paragraph("Automated digital transfer requisition (< 1h)", table_cell_style)],
    ]
    t_comp = Table(comp_data, colWidths=[115, 185, 215])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0F766E")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 6))

    # ── SECTION 2: SYSTEM OVERVIEW ──
    story.append(Paragraph("2. System Overview & Core Modules", h1_style))
    modules_data = [
        [Paragraph("MODULE", table_header_style), Paragraph("KEY CAPABILITIES", table_header_style), Paragraph("ADMINISTRATIVE VALUE", table_header_style)],
        [Paragraph("Executive Dashboard", table_cell_bold), Paragraph("Macro KPI cards, bed census charts, critical risk alerts, live transfer status.", table_cell_style), Paragraph("Instant executive situational awareness.", table_cell_style)],
        [Paragraph("PHC Network", table_cell_bold), Paragraph("Digital directory of all PHCs, CHCs, SDHs and DHs with contact, GPS & beds.", table_cell_style), Paragraph("100% facility asset and contact mapping.", table_cell_style)],
        [Paragraph("Inventory & Medicines", table_cell_bold), Paragraph("Essential Drug List (EDL) compliance, supply runways (days), batch expiry tracking.", table_cell_style), Paragraph("Eliminates emergency medicine stockouts.", table_cell_style)],
        [Paragraph("Bed & ICU Surge", table_cell_bold), Paragraph("Live occupancy rates for general, ICU and oxygen-supported beds.", table_cell_style), Paragraph("Surge capacity routing & divert planning.", table_cell_style)],
        [Paragraph("Staff & Attendance", table_cell_bold), Paragraph("Clinical rosters (Doctors, Nurses, ANMs, Pharmacists) and shift attendance.", table_cell_style), Paragraph("Enforces 100% clinical doctor coverage.", table_cell_style)],
        [Paragraph("AI Forecasting", table_cell_bold), Paragraph("14-day outpatient footfall and critical drug consumption projections.", table_cell_style), Paragraph("Enables proactive buffer stocking.", table_cell_style)],
        [Paragraph("Risk Early Warnings", table_cell_bold), Paragraph("Automated anomaly detection (Critical, High, Moderate) with AI action prompts.", table_cell_style), Paragraph("Prioritizes urgent interventions.", table_cell_style)],
        [Paragraph("Resource Transfers", table_cell_bold), Paragraph("Inter-facility stock balancing with digital dispatch, approval, and ETA tracking.", table_cell_style), Paragraph("Rapid mutual-aid supply logistics.", table_cell_style)],
        [Paragraph("Audit Logs", table_cell_bold), Paragraph("Immutable compliance ledger of all user actions, logins, and authorizations.", table_cell_style), Paragraph("Complete governance and accountability.", table_cell_style)],
    ]
    t_mod = Table(modules_data, colWidths=[100, 240, 175])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_mod)
    story.append(Spacer(1, 6))

    # Page Break for clean section grouping
    story.append(PageBreak())

    # ── SECTION 3: USER ROLES ──
    story.append(Paragraph("3. Administrative User Roles & Hierarchy", h1_style))
    roles_data = [
        [Paragraph("USER ROLE", table_header_style), Paragraph("ADMINISTRATIVE SCOPE", table_header_style), Paragraph("PRIMARY RESPONSIBILITIES", table_header_style)],
        [Paragraph("National Administrator", table_cell_bold), Paragraph("Nationwide Health Network", table_cell_style), Paragraph("Macro KPIs, inter-state health corridor monitoring, national central buffer allocation.", table_cell_style)],
        [Paragraph("State Administrator", table_cell_bold), Paragraph("State-Wide (All Districts)", table_cell_style), Paragraph("State buffer depots, inter-district resource transfers, regional outbreak surge management.", table_cell_style)],
        [Paragraph("District Administrator (CDMO)", table_cell_bold), Paragraph("District Network (PHCs & CHCs)", table_cell_style), Paragraph("Authorize local resource transfers, review daily census, resolve staffing and stock deficits.", table_cell_style)],
        [Paragraph("PHC Administrator (MO / Store)", table_cell_bold), Paragraph("Local Health Facility", table_cell_style), Paragraph("Daily OPD census entry, medicine inward verification, batch monitoring, transfer requests.", table_cell_style)],
    ]
    t_roles = Table(roles_data, colWidths=[110, 130, 275])
    t_roles.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0D9488")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_roles)
    story.append(Spacer(1, 6))

    # ── SECTION 4: HOW TO USE ──
    story.append(Paragraph("4. Step-by-Step Operational Routine (7 Steps)", h1_style))
    story.append(Paragraph("<b>Step 1: Secure Login:</b> Access <code>http://localhost:3000</code> with authorized government credentials.", bullet_style))
    story.append(Paragraph("<b>Step 2: Executive Dashboard Inspection:</b> Open Dashboard to review 7 top health indicators and live grid sync.", bullet_style))
    story.append(Paragraph("<b>Step 3: Review Health Indicators:</b> Audit facilities mapped, active PHCs, drug availability (%), and bed occupancy.", bullet_style))
    story.append(Paragraph("<b>Step 4: Triage Critical Risk Alerts:</b> Review Red/Amber early warnings (e.g. stockout predicted in < 36 hours).", bullet_style))
    story.append(Paragraph("<b>Step 5: Audit Medicine Inventory:</b> Inspect items with < 7 days supply runway and check cold-chain 2°C-8°C biologicals.", bullet_style))
    story.append(Paragraph("<b>Step 6: Gap Analysis:</b> Identify nearest health centres holding surplus stock of the deficit item.", bullet_style))
    story.append(Paragraph("<b>Step 7: Execute Resource Reallocation:</b> Initiate digital transfer from surplus source to target PHC in one click.", bullet_style))
    story.append(Spacer(1, 6))

    # ── SECTION 5: DASHBOARD EXPLANATION ──
    story.append(Paragraph("5. Dashboard Metrics & Indicator Thresholds", h1_style))
    metrics_data = [
        [Paragraph("INDICATOR", table_header_style), Paragraph("BENCHMARK", table_header_style), Paragraph("OPERATIONAL MEANING", table_header_style), Paragraph("ACTION THRESHOLD", table_header_style)],
        [Paragraph("Total Facilities", table_cell_bold), Paragraph("1,248 Units", table_cell_style), Paragraph("Total mapped public health facilities in grid", table_cell_style), Paragraph("Maintain 100% digital telemetry", table_cell_style)],
        [Paragraph("Active PHCs", table_cell_bold), Paragraph("892 Units (98.6%)", table_cell_style), Paragraph("Health centres actively reporting daily OPD", table_cell_style), Paragraph("Flag if active rate drops < 95%", table_cell_style)],
        [Paragraph("Medicine Availability", table_cell_bold), Paragraph("92.4%", table_cell_style), Paragraph("Essential Drug List (EDL) in-stock ratio", table_cell_style), Paragraph("Target >= 90%. Action below 85%", table_cell_style)],
        [Paragraph("Bed Availability", table_cell_bold), Paragraph("74.8% (4,820 Ready)", table_cell_style), Paragraph("Occupancy load across general & ICU wards", table_cell_style), Paragraph("Prepare surge divert if > 85%", table_cell_style)],
        [Paragraph("Staff Strength", table_cell_bold), Paragraph("6,420 (91.4%)", table_cell_style), Paragraph("Registered doctors, nurses, ANMs on duty", table_cell_style), Paragraph("Audit rosters with attendance < 90%", table_cell_style)],
        [Paragraph("Critical Alerts", table_cell_bold), Paragraph("3 Active", table_cell_style), Paragraph("Imminent stockouts or outbreak surges", table_cell_style), Paragraph("Action within 24 hours mandatory", table_cell_style)],
        [Paragraph("Pending Transfers", table_cell_bold), Paragraph("8 En-Route", table_cell_style), Paragraph("Active inter-facility logistics shipments", table_cell_style), Paragraph("Monitor deliveries taking > 6h", table_cell_style)],
    ]
    t_met = Table(metrics_data, colWidths=[100, 95, 175, 145])
    t_met.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_met)
    story.append(Spacer(1, 6))

    # Page Break for clean presentation
    story.append(PageBreak())

    # ── SECTION 6: COMMON USER WORKFLOWS ──
    story.append(Paragraph("6. Practical User Walkthrough Scenarios", h1_style))

    story.append(Paragraph("Scenario A: Resolving a Critical Medicine Stockout Threat", h2_style))
    story.append(Paragraph("<b>1. Alert Trigger:</b> District dashboard flags Red alert: <i>'Tangi CHC Amoxicillin stockout in < 36 hrs (80 vials remain)'</i>.", bullet_style))
    story.append(Paragraph("<b>2. Automated Discovery:</b> System scans regional inventory and identifies <i>SCB Medical College Store</i> with 4,200 surplus vials (35 km away).", bullet_style))
    story.append(Paragraph("<b>3. Requisition Approval:</b> CDMO authorizes transfer of 1,000 vials. Depot confirms packing; status updates to <b>In Transit</b>.", bullet_style))
    story.append(Paragraph("<b>4. Delivery & Verification:</b> Tangi CHC scans batch QR code on arrival. Inventory increments and alert auto-resolves.", bullet_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("Scenario B: Emergency Bed Surge Management During Outbreak", h2_style))
    story.append(Paragraph("<b>1. Outbreak Flag:</b> Dengue cluster detected in Gop Block; <i>Konark PHC</i> reaches 93.3% bed occupancy (28/30 beds).", bullet_style))
    story.append(Paragraph("<b>2. Cluster Capacity Scan:</b> District Officer reviews Bed Management map, finding <i>Pipili PHC</i> (22 km away) at 58% occupancy with 10 vacant beds.", bullet_style))
    story.append(Paragraph("<b>3. Proactive Divert:</b> 108 emergency ambulance dispatch protocol temporarily diverts non-critical admissions to Pipili PHC.", bullet_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("Scenario C: Weekend Specialist & Nursing Deficit Resolution", h2_style))
    story.append(Paragraph("<b>1. Gap Detection:</b> Staff module flags zero anesthetist coverage for upcoming Saturday night shift at <i>Soro SDH</i>.", bullet_style))
    story.append(Paragraph("<b>2. Reserve Pool Lookup:</b> System finds 2 available specialist officers on reserve duty in the Balasore District Headquarters pool.", bullet_style))
    story.append(Paragraph("<b>3. Digital Assignment:</b> Administrator issues temporary roster reassignment, transmitting automated SMS confirmation.", bullet_style))
    story.append(Spacer(1, 6))

    # ── SECTION 7: BEST PRACTICES ──
    story.append(Paragraph("7. Administrative Best Practice Guidelines", h1_style))
    bp_data = [
        [Paragraph("TIMING", table_header_style), Paragraph("PROTOCOL", table_header_style), Paragraph("KEY OBJECTIVE", table_header_style)],
        [Paragraph("08:30 IST (Morning)", table_cell_bold), Paragraph("Review top KPI cards; triage Red critical alerts.", table_cell_style), Paragraph("Prevent same-day stockouts and clinical disruptions.", table_cell_style)],
        [Paragraph("14:00 IST (Mid-Day)", table_cell_bold), Paragraph("Authorize inter-facility transfer slips; audit inward arrivals.", table_cell_style), Paragraph("Ensure timely logistics dispatch before road peak hours.", table_cell_style)],
        [Paragraph("17:30 IST (Evening)", table_cell_bold), Paragraph("Verify bed occupancy updates; audit clinical duty rosters.", table_cell_style), Paragraph("Guarantee 100% emergency night-shift coverage.", table_cell_style)],
        [Paragraph("Weekly Audit", table_cell_bold), Paragraph("Review 14-day AI forecast models and 90-day expiry schedules.", table_cell_style), Paragraph("Zero medicine expiration waste across all district depots.", table_cell_style)],
    ]
    t_bp = Table(bp_data, colWidths=[95, 235, 185])
    t_bp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0D9488")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_bp)
    story.append(Spacer(1, 6))

    # ── SECTION 8: FAQ ──
    story.append(Paragraph("8. Frequently Asked Questions (FAQ)", h1_style))
    story.append(Paragraph("<b>Q1: What is SwasthyaGrid?</b><br/><b>A:</b> An AI-powered public health resilience platform unifying Primary Health Centres, Community Health Centres, and District Hospitals into a coordinated resource tracking and mutual-aid sharing network.", body_style))
    story.append(Paragraph("<b>Q2: Who is authorized to access SwasthyaGrid?</b><br/><b>A:</b> Public health personnel including National Health Mission directors, State Health Secretaries, Chief District Medical Officers (CDMOs), PHC Medical Officers, Hospital Superintendents, and medical storekeepers.", body_style))
    story.append(Paragraph("<b>Q3: What data does the platform manage?</b><br/><b>A:</b> Essential medicine inventory, batch expiries, cold-chain telemetry (2-8°C), general & ICU bed census, clinical duty rosters, epidemiological outbreak indicators, and inter-facility logistics.", body_style))
    story.append(Paragraph("<b>Q4: How does SwasthyaGrid support decision-making?</b><br/><b>A:</b> Replaces slow manual reports with real-time telemetry, automated risk alerts, and prescriptive AI recommendations that calculate exact transfer amounts to avert shortages.", body_style))
    story.append(Paragraph("<b>Q5: Can the platform scale across multiple states?</b><br/><b>A:</b> Yes. SwasthyaGrid is architected on a high-concurrency microservice foundation designed to connect over 30,000 health centres nationwide across all states and union territories.", body_style))
    story.append(Spacer(1, 6))

    # Support Box
    support_html = "<b>National Health Systems Helpdesk:</b> Email: <code>support@swasthya-grid.gov.in</code> | Toll-Free Emergency Helpline: <code>1800-11-HEALTH</code> | National Health Mission Integrated Operations Command"
    support_table = Table([[Paragraph(support_html, callout_style)]], colWidths=[515])
    support_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(support_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {filename}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "SwasthyaGrid_User_Guide.pdf"
    build_pdf(out_file)
