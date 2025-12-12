"""Query generation module for Lead Generation Bot."""

# 🎯 RAGSPRO TARGET CITIES - WORLDWIDE HIGH-PAYING MARKETS
# 200+ cities across all major countries for maximum lead coverage
CITIES = [
    # 🇺🇸 USA - TIER 1 (Highest paying: $5000-$100000 projects)
    # Tech Hubs & Major Cities
    "San Francisco, USA", "San Jose, USA", "Palo Alto, USA", "Mountain View, USA",
    "Austin, USA", "Seattle, USA", "Bellevue, USA", "Redmond, USA",
    "New York, USA", "Manhattan, USA", "Brooklyn, USA", "Queens, USA",
    "Boston, USA", "Cambridge, USA", "Los Angeles, USA", "Santa Monica, USA",
    "Chicago, USA", "Miami, USA", "Fort Lauderdale, USA", "Orlando, USA",
    "Denver, USA", "Boulder, USA", "San Diego, USA", "Dallas, USA",
    "Houston, USA", "Atlanta, USA", "Phoenix, USA", "Scottsdale, USA",
    "Philadelphia, USA", "Washington DC, USA", "Portland, USA", "Nashville, USA",
    "Charlotte, USA", "Raleigh, USA", "Salt Lake City, USA", "Las Vegas, USA",
    "Minneapolis, USA", "Detroit, USA", "Tampa, USA", "Columbus, USA",
    "Indianapolis, USA", "Jacksonville, USA", "San Antonio, USA", "Sacramento, USA",
    
    # 🇬🇧 UK - TIER 1 (High paying: £3000-£50000 projects)
    "London, UK", "Westminster, UK", "City of London, UK", "Canary Wharf, UK",
    "Manchester, UK", "Birmingham, UK", "Edinburgh, UK", "Glasgow, UK",
    "Bristol, UK", "Leeds, UK", "Liverpool, UK", "Newcastle, UK",
    "Sheffield, UK", "Nottingham, UK", "Southampton, UK", "Brighton, UK",
    "Cambridge, UK", "Oxford, UK", "Cardiff, UK", "Belfast, UK",
    
    # 🇦🇪 UAE - TIER 1 (Very high paying: AED 20000-300000 projects)
    "Dubai, UAE", "Downtown Dubai, UAE", "Dubai Marina, UAE", "Business Bay, UAE",
    "Abu Dhabi, UAE", "Sharjah, UAE", "Ajman, UAE", "Ras Al Khaimah, UAE",
    "Fujairah, UAE", "Al Ain, UAE",
    
    # 🇨🇦 Canada - TIER 1 (High paying: CAD 5000-80000 projects)
    "Toronto, Canada", "Vancouver, Canada", "Montreal, Canada", "Calgary, Canada",
    "Ottawa, Canada", "Edmonton, Canada", "Mississauga, Canada", "Winnipeg, Canada",
    "Quebec City, Canada", "Hamilton, Canada", "Kitchener, Canada", "Victoria, Canada",
    
    # 🇦🇺 Australia - TIER 1 (High paying: AUD 5000-80000 projects)
    "Sydney, Australia", "Melbourne, Australia", "Brisbane, Australia", "Perth, Australia",
    "Adelaide, Australia", "Gold Coast, Australia", "Canberra, Australia", "Newcastle, Australia",
    "Wollongong, Australia", "Hobart, Australia",
    
    # 🇸🇬 Singapore - TIER 1 (Very high paying: SGD 5000-100000 projects)
    "Singapore", "Marina Bay, Singapore", "Orchard, Singapore", "Raffles Place, Singapore",
    
    # 🇫🇷 France - TIER 2 (Good paying: €3000-50000 projects)
    "Paris, France", "Lyon, France", "Marseille, France", "Toulouse, France",
    "Nice, France", "Nantes, France", "Strasbourg, France", "Bordeaux, France",
    "Lille, France", "Rennes, France", "Montpellier, France",
    
    # 🇩🇪 Germany - TIER 2 (Good paying: €3000-50000 projects)
    "Berlin, Germany", "Munich, Germany", "Frankfurt, Germany", "Hamburg, Germany",
    "Cologne, Germany", "Stuttgart, Germany", "Düsseldorf, Germany", "Dortmund, Germany",
    "Essen, Germany", "Leipzig, Germany", "Bremen, Germany", "Dresden, Germany",
    
    # 🇳🇱 Netherlands - TIER 2 (Good paying: €3000-50000 projects)
    "Amsterdam, Netherlands", "Rotterdam, Netherlands", "The Hague, Netherlands",
    "Utrecht, Netherlands", "Eindhoven, Netherlands", "Groningen, Netherlands",
    
    # 🇨🇭 Switzerland - TIER 1 (Very high paying: CHF 5000-100000 projects)
    "Zurich, Switzerland", "Geneva, Switzerland", "Basel, Switzerland", "Bern, Switzerland",
    "Lausanne, Switzerland", "Lucerne, Switzerland",
    
    # 🇸🇪 Sweden - TIER 2 (Good paying: SEK 30000-500000 projects)
    "Stockholm, Sweden", "Gothenburg, Sweden", "Malmö, Sweden", "Uppsala, Sweden",
    
    # 🇳🇴 Norway - TIER 2 (Good paying: NOK 40000-600000 projects)
    "Oslo, Norway", "Bergen, Norway", "Trondheim, Norway", "Stavanger, Norway",
    
    # 🇩🇰 Denmark - TIER 2 (Good paying: DKK 20000-400000 projects)
    "Copenhagen, Denmark", "Aarhus, Denmark", "Odense, Denmark", "Aalborg, Denmark",
    
    # 🇮🇪 Ireland - TIER 2 (Good paying: €3000-50000 projects)
    "Dublin, Ireland", "Cork, Ireland", "Galway, Ireland", "Limerick, Ireland",
    
    # 🇧🇪 Belgium - TIER 2 (Good paying: €3000-40000 projects)
    "Brussels, Belgium", "Antwerp, Belgium", "Ghent, Belgium", "Bruges, Belgium",
    
    # 🇦🇹 Austria - TIER 2 (Good paying: €3000-40000 projects)
    "Vienna, Austria", "Salzburg, Austria", "Innsbruck, Austria", "Graz, Austria",
    
    # 🇪🇸 Spain - TIER 2 (Medium paying: €2000-30000 projects)
    "Madrid, Spain", "Barcelona, Spain", "Valencia, Spain", "Seville, Spain",
    "Bilbao, Spain", "Málaga, Spain", "Zaragoza, Spain",
    
    # 🇮🇹 Italy - TIER 2 (Medium paying: €2000-30000 projects)
    "Rome, Italy", "Milan, Italy", "Naples, Italy", "Turin, Italy",
    "Florence, Italy", "Venice, Italy", "Bologna, Italy",
    
    # 🇵🇹 Portugal - TIER 2 (Medium paying: €2000-25000 projects)
    "Lisbon, Portugal", "Porto, Portugal", "Faro, Portugal", "Braga, Portugal",
    
    # 🇸🇦 Saudi Arabia - TIER 2 (High paying: SAR 20000-200000 projects)
    "Riyadh, Saudi Arabia", "Jeddah, Saudi Arabia", "Dammam, Saudi Arabia",
    "Mecca, Saudi Arabia", "Medina, Saudi Arabia", "Khobar, Saudi Arabia",
    
    # 🇶🇦 Qatar - TIER 2 (High paying: QAR 20000-200000 projects)
    "Doha, Qatar", "Al Wakrah, Qatar", "Al Rayyan, Qatar",
    
    # 🇰🇼 Kuwait - TIER 2 (Good paying: KWD 1000-15000 projects)
    "Kuwait City, Kuwait", "Hawalli, Kuwait", "Salmiya, Kuwait",
    
    # 🇴🇲 Oman - TIER 2 (Good paying: OMR 2000-25000 projects)
    "Muscat, Oman", "Salalah, Oman", "Sohar, Oman",
    
    # 🇧🇭 Bahrain - TIER 2 (Good paying: BHD 2000-25000 projects)
    "Manama, Bahrain", "Riffa, Bahrain", "Muharraq, Bahrain",
    
    # 🇭🇰 Hong Kong - TIER 1 (High paying: HKD 40000-600000 projects)
    "Hong Kong", "Central, Hong Kong", "Kowloon, Hong Kong", "Tsim Sha Tsui, Hong Kong",
    
    # 🇯🇵 Japan - TIER 2 (Good paying: ¥500000-5000000 projects)
    "Tokyo, Japan", "Osaka, Japan", "Kyoto, Japan", "Yokohama, Japan",
    "Nagoya, Japan", "Sapporo, Japan", "Fukuoka, Japan",
    
    # 🇰🇷 South Korea - TIER 2 (Good paying: ₩5000000-50000000 projects)
    "Seoul, South Korea", "Busan, South Korea", "Incheon, South Korea",
    "Daegu, South Korea", "Daejeon, South Korea",
    
    # 🇳🇿 New Zealand - TIER 2 (Good paying: NZD 5000-60000 projects)
    "Auckland, New Zealand", "Wellington, New Zealand", "Christchurch, New Zealand",
    "Hamilton, New Zealand", "Dunedin, New Zealand",
    
    # 🇿🇦 South Africa - TIER 3 (Medium paying: ZAR 50000-500000 projects)
    "Johannesburg, South Africa", "Cape Town, South Africa", "Durban, South Africa",
    "Pretoria, South Africa", "Port Elizabeth, South Africa",
    
    # 🇮🇳 India - TIER 3 (High volume: ₹50000-₹1000000 projects)
    # Major Metro Cities
    "Delhi, India", "New Delhi, India", "Gurgaon, India", "Noida, India", "Faridabad, India",
    "Mumbai, India", "Navi Mumbai, India", "Thane, India", "Pune, India",
    "Bangalore, India", "Bengaluru, India", "Hyderabad, India", "Chennai, India",
    "Kolkata, India", "Ahmedabad, India", "Surat, India", "Jaipur, India",
    "Lucknow, India", "Kanpur, India", "Nagpur, India", "Indore, India",
    "Bhopal, India", "Visakhapatnam, India", "Patna, India", "Vadodara, India",
    "Ludhiana, India", "Agra, India", "Nashik, India", "Chandigarh, India",
    "Coimbatore, India", "Kochi, India", "Thiruvananthapuram, India", "Mysore, India",
]

# 🎯 RAGSPRO TARGET CATEGORIES - ALL HIGH-PAYING BUSINESSES
# 150+ categories covering every profitable business type
CATEGORIES = [
    # 💻 TECH & SOFTWARE (HIGHEST: $10k-$200k+ projects)
    "SaaS company", "tech startup", "software company", "software development",
    "fintech company", "fintech startup", "AI company", "machine learning company",
    "blockchain company", "cryptocurrency company", "cybersecurity company",
    "cloud computing company", "data analytics company", "big data company",
    "e-commerce platform", "marketplace platform", "mobile app development",
    "web development agency", "IT consulting", "technology consulting",
    
    # 💰 FINANCE & INVESTMENT (HIGHEST: $15k-$300k+ projects)
    "investment firm", "investment bank", "hedge fund", "private equity firm",
    "venture capital", "wealth management", "asset management", "portfolio management",
    "financial advisor", "financial planner", "cryptocurrency exchange",
    "forex trading", "stock brokerage", "insurance company", "reinsurance company",
    "pension fund", "mutual fund", "family office", "trust company",
    
    # ⚖️ PROFESSIONAL SERVICES (HIGH: $8k-$150k projects)
    "law firm", "corporate law firm", "international law firm", "legal services",
    "accounting firm", "audit firm", "tax consulting", "tax advisory",
    "management consulting", "business consulting", "strategy consulting",
    "HR consulting", "recruitment agency", "executive search", "headhunting",
    "business advisory", "corporate advisory", "M&A advisory",
    
    # 🏢 REAL ESTATE (HIGH: $10k-$200k projects)
    "real estate agency", "luxury real estate", "commercial real estate",
    "property management", "real estate developer", "real estate investment",
    "property developer", "construction company", "real estate broker",
    "property consultant", "real estate marketing", "property portal",
    
    # 🏥 HEALTHCARE & MEDICAL (HIGH: $7k-$100k projects)
    "cosmetic surgery", "plastic surgery", "cosmetic surgeon", "plastic surgeon",
    "dental clinic", "dental implant", "cosmetic dentist", "orthodontist",
    "medical clinic", "multi-specialty hospital", "specialty clinic",
    "fertility clinic", "IVF clinic", "dermatology clinic", "skin clinic",
    "eye clinic", "laser eye surgery", "veterinary clinic", "pet hospital",
    "mental health clinic", "psychiatry clinic", "physiotherapy clinic",
    "chiropractic clinic", "wellness clinic", "diagnostic center",
    
    # 🛍️ E-COMMERCE & RETAIL (GOOD: $5k-$80k projects)
    "luxury boutique", "fashion boutique", "designer boutique",
    "jewelry store", "diamond jewelry", "luxury jewelry", "watch store",
    "luxury watch", "fashion brand", "clothing brand", "online store",
    "e-commerce store", "electronics store", "furniture store",
    "luxury furniture", "home decor store", "luxury goods", "premium retail",
    
    # 🏨 HOSPITALITY & TRAVEL (GOOD: $6k-$100k projects)
    "luxury hotel", "5-star hotel", "boutique hotel", "resort", "luxury resort",
    "spa resort", "beach resort", "travel agency", "luxury travel",
    "tour operator", "destination management", "event venue", "banquet hall",
    "wedding venue", "conference center", "hotel chain", "hospitality group",
    
    # 🍽️ FOOD & BEVERAGE (MEDIUM-HIGH: $4k-$60k projects)
    "fine dining restaurant", "luxury restaurant", "restaurant chain",
    "cafe chain", "coffee shop chain", "bakery chain", "catering company",
    "cloud kitchen", "ghost kitchen", "food delivery", "restaurant group",
    "bar", "nightclub", "lounge", "brewery", "winery", "distillery",
    
    # 💪 FITNESS & WELLNESS (GOOD: $5k-$80k projects)
    "luxury spa", "day spa", "wellness center", "wellness resort",
    "fitness center", "gym chain", "fitness chain", "yoga studio",
    "pilates studio", "meditation center", "health club", "sports club",
    "personal training", "nutrition consulting", "weight loss clinic",
    
    # 🎓 EDUCATION & TRAINING (GOOD: $5k-$80k projects)
    "online education", "e-learning platform", "coaching institute",
    "test prep", "language school", "business school", "MBA program",
    "executive education", "professional training", "certification courses",
    "skill development", "corporate training", "university", "college",
    
    # 📢 MARKETING & MEDIA (HIGH: $8k-$150k projects)
    "marketing agency", "digital marketing agency", "advertising agency",
    "creative agency", "branding agency", "PR agency", "public relations",
    "media agency", "social media agency", "content marketing",
    "SEO agency", "performance marketing", "growth marketing",
    "video production", "film production", "media production",
    
    # 🏭 MANUFACTURING & B2B (HIGH: $10k-$200k projects)
    "manufacturing company", "industrial manufacturing", "factory",
    "industrial equipment", "machinery manufacturer", "B2B software",
    "enterprise software", "wholesale distributor", "import export",
    "trading company", "supply chain", "logistics company",
    "freight forwarding", "shipping company", "warehouse",
    
    # 🏗️ CONSTRUCTION & INFRASTRUCTURE (HIGH: $10k-$200k projects)
    "construction company", "building contractor", "general contractor",
    "civil engineering", "infrastructure company", "real estate construction",
    "commercial construction", "residential construction", "renovation company",
    "interior contractor", "MEP contractor", "project management",
    
    # 🎨 DESIGN & CREATIVE (GOOD: $5k-$80k projects)
    "interior design", "architecture firm", "landscape architecture",
    "graphic design agency", "UI/UX design", "product design",
    "industrial design", "fashion design", "jewelry design",
    
    # 🚗 AUTOMOTIVE (GOOD: $6k-$100k projects)
    "luxury car dealership", "car dealership", "auto dealer",
    "car showroom", "motorcycle dealer", "auto repair", "car service",
    "auto parts", "car accessories", "car rental", "luxury car rental",
    
    # ⚡ ENERGY & UTILITIES (HIGH: $10k-$150k projects)
    "solar energy", "solar company", "renewable energy", "wind energy",
    "energy consulting", "power company", "utility company",
    "oil and gas", "petroleum company", "energy trading",
    
    # 🏠 HOME SERVICES (MEDIUM-HIGH: $4k-$60k projects)
    "HVAC contractor", "air conditioning", "heating contractor",
    "roofing company", "plumbing company", "electrical contractor",
    "home automation", "smart home", "security systems",
    "cleaning services", "pest control", "landscaping",
    "pool maintenance", "home renovation", "kitchen remodeling",
    
    # 💎 LUXURY & PREMIUM (HIGH: $8k-$150k projects)
    "luxury brand", "premium brand", "high-end retail",
    "luxury services", "concierge services", "VIP services",
    "yacht charter", "private jet", "luxury lifestyle",
    "art gallery", "auction house", "antique dealer",
    
    # 🎯 SPECIALIZED SERVICES (GOOD: $5k-$80k projects)
    "event management", "wedding planner", "party planner",
    "photography studio", "video studio", "recording studio",
    "printing services", "packaging company", "label printing",
    "translation services", "interpretation services",
    "security services", "private security", "investigation services",
]


def generate_queries() -> list[str]:
    """
    Generate all city × category query combinations.
    
    Returns:
        List of search query strings in format "{category} in {city}"
    """
    queries = []
    for city in CITIES:
        for category in CATEGORIES:
            query = f"{category} in {city}"
            queries.append(query)
    return queries
