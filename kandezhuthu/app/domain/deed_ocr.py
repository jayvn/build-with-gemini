"""Multimodal Deed OCR & Document Ingestion Engine for Kerala Real Estate Deeds.

Uses Gemini Vision models via Google GenAI SDK to read scanned Malayalam & English
deed documents (PDF, PNG, JPG, WEBP), extract 4 boundaries (ചതുരതിരുകൾ),
extent (വിസ്തീർണ്ണം), prior deeds (മുന്നാധാരം), and pipe them directly into
deterministic legal sanity auditing and database persistence.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

from dotenv import load_dotenv
from google.genai import Client, types
from pydantic import BaseModel, Field

from app.db.repository import AuditRepository, KnowledgeRepository
from app.domain.single_deed_scanner import DeedSanityResult, SingleDeedScanner

load_dotenv()
logger = logging.getLogger(__name__)

# Primary OCR vision models supported on Vertex AI / Gemini API
OCR_MODEL_CANDIDATES = [
    "gemini-2.5-flash",
    "gemini-1.5-flash",
]


class DeedBoundary(BaseModel):
    direction: str = Field(description="Direction: East (കിഴക്ക്), South (തെക്ക്), West (പടിഞ്ഞാറ്), or North (വടക്ക്)")
    boundary_description: str = Field(description="Boundary description (e.g. 'Road / പഞ്ചായത്ത് വഴി', 'Canal / തോട്', 'Property of...')")


class PriorDeedReference(BaseModel):
    doc_number: str = Field(description="Document registration number (e.g. '1420/2014')")
    year: int | None = Field(default=None, description="Year of registration")
    sro_name: str | None = Field(default=None, description="Sub-Registrar Office name")
    deed_type: str | None = Field(default=None, description="Deed type (e.g. 'Theeradharam', 'Bhagapathram', 'Pattayam')")
    grantor: str | None = Field(default=None, description="Grantor or prior owner name")
    grantee: str | None = Field(default=None, description="Grantee or acquirer name")
    notes: str | None = Field(default=None, description="Any specific recitals regarding this prior title")


class ExtractedDeedMetadata(BaseModel):
    document_number: str | None = Field(default=None, description="Document number of the current deed (e.g. '892/2018')")
    year: int | None = Field(default=None, description="Registration year")
    sro_name: str | None = Field(default=None, description="Sub-Registrar Office (SRO) name (e.g. 'Aluva', 'Ernakulam')")
    deed_type: str | None = Field(default=None, description="Nature of deed (e.g. 'തീറാധാരം / Sale Deed', 'ഭാഗപത്രം / Partition Deed')")
    survey_no: str = Field(default="Unknown", description="Survey or Re-Survey number (e.g. '345/1', '120/4B')")
    re_survey_no: str | None = Field(default=None, description="Re-survey number if differentiated")
    village: str = Field(default="Unknown", description="Village name")
    taluk: str | None = Field(default=None, description="Taluk name")
    district: str | None = Field(default=None, description="District name in Kerala")
    extent_cents: float = Field(default=0.0, description="Total land area in Kerala Cents")
    extent_ares: float | None = Field(default=None, description="Land area in Ares (1 Cent = 0.404686 Ares)")
    revenue_classification: str = Field(default="Purayidam", description="BTR / Revenue classification: 'Purayidam' (Garden/Dry land) or 'Nilam' (Paddy/Wetland)")
    is_paddy_wetland_risk: bool = Field(default=False, description="True if text mentions Nilam, Nanja, Punja, Thanneerthadam, or paddy land history")
    boundaries: list[DeedBoundary] = Field(default_factory=list, description="4 boundaries of the property schedule")
    grantors: list[str] = Field(default_factory=list, description="Names of sellers / transferors")
    grantees: list[str] = Field(default_factory=list, description="Names of buyers / transferees")
    prior_deeds: list[PriorDeedReference] = Field(default_factory=list, description="All prior deeds (Munnadharam) mentioned in recitals")
    easements_reserved: list[str] = Field(default_factory=list, description="Pathways, right-of-way, well access, or servitude clauses reserved")
    minor_involvement: str | None = Field(default=None, description="Any mention of minor children, guardians, or District Court orders")
    maintenance_covenants: str | None = Field(default=None, description="Any condition to maintain parents/donors or life interest reservation")
    raw_schedule_snippet: str = Field(default="", description="Verbatim Malayalam or English text snippet of property schedule and recitals")
    malayalam_summary: str = Field(default="", description="Concise bilingual summary of the property in Malayalam & English")


class DeedOCRResult(BaseModel):
    metadata: ExtractedDeedMetadata
    sanity_result: DeedSanityResult
    building_rules: dict[str, Any] | None = None
    paddy_conversion: dict[str, Any] | None = None
    whatsapp_draft: str = ""
    field_verification_checklist: list[str] = Field(default_factory=list)


def _get_genai_client() -> Client:
    """Instantiates a Google GenAI Client targeting Vertex AI or API key."""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if api_key:
        return Client(api_key=api_key)

    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    return Client(vertexai=True, project=project, location=location)


class DeedOCREngine:
    """Multimodal document understanding engine for Kerala real estate deeds."""

    EXTRACTION_PROMPT = """
You are a senior Kerala High Court Property Document Expert and Malayalam Paleographer.
Analyze the attached scanned Kerala Title Deed (ആധാരം) / Encumbrance Certificate (കുടിക്കടം) image or PDF document.

TASK:
Perform high-precision Optical Character Recognition (OCR) on the Malayalam and English text.
Extract the legal deed particulars, parties, property schedule (ഷെഡ്യൂൾ), four boundaries (ചതുരതിരുകൾ),
prior deeds lineage (മുന്നാധാരം), pathways/easements (നടപ്പുവഴി / വഴിയവകാശം), land nature (നിലം vs പുരയിടം),
and any restrictive covenants into the specified structured JSON schema.

KEY KERALA LEGAL GUIDELINES:
1. Four Boundaries (ചതുരതിരുകൾ):
   - കിഴക്ക് (East), തെക്ക് (South), പടിഞ്ഞാറ് (West), വടക്ക് (North).
   - Accurately record if any boundary specifies a pathway (വഴി), road (റോഡ്), or canal (തോട്).
2. Land Classification (ഭൂമി തരംതിരിവ്):
   - Check if described as പുരയിടം (Purayidam/Garden Land), തോട്ടം (Dry land) OR നിലം (Nilam/Paddy land), നഞ്ച (Nanja), പുഞ്ച (Punja), തണ്ണീർത്തടം (Wetland).
3. Prior Title Lineage (മുന്നാധാരം):
   - Extract any previous deed numbers, registration years, and SRO names cited in the preamble/recitals.
4. Encumbrances & Easements:
   - Carefully extract any pathway reservations (e.g., "3 മീറ്റർ വീതിയിൽ വഴി അവകാശം", "നടപ്പുവഴി"), well access (കിണർ അവകാശം), or senior citizen maintenance conditions.
5. Area & Units:
   - Convert or record extent in Cents (സെന്റ്) and Ares (ആർ). (1 Cent = 0.404686 Ares).

Extract all details faithfully without fabrication. If a field is not mentioned in the document, leave it as null or empty list.
"""

    def __init__(self, client: Client | None = None):
        self.client = client or _get_genai_client()
        self.scanner = SingleDeedScanner()
        self.knowledge_repo = KnowledgeRepository()
        self.audit_repo = AuditRepository()

    def process_file_bytes(
        self,
        file_bytes: bytes,
        mime_type: str,
        session_id: str | None = None,
    ) -> DeedOCRResult:
        """Processes deed bytes (PDF or Image), performs multimodal OCR, evaluates legal traps, and persists findings."""
        part = types.Part.from_bytes(data=file_bytes, mime_type=mime_type)

        last_error = None
        extracted_metadata: ExtractedDeedMetadata | None = None

        for model_name in OCR_MODEL_CANDIDATES:
            try:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=[part, self.EXTRACTION_PROMPT],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=ExtractedDeedMetadata,
                        temperature=0.1,
                    ),
                )
                if response.text:
                    parsed_json = json.loads(response.text)
                    extracted_metadata = ExtractedDeedMetadata(**parsed_json)
                    logger.info(f"Successfully extracted deed metadata using {model_name}")
                    break
            except Exception as e:
                logger.warning(f"Failed OCR extraction with model {model_name}: {e}")
                last_error = e

        if not extracted_metadata:
            raise RuntimeError(f"Multimodal OCR extraction failed across all model candidates: {last_error}")

        # Deterministic Legal Sanity Scan
        scan_payload = (
            f"Property Schedule:\n"
            f"Survey No: {extracted_metadata.survey_no}, Village: {extracted_metadata.village}\n"
            f"Extent: {extracted_metadata.extent_cents} Cents\n"
            f"Classification: {extracted_metadata.revenue_classification}\n"
            f"Boundaries:\n"
            + "\n".join(f"- {b.direction}: {b.boundary_description}" for b in extracted_metadata.boundaries)
            + f"\nEasements: {', '.join(extracted_metadata.easements_reserved) if extracted_metadata.easements_reserved else 'None'}\n"
            f"Minor: {extracted_metadata.minor_involvement or 'None'}\n"
            f"Maintenance: {extracted_metadata.maintenance_covenants or 'None'}\n\n"
            f"Verbatim Snippet:\n{extracted_metadata.raw_schedule_snippet}"
        )

        sanity_result = self.scanner.scan(scan_payload)

        # Lookup KPBR 2019 Building Rules for the plot extent
        building_rule = None
        if extracted_metadata.extent_cents > 0:
            building_rule = self.knowledge_repo.get_building_rule(
                plot_cents=extracted_metadata.extent_cents,
                occupancy_type="residential",
            )

        # Calculate Paddy Conversion Fee if classified as Nilam or flagged as wetland
        paddy_calc = None
        if extracted_metadata.revenue_classification.lower() == "nilam" or extracted_metadata.is_paddy_wetland_risk:
            paddy_calc = self.knowledge_repo.calculate_paddy_conversion_fee(
                plot_cents=extracted_metadata.extent_cents or 10.0,
                fair_value_per_are=200000.0,  # Benchmark default fair value
            )

        # Generate culturally polite WhatsApp draft for seller
        whatsapp_draft = ""
        for finding in sanity_result.findings:
            if finding.whatsapp_question_for_seller:
                whatsapp_draft = finding.whatsapp_question_for_seller
                break

        if not whatsapp_draft:
            whatsapp_draft = (
                f"നമസ്കാരം, സർവേ നമ്പർ {extracted_metadata.survey_no}-ൽപ്പെട്ട {extracted_metadata.extent_cents} സെന്റ് "
                f"വസ്തുവിന്റെ മുൻ ആധാരങ്ങളുടെ പകർപ്പും (മുന്നാധാരം), പുതിയ കുടിക്കട സർട്ടിഫിക്കറ്റും (EC - കഴിഞ്ഞ 30 വർഷത്തെ) "
                f"അഡ്വാൻസ് നൽകുന്നതിന് മുൻപായി ഒന്ന് അയച്ചുതരുമോ? നന്ദി."
            )

        # Persist scan into database
        try:
            self.audit_repo.save_single_deed_scan(
                snippet=scan_payload,
                result_dict=sanity_result.model_dump(),
                session_id=session_id,
            )
        except Exception as e:
            logger.warning(f"Could not persist deed scan to database: {e}")

        return DeedOCRResult(
            metadata=extracted_metadata,
            sanity_result=sanity_result,
            building_rules=building_rule,
            paddy_conversion=paddy_calc,
            whatsapp_draft=whatsapp_draft,
            field_verification_checklist=sanity_result.what_ai_cannot_verify,
        )
