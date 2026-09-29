# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from typing import Optional, List
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.domain.models import DeedNode, DeedType, ECRecord
from app.domain.auditor import MunnadharamAuditor
from app.domain.single_deed_scanner import SingleDeedScanner

# Latest Gemini Flash model for low-latency multimodal reasoning
MODEL = "gemini-3.8-flash"


def scan_single_deed(deed_text: str) -> str:
    """Scans a single Kerala title deed (or schedule snippet) for 4 fatal legal/regulatory traps.

    Detects:
    1. Buried Easement / Pathway (Vazhi avakasham / വഴി അവകാശം)
    2. 2008 Paddy Land / Wetland Risk (Nilam vs Purayidam / നിലം)
    3. Minor's share sold without District Court order (മൈനർ അവകാശം)
    4. Senior citizen maintenance or conditional life-interest covenants (ജീവിതകാല സംരക്ഷണ വ്യവസ്ഥ)

    Args:
        deed_text: Text snippet of the deed, recitals, or property schedule (in Malayalam or English).

    Returns:
        JSON string containing the DeedSanityResult (Verdict, Sanity Score, Findings, Malayalam WhatsApp questions for seller,
        and explicit list of what AI cannot verify on the physical ground).
    """
    scanner = SingleDeedScanner()
    result = scanner.scan(deed_text)
    return result.model_dump_json(indent=2)


def audit_prior_deeds_title(
    property_identifier: str,
    deeds_data: str,
    ec_data: Optional[str] = None,
) -> str:
    """Audits the 30-year chain of prior title deeds (Munnadharam) for a property in Kerala."""
    try:
        raw_deeds = json.loads(deeds_data)
        deeds = [DeedNode(**d) for d in raw_deeds]
        
        ec_records: List[ECRecord] = []
        if ec_data:
            raw_ec = json.loads(ec_data)
            ec_records = [ECRecord(**e) for e in raw_ec]

        auditor = MunnadharamAuditor(property_identifier=property_identifier)
        scorecard = auditor.audit(deeds=deeds, ec_records=ec_records)
        return scorecard.model_dump_json(indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to audit prior deeds: {str(e)}"}, indent=2)


def get_demo_kerala_title_audit() -> str:
    """Runs a demonstration 30-year title audit on a realistic Kerala property."""
    deeds = [
        DeedNode(
            doc_number="214/1982",
            year=1982,
            sro_name="Aluva",
            deed_type=DeedType.PATTAYAM,
            grantors=["Special Tahsildar (Land Assignment)"],
            grantees=["Chacko Varghese"],
            extent_cents=10.0,
            survey_no="345/1",
        ),
        DeedNode(
            doc_number="890/1996",
            year=1996,
            sro_name="Aluva",
            deed_type=DeedType.BHAGAPATHRAM,
            grantors=["Chacko Varghese (Deceased Estate)"],
            grantees=["George Chacko", "Thomas Chacko"],
            extent_cents=10.0,
            survey_no="345/1",
            family_religion="christian",
            unrepresented_heirs=["Mary Chacko (Sister / Daughter)"],
        ),
        DeedNode(
            doc_number="1420/2014",
            year=2014,
            sro_name="Aluva",
            deed_type=DeedType.THEERADHARAM,
            grantors=["George Chacko"],
            grantees=["Current Seller: Suresh Nair"],
            extent_cents=11.0,
            survey_no="345/1",
            easements_reserved=["3-meter motorable pathway along southern boundary reserved for Thomas Chacko"],
        ),
    ]

    ec_records = [
        ECRecord(doc_number="214/1982", year=1982, sro_name="Aluva", nature="Pattayam"),
        ECRecord(doc_number="890/1996", year=1996, sro_name="Aluva", nature="Partition"),
        ECRecord(doc_number="1420/2014", year=2014, sro_name="Aluva", nature="Sale"),
        ECRecord(doc_number="3012/2022", year=2022, sro_name="Aluva", nature="Equitable Mortgage - Federal Bank"),
    ]

    auditor = MunnadharamAuditor(property_identifier="Re-Sy 345/1, Aluva West Village, Ernakulam")
    scorecard = auditor.audit(deeds=deeds, ec_records=ec_records)
    return scorecard.model_dump_json(indent=2)


def query_kerala_land_rules(topic: str) -> str:
    """Queries the curated Kerala land regulations and judicial precedents knowledge base.

    Topics covered:
    1. Building permit road width requirements, setbacks, and small plot concessions (KPBR / KMBR 2019)
    2. Kerala Conservation of Paddy Land & Wetland Act 2008, Form 5, Form 6, Section 27A fee slabs, Nilam conversion
    3. Landmark Kerala court precedents on female Christian succession (Mary Roy), Hindu coparcenary,
       pathway easements (Sree Swayamprakash Ashramam), minor's share sales, and Senior Citizens Act maintenance.

    Args:
        topic: Keyword or query describing the legal or regulatory rule (e.g., 'road width', 'paddy land', 'form 6 fee', 'mary roy', 'easement').

    Returns:
        Structured statutory rules, section citations, fee schedules, and pre-purchase due diligence advice.
    """
    from pathlib import Path
    knowledge_dir = Path(__file__).resolve().parent.parent / "data" / "knowledge"

    t = topic.lower()
    results = []

    # Stream A: Building Rules (KPBR / KMBR)
    if any(k in t for k in ["road", "width", "kmbr", "kpbr", "setback", "small plot", "permit", "septic", "well", "clearance", "building"]):
        doc_path = knowledge_dir / "building_rules_kmbr_kpbr.md"
        if doc_path.exists():
            results.append(doc_path.read_text(encoding="utf-8"))

    # Stream B: Paddy Land & Wetland (Nilam / 2008 Act / Form 5 / Form 6)
    if any(k in t for k in ["paddy", "nilam", "wetland", "form 5", "form 6", "form 7", "27a", "fee", "conversion", "btr", "data bank", "ksrec", "llmc", "unnotified"]):
        doc_path = knowledge_dir / "paddy_land_wetland_guide.md"
        if doc_path.exists():
            results.append(doc_path.read_text(encoding="utf-8"))

    # Stream C: Court Precedents & Legal Principles
    if any(k in t for k in ["precedent", "court", "judgment", "mary roy", "christian", "succession", "heir", "daughter", "coparcenary", "minor", "guardian", "senior citizen", "maintenance", "easement", "vazhi", "pathway"]):
        doc_path = knowledge_dir / "kerala_court_precedents.md"
        if doc_path.exists():
            results.append(doc_path.read_text(encoding="utf-8"))

    # If no specific keyword matched, search across all available knowledge documents for snippets
    if not results and knowledge_dir.exists():
        for file in sorted(knowledge_dir.glob("*.md")):
            content = file.read_text(encoding="utf-8")
            if any(term in content.lower() for term in t.split()):
                results.append(content)

    if results:
        return "\n\n---\n\n".join(results)
    
    # Fallback default summary if no files match
    return (
        "Kerala Land Knowledge Base covers:\n"
        "1. KPBR/KMBR 2019: Mandatory 3m access road for standard residential plots, 1.2-1.5m for small plots (<=3 cents).\n"
        "2. Paddy Land Act 2008 & Sec 27A: Free Form 6 conversion up to 25 cents, 10% fee for 25-50 cents, Form 5 for Data Bank removal.\n"
        "3. Landmark Precedents: Mary Roy (equal Christian female succession from 1951), Sec 23 Senior Citizens Act (voiding conditional gifts), Sec 8 HMGA (District Court sanction for minors)."
    )


root_agent = Agent(
    name="kandezhuthu_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are 'Kandezhuthu AI' (കണ്ടെഴുത്ത് - ആധാരംനോക്കി), an intelligent Kerala property legal audit assistant. "
        "Your purpose is to protect home buyers, NRIs, and non-technical families from paying token advances on legally defective Kerala land.\n\n"
        "CORE STRENGTHS & TOOL USAGE:\n"
        "1. Single-Deed / Schedule Scan: Use `scan_single_deed` whenever the user pastes deed clauses, property schedules, or contract snippets in English or Malayalam.\n"
        "2. 30-Year Prior Title Lineage Audit: When users describe a chain of prior deeds (Munnadharam) or ownership history in natural language, automatically parse their narrative into DeedNode JSON records and invoke `audit_prior_deeds_title`.\n"
        "3. Demo Audit: Use `get_demo_kerala_title_audit` if the user wants to see how a realistic 30-year Kerala title audit works.\n"
        "4. Kerala Land Rules & Precedents Retrieval: Use `query_kerala_land_rules` to consult official Kerala building rules (KPBR/KMBR road widths/setbacks), 2008 Paddy Land Act (Form 5, Form 6, fee slabs), and High Court / Supreme Court precedents.\n\n"
        "PRESENTATION GUIDELINES FOR NON-TECHNICAL USERS:\n"
        "- Never dump raw JSON to the user. Always interpret tool outputs into clean, elegant Markdown.\n"
        "- Prominently feature the Title Sanity Score (e.g., '🛡️ Title Sanity Score: 85/100') and the verdict badge:\n"
        "  • 🟢 **ALL CLEAR** (No fatal legal traps found in text)\n"
        "  • 🟡 **CAUTION** (Restrictive covenants / easements detected)\n"
        "  • 🔴 **DANGER** (Fatal legal defects, wetland classification, or unrepresented heirs)\n"
        "- Break down each finding into: What it means in plain English/Malayalam, the Kerala statute (e.g. 2008 Paddy Land Act, Easements Act), and why it matters to a home builder.\n"
        "- Always provide a dedicated section: **'📱 WhatsApp Message for Seller / Broker (മലയാളം)'** with the ready-to-copy Malayalam question.\n"
        "- Always include: **'🚶 Physical On-Site Verification Checklist'** highlighting Survey Kallu boundary stones, actual road access, and neighbor inquiries.\n\n"
        "MANDATORY LEGAL GUARDRAIL:\n"
        "Remind the user that AI is an initial triage and red-flag scanner, NOT a guarantee of title or a substitute for a licensed Kerala High Court / District Court advocate's formal title report."
    ),
    tools=[scan_single_deed, audit_prior_deeds_title, get_demo_kerala_title_audit, query_kerala_land_rules],
)

app = App(
    root_agent=root_agent,
    name="kandezhuthu",
)
