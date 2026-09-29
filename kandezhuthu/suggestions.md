# 🌴 Kandezhuthu AI (കണ്ടെഴുത്ത് - ആധാരംനോക്കി)
## Comprehensive UI/UX Test Audit & Strategic Product Roadmap (`suggestions.md`)

---

## 1. Executive Summary & Automated Playwright UI Testing Results

To guarantee that **Kandezhuthu AI** is intuitive and frictionless for non-technical buyers, Non-Resident Indians (NRIs), and advocates, an end-to-end automated UI test suite was built and executed using **Playwright** (`tests/ui/test_ui_playwright.py`). 

### Automated Test Suite Execution
- **Test Framework**: Playwright Python 1.63.0 on Chromium Linux Headless
- **Target URL**: `http://localhost:8081` (Local FastAPI Runner with Leaflet + Google Maps Satellite)
- **Viewport Profiles Tested**:
  - **Desktop Workstation**: 1440 × 900 (High-DPI Split View & Map Inspection)
  - **Mobile Device**: 375 × 812 (iPhone X/12 Mobile Field Inspection)
- **Test Run Outcome**: **8 / 8 Tests Passed (100% Success Rate)**
- **Console Errors**: Zero functional runtime errors.

| Test Case | Scenario Tested | Status | Visual Evidence |
|---|---|---|---|
| **01_initial_split_view** | Initial dual-pane split view, Google Satellite Hybrid tiles, sample plot HUD | ✅ PASSED | `01_initial_split_view.png` |
| **02_view_switcher** | Seamless switching between Chat-Only, Map-Only, and Split layouts | ✅ PASSED | `02_chat_only_view.png`, `03_map_only_view.png` |
| **03_preset_kakkanad** | Selecting Kerala region preset (Kakkanad / Infopark), updating coordinates & HUD | ✅ PASSED | `04_preset_kakkanad.png` |
| **04_draw_plot_and_undo** | Interactive plot polygon drawing, Cents calculation, and **Undo Point** action | ✅ PASSED | `05_drawn_plot.png` |
| **05_road_width** | Two-point access road measurement and statutory **KPBR 2019 Rule Badge** | ✅ PASSED | `06_road_width_measurement.png` |
| **06_send_plot_to_auditor** | HUD "Send Plot to Auditor AI" bridge populating chat input and initiating triage | ✅ PASSED | `07_plot_sent_to_auditor.png` |
| **07_agent_response** | Gemini 3.8 Flash live inference, Kerala building rules analysis & WhatsApp draft | ✅ PASSED | `08_agent_response_received.png` |
| **08_mobile_view** | Mobile viewport (375px) responsive layout, full-width selectors, and touch UI | ✅ PASSED | `09_mobile_initial.png`, `10_mobile_map_view.png` |

---

## 2. Intuitiveness Upgrades Implemented in this Cycle

Based on screenshot analysis and friction discovery during Playwright testing, the following usability improvements were implemented in `frontend/static/index.html`:

1. **Active Tool Interactive Guidance Bar (`.map-guidance-bar`)**:
   - Positioned directly below the map toolbar with clear contextual instructions for each tool mode (*Pin Location*, *Draw Plot*, *Measure Road*).
   - In plot drawing mode, displays live corner count: `Plot in progress: 4 corner stones marked (10.85 Cents). Click 'Seal Plot' to finish.`

2. **Undo Last Point Capability (`↩️ Undo`)**:
   - Added an active `Undo` button in both the map toolbar and guidance bar.
   - Allows users who misclick a boundary stone (*Survey Kallu*) to pop the last point without having to clear and redraw the entire plot.

3. **Survey-Style Segment Dimensioning (FMB Style)**:
   - Along each boundary edge of a drawn plot, lightweight floating dimension badges dynamically display edge lengths in meters (e.g. `21.9m`, `18.5m`).
   - Directly mirrors how Kerala Survey sketches (*Field Measurement Book - FMB*) record property boundaries.

4. **Interactive On-Site Field Check Essentials (`.checklist-panel`)**:
   - Replaced the intrusive static overlay with a toggleable panel and toolbar badge showing completion progress (e.g., `Checklist 2/4`).
   - Users on-site can check off:
     - [ ] **Survey Kallu**: All 4 boundary corner stones physically verified.
     - [ ] **Road Access**: Minimum 3.0m motorable road confirmed for KPBR permit.
     - [ ] **Wetland Proximity**: Spotting adjacent paddy fields/streams via satellite.
     - [ ] **Overhead Lines**: Absence of dangerous High-Tension (HT) electric lines.

5. **Minimizable & Responsive Live Plot HUD (`.map-hud`)**:
   - Added a minimize toggle (`_` / `↗`) so users can collapse the HUD when inspecting satellite tile details.
   - Formatted road width with instant color-coded KPBR badges:
     - `✅ KPBR Pass (≥3m)` (Green)
     - `⚠️ Small Plot Only (1.2m–3m)` (Amber - KPBR Rule 59 restricted built-up area)
     - `❌ Defective Access (<1.2m)` (Red - Fatal permit trap)
   - Displays land extent in **Kerala Cents**, **Revenue Ares**, and **Square Meters**.

6. **Clean Malayalam WhatsApp Inquiry Card & Direct Share**:
   - Fixed regex parsing so legal disclaimers and statutory guardrails never bleed into the seller inquiry draft.
   - Added a direct **💬 Open in WhatsApp** link (`https://api.whatsapp.com/send?text=...`) alongside the copy button for instant 1-tap messaging to brokers and sellers.

---

## 3. Prioritized Strategic Roadmap & Suggestions

### Tier 1: High Priority (Immediate Value for Kerala Property Buyers)

#### 1.1 Drag-and-Drop Deed Image & PDF OCR (Multimodal Ingestion)
- **Problem**: Most Kerala buyers possess scanned PDFs or mobile photos of Malayalam sale deeds (*Theeradharam*), partition deeds (*Bhagapathram*), and settlement deeds (*Dhananischayam*). Manually typing legal recitals into chat creates friction.
- **Suggestion**: Add a drag-and-drop file uploader in the chat pane. Use Gemini 3.8 Flash's native vision capabilities with OCR prompt engineering tailored for Malayalam legal script to automatically extract:
  - Document Number, Year, and Sub-Registrar Office (SRO).
  - Prior Deed references (*Munnadharam* numbers and dates).
  - Schedule description: Re-Survey number, Block number, Extent in Cents/Ares, and Four Boundaries (*Chathur-sthaakol* / ചതുർസീമകൾ).
  - Buried covenants (pathway rights, life interest, maintenance clauses).

#### 1.2 Draggable Boundary Vertices
- **Problem**: When a user clicks to place a corner stone on satellite imagery, minor finger or mouse slippage can place the stone 1–2 meters off the fence line.
- **Suggestion**: Make polygon vertices draggable. When a user drags a vertex, dynamically recalculate edge distances and land extent in Kerala Cents in real-time.

#### 1.3 Automatic SRO Encumbrance Certificate (EC) PDF Ingestion
- **Problem**: Kerala SROs issue digitized Nil-Encumbrance / Encumbrance Certificates through `pearl.registration.kerala.gov.in`. Non-lawyers struggle to read the tabular format.
- **Suggestion**: Create an EC PDF parser tool that extracts tabular registration columns (Volume, Page, Doc No, Consideration, Nature of Act: Gehan, Mortgage, Attachment). Cross-reference directly with the title chain to flag undisclosed bank loans or civil court attachments.

---

### Tier 2: Kerala GIS & Satellite Diligence Innovations

#### 2.1 Cadastral Survey Sketch Overlay (BhuNaksha / ILIMS Integration)
- **Problem**: Satellite imagery shows trees, roofs, and walls, but legal property boundaries are defined by Revenue Survey Subdivisions (*Re-Survey Sub-division sketch*).
- **Suggestion**:
  - Connect to the Kerala Revenue Department's **BhuNaksha / ILIMS Web Map Service (WMS)** where publicly accessible.
  - Allow users to enter District, Taluk, Village, Block, and Re-Survey Number (e.g., *Ernakulam / Aluva / Aluva West / Block 12 / Re-Sy 345/1*) to auto-fetch and overlay the official digital cadastral parcel boundaries directly onto the satellite layer.

#### 2.2 KSDMA Flood Hazard & Topography Layer
- **Problem**: Plots in river valleys (Periyar, Pamba, Meenachil) or wetland fringes may appear dry in February/March but submerge under 6 feet of water during the South-West Monsoon.
- **Suggestion**:
  - Overlay Kerala State Disaster Management Authority (KSDMA) 100-year flood hazard maps and high-resolution elevation contours (SRTM/Copernicus 30m DEM).
  - Alert the buyer: `⚠️ Flood Risk Warning: This plot is in the 2018 Periyar Inundation Zone (Elevation: +3.2m MSL). Check physical high-water marks on adjacent compound walls.`

#### 2.3 Kerala Agricultural Data Bank Overlay (Paddy Land Act 2008)
- **Problem**: If land is included in the statutory *Data Bank* prepared by the Local Level Monitoring Committee (LLMC), it cannot be used for house construction without Form 5 exclusion, even if physically dry.
- **Suggestion**: Integrate village-level Data Bank records. When a user selects a survey number, check whether it is marked as *Paddy / Nilam* in the Data Bank and calculate the applicable Form 6 conversion fee under Section 27A (including the 25-cent free exemption rule).

---

### Tier 3: Workflow & NRI Accessibility

#### 3.1 WhatsApp Bot & Telegram Forwarding Channel
- **Problem**: NRIs in the GCC (UAE, Saudi Arabia, Qatar) frequently receive deed photos and Google Maps location pins from brokers while on mobile messaging apps.
- **Suggestion**: Deploy a webhook connecting a Twilio WhatsApp Business number directly to the Kandezhuthu FastAPI server. Allow an NRI buyer to forward a location pin and deed photo, receiving a 60-second audio summary and PDF scorecard directly in their WhatsApp chat.

#### 3.2 Offline Field Inspection Mode (PWA with Local Storage)
- **Problem**: Remote rural plots in Idukki, Wayanad, or eastern Pathanamthitta often have weak cellular data connectivity during on-site property walkthroughs.
- **Suggestion**: Turn the frontend into an installable Progressive Web App (PWA). Pre-cache selected village satellite tiles and allow users to record GPS waypoints, take photos of physical boundary stones (*Survey Kallu*), and check off items offline, syncing back once 4G is restored.

#### 3.3 One-Click Advocate-Ready Legal Dossier Export (PDF)
- **Problem**: Buyers need to hand over findings to a licensed Kerala High Court or District advocate for final vetting before executing the agreement.
- **Suggestion**: Add an "Export Title Audit Report" button that compiles:
  - Satellite plot boundary with FMB side dimensions and coordinates.
  - 30-year chronological chain of title with flagged gaps.
  - Statutory KPBR road compliance scorecard.
  - 5 specific legal questions customized for the advocate to verify in SRO Volume Registers (*Pothu Vivaram*).

---

## 4. Summary Table of Proposed Enhancements

| Feature | Category | Effort | Impact | Target Users |
|---|---|---|---|---|
| **Multimodal Deed Image OCR** | AI / Agent | Medium | 🟢 High | All buyers, NRIs |
| **Draggable Boundary Stones** | Frontend UX | Low | 🟢 High | Surveyors, Buyers |
| **BhuNaksha Cadastral Overlay** | GIS / Map | High | 🟢 Critical | Buyers, Advocates |
| **KSDMA Flood Zonation** | GIS / Safety | Medium | 🟡 High | Home Builders |
| **EC PDF Automated Audit** | Legal / NLP | Medium | 🟢 Critical | Advocates, NRIs |
| **WhatsApp Bot Gateway** | Platform | Medium | 🟢 High | GCC NRIs, Brokers |
| **Advocate PDF Dossier Export** | Reporting | Low | 🟡 Medium | Buyers |
| **Offline PWA Caching** | Mobile / Offline | Medium | 🟡 Medium | On-site Surveyors |

---
*Generated by Kandezhuthu AI Engineering Team — Safeguarding Kerala Real Estate Buyers.*
