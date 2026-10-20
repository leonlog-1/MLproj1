"""
disease_info.py
===============
Clinical explanation dictionary, triage metadata, and patient guidance
for all 41 conditions in the dataset.
"""

from typing import Dict, Any

DISEASE_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "(vertigo) Paroymsal  Positional Vertigo": {
        "display_name": "Benign Paroxysmal Positional Vertigo (BPPV)",
        "category": "Neurological / ENT",
        "system": "Inner Ear & Vestibular System",
        "severity": "Moderate",
        "urgency_color": "#0284c7",
        "specialist": "ENT Specialist / Neurologist",
        "explanation": "BPPV is an inner ear disorder characterized by brief, recurring episodes of rotational dizziness or vertigo triggered by specific changes in head position. It occurs when tiny calcium carbonate crystals (otoconia) become dislodged from their normal location in the utricle and migrate into one of the semicircular canals.",
        "precautions": [
            "Avoid rapid head movements and sudden bending over.",
            "Sleep with your head slightly elevated on two pillows.",
            "Sit down immediately upon feeling dizzy to prevent falls or injury.",
            "Consult an ENT physician for canalith repositioning procedures (Epley maneuver)."
        ]
    },
    "AIDS": {
        "display_name": "Acquired Immunodeficiency Syndrome (AIDS)",
        "category": "Infectious & Immunological",
        "system": "Immune System",
        "severity": "High / Urgent",
        "urgency_color": "#dc2626",
        "specialist": "Infectious Disease Specialist / Immunologist",
        "explanation": "AIDS represents the advanced stage of infection caused by the Human Immunodeficiency Virus (HIV). HIV progressively depletes CD4+ T-helper lymphocytes, crippling cell-mediated immunity and rendering the body vulnerable to opportunistic infections and atypical malignancies.",
        "precautions": [
            "Undergo immediate confirmatory HIV ELISA/Western Blot or viral load testing.",
            "Begin and strictly adhere to Antiretroviral Therapy (ART) as prescribed.",
            "Practice safe barrier contraception and prevent blood-borne exposure.",
            "Avoid exposure to unpasteurized food or sick contacts to prevent opportunistic infections."
        ]
    },
    "Acne": {
        "display_name": "Acne Vulgaris",
        "category": "Dermatology",
        "system": "Integumentary (Skin)",
        "severity": "Mild",
        "urgency_color": "#10b981",
        "specialist": "Dermatologist",
        "explanation": "Acne vulgaris is a chronic inflammatory dermatosis of the pilosebaceous units. It develops from follicular hyperkeratinization, excess sebum secretion under androgenic stimulation, Cutibacterium acnes proliferation, and localized immunological inflammation, leading to comedones, papules, and pustules.",
        "precautions": [
            "Cleanse the face twice daily with a mild, non-comedogenic cleanser.",
            "Do not squeeze, pick, or pop pimples to prevent scarring and secondary bacterial infection.",
            "Avoid heavy oil-based cosmetic formulations.",
            "Consult a dermatologist for topical retinoids, benzoyl peroxide, or systemic therapies."
        ]
    },
    "Alcoholic hepatitis": {
        "display_name": "Alcoholic Hepatitis",
        "category": "Gastroenterology / Hepatology",
        "system": "Hepatic & Digestive System",
        "severity": "High / Urgent",
        "urgency_color": "#dc2626",
        "specialist": "Hepatologist / Gastroenterologist",
        "explanation": "Alcoholic hepatitis is acute hepatocellular inflammation and necrosis induced by toxic acetaldehyde metabolites from heavy alcohol consumption. It frequently presents with jaundice, right upper quadrant pain, hepatomegaly, anorexia, and deranged liver function tests.",
        "precautions": [
            "Complete and immediate cessation of all alcohol consumption.",
            "Seek urgent medical evaluation for hepatic panel and coagulopathy assessment.",
            "Maintain a high-calorie, high-protein diet with nutritional supplementation.",
            "Monitor closely for signs of ascites, encephalopathy, or gastrointestinal bleeding."
        ]
    },
    "Allergy": {
        "display_name": "Allergic Reaction / Hypersensitivity",
        "category": "Immunology & Allergy",
        "system": "Immune & Respiratory System",
        "severity": "Mild to Moderate",
        "urgency_color": "#0284c7",
        "specialist": "Allergist / Immunologist",
        "explanation": "An allergy is an exaggerated IgE-mediated immune response to foreign antigens (allergens) such as pollen, pet dander, foods, or insect stings. Mast cell degranulation releases histamine and leukotrienes, causing mucosal hypersecretion, sneezing, pruritus, and localized edema.",
        "precautions": [
            "Identify and remove environmental allergen triggers.",
            "Use over-the-counter or prescribed oral antihistamines for symptom relief.",
            "Rinse nasal passages with sterile saline solution to clear airborne irritants.",
            "Seek immediate emergency care if wheezing, facial swelling, or breathing difficulty occurs."
        ]
    },
    "Arthritis": {
        "display_name": "Arthritis (Inflammatory Joint Disease)",
        "category": "Rheumatology",
        "system": "Musculoskeletal System",
        "severity": "Moderate",
        "urgency_color": "#f59e0b",
        "specialist": "Rheumatologist / Orthopedic Specialist",
        "explanation": "Arthritis encompasses conditions causing inflammation, cartilage breakdown, and mechanical pain within one or more synovial joints. Chronic inflammatory cascades result in joint stiffness, effusion, restricted range of motion, and periarticular tenderness.",
        "precautions": [
            "Engage in low-impact physical exercise such as swimming or cycling to maintain joint mobility.",
            "Apply warm compresses for morning stiffness and ice packs for acute swelling.",
            "Maintain an optimal body weight to decrease mechanical stress on weight-bearing joints.",
            "Consult a rheumatologist for differential diagnostics (rheumatoid factor, ESR, uric acid)."
        ]
    },
    "Bronchial Asthma": {
        "display_name": "Bronchial Asthma",
        "category": "Pulmonology",
        "system": "Respiratory System",
        "severity": "Moderate to High",
        "urgency_color": "#f59e0b",
        "specialist": "Pulmonologist / Chest Physician",
        "explanation": "Bronchial asthma is a chronic inflammatory disorder of the conducting airways characterized by bronchial hyperresponsiveness, reversible airway obstruction, smooth muscle bronchospasm, and excessive mucus plugging, manifesting as episodic dyspnea, wheezing, and chest tightness.",
        "precautions": [
            "Carry a prescribed fast-acting bronchodilator (inhaler) at all times.",
            "Avoid exposure to tobacco smoke, dust mites, strong perfumes, and sudden cold air.",
            "Monitor peak expiratory flow rates to detect early airway constriction.",
            "Seek immediate emergency medical assistance if lips turn blue or inhalers fail to relieve dyspnea."
        ]
    },
    "Cervical spondylosis": {
        "display_name": "Cervical Spondylosis",
        "category": "Orthopedics & Spine",
        "system": "Musculoskeletal & Nervous System",
        "severity": "Moderate",
        "urgency_color": "#0284c7",
        "specialist": "Orthopedic Spine Surgeon / Physiotherapist",
        "explanation": "Cervical spondylosis is age-related chronic osteoarthritic degeneration of the cervical vertebrae and intervertebral discs. Bone spur formation (osteophytes) and disc herniation can compress nerve roots or the spinal cord, causing neck stiffness, radicular arm pain, and paresthesias.",
        "precautions": [
            "Maintain ergonomic posture while working at desks or computers.",
            "Perform gentle neck isometric and range-of-motion physiotherapy exercises.",
            "Use a firm, supportive cervical orthopedic pillow while sleeping.",
            "Avoid carrying heavy loads on shoulders or craning the neck downward for extended periods."
        ]
    },
    "Chicken pox": {
        "display_name": "Varicella (Chickenpox)",
        "category": "Infectious Disease / Pediatrics",
        "system": "Integumentary & Immune System",
        "severity": "Moderate",
        "urgency_color": "#f59e0b",
        "specialist": "Pediatrician / General Physician",
        "explanation": "Chickenpox is a contagious viral infection caused by the Varicella-Zoster Virus (VZV). It typically begins with mild fever and malaise, followed by a pruritic pleomorphic rash progressing rapidly from rose-colored macules to clear vesicles ('dewdrops on a rose petal'), pustules, and crusts.",
        "precautions": [
            "Isolate patient at home until all cutaneous vesicles have fully dried and crusted over.",
            "Apply calamine lotion and take cool colloidal oatmeal baths to soothe intense itching.",
            "Trim fingernails and wear soft gloves during sleep to prevent bacterial skin superinfection.",
            "Avoid aspirin in children due to the risk of Reye's syndrome; consult a physician for paracetamol."
        ]
    },
    "Chronic cholestasis": {
        "display_name": "Chronic Cholestasis",
        "category": "Gastroenterology / Hepatology",
        "system": "Biliary & Hepatic System",
        "severity": "High",
        "urgency_color": "#dc2626",
        "specialist": "Gastroenterologist / Hepatologist",
        "explanation": "Chronic cholestasis refers to prolonged impairment or obstruction of bile secretion or flow from the liver into the duodenum. Bile acids, bilirubin, and alkaline phosphatase accumulate in systemic circulation, leading to deep jaundice, intractable pruritus, dark urine, and pale stools.",
        "precautions": [
            "Obtain comprehensive liver function tests, serum bile acid quantification, and abdominal ultrasound.",
            "Avoid hepatotoxic medications and alcohol consumption entirely.",
            "Maintain supplementation of fat-soluble vitamins (A, D, E, K) as bile deficiency impairs absorption.",
            "Consult a specialist for evaluation of primary biliary cholangitis or biliary strictures."
        ]
    },
    "Common Cold": {
        "display_name": "Acute Viral Rhinitis (Common Cold)",
        "category": "Infectious & Upper Respiratory",
        "system": "Upper Respiratory Tract",
        "severity": "Mild",
        "urgency_color": "#10b981",
        "specialist": "General Physician / Family Doctor",
        "explanation": "The common cold is an acute, self-limiting viral infection of the upper respiratory mucosa, most commonly caused by Rhinoviruses or Coronaviruses. It triggers local inflammatory cytokine release, resulting in rhinorrhea, nasal congestion, mild sore throat, sneezing, and low-grade constitutional symptoms.",
        "precautions": [
            "Get plenty of restful sleep and hydrate adequately with warm fluids.",
            "Use warm saline gargles and steam inhalation to relieve throat and sinus congestion.",
            "Wash hands frequently and practice respiratory etiquette to avoid transmission.",
            "Avoid unnecessary antibiotic usage as the condition is purely viral."
        ]
    },
    "Dengue": {
        "display_name": "Dengue Fever",
        "category": "Tropical & Infectious Disease",
        "system": "Circulatory & Hematologic System",
        "severity": "High / Urgent",
        "urgency_color": "#dc2626",
        "specialist": "Infectious Disease Specialist / Physician",
        "explanation": "Dengue is an acute mosquito-borne flaviviral infection transmitted by Aedes aegypti. It presents with sudden high fever, retro-orbital eye pain, severe arthralgia and myalgia ('breakbone fever'), and petechial rash. Severe forms carry risks of thrombocytopenia, plasma leakage, and dengue hemorrhagic shock.",
        "precautions": [
            "Monitor platelet counts and hematocrit daily via complete blood count (CBC).",
            "Maintain aggressive oral and intravenous fluid hydration to prevent hypovolemic shock.",
            "Avoid NSAIDs, aspirin, and ibuprofen due to bleeding risk; use only paracetamol for fever.",
            "Seek immediate hospitalization if persistent vomiting, abdominal pain, or mucosal bleeding develops."
        ]
    },
    "Diabetes ": {
        "display_name": "Diabetes Mellitus",
        "category": "Endocrinology & Metabolism",
        "system": "Endocrine & Metabolic System",
        "severity": "High / Chronic",
        "urgency_color": "#f59e0b",
        "specialist": "Endocrinologist / Diabetologist",
        "explanation": "Diabetes mellitus is a chronic metabolic disorder marked by persistent hyperglycemia resulting from defects in insulin secretion, peripheral insulin action, or both. Chronic osmotic diuresis leads to classic polyuria, polydipsia, polyphagia, and progressive micro- and macrovascular complications.",
        "precautions": [
            "Check fasting blood glucose and HbA1c levels promptly.",
            "Adopt a controlled carbohydrate, high-fiber, low-glycemic dietary regimen.",
            "Engage in regular moderate aerobic exercise to improve peripheral insulin sensitivity.",
            "Perform daily foot examinations and adhere consistently to prescribed antidiabetic medications."
        ]
    },
    "Dimorphic hemmorhoids(piles)": {
        "display_name": "Hemorrhoidal Disease (Piles)",
        "category": "Proctology / Colorectal",
        "system": "Gastrointestinal & Vascular System",
        "severity": "Moderate",
        "urgency_color": "#0284c7",
        "specialist": "Colorectal Surgeon / Proctologist",
        "explanation": "Hemorrhoids are pathologically dilated, inflamed venous cushions located in the sub-mucosal lining of the distal rectum and anal canal. Straining during defecation and chronic constipation elevate intra-abdominal venous pressure, inducing bright red painless bleeding, prolapse, and perianal thrombosis.",
        "precautions": [
            "Increase dietary soluble and insoluble fiber intake to soften stool consistency.",
            "Drink at least 2.5 to 3 liters of water daily to prevent defecatory straining.",
            "Take warm sitz baths for 15 minutes twice daily to relieve perianal discomfort.",
            "Avoid prolonged sitting on the toilet and consult a proctologist if bleeding is persistent."
        ]
    },
    "Drug Reaction": {
        "display_name": "Adverse Cutaneous Drug Reaction",
        "category": "Allergy & Dermatology",
        "system": "Immune & Integumentary System",
        "severity": "High / Urgent",
        "urgency_color": "#dc2626",
        "specialist": "Dermatologist / Allergist",
        "explanation": "An adverse drug eruption is an unwanted immunological or non-immunological reaction of the skin and mucous membranes following medication intake. Manifestations range from mild exanthematous morbilliform rashes to severe cutaneous adverse reactions like Stevens-Johnson syndrome.",
        "precautions": [
            "Immediately contact a physician and discontinue the suspected culprit medication.",
            "Keep a written log of all recent medications, antibiotics, and over-the-counter supplements.",
            "Apply soothing emollient creams and avoid hot showers.",
            "Seek emergency care if mucosal peeling, facial blistering, or breathing distress develops."
        ]
    },
    "Fungal infection": {
        "display_name": "Dermatophytosis (Fungal Skin Infection)",
        "category": "Dermatology / Mycology",
        "system": "Integumentary System (Skin)",
        "severity": "Mild to Moderate",
        "urgency_color": "#10b981",
        "specialist": "Dermatologist",
        "explanation": "Superficial fungal infections (tinea/dermatophytosis) are caused by keratinophilic fungi such as Trichophyton and Microsporum. Fungi digest keratin in the stratum corneum, creating classic annular erythematous plaques with raised, active scaling borders and central clearing.",
        "precautions": [
            "Keep affected skin folds clean, cool, and completely dry.",
            "Apply topical antifungal creams (e.g. Clotrimazole or Terbinafine) consistently as directed.",
            "Wear loose-fitting, breathable cotton clothing and change undergarments daily.",
            "Do not share towels, combs, or personal grooming articles with household members."
        ]
    },
    "GERD": {
        "display_name": "Gastroesophageal Reflux Disease (GERD)",
        "category": "Gastroenterology",
        "system": "Digestive & Upper GI System",
        "severity": "Moderate",
        "urgency_color": "#0284c7",
        "specialist": "Gastroenterologist",
        "explanation": "GERD develops when gastric acidic contents repetitively flow retrograde through an incompetent lower esophageal sphincter (LES) into the esophagus. Acid exposure irritates esophageal mucosa, causing retrosternal burning pain (heartburn), acid regurgitation, dysphagia, and nocturnal cough.",
        "precautions": [
            "Avoid large, heavy meals right before bedtime; allow at least 3 hours before lying down.",
            "Elevate the head of your bed by 6 inches using bed risers.",
            "Limit consumption of acidic, fatty, spicy foods, caffeine, chocolate, and carbonated beverages.",
            "Consult a doctor regarding acid-suppression therapy (PPIs or H2 receptor blockers)."
        ]
    },
    "Gastroenteritis": {
        "display_name": "Acute Gastroenteritis (Stomach Flu)",
        "category": "Gastroenterology / Infectious",
        "system": "Gastrointestinal System",
        "severity": "Moderate",
        "urgency_color": "#f59e0b",
        "specialist": "General Physician / Gastroenterologist",
        "explanation": "Acute gastroenteritis is an inflammatory condition of the mucosal lining of the stomach and intestines, typically caused by viral (Norovirus, Rotavirus) or bacterial pathogens. Intestinal inflammation impairs fluid and nutrient absorption, triggering watery diarrhea, emesis, and abdominal cramps.",
        "precautions": [
            "Prioritize oral rehydration solutions (ORS) and electrolyte replacement to prevent dehydration.",
            "Follow the BRAT diet (Bananas, Rice, Applesauce, Toast) during early recovery.",
            "Avoid dairy, greasy foods, caffeine, and high-sugar fruit juices.",
            "Seek urgent medical evaluation if unable to keep fluids down or if stool contains blood."
        ]
    },
    "Heart attack": {
        "display_name": "Acute Myocardial Infarction (Heart Attack)",
        "category": "Cardiology / Emergency",
        "system": "Cardiovascular System",
        "severity": "CRITICAL EMERGENCY",
        "urgency_color": "#b91c1c",
        "specialist": "Interventional Cardiologist / ER Team",
        "explanation": "Myocardial infarction occurs when coronary blood flow is abruptly occluded—typically by atheromatous plaque rupture and subsequent thrombus formation. Cardiac myocytes downstream undergo acute ischemic injury and irreversible necrosis within hours unless revascularized.",
        "precautions": [
            "CALL EMERGENCY SERVICES (911/112/108) IMMEDIATELY — TIME IS MUSCLE.",
            "Chew an unbuffered aspirin (325mg) if advised by emergency operators and not allergic.",
            "Rest in a comfortable, seated or semi-reclined position to reduce myocardial oxygen demand.",
            "Do not drive yourself to the hospital; await paramedics equipped with defibrillators."
        ]
    },
    "Hepatitis B": {
        "display_name": "Viral Hepatitis B",
        "category": "Hepatology & Infectious Disease",
        "system": "Hepatic (Liver) System",
        "severity": "High",
        "urgency_color": "#dc2626",
        "specialist": "Hepatologist / Infectious Disease Specialist",
        "explanation": "Hepatitis B is a viral infection caused by the Hepatitis B Virus (HBV), transmitted via contact with infectious blood or bodily fluids. The host immune response against infected hepatocytes produces liver inflammation, jaundice, malaise, and can progress to cirrhosis or hepatocellular carcinoma.",
        "precautions": [
            "Undergo quantitative HBV DNA testing, HBsAg confirmation, and complete liver panel.",
            "Completely abstain from all alcoholic beverages and avoid hepatotoxic drugs.",
            "Ensure household contacts and sexual partners receive the Hepatitis B vaccination.",
            "Consult a hepatologist to evaluate indications for oral antiviral therapies (e.g. Entecavir)."
        ]
    },
    "Hepatitis C": {
        "display_name": "Viral Hepatitis C",
        "category": "Hepatology & Infectious Disease",
        "system": "Hepatic (Liver) System",
        "severity": "High",
        "urgency_color": "#dc2626",
        "specialist": "Hepatologist / Infectious Disease Specialist",
        "explanation": "Hepatitis C is a blood-borne infection caused by the Hepatitis C Virus (HCV). Chronic infection occurs in over 75% of exposed individuals, typically remaining asymptomatic for decades while slowly causing progressive hepatic fibrosis, cirrhosis, and liver failure.",
        "precautions": [
            "Consult a hepatologist for HCV RNA quantification and viral genotype testing.",
            "Modern direct-acting antivirals (DAAs) achieve cure rates over 95% in 8-12 weeks.",
            "Avoid alcohol and consult your physician before starting any prescription medications.",
            "Get vaccinated against Hepatitis A and B to protect against concurrent liver insults."
        ]
    },
    "Hepatitis D": {
        "display_name": "Viral Hepatitis D (Delta Virus)",
        "category": "Hepatology & Infectious Disease",
        "system": "Hepatic (Liver) System",
        "severity": "High / Severe",
        "urgency_color": "#dc2626",
        "specialist": "Hepatologist",
        "explanation": "Hepatitis D is caused by the Hepatitis Delta Virus (HDV), a defective satellite virus that requires the presence of Hepatitis B surface antigen (HBsAg) to assemble and replicate. Co-infection or superinfection with HDV accelerates the progression of hepatic necroinflammation and cirrhosis.",
        "precautions": [
            "Confirm HDV RNA and antibody status in any HBsAg-positive patient.",
            "Specialized antiviral therapy (e.g. Bulevirtide or Pegylated Interferon) requires expert hepatologist supervision.",
            "Strictly avoid alcohol and hepatotoxic compounds.",
            "Monitor liver stiffness via elastography and screen regularly for hepatic decompensation."
        ]
    },
    "Hepatitis E": {
        "display_name": "Viral Hepatitis E",
        "category": "Hepatology / Enteric Infectious",
        "system": "Hepatic & Digestive System",
        "severity": "Moderate to High",
        "urgency_color": "#f59e0b",
        "specialist": "Gastroenterologist / Infectious Disease Specialist",
        "explanation": "Hepatitis E is an enterically transmitted viral infection primarily contracted through ingestion of fecal-contaminated drinking water. It causes acute self-limited viral hepatitis characterized by jaundice, fatigue, hepatomegaly, and nausea. It carries severe risk of fulminant liver failure in pregnant women.",
        "precautions": [
            "Drink only bottled, boiled, or chemically purified water.",
            "Maintain strict hand hygiene before meals and food preparation.",
            "Pregnant women exhibiting symptoms require immediate hospitalization and close maternal-fetal monitoring.",
            "Rest adequately and consume a light, easily digestible carbohydrate-rich diet."
        ]
    },
    "Hypertension ": {
        "display_name": "Essential Hypertension (High Blood Pressure)",
        "category": "Cardiology",
        "system": "Cardiovascular & Vascular System",
        "severity": "High / Chronic",
        "urgency_color": "#f59e0b",
        "specialist": "Cardiologist / General Physician",
        "explanation": "Hypertension is a chronic elevation of systemic arterial blood pressure (systolic ≥ 130 mmHg or diastolic ≥ 80 mmHg). Sustained hemodynamic stress forces myocardial hypertrophy and accelerates endothelial atherogenesis, dramatically raising the risk of stroke, heart failure, and renal insufficiency.",
        "precautions": [
            "Adopt the DASH diet (rich in fruits, vegetables, and low-fat dairy; low in saturated fat).",
            "Reduce dietary sodium intake to less than 2,000 mg per day.",
            "Engage in at least 150 minutes of moderate-intensity aerobic exercise each week.",
            "Monitor blood pressure regularly at home and strictly take antihypertensive medications."
        ]
    },
    "Hyperthyroidism": {
        "display_name": "Hyperthyroidism (Overactive Thyroid)",
        "category": "Endocrinology",
        "system": "Endocrine & Metabolic System",
        "severity": "Moderate to High",
        "urgency_color": "#f59e0b",
        "specialist": "Endocrinologist",
        "explanation": "Hyperthyroidism results from hypersecretion of free thyroid hormones (T3 and T4) by an overactive thyroid gland (most often due to Graves' disease or toxic nodular goiter). Excessive thyroid hormones hyperstimulate metabolic rate, causing tachycardia, weight loss, tremor, heat intolerance, and insomnia.",
        "precautions": [
            "Obtain serum TSH, free T4, free T3, and anti-TSH receptor antibody tests.",
            "Avoid high-iodine supplements, kelp, and excessive caffeine.",
            "Consult an endocrinologist regarding antithyroid medications (Methimazole) or beta-blockers.",
            "Report palpitations, sudden eye protrusion, or high fever immediately."
        ]
    },
    "Hypoglycemia": {
        "display_name": "Hypoglycemia (Low Blood Sugar)",
        "category": "Endocrinology / Acute Metabolic",
        "system": "Metabolic & Neurological System",
        "severity": "High / Urgent",
        "urgency_color": "#dc2626",
        "specialist": "Endocrinologist / ER Physician",
        "explanation": "Hypoglycemia is an acute drop in blood glucose below physiological requirements (< 70 mg/dL). Autonomic counter-regulatory activation causes diaphoresis, tremors, tachycardia, and anxiety, while neuroglycopenia starves the brain, producing dizziness, confusion, seizures, or coma if uncorrected.",
        "precautions": [
            "Follow the 'Rule of 15': Ingest 15g of fast-acting simple carbohydrates (fruit juice or glucose tablets).",
            "Re-check blood glucose after 15 minutes; repeat if still below 70 mg/dL.",
            "Once stabilized, eat a balanced snack containing complex carbohydrates and protein.",
            "Review insulin or sulfonylurea dosing with your treating physician immediately."
        ]
    },
    "Hypothyroidism": {
        "display_name": "Hypothyroidism (Underactive Thyroid)",
        "category": "Endocrinology",
        "system": "Endocrine & Metabolic System",
        "severity": "Moderate / Chronic",
        "urgency_color": "#0284c7",
        "specialist": "Endocrinologist",
        "explanation": "Hypothyroidism is a systemic deficiency in thyroid hormone action, most commonly caused in adults by chronic autoimmune Hashimoto's thyroiditis. Diminished metabolic rate causes generalized lethargy, cold intolerance, unexplained weight gain, dry skin, bradycardia, and cognitive slowing.",
        "precautions": [
            "Obtain serum TSH and Free T4 measurements to confirm diagnosis.",
            "Take prescribed synthetic levothyroxine consistently on an empty stomach 30-60 min before breakfast.",
            "Avoid taking calcium or iron supplements within 4 hours of levothyroxine.",
            "Schedule follow-up thyroid panel checks every 6 to 12 weeks during dose titration."
        ]
    },
    "Impetigo": {
        "display_name": "Impetigo Contagiosa",
        "category": "Dermatology / Pediatric",
        "system": "Integumentary System (Skin)",
        "severity": "Mild to Moderate",
        "urgency_color": "#10b981",
        "specialist": "Dermatologist / Pediatrician",
        "explanation": "Impetigo is a contagious superficial bacterial pyoderma primarily caused by Staphylococcus aureus or Streptococcus pyogenes. Bacterial toxins disrupt epidermal cell adhesion, resulting in fragile intraepidermal blisters that rupture and form characteristic honey-colored ('golden') crusts.",
        "precautions": [
            "Gently cleanse crusts with antibacterial soap and warm water.",
            "Apply prescribed topical antibiotic ointment (e.g., Mupirocin) to lesions.",
            "Wash patient's towels, linens, and clothes separately in hot water.",
            "Keep children home from school until 24-48 hours after initiating antibiotic therapy."
        ]
    },
    "Jaundice": {
        "display_name": "Hyperbilirubinemia (Jaundice)",
        "category": "Hepatology / Gastroenterology",
        "system": "Hepatobiliary & Hemolytic System",
        "severity": "High",
        "urgency_color": "#dc2626",
        "specialist": "Gastroenterologist / Hepatologist",
        "explanation": "Jaundice (icterus) is yellowish discoloration of the sclerae, mucous membranes, and skin resulting from elevated serum bilirubin (> 2.5 mg/dL). It is a clinical sign of underlying pre-hepatic hemolysis, intra-hepatic hepatocellular injury, or post-hepatic biliary tract obstruction.",
        "precautions": [
            "Seek urgent medical evaluation with fractionated bilirubin and liver function panel.",
            "Undergo abdominal ultrasonography to assess for gallstones or bile duct dilatation.",
            "Avoid alcohol, acetaminophen, and non-prescribed supplements completely.",
            "Drink plenty of water and maintain adequate caloric nutrition."
        ]
    },
    "Malaria": {
        "display_name": "Malaria Infection",
        "category": "Infectious & Tropical Disease",
        "system": "Hematologic & Systemic",
        "severity": "High / Urgent",
        "urgency_color": "#dc2626",
        "specialist": "Infectious Disease Specialist / Physician",
        "explanation": "Malaria is a protozoan parasitic disease caused by Plasmodium species (e.g. P. falciparum, P. vivax) transmitted via the bite of infected female Anopheles mosquitoes. Parasitic multiplication within red blood cells culminates in cyclical hemolysis, causing paroxysms of severe chills, high spiking fevers, and profuse diaphoresis.",
        "precautions": [
            "Undergo immediate blood smear microscopy or Rapid Diagnostic Test (RDT) for Plasmodium.",
            "Begin Artemisinin-based Combination Therapy (ACT) promptly as prescribed.",
            "Maintain aggressive oral hydration and take paracetamol for fever control.",
            "Sleep under insecticide-treated bed nets and eliminate standing water around living areas."
        ]
    },
    "Migraine": {
        "display_name": "Migraine Headache",
        "category": "Neurology",
        "system": "Central Nervous System & Cranial Vasculature",
        "severity": "Moderate",
        "urgency_color": "#0284c7",
        "specialist": "Neurologist",
        "explanation": "Migraine is a neurovascular disorder characterized by recurrent attacks of severe, unilateral, throbbing headache typically lasting 4 to 72 hours. Trigeminal nerve sensory activation releases inflammatory neuropeptides, causing cranial neurogenic inflammation, photophobia, phonophobia, and nausea.",
        "precautions": [
            "Rest in a quiet, dark, temperature-controlled room during acute attacks.",
            "Identify and avoid personal dietary triggers (aged cheese, red wine, MSG, artificial sweeteners).",
            "Maintain consistent sleep schedules and avoid skipping meals.",
            "Consult a neurologist for abortive (triptans) and prophylactic migraine therapies."
        ]
    },
    "Osteoarthristis": {
        "display_name": "Osteoarthritis (Degenerative Joint Disease)",
        "category": "Rheumatology / Orthopedics",
        "system": "Musculoskeletal System",
        "severity": "Moderate / Chronic",
        "urgency_color": "#0284c7",
        "specialist": "Orthopedic Specialist / Rheumatologist",
        "explanation": "Osteoarthritis is progressive non-inflammatory degenerative joint disease characterized by progressive breakdown of articular cartilage, subchondral bone remodeling, and marginal osteophyte formation. It manifests with mechanical joint pain exacerbated by activity, joint stiffness, and crepitus.",
        "precautions": [
            "Engage in non-weight-bearing physical therapy (aquatic therapy, stationary cycling).",
            "Weight management is paramount to reduce mechanical stress on knees and hips.",
            "Use supportive footwear or assistive walking devices when necessary.",
            "Discuss topical NSAIDs, acetaminophen, or hyaluronic acid joint injections with your doctor."
        ]
    },
    "Paralysis (brain hemorrhage)": {
        "display_name": "Hemorrhagic Stroke / Hemiplegia",
        "category": "Neurology / Neurovascular",
        "system": "Central Nervous System (Brain)",
        "severity": "CRITICAL EMERGENCY",
        "urgency_color": "#b91c1c",
        "specialist": "Neurologist / Neurosurgeon / Stroke Team",
        "explanation": "Intracranial hemorrhage results from rupture of a weakened cerebral blood vessel (often due to chronic hypertension or arteriovenous malformation). Hematoma expansion compresses neural tissue, elevating intracranial pressure and causing contralateral hemiparesis or paralysis, dysphasia, and altered consciousness.",
        "precautions": [
            "ACT FAST — CALL EMERGENCY SERVICES (911/112/108) IMMEDIATELY.",
            "Note the exact time symptoms began for critical treatment window calculations.",
            "Do NOT administer aspirin or anticoagulants as bleeding in the brain will worsen.",
            "Keep patient lying on their side with head elevated 30 degrees to prevent aspiration."
        ]
    },
    "Peptic ulcer diseae": {
        "display_name": "Peptic Ulcer Disease (PUD)",
        "category": "Gastroenterology",
        "system": "Gastrointestinal System",
        "severity": "Moderate to High",
        "urgency_color": "#f59e0b",
        "specialist": "Gastroenterologist",
        "explanation": "Peptic ulcer disease is a mucosal breach in the stomach or proximal duodenum extending through the muscularis mucosae. It arises from an imbalance between aggressive factors (gastric acid, pepsin, H. pylori infection, NSAID use) and protective mucosal defenses, causing burning epigastric pain that fluctuates with meals.",
        "precautions": [
            "Consult a gastroenterologist for H. pylori testing (urea breath test or stool antigen) and endoscopy.",
            "Avoid NSAIDs (aspirin, ibuprofen, naproxen); use paracetamol for analgesia if needed.",
            "Stop smoking and avoid alcohol, both of which severely impair mucosal ulcer healing.",
            "Seek immediate medical attention if vomiting dark blood or passing black, tarry stools."
        ]
    },
    "Pneumonia": {
        "display_name": "Pneumonia (Lower Respiratory Infection)",
        "category": "Pulmonology / Infectious Disease",
        "system": "Lower Respiratory & Alveolar System",
        "severity": "High / Urgent",
        "urgency_color": "#dc2626",
        "specialist": "Pulmonologist / Chest Physician",
        "explanation": "Pneumonia is an acute infection of the lung parenchyma caused by bacteria (Streptococcus pneumoniae), viruses, or fungi. Alveoli fill with inflammatory exudate and cellular debris (consolidation), impairing gas exchange and causing fever, productive cough with purulent sputum, pleuritic chest pain, and dyspnea.",
        "precautions": [
            "Obtain a chest X-ray, complete blood count, and sputum culture.",
            "Complete the entire course of prescribed antibiotics or antivirals without stopping early.",
            "Monitor blood oxygen saturation ($SpO_2$) with a pulse oximeter regularly.",
            "Seek emergency care if oxygen levels drop below 92%, or if confusion and severe breathlessness occur."
        ]
    },
    "Psoriasis": {
        "display_name": "Psoriasis Vulgaris",
        "category": "Dermatology / Autoimmune",
        "system": "Integumentary & Immune System",
        "severity": "Moderate / Chronic",
        "urgency_color": "#0284c7",
        "specialist": "Dermatologist",
        "explanation": "Psoriasis is a chronic, immune-mediated inflammatory dermatosis driven by dysregulated T-lymphocyte cytokine signaling (IL-17, IL-23, TNF-alpha). This accelerates epidermal keratinocyte proliferation, causing thick, sharply demarcated erythematous plaques covered by characteristic silvery-white micaceous scales.",
        "precautions": [
            "Keep skin continuously moisturized using thick ointment-based emollients.",
            "Avoid skin injury, cuts, and friction, which trigger new lesions (Koebner phenomenon).",
            "Moderate, controlled natural sunlight exposure can be beneficial under dermatological advice.",
            "Consult a dermatologist regarding topical corticosteroids, vitamin D analogs, or biologic agents."
        ]
    },
    "Tuberculosis": {
        "display_name": "Pulmonary Tuberculosis (TB)",
        "category": "Infectious & Pulmonology",
        "system": "Respiratory & Lymphatic System",
        "severity": "High / Urgent",
        "urgency_color": "#dc2626",
        "specialist": "Pulmonologist / Infectious Disease Specialist",
        "explanation": "Tuberculosis is a contagious granulomatous bacterial infection caused by Mycobacterium tuberculosis. Inhaled bacilli reach lung alveoli and trigger cell-mediated immune defense forming caseating granulomas, presenting with chronic cough lasting >3 weeks, hemoptysis, drenching night sweats, and significant cachexia.",
        "precautions": [
            "Obtain sputum acid-fast bacilli (AFB) smear, GeneXpert molecular testing, and chest radiograph.",
            "Strictly complete the full multi-month course of anti-tubercular therapy (ATT) to prevent drug resistance.",
            "Wear a well-fitted mask and isolate in well-ventilated rooms during early infectious phase.",
            "Ensure all close household contacts are screened for latent tuberculosis infection."
        ]
    },
    "Typhoid": {
        "display_name": "Enteric Fever (Typhoid)",
        "category": "Infectious & Tropical Disease",
        "system": "Gastrointestinal & Reticuloendothelial",
        "severity": "High / Urgent",
        "urgency_color": "#dc2626",
        "specialist": "Infectious Disease Specialist / Physician",
        "explanation": "Typhoid fever is a systemic bacteremia caused by Salmonella enterica serovar Typhi, contracted via fecal-oral contamination of food or water. Bacteria invade intestinal Peyer's patches and disseminate, causing a classic 'step-ladder' rising fever, relative bradycardia, abdominal tenderness, hepatosplenomegaly, and rose spots.",
        "precautions": [
            "Perform blood and stool cultures to confirm Salmonella Typhi and test antibiotic sensitivity.",
            "Complete the entire course of targeted antibiotic therapy prescribed by your doctor.",
            "Drink only boiled or bottled water and consume freshly cooked, piping-hot meals.",
            "Practice scrupulous hand hygiene with soap and water after using the restroom."
        ]
    },
    "Urinary tract infection": {
        "display_name": "Urinary Tract Infection (UTI / Cystitis)",
        "category": "Urology / Nephrology",
        "system": "Urinary & Renal System",
        "severity": "Moderate",
        "urgency_color": "#0284c7",
        "specialist": "Urologist / General Physician",
        "explanation": "A UTI is an infection of the urinary tract, most commonly acute bacterial cystitis caused by uropathogenic Escherichia coli ascending through the urethra. Bacterial proliferation and mucosal inflammation cause burning micturition (dysuria), urinary frequency, urgency, and suprapubic pain.",
        "precautions": [
            "Drink large amounts of water (2 to 3 liters daily) to promote frequent flushing of the urinary bladder.",
            "Submit a clean-catch midstream urine sample for urinalysis and culture.",
            "Complete full prescribed antibiotic therapy even if burning sensation disappears quickly.",
            "Seek urgent care if high fever, chills, or flank pain develops (signs of ascending pyelonephritis)."
        ]
    },
    "Varicose veins": {
        "display_name": "Chronic Venous Insufficiency (Varicose Veins)",
        "category": "Vascular Surgery / Phlebology",
        "system": "Venous & Circulatory System",
        "severity": "Moderate",
        "urgency_color": "#0284c7",
        "specialist": "Vascular Surgeon / Phlebologist",
        "explanation": "Varicose veins are dilated, tortuous superficial veins (predominantly in the lower extremities) caused by incompetent venous valves and venous wall weakness. Retrograde venous pooling elevates hydrostatic pressure, resulting in leg heaviness, dull aching pain, peripheral edema, and venous stasis dermatitis.",
        "precautions": [
            "Wear graduated medical compression stockings (Class II) during daytime standing or sitting.",
            "Elevate your legs above heart level for 15 minutes 3-4 times daily to facilitate venous return.",
            "Avoid prolonged periods of uninterrupted standing or sitting; flex ankles periodically.",
            "Engage in regular calf-strengthening walking exercises to activate the muscular calf venous pump."
        ]
    },
    "hepatitis A": {
        "display_name": "Viral Hepatitis A",
        "category": "Hepatology / Enteric Infectious",
        "system": "Hepatic & Digestive System",
        "severity": "Moderate to High",
        "urgency_color": "#f59e0b",
        "specialist": "Gastroenterologist / Physician",
        "explanation": "Hepatitis A is an acute, self-limiting liver infection caused by the Hepatitis A Virus (HAV), spread via ingestion of food or water contaminated with feces. It causes acute hepatocellular inflammation with clinical jaundice, dark amber urine, profound fatigue, nausea, and right upper quadrant abdominal tenderness.",
        "precautions": [
            "Ensure complete physical rest while the acute liver inflammation resolves.",
            "Drink plenty of fluids and maintain small, light carbohydrate meals that are easy to digest.",
            "Avoid alcohol and any hepatotoxic medications (consult doctor before taking any analgesics).",
            "Maintain strict handwashing hygiene and ensure household contacts receive the HAV vaccine."
        ]
    }
}


def get_disease_details(disease_key: str) -> Dict[str, Any]:
    """
    Returns rich metadata, clinical description, precautions,
    and visual attributes for a predicted disease.
    """
    if disease_key in DISEASE_KNOWLEDGE_BASE:
        return DISEASE_KNOWLEDGE_BASE[disease_key]

    # Try stripped or title-cased fallback
    stripped_key = disease_key.strip()
    for key, data in DISEASE_KNOWLEDGE_BASE.items():
        if key.strip().lower() == stripped_key.lower():
            return data

    # Default fallback
    return {
        "display_name": disease_key.strip().title(),
        "category": "General Clinical",
        "system": "Systemic",
        "severity": "Moderate",
        "urgency_color": "#0284c7",
        "specialist": "General Physician",
        "explanation": (
            f"The model has identified clinical symptom co-occurrences aligning with {disease_key}. "
            "Please consult a certified medical practitioner for professional diagnostic confirmation."
        ),
        "precautions": [
            "Monitor symptoms closely and record any changes in severity.",
            "Maintain adequate hydration and rest.",
            "Consult a healthcare professional for clinical examination.",
            "Seek emergency assistance if severe pain or shortness of breath develops."
        ]
    }
