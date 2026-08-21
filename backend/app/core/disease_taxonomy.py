"""
SmartAgri AI - Canonical Disease & Plant Health Taxonomy
Structured mapping of Crop -> Condition ID -> Scientific Name, Synonyms, Disease/Pest Flag, Dataset Provenance, and Verified Remedial Actions.
"""

from typing import Dict, Any, List, Optional

CANONICAL_DISEASE_TAXONOMY: Dict[str, Dict[str, Any]] = {
    # ------------------ GROUNDNUT (Dataset: WB Mendeley + Karnataka Mendeley) ------------------
    "Groundnut___Rust": {
        "crop": "Groundnut",
        "condition": "Puccinia Rust",
        "status": "Diseased",
        "severity": "High",
        "is_pest_damage": False,
        "scientific_name": "Puccinia arachidis",
        "synonyms": ["Peanut Rust", "Groundnut Puccinia Spot"],
        "dataset_sources": ["Groundnut West Bengal (Purba Medinipur)", "Groundnut Karnataka (Koppal)"],
        "symptoms": "Small brown/orange reddish pustules appearing on lower leaf surfaces, leading to early leaf drying and defoliation.",
        "immediate_action": "Remove heavily rusted lower leaves. Avoid flood irrigation that raises canopy relative humidity above 85%.",
        "organic_treatment": "Spray Neem Seed Kernel Extract (NSKE 5%) or Trichoderma harzianum @ 5g/L at first sign of pustules.",
        "chemical_treatment": "Spray Mancozeb 75% WP @ 2g/L or Tebuconazole 25.9% EC @ 1 ml/L. Repeat after 14 days if wet weather persists.",
        "prevention": "Use resistant groundnut varieties (ICGV 91114, GPBD 4). Maintain optimal plant spacing (30x10 cm)."
    },
    "Groundnut___Leaf_Spot": {
        "crop": "Groundnut",
        "condition": "Tikka Leaf Spot (Cercospora)",
        "status": "Diseased",
        "severity": "Moderate-High",
        "is_pest_damage": False,
        "scientific_name": "Cercospora arachidicola / Cercosporidium personatum",
        "synonyms": ["Tikka Disease", "Early & Late Leaf Spot"],
        "dataset_sources": ["Groundnut West Bengal", "Groundnut Karnataka"],
        "symptoms": "Circular dark brown spots surrounded by a yellow halo on upper leaf surfaces.",
        "immediate_action": "Collect and destroy diseased crop debris to reduce overwintering fungal spores.",
        "organic_treatment": "Spray Pseudomonas fluorescens @ 10g/L or copper oxychloride bio-formulation.",
        "chemical_treatment": "Spray Carbendazim 50% WP @ 1g/L + Mancozeb @ 2g/L mix (Saaf @ 2g/L).",
        "prevention": "Crop rotation with non-legumes (Maize, Sorghum). Seed treatment with Trichoderma viride @ 10g/kg."
    },
    "Groundnut___Rosette": {
        "crop": "Groundnut",
        "condition": "Groundnut Rosette Virus",
        "status": "Diseased",
        "severity": "High",
        "is_pest_damage": True, # Vector transmitted by Aphids
        "scientific_name": "Groundnut rosette assistor virus (GRAV)",
        "synonyms": ["Rosette Stunting"],
        "dataset_sources": ["Groundnut West Bengal"],
        "symptoms": "Severe stunting, bushy leaf clustering, chlorosis, yellowing, and malformed leaves.",
        "immediate_action": "Uproot and burn virus-infected stunted plants immediately to stop vector spread.",
        "organic_treatment": "Spray Neem oil (10,000 ppm) @ 3 ml/L to control aphid vector populations.",
        "chemical_treatment": "Spray Imidacloprid 17.8% SL @ 0.5 ml/L or Thiamethoxam 25% WG @ 0.3g/L for aphid vector management.",
        "prevention": "Sow early in the Kharif season at high density to shade ground cover and discourage aphid landing."
    },
    "Groundnut___healthy": {
        "crop": "Groundnut",
        "condition": "Healthy Leaf",
        "status": "Healthy",
        "severity": "None",
        "is_pest_damage": False,
        "scientific_name": "Arachis hypogaea",
        "synonyms": ["Normal Foliage"],
        "dataset_sources": ["Groundnut West Bengal", "Groundnut Karnataka"],
        "symptoms": "Vibrant green quadrifoliate leaves with intact cuticle and zero lesions.",
        "immediate_action": "Maintain routine field operations and balanced NPK fertigation.",
        "organic_treatment": "Apply organic vermicompost tea or panchagavya foliar spray for vigor.",
        "chemical_treatment": "No chemical intervention needed.",
        "prevention": "Ensure well-drained soil and avoid waterlogging during pegging stage."
    },

    # ------------------ RICE (Dataset: RiceGuard 19k + RiceLeafs) ------------------
    "Rice___Brown_Spot": {
        "crop": "Rice",
        "condition": "Brown Spot (Bipolaris)",
        "status": "Diseased",
        "severity": "Moderate",
        "is_pest_damage": False,
        "scientific_name": "Bipolaris oryzae / Helminthosporium oryzae",
        "synonyms": ["Rice Sesame Leaf Spot"],
        "dataset_sources": ["RiceGuard 19k", "RiceLeafs"],
        "symptoms": "Oval or sesame-shaped reddish-brown spots with grey centers distributed across leaf blades.",
        "immediate_action": "Correction of soil potash (K) and nitrogen deficiency.",
        "organic_treatment": "Spray Pseudomonas fluorescens @ 10g/L.",
        "chemical_treatment": "Spray Propiconazole 25% EC @ 1 ml/L or Edifenphos @ 1 ml/L.",
        "prevention": "Soil fertility management, balanced potassium application, and seed soaking in carbendazim."
    },
    "Rice___Hispa": {
        "crop": "Rice",
        "condition": "Rice Hispa Pest Damage",
        "status": "Diseased",
        "severity": "Moderate",
        "is_pest_damage": True,
        "scientific_name": "Dicladispa armigera",
        "synonyms": ["Hispa Leaf Miner Scrapes"],
        "dataset_sources": ["RiceGuard 19k", "RiceLeafs"],
        "symptoms": "Parallel white translucent streaks along leaf veins caused by adult beetles scraping chlorophyll.",
        "immediate_action": "Clip infested leaf tips containing Hispa grubs before transplanting or early crop stage.",
        "organic_treatment": "Spray Neem oil 1% @ 5 ml/L or release native mirid bug predators.",
        "chemical_treatment": "Spray Chlorpyrifos 20% EC @ 2 ml/L or Quinalphos 25% EC @ 2 ml/L.",
        "prevention": "Clear grassy weeds from field bunds where adult beetles harbor."
    },
    "Rice___Leaf_Blast": {
        "crop": "Rice",
        "condition": "Rice Blast (Pyricularia)",
        "status": "Diseased",
        "severity": "High",
        "is_pest_damage": False,
        "scientific_name": "Pyricularia oryzae / Magnaporthe oryzae",
        "synonyms": ["Blast Spot", "Spindle Spot"],
        "dataset_sources": ["RiceGuard 19k", "RiceLeafs"],
        "symptoms": "Diamond or spindle-shaped lesions with pointed ends, greyish-white centers, and brown borders.",
        "immediate_action": "Drain standing water temporarily and avoid high nitrogen top-dressing during cloudy damp weather.",
        "organic_treatment": "Foliar application of Bacillus subtilis @ 5g/L.",
        "chemical_treatment": "Spray Tricyclazole 75% WP @ 0.6g/L or Isoprothiolane 40% EC @ 1.5 ml/L.",
        "prevention": "Use blast-resistant cultivars (PR 126, Pusa 44) and avoid excessive urea application."
    },
    "Rice___Bacterial_Leaf_Blight": {
        "crop": "Rice",
        "condition": "Bacterial Leaf Blight (Xanthomonas)",
        "status": "Diseased",
        "severity": "High",
        "is_pest_damage": False,
        "scientific_name": "Xanthomonas oryzae pv. oryzae",
        "synonyms": ["BLB", "Kresek Phase"],
        "dataset_sources": ["RiceGuard 19k"],
        "symptoms": "Water-soaked translucent lesions turning yellow/white starting from leaf tips and margins.",
        "immediate_action": "Drain field excess water and withhold nitrogen fertilizer application until bacterial spread stops.",
        "organic_treatment": "Spray fresh cow dung extract (20%) filtered spray or copper hydroxide.",
        "chemical_treatment": "Spray Streptocycline @ 0.15g/L + Copper Oxychloride @ 2.5g/L in 500L water/ha.",
        "prevention": "Avoid clipping leaf tips during transplanting; maintain dry field drainage intervals."
    },
    "Rice___healthy": {
        "crop": "Rice",
        "condition": "Healthy Leaf",
        "status": "Healthy",
        "severity": "None",
        "is_pest_damage": False,
        "scientific_name": "Oryza sativa",
        "synonyms": ["Normal Paddy Foliage"],
        "dataset_sources": ["RiceGuard 19k", "RiceLeafs"],
        "symptoms": "Uniform deep green erect linear leaves free from necrotic spots or insect frass.",
        "immediate_action": "Maintain optimal standing water depth (2-5 cm) according to crop growth phase.",
        "organic_treatment": "Apply Azospirillum / PSB bio-fertilizers.",
        "chemical_treatment": "No chemical intervention needed.",
        "prevention": "Standard agronomic practices and field weed management."
    },

    # ------------------ CASSAVA (Dataset: Cassava Competition) ------------------
    "Cassava___Mosaic_Disease": {
        "crop": "Cassava",
        "condition": "Cassava Mosaic Virus (CMD)",
        "status": "Diseased",
        "severity": "High",
        "is_pest_damage": True, # Whitefly vector
        "scientific_name": "African cassava mosaic virus (ACMV)",
        "synonyms": ["CMD Leaf Distortion"],
        "dataset_sources": ["Cassava Leaf Disease Classification"],
        "symptoms": "Severe yellow mosaic patterns, twisted leaf blades, leaf curling, and marked plant stunting.",
        "immediate_action": "Uproot infected cassava stems and destroy infected planting stakes.",
        "organic_treatment": "Spray Neem oil @ 5 ml/L to control whitefly vector (Bemisia tabaci).",
        "chemical_treatment": "Spray Spiromesifen 22.9% SC @ 1 ml/L or Thiamethoxam @ 0.3g/L for whitefly control.",
        "prevention": "Use virus-free disease-resistant stem cuttings (TME 419, TMS 30572)."
    },
    "Cassava___Brown_Streak_Disease": {
        "crop": "Cassava",
        "condition": "Cassava Brown Streak (CBSD)",
        "status": "Diseased",
        "severity": "High",
        "is_pest_damage": True,
        "scientific_name": "Cassava brown streak virus (CBSV)",
        "synonyms": ["CBSD Root Necrosis"],
        "dataset_sources": ["Cassava Leaf Disease Classification"],
        "symptoms": "Feathery yellow chlorosis along secondary leaf veins and brown necrotic streaks on green stems.",
        "immediate_action": "Rogue out infected plants to prevent whitefly vector transmission.",
        "organic_treatment": "Plant border barrier crops (Maize/Sorghum) to reduce insect vector drift.",
        "chemical_treatment": "Spray Systemic Insecticides against whiteflies.",
        "prevention": "Plant clean certified stem cuttings from tissue culture source."
    },
    "Cassava___healthy": {
        "crop": "Cassava",
        "condition": "Healthy Leaf",
        "status": "Healthy",
        "severity": "None",
        "is_pest_damage": False,
        "scientific_name": "Manihot esculenta",
        "synonyms": ["Normal Tapioca Foliage"],
        "dataset_sources": ["Cassava Leaf Disease Classification"],
        "symptoms": "Palmate green lobed leaves with smooth intact margins and vigorous stem node growth.",
        "immediate_action": "Maintain soil weeding and organic mulching.",
        "organic_treatment": "Apply composted manure around stem base.",
        "chemical_treatment": "No chemical intervention needed.",
        "prevention": "Regular field scouting for whitefly populations."
    },

    # ------------------ APPLE (Dataset: Plant Pathology 2020 FGVC7 + PlantVillage) ------------------
    "Apple___Cedar_apple_rust": {
        "crop": "Apple",
        "condition": "Cedar Apple Rust",
        "status": "Diseased",
        "severity": "Moderate-High",
        "is_pest_damage": False,
        "scientific_name": "Gymnosporangium juniperi-virginianae",
        "synonyms": ["Gymnosporangium Rust"],
        "dataset_sources": ["Plant Pathology 2020 FGVC7", "PlantDoc", "PlantVillage"],
        "symptoms": "Bright yellow-orange spots on upper leaf surfaces; tube-like spore structures under leaf undersides.",
        "immediate_action": "Remove nearby alternate cedar/juniper host trees within 250m if possible.",
        "organic_treatment": "Spray sulfur powder or liquid copper octanoate at pink bud stage.",
        "chemical_treatment": "Spray Myclobutanil 10% WP @ 0.4g/L or Mancozeb 75% WP @ 2.5g/L.",
        "prevention": "Plant resistant apple varieties (Enterprise, Liberty, Redfree)."
    },
    "Apple___Apple_scab": {
        "crop": "Apple",
        "condition": "Apple Scab (Venturia)",
        "status": "Diseased",
        "severity": "High",
        "is_pest_damage": False,
        "scientific_name": "Venturia inaequalis",
        "synonyms": ["Venturia Leaf Scab"],
        "dataset_sources": ["Plant Pathology 2020 FGVC7", "PlantDoc", "PlantVillage"],
        "symptoms": "Olive-green to velvety dark brown lesions on leaves and fruit skin.",
        "immediate_action": "Rake and burn fallen leaf litter in autumn to destroy overwintering perithecia spores.",
        "organic_treatment": "Spray Potassium Bicarbonate @ 4g/L or Lime Sulfur during dormant bud stage.",
        "chemical_treatment": "Spray Difenoconazole 25% EC @ 0.5 ml/L or Captan 50% WP @ 2.5g/L.",
        "prevention": "Prune orchard canopy tree branches to maximize air circulation and sunlight penetration."
    },
    "Apple___healthy": {
        "crop": "Apple",
        "condition": "Healthy Leaf",
        "status": "Healthy",
        "severity": "None",
        "is_pest_damage": False,
        "scientific_name": "Malus domestica",
        "synonyms": ["Normal Apple Orchard Leaf"],
        "dataset_sources": ["Plant Pathology 2020 FGVC7", "PlantDoc", "PlantVillage"],
        "symptoms": "Dark green serrated leaves with firm texture and clean veins.",
        "immediate_action": "Maintain canopy pruning and annual orchard fertigation.",
        "organic_treatment": "Foliar spray of seaweed extract for vigor.",
        "chemical_treatment": "No chemical intervention needed.",
        "prevention": "Routine orchard sanitation and dormant oil spraying."
    }
}

def get_taxonomy_entry(class_id: str) -> Dict[str, Any]:
    """
    Retrieves canonical taxonomy details for a class ID or generates structured fallback.
    """
    if class_id in CANONICAL_DISEASE_TAXONOMY:
        return CANONICAL_DISEASE_TAXONOMY[class_id]

    parts = class_id.split("___")
    crop = parts[0].replace("_", " ")
    condition = parts[-1].replace("_", " ") if len(parts) > 1 else "Condition"
    is_healthy = "healthy" in class_id.lower()
    
    return {
        "crop": crop,
        "condition": condition,
        "status": "Healthy" if is_healthy else "Diseased",
        "severity": "None" if is_healthy else "Moderate",
        "is_pest_damage": "pest" in class_id.lower() or "hispa" in class_id.lower() or "borer" in class_id.lower(),
        "scientific_name": f"{crop} species",
        "synonyms": [condition],
        "dataset_sources": ["PlantVillage / PlantDoc Canonical Ontology"],
        "symptoms": "Healthy leaf structure." if is_healthy else f"Pathological lesions characteristic of {condition} on {crop} foliage.",
        "immediate_action": "Maintain routine crop monitoring." if is_healthy else f"Isolate affected {crop} plants and reduce canopy moisture.",
        "organic_treatment": "Apply bio-fertilizers or neem formulation.",
        "chemical_treatment": "No chemical intervention needed." if is_healthy else f"Apply recommended protective fungicide/bactericide for {condition}.",
        "prevention": "Standard agricultural practices and balanced NPK fertigation."
    }
