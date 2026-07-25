import os
import glob

# ==========================================
# 1. KNOWLEDGE BASE (Questions & Options)
# ==========================================

QUESTIONS = [
    {
        "id": "reason",
        "text_en": "What is the primary reason for your trip?",
        "text_ar": "ما هو السبب الرئيسي لسفرك؟",
        "options": [
            ({"en": "Job/Study Burnout (Need a Quick Escape)", "ar": "احتراق وظيفي أو دراسي (أحتاج مهرباً سريعاً)"}, "burnout"),
            ({"en": "Relaxation & Self-Care", "ar": "الاستجمام والترفيه عن النفس"}, "relax"),
            ({"en": "Adventure & Exploration", "ar": "المغامرة والاستكشاف"}, "adventure"),
            ({"en": "Education & Study", "ar": "التعليم والدراسة"}, "study"),
            ({"en": "Medical Treatment & Recovery", "ar": "العلاج والاستشفاء"}, "medical"),
            ({"en": "Honeymoon / Marriage", "ar": "شهر العسل / الزواج"}, "honeymoon"),
            ({"en": "Charity & Volunteering", "ar": "العمل التطوعي وعمل الخير"}, "charity")
        ],
        "why_en": "The core purpose shapes the overall travel itinerary—from fast weekend escapes to medical or volunteer journeys.",
        "why_ar": "الهدف الأساسي يحدد مسار الرحلة بالكامل، سواء كانت رحلة استرخاء سريعة أو علاج أو عمل تطوعي."
    },

    # --- Medical Follow-Up Questions (Germany & California sub-branch) ---
    # --- Medical Follow-Up Questions ---
    {
        "id": "medical_type",
        "text_en": "What type of healthcare environment do you require?",
        "text_ar": "ما هو نوع البيئة العلاجية التي تحتاجها؟",
        "options": [
            ({"en": "World-Class Surgical & University Clinics", "ar": "مستشفيات جامعية ومراكز جراحية عالمية"}, "clinical"),
            ({"en": "Thermal Springs & Spa Recovery", "ar": "منتجعات استشفائية ومياه كبريتية في الطبيعة"}, "spa")
        ],
        "why_en": "Helps customize whether you need urban medical hubs in Germany or thermal springs in California.",
        "why_ar": "يساعد في تحديد ما إذا كنت بحاجة لمراكز طبية في ألمانيا أو منتجعات استشفاء في كاليفورنيا."
    },

    # --- Charity Follow-Up Questions ---
    {
        "id": "charity_type",
        "text_en": "What kind of volunteer work inspires you most?",
        "text_ar": "ما هو نوع العمل التطوعي الذي يلهمك أكثر؟",
        "options": [
            ({"en": "Teaching Children & Community Education (Nepal)", "ar": "تعليم الأطفال والدعم التعليمي المجتمعي (نيبال)"}, "teaching"),
            ({"en": "Rainforest & Eco-Conservation (Indonesia)", "ar": "حماية الغابات المطيرة والبيئة البحرية (إندونيسيا)"}, "eco")
        ],
        "why_en": "Aligns your personal skills with community and environmental projects in Nepal and Indonesia.",
        "why_ar": "يطابق مهاراتك مع المشاريع المجتمعية والبيئية في نيبال وإندونيسيا."
    },

    # --- General Questions ---
    {
        "id": "duration",
        "text_en": "How long do you plan to travel?",
        "text_ar": "كم عدد الأيام أو المدة التي ستقضيها؟",
        "options": [
            ({"en": "A short weekend (2-3 days)", "ar": "عطلة نهاية أسبوع قصيرة (2-3 أيام)"}, "weekend"),
            ({"en": "1 to 2 Weeks", "ar": "أسبوع إلى أسبوعين"}, "medium"),
            ({"en": "3+ Weeks (Long Trip)", "ar": "أكثر من 3 أسابيع (رحلة طويلة)"}, "long")
        ],
        "why_en": "Duration decides if we suggest accessible local spots or long-haul international voyages.",
        "why_ar": "المدة تحدد ما إذا كنا سنقترح وجهات محلية قريبة أم رحلات دولية طويلة."
    },
    {
        "id": "phobia",
        "text_en": "Do you have any specific travel fears or phobias?",
        "text_ar": "هل تعاني من أي مخاوف معينة أثناء السفر؟",
        "options": [
            ({"en": "None, I'm ready for anything!", "ar": "لا يوجد، أنا مستعد لأي شيء!"}, "none"),
            ({"en": "Fear of Flying (Aviophobia)", "ar": "الخوف من الطيران"}, "flying"),
            ({"en": "Fear of Heights (Acrophobia)", "ar": "الخوف من المرتفعات والجبال"}, "heights")
        ],
        "why_en": "We filter out high-altitude mountain locations or long-distance flights based on your comfort.",
        "why_ar": "نقوم باستبعاد الأماكن الجبلية المرتفعة أو الرحلات الجوية الطويلة لضمان راحتك."
    },
    {
        "id": "budget",
        "text_en": "What is your budget level?",
        "text_ar": "ما هو مستوى ميزانيتك المقترحة؟",
        "options": [
            ({"en": "Low / Backpacking Style", "ar": "ميزانية محدودة / سياحة اقتصادية"}, "low"),
            ({"en": "Medium / Standard Comfort", "ar": "متوسطة / راحة تقليدية متوازنة"}, "medium"),
            ({"en": "High / Ultra Luxury", "ar": "عالية جداً / رفاهية مطلقة وفخمة"}, "high")
        ],
        "why_en": "Budget maps the destination to affordable hidden gems or elite premium resorts.",
        "why_ar": "الميزانية تربط وجهتك بأماكن اقتصادية مميزة أو منتجعات فاخرة."
    },
    {
        "id": "vibe",
        "text_en": "What kind of atmosphere vibe pulls you in?",
        "text_ar": "ما هو الجو العام والبيئة التي تستهويك؟",
        "options": [
            ({"en": "Serene Nature & Greenery", "ar": "الطبيعة العذراء والمناظر الخضراء"}, "nature"),
            ({"en": "Ultra-Modern Cities & Tech", "ar": "المدن العصرية الحديثة والتقنية الفائقة"}, "modern"),
            ({"en": "Deep History, Ruins & Museums", "ar": "التاريخ العريق والآثار والمتاحف"}, "history"),
            ({"en": "Deep Seas, Beaches & Marine Life", "ar": "أعماق البحار، الشواطئ، والأنشطة البحرية"}, "sea")
        ],
        "why_en": "Vibe preferences guide whether we route you to tech hubs, pristine nature, or ancient ruins.",
        "why_ar": "تفضيلك للجو يحدد الوجهة المناسبة سواء كانت مدناً تقنية أو طبيعة أو آثاراً قديمة."
    }
]

# ==========================================
# 2. RULE SYSTEM (Forward Chaining Rules)
# ==========================================

RULES = [
    # --- LEVEL 1: Base Categories ---
    {
        "id": "Rule 1", "conditions": {"reason": "burnout", "duration": "weekend"},
        "conclusions": {"travel_category": "domestic_escape"},
        "explanation_en": "IF burnout AND weekend, THEN strict Domestic Escape."
    },
    {
        "id": "Rule 2", "conditions": {"phobia": "flying", "duration": "weekend"},
        "conclusions": {"travel_category": "domestic_escape"},
        "explanation_en": "IF fear of flying AND short duration, THEN Domestic Escape."
    },
    {
        "id": "Rule 3", "conditions": {"phobia": "flying", "duration": "medium"},
        "conclusions": {"travel_category": "ground_journey"},
        "explanation_en": "IF fear of flying AND medium duration, THEN Ground Journey."
    },
    {
        "id": "Rule 4", "conditions": {"phobia": "flying", "duration": "long"},
        "conclusions": {"travel_category": "ground_journey"},
        "explanation_en": "IF fear of flying AND long duration, THEN Ground Journey."
    },

    # International Budgets
    {
        "id": "Rule 5", "conditions": {"phobia": "none", "budget": "high"},
        "conclusions": {"travel_category": "int_premium"},
        "explanation_en": "IF high budget AND no flight fear, THEN International Premium."
    },
    {
        "id": "Rule 6", "conditions": {"phobia": "heights", "budget": "high"},
        "conclusions": {"travel_category": "int_premium"},
        "explanation_en": "IF high budget AND fear of heights (can fly), THEN International Premium."
    },
    {
        "id": "Rule 7", "conditions": {"phobia": "none", "budget": "medium"},
        "conclusions": {"travel_category": "int_standard"},
        "explanation_en": "IF medium budget AND no flight fear, THEN International Standard."
    },
    {
        "id": "Rule 8", "conditions": {"phobia": "heights", "budget": "medium"},
        "conclusions": {"travel_category": "int_standard"},
        "explanation_en": "IF medium budget AND fear of heights (can fly), THEN International Standard."
    },
    {
        "id": "Rule 9", "conditions": {"phobia": "none", "budget": "low"},
        "conclusions": {"travel_category": "int_budget"},
        "explanation_en": "IF low budget AND no flight fear, THEN International Budget."
    },
    {
        "id": "Rule 10", "conditions": {"phobia": "heights", "budget": "low"},
        "conclusions": {"travel_category": "int_budget"},
        "explanation_en": "IF low budget AND fear of heights (can fly), THEN International Budget."
    },

    # --- LEVEL 2: Destination Mappings ---
    {
        "id": "Rule 11", "conditions": {"travel_category": "domestic_escape"},
        "conclusions": {"recommendation": {"en": "Jeddah & Riyadh, Saudi Arabia", "ar": "جدة والرياض، المملكة العربية السعودية"},
                        "folder_key": "jeddah_ryiadh",
                        "warning": "Check local weekend traffic & event schedules.", "rating": "4.6/5"},
        "explanation_en": "IF Domestic Escape, THEN recommend major local hubs (Jeddah & Riyadh)."
    },
    {
        "id": "Rule 12", "conditions": {"travel_category": "ground_journey", "vibe": "nature"},
        "conclusions": {"recommendation": {"en": "Salalah, Oman", "ar": "صلالة، عُمان"},
                        "folder_key": "salalah",
                        "warning": "Service vehicle brakes for mountain passes.", "rating": "4.8/5"},
        "explanation_en": "IF Ground Journey AND Nature, THEN Salalah, Oman."
    },
    {
        "id": "Rule 13", "conditions": {"travel_category": "ground_journey", "vibe": "history"},
        "conclusions": {"recommendation": {"en": "Al-Ula, Saudi Arabia", "ar": "العُلا، المملكة العربية السعودية"},
                        "folder_key": "alula",
                        "warning": "Book heritage site slots well in advance.", "rating": "4.9/5"},
        "explanation_en": "IF Ground Journey AND History, THEN Al-Ula."
    },
    {
        "id": "Rule 14", "conditions": {"travel_category": "ground_journey", "vibe": "sea"},
        "conclusions": {"recommendation": {"en": "Red Sea Luxury Cruise", "ar": "رحلة سفينة كروز البحر الأحمر"},
                        "folder_key": "Cruise Ship",
                        "warning": "Verify seasonal sailing dates.", "rating": "4.7/5"},
        "explanation_en": "IF Ground Journey AND Sea, THEN Red Sea Cruise."
    },

    # International Premium
    {
        "id": "Rule 15", "conditions": {"travel_category": "int_premium", "vibe": "modern"},
        "conclusions": {"recommendation": {"en": "Tokyo, Japan", "ar": "طوكيو، اليابان"},
                        "folder_key": "tokyo",
                        "warning": "Expect high density in central transit hubs.", "rating": "4.9/5"},
        "explanation_en": "IF Premium AND Modern, THEN Tokyo."
    },
    {
        "id": "Rule 16", "conditions": {"travel_category": "int_premium", "vibe": "nature"},
        "conclusions": {"recommendation": {"en": "Swiss Alps, Switzerland", "ar": "جبال الألب، سويسرا"},
                        "folder_key": "Switzerland",
                        "warning": "Peak season accommodation costs are high.", "rating": "4.95/5"},
        "explanation_en": "IF Premium AND Nature, THEN Switzerland."
    },
    {
        "id": "Rule 17", "conditions": {"travel_category": "int_premium", "vibe": "sea"},
        "conclusions": {"recommendation": {"en": "Bora Bora & Maldives", "ar": "بورا بورا والمالديف"},
                        "folder_key": "bora_bora_maldives",
                        "warning": "High UV index; pack coral-safe sunscreen.", "rating": "5.0/5"},
        "explanation_en": "IF Premium AND Sea, THEN Bora Bora & Maldives."
    },
    {
        "id": "Rule 18", "conditions": {"travel_category": "int_premium", "vibe": "history"},
        "conclusions": {"recommendation": {"en": "Rome, Italy", "ar": "روما، إيطاليا"},
                        "folder_key": "rome",
                        "warning": "Watch for pickpockets near popular monuments.", "rating": "4.8/5"},
        "explanation_en": "IF Premium AND History, THEN Rome."
    },

    # International Standard
    {
        "id": "Rule 19", "conditions": {"travel_category": "int_standard", "vibe": "modern"},
        "conclusions": {"recommendation": {"en": "Kuala Lumpur, Malaysia", "ar": "كوالالمبور، ماليزيا"},
                        "folder_key": "kuala lampour",
                        "warning": "Monsoon downpours occur frequently in afternoons.", "rating": "4.6/5"},
        "explanation_en": "IF Standard AND Modern, THEN Kuala Lumpur."
    },
    {
        "id": "Rule 20", "conditions": {"travel_category": "int_standard", "vibe": "nature"},
        "conclusions": {"recommendation": {"en": "Phuket, Thailand", "ar": "بوكيت، تايلاند"},
                        "folder_key": "Phuket",
                        "warning": "High humidity; stay hydrated.", "rating": "4.7/5"},
        "explanation_en": "IF Standard AND Nature, THEN Phuket."
    },
    {
        "id": "Rule 21", "conditions": {"travel_category": "int_standard", "vibe": "history"},
        "conclusions": {"recommendation": {"en": "Istanbul, Turkey", "ar": "إسطنبول، تركيا"},
                        "folder_key": "instunbul",
                        "warning": "Confirm taxi meter usage in tourist areas.", "rating": "4.8/5"},
        "explanation_en": "IF Standard AND History, THEN Istanbul."
    },
    {
        "id": "Rule 22", "conditions": {"travel_category": "int_standard", "vibe": "sea"},
        "conclusions": {"recommendation": {"en": "Santorini, Greece", "ar": "سانتوريني، اليونان"},
                        "folder_key": "Santorini",
                        "warning": "Steep cobblestone staircases throughout island roads.", "rating": "4.8/5"},
        "explanation_en": "IF Standard AND Sea, THEN Santorini."
    },

    # International Budget
    {
        "id": "Rule 23", "conditions": {"travel_category": "int_budget", "vibe": "nature"},
        "conclusions": {"recommendation": {"en": "Tian Shan Mountains, Kyrgyzstan", "ar": "جبال تيان شان، قيرغيزستان"},
                        "folder_key": "Kyrgyzstan",
                        "warning": "Ensure cash reserves for rural yurt stays.", "rating": "4.7/5"},
        "explanation_en": "IF Budget AND Nature, THEN Kyrgyzstan."
    },
    {
        "id": "Rule 24", "conditions": {"travel_category": "int_budget", "vibe": "history"},
        "conclusions": {"recommendation": {"en": "Cairo & Luxor, Egypt", "ar": "القاهرة والأقصر، مصر"},
                        "folder_key": "cairo",
                        "warning": "Negotiate guide & camel tour rates beforehand.", "rating": "4.6/5"},
        "explanation_en": "IF Budget AND History, THEN Cairo & Luxor."
    },
    {
        "id": "Rule 25", "conditions": {"travel_category": "int_budget", "vibe": "modern"},
        "conclusions": {"recommendation": {"en": "Ho Chi Minh City, Vietnam", "ar": "مدينة هو تشي منه، فيتنام"},
                        "folder_key": "vietnam",
                        "warning": "Exercise caution when crossing scooter-dense roads.", "rating": "4.5/5"},
        "explanation_en": "IF Budget AND Modern, THEN Vietnam."
    },
    {
        "id": "Rule 26", "conditions": {"travel_category": "int_budget", "vibe": "sea"},
        "conclusions": {"recommendation": {"en": "Palawan, Philippines", "ar": "بالوان، الفلبين"},
                        "folder_key": "palawan",
                        "warning": "Check seasonal typhoon warnings.", "rating": "4.8/5"},
        "explanation_en": "IF Budget AND Sea, THEN Palawan."
    },

    # --- LEVEL 3: Sub-Branch Multi-Step Rules for Germany, California, Nepal & Indonesia ---
    # Medical Branch (Requires reason + medical_type + medical_duration)
    {
        "id": "Rule 27-A", "conditions": {"reason": "medical", "medical_type": "clinical"},
        "conclusions": {"recommendation": {"en": "Heidelberg & Munich Medical Hubs, Germany", "ar": "مراكز هيدلبرغ وميونيخ الطبية، ألمانيا"},
                        "folder_key": "germany_health",
                        "warning": "Requires medical visa invitation letter from clinic.", "rating": "4.95/5"},
        "explanation_en": "IF reason is Medical AND clinical hospital focus, THEN recommend Heidelberg & Munich, Germany."
    },
    {
        "id": "Rule 27-B", "conditions": {"reason": "medical", "medical_type": "spa"},
        "conclusions": {"recommendation": {"en": "Calistoga Thermal Springs & Spa, California, USA", "ar": "منتجعات كالستوغا الدافئة، كاليفورنيا، الولايات المتحدة الأمريكية"},
                        "folder_key": "thermal",
                        "warning": "Advance reservation needed for thermal hydrotherapy mineral baths.", "rating": "4.9/5"},
        "explanation_en": "IF reason is Medical AND thermal springs focus, THEN recommend California, USA."
    },

    # Charity / Volunteer Branch (Requires reason + charity_type + charity_intensity)
    {
        "id": "Rule 28-A", "conditions": {"reason": "charity", "charity_type": "teaching"},
        "conclusions": {"recommendation": {"en": "Kathmandu Valley Community Teaching, Nepal", "ar": "التعليم التطوعي في وادي كاتماندو، نيبال"},
                        "folder_key": "nepal",
                        "warning": "Apply for volunteer clearance via local NGO partners.", "rating": "4.85/5"},
        "explanation_en": "IF reason is Charity AND community teaching, THEN recommend Kathmandu Valley, Nepal."
    },
    {
        "id": "Rule 28-B", "conditions": {"reason": "charity", "charity_type": "eco"},
        "conclusions": {"recommendation": {"en": "Bali & Rainforest Eco-Volunteer Program, Indonesia", "ar": "برنامج التطوع لحماية بيئة بالي والغابات المطيرة، إندونيسيا"},
                        "folder_key": "indonesia",
                        "warning": "Respect local island customs and environmental guidelines.", "rating": "4.9/5"},
        "explanation_en": "IF reason is Charity AND eco conservation, THEN recommend Bali, Indonesia."
    }
]

# ==========================================
# 3. INFERENCE ENGINE (Forward Chaining)
# ==========================================

class InferenceEngine:
    def __init__(self, rules=RULES, questions=QUESTIONS):
        self.rules = rules
        self.questions = questions

    def get_next_question_id(self, facts):
        """Intelligently branch and determine the next question based on current facts."""
        # First question: always ask 'reason' first
        if "reason" not in facts:
            return "reason"

        reason = facts.get("reason")
        
        # Medical Branch: Direct result after medical_type
        if reason == "medical":
            if "medical_type" not in facts:
                return "medical_type"
            return None
        
        # Charity Branch: Direct result after charity_type
        if reason == "charity":
            if "charity_type" not in facts:
                return "charity_type"
            return None

        # General Branch Questions
        if "duration" not in facts:
            return "duration"
            
        if facts.get("reason") == "burnout" and facts.get("duration") == "weekend":
            return None
            
        if "phobia" not in facts:
            return "phobia"
            
        if facts.get("phobia") == "flying":
            if facts.get("duration") == "weekend":
                return None
            if "vibe" not in facts:
                return "vibe"
            return None

        if "budget" not in facts:
            return "budget"
            
        if "vibe" not in facts:
            return "vibe"

        return None

    def forward_chain(self, facts):
        inferred_facts = facts.copy()
        rules_fired = []
        new_fact_added = True

        while new_fact_added:
            new_fact_added = False
            for rule in self.rules:
                if rule['id'] in [r['id'] for r in rules_fired]:
                    continue

                conditions_met = True
                for key, val in rule['conditions'].items():
                    if key not in inferred_facts or inferred_facts[key] != val:
                        conditions_met = False
                        break

                if conditions_met:
                    for k, v in rule['conclusions'].items():
                        if k == 'recommendation':
                            if k not in inferred_facts:
                                inferred_facts[k] = []
                            if not any(existing_v == v for existing_v in inferred_facts[k]):
                                inferred_facts[k].append(v)
                                new_fact_added = True
                        elif k in ['warning', 'rating', 'folder_key']:
                            inferred_facts[k] = v
                        else:
                            if k not in inferred_facts or inferred_facts[k] != v:
                                inferred_facts[k] = v
                                new_fact_added = True

                    rules_fired.append(rule)

        return inferred_facts, rules_fired

# Helper to scan image gallery files for a specific folder_key (handles both subdirectories and flat files)
FLAT_IMAGE_MAP = {
    "jeddah_ryiadh": ["jeddah.png", "ryiadh.png"],
    "salalah": ["salala.png"],
    "alula": ["alola.png"],
    "Cruise Ship": ["cruz_ship.png"],
    "tokyo": ["tokyo.png"],
    "Switzerland": ["Switzerland.png"],
    "bora_bora_maldives": ["bora_bora.png"],
    "rome": ["rome.png"],
    "kuala lampour": ["Kuala Lumpur.png"],
    "Phuket": ["Phuket.png"],
    "instunbul": ["intanbul.jpg"],
    "Santorini": ["Santorini.png"],
    "Kyrgyzstan": ["Kyrgyzstan.png"],
    "cairo": ["cairo.png"],
    "vietnam": ["Vietnam.png"],
    "palawan": ["Palawan.png"],
    "germany_health": ["germany.png"],
    "nepal": ["nepal.png"],
    "thermal": ["thermal_1.png", "thermal_2.png"],
    "indonesia": ["indonesia_1.png", "indonesia_2.png"]
}

def get_gallery_images_for_folder(folder_key, base_images_dir):
    """Scan static/images/<folder_key> for all image files (supports subdirs, flat files & multiple folders)."""
    if not folder_key or not os.path.exists(base_images_dir):
        return []

    if isinstance(folder_key, list):
        imgs = []
        for fk in folder_key:
            imgs.extend(get_gallery_images_for_folder(fk, base_images_dir))
        return list(dict.fromkeys(imgs))

    if ',' in folder_key:
        imgs = []
        for fk in folder_key.split(','):
            imgs.extend(get_gallery_images_for_folder(fk.strip(), base_images_dir))
        return list(dict.fromkeys(imgs))

    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
    image_paths = []

    # 1. Check for nested subdirectory
    target_dir = os.path.join(base_images_dir, folder_key)
    if not os.path.exists(target_dir):
        all_subdirs = [d for d in os.listdir(base_images_dir) if os.path.isdir(os.path.join(base_images_dir, d))]
        matched_dir = next((d for d in all_subdirs if d.lower() == folder_key.lower()), None)
        if matched_dir:
            target_dir = os.path.join(base_images_dir, matched_dir)

    if os.path.exists(target_dir) and os.path.isdir(target_dir):
        for root, _, files in os.walk(target_dir):
            for file in files:
                if file.lower().endswith(valid_extensions):
                    rel_path = os.path.relpath(os.path.join(root, file), base_images_dir).replace('\\', '/')
                    image_paths.append(rel_path)
        image_paths.sort()
        if image_paths:
            return image_paths

    # 2. Fallback: Check flat files in base_images_dir matching FLAT_IMAGE_MAP
    if folder_key in FLAT_IMAGE_MAP:
        for mapped_file in FLAT_IMAGE_MAP[folder_key]:
            full_p = os.path.join(base_images_dir, mapped_file)
            if os.path.exists(full_p):
                image_paths.append(mapped_file)
        if image_paths:
            return image_paths

    # 3. Fuzzy search flat files in base_images_dir
    key_tokens = [t.lower() for t in folder_key.replace('_', ' ').split()]
    all_files = [f for f in os.listdir(base_images_dir) if os.path.isfile(os.path.join(base_images_dir, f)) and f.lower().endswith(valid_extensions)]

    for f in all_files:
        f_lower = f.lower()
        if any(token in f_lower for token in key_tokens):
            image_paths.append(f)

    image_paths.sort()
    return image_paths

