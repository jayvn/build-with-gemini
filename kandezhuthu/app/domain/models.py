"""Domain models for Munnadharam AI: Kerala Prior Deeds Title Lineage Auditor."""

from enum import Enum

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
    grantors: list[str] = Field(description="Parties conveying title (sellers / releasors / donors)")
    grantees: list[str] = Field(description="Parties receiving title (buyers / releasees / donees)")
    extent_cents: float = Field(description="Land extent mentioned in cents (1 cent = 40.4686 sq m)")
    survey_no: str
    resurvey_no: str | None = None
    consideration_inr: float = 0.0
    prior_doc_referenced: str | None = None

    # Crucial legal condition markers
    is_minor_involved: bool = False
    minor_court_sanction_present: bool = False
    unrepresented_heirs: list[str] = Field(default_factory=list, description="Known legal heirs omitted from partition or release")
    easements_reserved: list[str] = Field(default_factory=list, description="Easements, pathways, or well-access covenants")
    family_religion: str | None = "hindu"  # hindu, christian, muslim


class ECRecord(BaseModel):
    """Represents an entry in the SRO Encumbrance Certificate (EC)."""
    doc_number: str
    year: int
    sro_name: str
    nature: str
    parties: list[str] = Field(default_factory=list)


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
    lineage_path: list[str]
    risk_flags: list[RiskFlag]
    recommendations_for_advocate: list[str]


class BuildingRuleMatch(BaseModel):
    occupancy_group: str
    plot_category: str
    min_road_width_m: float
    front_setback_m: float
    rear_setback_m: float
    side_setback_1_m: float
    side_setback_2_m: float
    well_septic_clearance_m: float = 7.5
    dead_wall_permitted: bool = False
    rule_citation: str
    notes: str | None = None


class PaddyLandFeeCalculation(BaseModel):
    extent_cents: float
    extent_ares: float
    fair_value_per_are_inr: float
    total_property_fair_value_inr: float
    applicable_fee_percentage: float
    statutory_conversion_fee_inr: float
    is_fee_exempt: bool
    description: str
    statutory_citation: str


class FloodRiskLevel(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ElevationFloodResult(BaseModel):
    latitude: float
    longitude: float
    elevation_meters: float
    resolution_meters: float | None = None
    locality_name: str
    district: str
    taluk_or_village: str | None = None
    flood_risk_level: FloodRiskLevel
    flood_risk_score: int = Field(description="Safety score 0-100 (100 = safe from flood, 0 = severe flood risk)")
    river_basin: str | None = None
    inundation_2018_zone: bool = False
    ksdma_hazard_advisory: str
    wetland_topography_risk: str
    recommended_plinth_height_m: float
    physical_inspection_checklist: list[str]
    whatsapp_inquiry_for_seller: str
