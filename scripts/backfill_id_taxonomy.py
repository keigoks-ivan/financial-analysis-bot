#!/usr/bin/env python3
"""One-shot backfill: add mega + sub_group to existing ID id-meta JSON blocks.

Source of truth: docs/id/taxonomy.md 表 3.
Usage: python3 scripts/backfill_id_taxonomy.py [--dry-run]
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
ID_DIR = ROOT / "docs" / "id"

# Mapping per docs/id/taxonomy.md 表 3 (89 IDs from initial scan + HBM4CustomBaseDie added)
MAPPING = {
    # semi.compute_demand
    "ID_AIAcceleratorDemand_20260419": ("semi", "compute_demand"),
    "ID_AIASICDesignService_20260419": ("semi", "compute_demand"),
    "ID_AIInferenceEconomics_20260430": ("semi", "compute_demand"),
    # semi.memory
    "ID_MemorySupercycle_20260430": ("semi", "memory"),
    "ID_HBM_Supercycle_20260419": ("semi", "memory"),
    "ID_HBM4CustomBaseDie_20260430": ("semi", "memory"),
    # semi.storage
    "ID_AIStorage_20260427": ("semi", "storage"),
    # semi.networking
    "ID_AINetworking_20260419": ("semi", "networking"),
    "ID_SiliconPhotonicsCPO_20260419": ("semi", "networking"),
    # semi.dc_infra
    "ID_AIDataCenter_20260419": ("semi", "dc_infra"),
    "ID_LiquidCooling_20260419": ("semi", "dc_infra"),
    "ID_Transformers_20260419": ("semi", "dc_infra"),
    "ID_AIDCPowerElectronics_20260421": ("semi", "dc_infra"),
    # semi.advanced_packaging
    "ID_AdvancedPackaging_20260419": ("semi", "advanced_packaging"),
    "ID_GlassSubstrate_20260420": ("semi", "advanced_packaging"),
    "ID_HybridBondingSoIC_20260420": ("semi", "advanced_packaging"),
    # semi.foundry_process
    "ID_LeadingEdgeNode_20260419": ("semi", "foundry_process"),
    "ID_FoundryGeography_20260427": ("semi", "foundry_process"),
    # semi.equipment_test
    "ID_WaferFabEquipment_20260430": ("semi", "equipment_test"),
    "ID_AITestEquipmentATE_20260427": ("semi", "equipment_test"),
    # semi.eda_ip
    "ID_AIEDAIP_20260427": ("semi", "eda_ip"),
    # semi.edge_ai
    "ID_EdgeAI_20260427": ("semi", "edge_ai"),
    # semi.emerging_compute
    "ID_QuantumComputing_20260427": ("semi", "emerging_compute"),

    # bio.glp1
    "ID_GLP1Master_20260429": ("bio", "glp1"),
    "ID_GLP1Treatment_20260428": ("bio", "glp1"),

    # cloud.cybersecurity
    "ID_CybersecurityPlatformConsolidation_20260423": ("cloud", "cybersecurity"),
    "ID_AICybersecurityDoubleEdge_20260423": ("cloud", "cybersecurity"),
    "ID_IdentityNewPerimeter_20260423": ("cloud", "cybersecurity"),
    "ID_DataSecurityBackupConvergence_20260423": ("cloud", "cybersecurity"),
    "ID_LLMVendorSecurityEconomics_20260423": ("cloud", "cybersecurity"),
    # cloud.agentic_ai
    "ID_AgenticAIPlatform_20260424": ("cloud", "agentic_ai"),
    "ID_AgenticAICommercialization_20260429": ("cloud", "agentic_ai"),
    "ID_TokenEconomics_20260427": ("cloud", "agentic_ai"),
    "ID_ProductivityCopilot_20260427": ("cloud", "agentic_ai"),
    # cloud.ai_cross_domain
    "ID_AICrossDomainImpact_20260429": ("cloud", "ai_cross_domain"),
    "ID_AppleIntelligencePlatformThreat_20260429": ("cloud", "ai_cross_domain"),
    "ID_AIAdRetailMedia_20260429": ("cloud", "ai_cross_domain"),
    # cloud.media_publishing
    "ID_PublishersStructuralReset_20260430": ("cloud", "media_publishing"),

    # energy.nuclear
    "ID_NuclearRenaissance_20260430": ("energy", "nuclear"),

    # consumer.apparel
    "ID_ApparelFootwear_20260427": ("consumer", "apparel"),
    "ID_AthleticFootwearSubsegments_20260427": ("consumer", "apparel"),
    "ID_AthleisureNewEntrants_20260427": ("consumer", "apparel"),
    "ID_ChannelPowerReversion_20260427": ("consumer", "apparel"),
    "ID_ChinaSportswearRise_20260427": ("consumer", "apparel"),
    # consumer.luxury
    "ID_GlobalLuxury_20260427": ("consumer", "luxury"),
    # consumer.restaurant
    "ID_USRestaurantChains_20260427": ("consumer", "restaurant"),
    "ID_FastCasualBifurcation_20260427": ("consumer", "restaurant"),
    "ID_CasualDiningTurnaround_20260427": ("consumer", "restaurant"),
    "ID_RestaurantTechSaaS_20260427": ("consumer", "restaurant"),
    # consumer.discount_retail
    "ID_DiscountRetailKShape_20260430": ("consumer", "discount_retail"),
    # consumer.ecommerce
    "ID_GlobalEcommerce_20260427": ("consumer", "ecommerce"),
    "ID_LATAMEcommerce_20260427": ("consumer", "ecommerce"),

    # finance.payment_network
    "ID_CardNetworkDuopoly_20260428": ("finance", "payment_network"),
    "ID_CobrandCardEcosystem_20260429": ("finance", "payment_network"),
    # finance.banks
    "ID_GlobalBankROE_20260428": ("finance", "banks"),
    # finance.stablecoin
    "ID_StablecoinPayments_20260430": ("finance", "stablecoin"),
    # finance.wealth_mgmt
    "ID_WealthTransfer25Year_20260429": ("finance", "wealth_mgmt"),

    # industrial.defense
    "ID_DefenseModernization_20260430": ("industrial", "defense"),
    "ID_DefenseAerospaceUpgrade_20260427": ("industrial", "defense"),
    # industrial.commercial_aero
    "ID_CommercialAerospace_20260427": ("industrial", "commercial_aero"),
    # industrial.robotics
    "ID_HumanoidIndustrialRobotics_20260427": ("industrial", "robotics"),
    "ID_IndustrialAutomation_20260427": ("industrial", "robotics"),
    # industrial.heavy_machinery
    "ID_HeavyMachineryMining_20260427": ("industrial", "heavy_machinery"),
    # industrial.autonomous_driving
    "ID_RobotaxiAutonomous_20260429": ("industrial", "autonomous_driving"),

    # staples.beverage
    "ID_BeverageEnergyDrink_20260428": ("staples", "beverage"),
    # staples.packaged_food
    "ID_GLP1PackagedFood_20260428": ("staples", "packaged_food"),
    # staples.restaurant_glp1
    "ID_GLP1RestaurantImpact_20260427": ("staples", "restaurant_glp1"),

    # reits.data_center
    "ID_DataCenterREITDuopoly_20260427": ("reits", "data_center"),

    # space.launch
    "ID_SpaceEconomy_20260430": ("space", "launch"),

    # housing.us_builders
    "ID_PublicBuilderEntryLevel_20260427": ("housing", "us_builders"),

    # transport.travel_master
    "ID_BoomerTravelSupercycle_20260429": ("transport", "travel_master"),
    # transport.hotel_lodging
    "ID_HotelChains_20260429": ("transport", "hotel_lodging"),
    # transport.cruise_luxury_travel
    "ID_LuxuryTravelCruise_20260427": ("transport", "cruise_luxury_travel"),
    # transport.ota_distribution
    "ID_OTAandAITravel_20260429": ("transport", "ota_distribution"),
    # transport.airline
    "ID_AirlineLoyaltyRepricing_20260429": ("transport", "airline"),
    # transport.casino_gaming
    "ID_CasinoGamingIR_20260429": ("transport", "casino_gaming"),

    # materials.industrial_metals
    "ID_CopperSupercycle_20260428": ("materials", "industrial_metals"),
    # materials.aerospace_defense_metals
    "ID_AerospaceMetals_20260427": ("materials", "aerospace_defense_metals"),

    # agri.livestock_meat
    "ID_BeefSupercycle_20260427": ("agri", "livestock_meat"),

    # macro.geopolitics_cntw (CNTW master + 10 subs)
    "ID_CNTW_Master_20260424": ("macro", "geopolitics_cntw"),
    "ID_CNTW_S1_Military_20260424": ("macro", "geopolitics_cntw"),
    "ID_CNTW_S2_GrayZone_20260424": ("macro", "geopolitics_cntw"),
    "ID_CNTW_S3_CNEconomy_20260424": ("macro", "geopolitics_cntw"),
    "ID_CNTW_S4_External_20260424": ("macro", "geopolitics_cntw"),
    "ID_CNTW_S5_Tripwires_20260424": ("macro", "geopolitics_cntw"),
    "ID_CNTW_S6_SemiDetw_20260424": ("macro", "geopolitics_cntw"),
    "ID_CNTW_S7_DefenseIndustry_20260424": ("macro", "geopolitics_cntw"),
    "ID_CNTW_S8_RareEarth_20260424": ("macro", "geopolitics_cntw"),
    "ID_CNTW_S9_Shipping_20260424": ("macro", "geopolitics_cntw"),
    "ID_CNTW_S10_TWDefense_20260424": ("macro", "geopolitics_cntw"),
}

ID_META_RE = re.compile(
    r'(<script\s+id="id-meta"\s+type="application/json"\s*>\s*)(.*?)(\s*</script>)',
    re.DOTALL,
)


def update_meta_json(raw_json: str, mega: str, sub_group: str) -> str:
    """Insert mega + sub_group into JSON, preserving order. Insert after ai_exposure
    if present, else after thesis_type, else at start of object."""
    try:
        meta = json.loads(raw_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parse error: {e}")

    # Already has it? No-op.
    if meta.get("mega") == mega and meta.get("sub_group") == sub_group:
        return raw_json

    # Build new dict with mega/sub_group inserted in a sensible position
    new_meta = {}
    inserted = False
    anchor_keys = ("ai_exposure", "industry_structure", "value_chain_position",
                   "growth_phase", "thesis_type")
    for k, v in meta.items():
        if k in ("mega", "sub_group"):
            continue  # we'll re-add fresh
        new_meta[k] = v
        if not inserted and k in anchor_keys:
            new_meta["mega"] = mega
            new_meta["sub_group"] = sub_group
            inserted = True
    if not inserted:
        # Anchor key absent; append at end
        new_meta["mega"] = mega
        new_meta["sub_group"] = sub_group

    return json.dumps(new_meta, ensure_ascii=False, indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    updated = 0
    skipped_already = 0
    not_in_mapping = []
    parse_errors = []

    for path in sorted(ID_DIR.glob("ID_*.html")):
        stem = path.stem
        if stem not in MAPPING:
            not_in_mapping.append(stem)
            continue
        mega, sub_group = MAPPING[stem]

        text = path.read_text(encoding="utf-8")
        m = ID_META_RE.search(text)
        if not m:
            # File may not have id-meta block (e.g., legacy). Skip.
            parse_errors.append(f"{stem}: no id-meta block")
            continue
        raw = m.group(2).strip()
        try:
            new_raw = update_meta_json(raw, mega, sub_group)
        except ValueError as e:
            parse_errors.append(f"{stem}: {e}")
            continue
        if new_raw == raw:
            skipped_already += 1
            continue
        new_text = text[:m.start(2)] + new_raw + text[m.end(2):]
        if args.dry_run:
            print(f"DRY: would update {stem} → mega={mega}, sub_group={sub_group}")
        else:
            path.write_text(new_text, encoding="utf-8")
            print(f"✅ {stem} → mega={mega}, sub_group={sub_group}")
        updated += 1

    print()
    print(f"Updated:      {updated}")
    print(f"Already had:  {skipped_already}")
    print(f"Not mapped:   {len(not_in_mapping)}")
    if not_in_mapping:
        for n in not_in_mapping:
            print(f"  · {n}")
    print(f"Parse errors: {len(parse_errors)}")
    for pe in parse_errors:
        print(f"  · {pe}")


if __name__ == "__main__":
    main()
