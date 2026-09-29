"""Domain models for Munnadharam AI: Kerala Prior Deeds Title Lineage Auditor."""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class DeedType(str, Enum):
    PATTAYAM = "Pattayam (Govt Land Assignment)"
    THEERADHARAM = "Theeradharam (Sale Deed)"
    BHAGAPATHRAM = "Bhagapathram (Partition Deed)"
    OZHIVUMURI = "Ozhivumuri (Release Deed)"
    DHANAM = "Dhanam (Gift Deed)"
    SETTLEMENT = "Settlement Deed"
    WILL_UDANPADI = "Will / Udanpadi"
    COURT_DECREE = "Court Decree / Auction"


class RiskSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class DeedNode(BaseModel):
    """Represents a single registered instrument in the chain of title."""
    doc_number: str = Field(description="Document number with year, e.g. 1420/1994")
    year: int
    sro_name: str = Field(description="Sub-Registrar Office where registered")
    deed_type: DeedType
    grantors: List[str] = Field(description="Parties conveying title (sellers / releasors / donors)")
    grantees: List[str] = Field(description="Parties receiving title (buyers / releasees / donees)")
    extent_cents: float = Field(description="Land extent mentioned in cents (1 cent = 40.4686 sq m)")
    survey_no: str
    resurvey_no: Optional[str] = None
    consideration_inr: float = 0.0
    prior_doc_referenced: Optional[str] = None
    
    # Crucial legal condition markers
    is_minor_involved: bool = False
    minor_court_sanction_present: bool = False
    unrepresented_heirs: List[str] = Field(default_factory=list, description="Known legal heirs omitted from partition or release")
    easements_reserved: List[str] = Field(default_factory=list, description="Easements, pathways, or well-access covenants")
    family_religion: Optional[str] = "hindu"  # hindu, christian, muslim


class ECRecord(BaseModel):
    """Represents an entry in the SRO Encumbrance Certificate (EC)."""
    doc_number: str
    year: int
    sro_name: str
    nature: str
    parties: List[str] = Field(default_factory=list)


class RiskFlag(BaseModel):
    category: str
    severity: RiskSeverity
    title: str
    description: str
    legal_citation: str
    remedial_action: str


class CleanTitleScorecard(BaseModel):
    property_identifier: str
    overall_score: int
    risk_level: str
    chain_of_custody_intact: bool
    lineage_path: List[str]
    risk_flags: List[RiskFlag]
    recommendations_for_advocate: List[str]
