"""Kandezhuthu AI - Kerala Land Judicial Precedents Extractor & Knowledge Generator.

Extracts, structures, and documents landmark judicial precedents governing:
- Christian female succession rights (Mary Roy v. State of Kerala)
- Senior citizen gift/settlement revocations (Section 23, Senior Citizens Act 2007)
- Easements of necessity & grant (Sree Swayamprakash Ashramam, Hero Vinoth)
- Hindu coparcenary rights of daughters (Vineeta Sharma v. Rakesh Sharma)
- Alienation of minor immovable property without court sanction (Section 8(2), HMGA 1956)
"""

from pathlib import Path
from typing import Dict, List, Any

KNOWLEDGE_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "knowledge"
KNOWLEDGE_FILE = KNOWLEDGE_OUTPUT_DIR / "kerala_court_precedents.md"

COURT_PRECEDENTS_CONTENT = """# Kerala Real Estate & Land Title Diligence · Landmark Judicial Precedents

> **Jurisdiction**: Supreme Court of India & High Court of Kerala
> **Core Focus**: Property title traps, succession omissions, easement enforceability, and voidable transfers.

---

## 1. Christian Succession & Omitted Female Heirs

### Landmark Ruling: *Mary Roy & Ors. v. State of Kerala & Ors.* (1986 AIR 1011 / 1986 SCR (1) 371)
- **Bench**: Supreme Court of India (Constitution Bench: P.N. Bhagwati, C.J., R.S. Pathak, J.)
- **Key Legal Principle**:
  - Declared that the discriminatory provisions of the Travancore Christian Succession Act, 1092 M.E. (Section 28–29) and the Cochin Christian Succession Act, 1097 M.E. stood repealed with effect from 1 April 1951 by the Part B States (Laws) Act, 1951.
  - Held that the **Indian Succession Act, 1925 applies uniformly** to Indian Christians in Travancore and Cochin territories for intestate succession since 1951.
  - Daughters inherit equally with sons in their parents' intestate property.
- **Title Trap for Property Buyers**:
  - In multi-decade title audits (*Munnadharam*), partition deeds (*ഭാഗപത്രം*) or release deeds (*ഒഴിവുമുറി*) executed among Syrian Christian families prior to 1986 frequently excluded sisters/daughters, paying them a nominal Streedhanam (₹5,000 or 1/3 of son's share).
  - Because *Mary Roy* operated retrospectively from 1951, daughters or their legal descendants can challenge these partition deeds if they never formally executed registered release deeds (*ഒഴിവുമുറി പ്രമാണം*).
- **Mandatory Diligence Rule**:
  - Always verify whether all female siblings signed the registered partition or release deed whenever title traces back to a Christian intestate ancestor who passed away after 1951.

---

## 2. Senior Citizen Maintenance & Revocation of Gift Deeds

### Governing Statute: Maintenance and Welfare of Parents and Senior Citizens Act, 2007 (Section 23)
### Key Rulings:
- *Subhashini v. District Collector, Kozhikode* (2020 (5) KLT 493 - Full Bench, Kerala HC)
- *Radhamani v. State of Kerala* (2016 (1) KLT 185 - Kerala HC)
- *S. Vanitha v. Deputy Commissioner, Bengaluru Urban* (2021 15 SCC 730 - Supreme Court)

- **Statutory Provision (Section 23(1))**:
  - Where any senior citizen (aged 60+) transfers property by gift or settlement, subject to the condition that the transferee shall provide basic amenities and physical needs, and the transferee fails to do so:
  - The transfer of property **shall be deemed to have been made by fraud or coercion or under undue influence** and can be declared **VOID** by the Maintenance Tribunal (presided over by the RDO / Sub-Collector).
- **Conditional vs Absolute Gift Controversy**:
  - Under the Kerala High Court Full Bench ruling in *Subhashini (2020)*, for Section 23 to apply, there must be an express or clearly ascertainable condition in the document that the transferee must maintain the senior citizen.
  - However, even without an express clause, disputes frequently result in Maintenance Tribunal stop-memos issued to Sub-Registrar Offices (SROs) and Village Offices, halting all registrations and tax remittances (*പോക്കുവരവ് തടയൽ*).
- **Title Trap for Property Buyers**:
  - If buying land from a person who acquired it within the last 15 years via a **Gift Deed (ദാന പ്രമാണം)** or **Settlement Deed (ധനനിശ്ചയ ആധാരം)** from an elderly parent:
  - If the parent is still alive and moves the Maintenance Tribunal alleging abandonment, the buyer's sale deed can be entangled in protracted litigation, and mutation of revenue records will be frozen.
- **Mandatory Diligence Rule**:
  - The elderly parent must either be an executing confirming party in the sale deed or execute an unencumbered NOC/discharge confirming satisfaction of all maintenance rights.

---

## 3. Easements of Necessity, Grant & Implied Pathways

### Governing Statute: Indian Easements Act, 1882 (Sections 13, 15, 19, 41)
### Key Rulings:
- *Sree Swayamprakash Ashramam & Anr. v. G. Anandavally Amma* (2010 2 SCC 689 - Supreme Court)
- *Hero Vinoth (Minor) v. Seshammal* (2006 5 SCC 545 - Supreme Court)

- **Key Legal Principles**:
  - **Easement by Grant**: An easement created by an express grant in a registered title deed **does not extinguish merely because the dominant owner acquires an alternative access road** (*Hero Vinoth*).
  - **Implied Grant / Continuous & Apparent User**: Where a pathway was continuously and openly used as the sole access to a property before severance of tenements, the easement passes to subsequent transferees as a necessary easement (*Sree Swayamprakash Ashramam*).
  - **Easements Run with the Land**: Easement rights belong to the land, not merely the individual (*Section 19*). When dominant heritage is transferred, the pathway rights transfer automatically, even if omitted in the subsequent conveyance deed recital.
- **Title Trap for Property Buyers**:
  - **Buried Servitudes**: A prior deed may have reserved a 3-meter pathway across the plot for the benefit of a back-plot neighbor (*കിഴക്ക്/പടിഞ്ഞാറ് ഭാഗത്ത് കൂടി 3 മീറ്റർ നടപ്പുവഴി അവകാശം*). If the buyer attempts to construct a gate or compound wall, the neighbor can obtain an immediate High Court / Munsiff Court injunction.
  - **Oral Passages (*വായമൊഴി വഴി*)**: An informal agreement allowing a neighbor to walk across the plot can mature into a prescriptive easement under Section 15 after 20 years of uninterrupted, peaceable use without license.
- **Mandatory Diligence Rule**:
  - Thoroughly inspect schedule boundaries and recitals of all prior deeds (*മുന്നാധാരം*) for terms like *വഴി അവകാശം*, *നടപ്പുവഴി*, *പൊതുവഴി*, or *എടുപ്പുവഴി*.
  - Conduct on-ground physical inspection to see if any tire tracks, worn walking paths, or neighboring gates open into the property.

---

## 4. Hindu Coparcenary Rights of Daughters

### Landmark Ruling: *Vineeta Sharma v. Rakesh Sharma & Ors.* (2020 9 SCC 1 - Supreme Court, 3-Judge Bench)
- **Bench**: Arun Mishra, S. Abdul Nazeer, M.R. Shah, JJ.
- **Key Legal Principle**:
  - Confirmed the retroactive operation of Section 6 of the Hindu Succession Act, 1956 as amended by the 2005 Amendment Act.
  - Held that a **daughter becomes a coparcener by birth in the same manner as a son**, with the same rights and liabilities in joint family property.
  - It is **irrelevant whether the father was alive or deceased** on the date of the amendment (9 September 2005).
  - Only registered partitions or court decrees finalized prior to 20 December 2004 are saved.
- **Title Trap for Property Buyers**:
  - Where ancestral or joint Hindu family property (*തറവാട് സ്വത്ത്*) was partitioned among brothers or sons, omitting daughters, any post-2004 transactions are vulnerable to partition suits instituted by coparcener daughters or their children.
- **Mandatory Diligence Rule**:
  - When ancestral Hindu property is in the title chain, verify that all coparcener daughters or their legal heirs executed the partition deed or a registered release of rights.

---

## 5. Alienation of Minor's Immovable Property

### Governing Statute: Hindu Minority and Guardianship Act, 1956 (Section 8) & Guardians and Wards Act, 1890
### Key Rulings:
- *Saroj v. Sunder Singh & Ors.* (2014 15 SCC 727 - Supreme Court)
- *K.M. Mathew v. Haneefa Rawther* (Kerala High Court)

- **Statutory Mandate (Section 8(2))**:
  - The natural guardian (even parents) of a Hindu minor **shall not, without the previous permission of the District Court**:
    1. Mortgage, charge, or transfer by sale, gift, or exchange any part of the minor's immovable property.
    2. Lease any part of such property for a term exceeding 5 years or for a term extending more than one year beyond the date on which the minor attains majority.
- **Consequences of Violation (Section 8(3))**:
  - Any disposal of immovable property by a natural guardian in contravention of Section 8(2) is **voidable at the instance of the minor** or any person claiming under him.
  - **Limitation Period**: Under Article 60 of the Limitation Act, 1963, the minor can file a suit to set aside the sale within **3 years after attaining majority (up to age 21)**.
- **Title Trap for Property Buyers**:
  - Parents frequently sign sale deeds stating: *"Representing myself and as natural guardian of minor child Master/Miss XYZ."*
  - If there is **no District Court Sanction Order (OP Guardian petition order)** explicitly sanctioning the specific sale and sale price, the conveyance is legally defective and can be set aside when the child turns 18.
- **Mandatory Diligence Rule**:
  - Never purchase property involving a minor's undivided or distinct share without inspecting the **original certified copy of the District Court's Sanction Order**.

---

## 6. Judicial Diligence Summary Table for Title Auditors

| Statutory Risk Area | Key Precedent / Statute | Fatal Defect / Ground for Invalidation | Preventive Diligence Requirement |
| :--- | :--- | :--- | :--- |
| **Christian Female Succession** | *Mary Roy* (1986 AIR 1011) | Omission of daughters in post-1951 intestate parental succession. | Require registered release deeds from all female heirs or their descendants. |
| **Senior Citizen Maintenance** | Section 23, Act 56 of 2007 (*Subhashini 2020*) | Maintenance Tribunal declaring parent's gift/settlement deed void. | Living elderly parents must join as consenting parties with independent legal advice. |
| **Pathway / Easement Rights** | *Sree Swayamprakash Ashramam* (2010 2 SCC 689) | Hidden pathway servitude running with the land blocking construction. | Inspect all prior deed boundary schedules and perform on-site path verification. |
| **Hindu Daughter Coparcenary** | *Vineeta Sharma* (2020 9 SCC 1) | Ancestral coparcenary partition excluding daughters post-2004. | All living daughters must execute partition or registered release. |
| **Minor Share Alienation** | Section 8(2), HMGA 1956 (*Saroj 2014*) | Sale by parents without District Court sanction order; voidable up to age 21. | Require certified District Court Guardian Sanction Order. |
"""


def get_precedent_summary(topic: str) -> Dict[str, Any]:
    """Retrieves structured summary of landmark precedents by topic."""
    lookup = {
        "christian_succession": {
            "case": "Mary Roy v. State of Kerala (1986 AIR 1011)",
            "statute": "Indian Succession Act, 1925",
            "rule": "Equal inheritance for Christian daughters from 1951 retrospectively.",
            "risk": "Partition deeds excluding daughters are voidable.",
        },
        "senior_citizen": {
            "case": "Subhashini v. District Collector (2020 (5) KLT 493)",
            "statute": "Section 23, Maintenance and Welfare of Parents Act, 2007",
            "rule": "Maintenance Tribunal can declare gift deed void if transferee fails to maintain.",
            "risk": "Deed cancellation and mutation freeze if living elderly parent is aggrieved.",
        },
        "easement": {
            "case": "Sree Swayamprakash Ashramam v. G. Anandavally Amma (2010 2 SCC 689)",
            "statute": "Indian Easements Act, 1882",
            "rule": "Easements of grant or necessity run with the land and bind subsequent buyers.",
            "risk": "Unilateral wall or gate construction blocked by injunction.",
        },
        "minor_share": {
            "case": "Saroj v. Sunder Singh (2014 15 SCC 727)",
            "statute": "Section 8(2), Hindu Minority and Guardianship Act, 1956",
            "rule": "Mandatory prior District Court sanction for alienating minor immovable property.",
            "risk": "Sale voidable by minor within 3 years of attaining majority (age 21).",
        },
    }
    return lookup.get(topic.lower(), {"error": f"Topic '{topic}' not found in precedents lookup."})


def generate_knowledge_doc() -> Path:
    """Writes the curated Kerala Judicial Precedents knowledge document."""
    KNOWLEDGE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    KNOWLEDGE_FILE.write_text(COURT_PRECEDENTS_CONTENT, encoding="utf-8")
    print(f"✅ Successfully generated Kerala Judicial Precedents knowledge document at: {KNOWLEDGE_FILE}")
    return KNOWLEDGE_FILE


if __name__ == "__main__":
    generate_knowledge_doc()
