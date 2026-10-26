# IMPERIA CW — Cold War: uae 1970 — flavour.
"""Finished English narrative for the approved UAE 1970 focus programme.

Effects, values, titles and geometry remain in the immutable approved design.
These overrides replace design commentary with country-specific game flavour.
"""

import json
from pathlib import Path
from revision import current_design


_DESIGN = current_design()

FOCUS_DESCRIPTIONS = {
    node["id"]: node["description"] for node in _DESIGN["nodes"]
}

_OVERRIDES = {
    "protected_administration": (
        "A renewed compact gives the rulers time to strengthen their courts, customs offices and commercial administration. "
        "Shared institutions can make the coast easier to govern while Britain retains responsibility for external affairs and defence."
    ),
    "orderly_handover": (
        "Independence transfers the burden of external affairs and defence to the coast. "
        "An orderly handover of responsibilities, stores and training arrangements will help the local administrations carry that burden."
    ),
    "british_friendship": (
        "Independence need not sever the coast's British connections. "
        "A new friendship agreement can preserve consultation, technical advice and commercial links on terms accepted by both governments."
    ),
    "council": (
        "British protection has ended, leaving the rulers responsible for the coast's external affairs and defence. "
        "Their separate courts and administrations must now decide how much authority to entrust to a common government."
    ),
    "charter": (
        "A provisional charter must turn consultation into workable common government. "
        "The rulers will expect safeguards for their authority and revenues before entrusting ministers with federal responsibilities."
    ),
    "dual_veto": (
        "The founding bargain rests on strong guarantees for the emirates and a decisive voice for Abu Dhabi and Dubai. "
        "Common ministries can grow within that settlement, although agreement among the ruling courts will remain slow and expensive."
    ),
    "federal_ministries": (
        "Federal ministries need a clear mandate if they are to coordinate development across the emirates. "
        "A broader delegation of authority asks the rulers to accept firmer common direction in return for safeguards and shared investment."
    ),
    "sovereign_union": (
        "The end of Britain's special treaty responsibilities leaves the coast to conduct its own foreign affairs and defence. "
        "The rulers can put their agreed constitutional settlement into effect and prepare to proclaim their union."
    ),
    "rak_accession": (
        "Ras Al Khaimah's security concerns and claims to the Tunbs have complicated its place in the union. "
        "A settlement that recognises those concerns can bring its ruler and institutions into the federal bargain."
    ),
    "majlis": (
        "The majlis gives merchants, tribal notables and petitioners personal access to the rulers. "
        "A regular forum among the ruling houses can carry that tradition into federal government, provided the courts make time and resources available."
    ),
    "rulers_compact": (
        "Abu Dhabi's development transfers and Dubai's commercial autonomy are central to the union's survival. "
        "Renewing the compact means negotiating both together and giving the smaller emirates a dependable stake in common government."
    ),
    "presidential_union": (
        "A stronger presidency can press ministries to carry out common policy and settle disputes over responsibility. "
        "The rulers must agree on the powers they delegate, or the effort to strengthen the federation will deepen opposition within it."
    ),
    "constitutional_crown": (
        "The ruling houses can remain constitutional partners while a responsible cabinet directs ordinary administration. "
        "A clear division between court and ministry offers continuity, but limits the government's freedom to act alone."
    ),
    "citizen_ballot": (
        "Citizens need a durable stake in the new constitutional order. "
        "Reserving a larger share of employment and residency opportunities for them can strengthen support for reform while reducing the labour available to the trading cities."
    ),
    "municipal_compact": (
        "Long-term residents have helped build the coast's commercial economy. "
        "More secure residency and advisory municipal participation can sustain that contribution, while placing wider obligations on local government."
    ),
    "republican_service": (
        "A republic will inherit the rival offices and limited trained personnel of the ruling courts. "
        "A professional civil service can bring those administrations together, but its officials must be recruited, trained and paid."
    ),
    "public_industry": (
        "A modest public industrial sector can broaden an economy built around oil receipts and commerce. "
        "The state will have to provide reliable power, skilled workers and sustained capital before new factories can meet that promise."
    ),
    "social_associations": (
        "Sunni educational and charitable associations provide the reform movement with trusted local networks. "
        "Bringing those networks into government requires a settlement with merchants, the ruling families and institutions outside the movement."
    ),
    "reform_education": (
        "The coast needs professional skills as well as religious education. "
        "Reformers must decide how schools and training institutions can serve both purposes, and how much independence their teachers and associations retain."
    ),
    "state_participation": (
        "A larger public equity share can bring more of the concession's income under the producing emirate's control. "
        "Foreign operators can remain technical partners, while the emirate assumes a greater share of the investment and operating risks."
    ),
    "partner_expertise": (
        "Reliable technical services and experienced management are valuable to a small producing state. "
        "Stronger guarantees can secure that expertise, but leave a larger commercial margin with the partners and tie local operations more closely to them."
    ),
    "offshore_second_phase": (
        "Further offshore expansion requires additional platforms, connections and marine support. "
        "Building on the first programme can raise operating capacity, but commits substantial capital that other parts of the federation also need. "
        "As the oil economy grows, crews and merchants find new work and the traditional coastal trades account for less of household income."
    ),
    "adia_savings": (
        "Abu Dhabi can turn exceptional oil receipts into a reserve and a professionally managed investment portfolio. "
        "Saving part of the windfall offers protection against future shocks while reducing the resources available for immediate development."
    ),
    "port_planning": (
        "Reliable landing grounds, ice stores and fish markets can reduce spoilage and give crews a steadier return for their catch. "
        "A more secure household income eases demand for assistance. The works will also serve coastal traders, "
        "although administration and refrigeration bring continuing costs and oil development draws activity towards new industries."
    ),
    "beyond_oil": (
        "Services and industry can provide earnings beyond the producing fields. "
        "A broader economy will be better placed to absorb a fall in oil receipts, although its firms will remain exposed to regional insecurity and world markets."
    ),
    "efficient_services": (
        "A growing population needs reliable district health services, trained staff and an administration able to maintain them. "
        "Professional management can keep those institutions effective as the towns expand, although continuing care will remain a permanent public expense."
    ),
    "shared_logistics": (
        "Compatible depots, transport and communications can make a common command effective across the emirates. "
        "Reliable support reduces waste in the field, but requires trained personnel and continuing expenditure at home."
    ),
    "security_contracts": (
        "Training agreements can give local personnel access to experienced instructors and established procedures. "
        "Their value depends on clear obligations, sustained funding and skills that the federation can retain in its own forces."
    ),
    "gulf_cooperation": (
        "The Gulf monarchies share interests in consultation, trade and security, alongside disputes over borders and policy. "
        "Common standards and regular meetings can deepen cooperation while leaving each member responsible for its own commitments."
    ),
    "dirham": (
        "Abu Dhabi uses the Bahraini dinar while the other emirates use the Qatar-Dubai riyal. "
        "A currency board and common dirham can simplify federal accounts and trade, provided the new monetary institutions earn confidence across the union."
    ),
}

FOCUS_DESCRIPTIONS.update(
    {"COLDWAR_UAE_" + suffix: description for suffix, description in _OVERRIDES.items()}
)

SPIRIT_DESCRIPTIONS = {
    "COLDWAR_UAE_fragmented_authority": (
        "The ruling courts retain separate administrations, customs revenues and forces. "
        "The Council can encourage cooperation, but carrying out common policy still requires negotiations among rulers with different priorities."
    ),
    "COLDWAR_UAE_unequal_development": (
        "Abu Dhabi's developing oil industry and Dubai's trading economy give the two leading emirates resources that the northern sheikhdoms lack. "
        "Unequal access to roads, public services and finance makes the distribution of development a political question."
    ),
    "COLDWAR_UAE_scarce_specialists": (
        "The coast has too few trained teachers, doctors, technicians and administrators for its ambitions. "
        "Foreign expertise can relieve immediate shortages, while building a local pool of specialists requires years of education and practical training."
    ),
    "COLDWAR_UAE_water_power": (
        "Expanding coastal towns depend on costly water distribution, desalination and reliable electricity. "
        "New households and businesses increase demand faster than a small technical workforce can extend and maintain these systems."
    ),
    "COLDWAR_UAE_narrow_revenues": (
        "Valuable oil reserves lie beneath the emirates, but the operating industry remains small and expensive to expand. "
        "The wider productive and service economy supplies only a narrow revenue base, leaving public ambitions exposed to the fortunes of a few sectors."
    ),
    "COLDWAR_UAE_expatriate_workforce": (
        "Workers from abroad allow the economy to grow beyond the limits of the small citizen population. "
        "The armed forces still rely on a small citizen cadre, making it harder to restore unit cohesion and readiness after sustained operations."
    ),
}

# Treaty lore is separate from the approved mechanical contract catalogue.
TREATY_SPIRIT_DESCRIPTIONS = {
    "starting": {
        "uae": (
            "Britain's treaties have long placed the coast's defence and foreign relations in British hands. "
            "London's 1968 announcement that its forces will leave the Gulf by the end of 1971 has unsettled this arrangement. "
            "The seven rulers must reconcile their separate interests and prepare common institutions before the protection on which they have relied comes to an end."
        ),
        "uk": (
            "The decision announced in 1968 to withdraw British forces from the Gulf by the end of 1971 marks the approaching end of Britain's special treaty relationship with the Trucial States. "
            "Defence and diplomatic responsibilities remain during the transition, while the rulers negotiate a union capable of standing on its own. "
            "An orderly departure must balance Britain's diminishing commitments with the coast's uncertain security."
        ),
    },
    "scheduled": {
        "uae": (
            "The rulers and Britain have agreed a new timetable for ending the special treaty relationship. "
            "A settled handover offers time to prepare an administration and assume responsibility for defence and foreign relations, "
            "but the approaching departure leaves little room for unresolved disputes among the emirates."
        ),
        "uk": (
            "Britain and the Trucial rulers have settled a revised date for the handover of defence and diplomatic responsibilities. "
            "The remaining transition must prepare the coast for independence while allowing Britain to bring its special treaty obligations to an orderly close."
        ),
    },
    "protection": {
        "uae": (
            "A renewed compact preserves British responsibility for defence and foreign relations beyond the original withdrawal timetable. "
            "The rulers retain a familiar source of security and expertise, but the coast's external sovereignty remains constrained. "
            "The next review will reopen the question of how long this arrangement should endure."
        ),
        "uk": (
            "A renewed compact extends Britain's protection of the Trucial coast. "
            "Continued defence and diplomatic responsibilities preserve British influence and reassure the rulers, "
            "while prolonging a commitment that the original withdrawal was intended to end."
        ),
    },
    "fulfilled": {
        "uae": (
            "The special treaty relationship with Britain has ended. Responsibility for defence and foreign relations now rests with the coast's own authorities. "
            "Independence brings the freedom to choose new partners, alongside the burden of providing security and making cooperation among the emirates endure."
        ),
        "uk": (
            "Britain's special treaty obligations on the Trucial coast have ended with the agreed handover. "
            "The withdrawal closes a long chapter of British protection in the Gulf; future cooperation must rest on agreements with independent authorities."
        ),
    },
    "friendship": {
        "uae": (
            "An independent friendship treaty preserves useful ties with Britain after the end of protection. "
            "Consultation and technical cooperation offer continuity as local institutions develop, "
            "while defence and foreign policy remain the responsibility of the country's own government."
        ),
        "uk": (
            "A friendship treaty establishes a new basis for relations with the independent emirates. "
            "Consultation and technical cooperation maintain Britain's connections to the coast through mutual consent, after the old obligations of protection have ended."
        ),
    },
}

_EXPECTED = {node["id"] for node in _DESIGN["nodes"]}
if set(FOCUS_DESCRIPTIONS) != _EXPECTED:
    raise ValueError("UAE narrative coverage differs from the approved focus catalogue")
