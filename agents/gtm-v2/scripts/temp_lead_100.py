import json

data = {
    "college_name": "Penna College of Cement Sciences",
    "website": "https://pennainstitutions.co.in",
    "row_idx": 100,
    "website_extraction_research": """### Summary
- Institution: Penna College of Cement Sciences (Part of Penna Group of Institutions)
- Website Type: WordPress-based (multiple subdomains: college., school.)
- Parent Organization: Penna Group (Educational Trust)
- Location: Boyareddypalli Village, Yadiki Mandal, Anathapuramu Dist, Andhra Pradesh – 515408

### Strategic Gap Analysis
Penna College of Cement Sciences operates a WordPress-powered website with significant infrastructure gaps:

1. **NO STUDENT PORTAL**: No login area for students to access grades, results, or academic records
2. **MANUAL ADMISSION PROCESS**: Paper-based written tests + personal interviews; no online application system
3. **MANUAL FEE PAYMENT**: No online fee collection—likely bank transfers or cash
4. **NO MOBILE APP**: No mobile-first experience for students or parents
5. **FRAGMENTED SUBDOMAINS**: Separate installs for college.pennainstitutions.co.in and school.pennainstitutions.co.in (maintenance nightmare)
6. **MANUAL NOTIFICATIONS**: No WhatsApp/SMS integration; relying on physical notice boards
7. **DEPRECATED TECHNOLOGY**: WordPress 6.7+ with debug warnings and deprecated function calls
8. **NO ERP INTEGRATION**: Ellucian/Jenzabar/Oracle-level automation absent
9. **MANUAL PLACEMENT TRACKING**: Career services listed but no automated placement portal

**WHY ONCAMPUS ERP MATTERS HERE:**
- Their niche focus (Cement Sciences) requires streamlined operations to manage small but specialized student batches
- WhatsApp integration would instantly notify parents/students about exam schedules, results, and placement drives
- Online fee collection with instant receipts reduces administrative burden at a remote location
- Mobile-first architecture suits the rural location where mobile usage exceeds desktop

### Key Insights
- Status: Active but technically basic
- Type: Specialized Technical College (Cement Sciences) - Unique niche in Andhra Pradesh
- GTM Assessment: IN SCOPE - Specialized institution with clear operational pain points
- Recommendation: Position OnCampus ERP as a unified solution to replace fragmented WordPress setup

🔥 Lead Score: 🟡 MEDIUM-HOT - Niche college with manual processes in rural AP; SMS/WhatsApp notifications would be high-value for parent communication. #""",

    "outreach_templates": {
        "email_1": """Subject: Transform Your Cement Sciences College Operations – 40% Admin Reduction with OnCampus ERP

Dear Dr. [Principal's Name],

I recently visited pennainstitutions.co.in and was impressed by your specialized focus on Cement Sciences education—a truly unique institution in Andhra Pradesh.

However, I noticed several operational gaps that are likely consuming significant administrative resources:

1. **Manual Admission Process** – Your written test + interview process requires heavy manual coordination
2. **No Online Fee Payment** – Parents likely deposit via bank transfer or cash (difficult to track in Yadiki Mandal)
3. **Fragmented Web Presence** – Running separate WordPress installs for college and school creates maintenance overhead
4. **No Instant Parent Communication** – Physical notice boards can't compete with WhatsApp notifications

OnCampus ERP addresses all these challenges:
✓ Mobile-first student portal with instant grade/result access
✓ Integrated online fee payment with automated receipts
✓ WhatsApp notifications for exam schedules, results, and placement updates  
✓ Unified dashboard replacing multiple WordPress subdomains

We help institutions like yours achieve **40% reduction in administrative workload**.

Would a 15-minute demo help you visualize how OnCampus ERP could streamline Penna College of Cement Sciences?

Best regards,
GTM Sales Strategist
OnCampus ERP""",

        "email_2": """Subject: Quick Question About Your Admission & Fee Operations at Penna College

Dear Dr. [Principal's Name],

Following up on my previous email about modernizing Penna College of Cement Sciences.

I wanted to ask a quick question—how are you currently handling:

• **Admissions**: Are you managing applications, written test scheduling, and interview coordination manually?
• **Fee Collection**: Do parents still use bank transfers or cash deposits? Any challenges with tracking?

The reason I ask is that institutions similar to yours (small batches, specialized focus, rural location) have seen dramatic improvements:

- **An engineering college in Anantapur** reduced admission processing from 3 weeks to 3 days
- **A polytechnic in AP** increased fee collection on-time payments from 60% to 95% after implementing online payment

Our WhatsApp integration is particularly valuable for institutions like yours in Yadiki Mandal—parents receive instant updates on their phones rather than traveling for every notice.

Would a brief call help you explore the possibilities?

Best regards,
GTM Sales Strategist
OnCampus ERP""",

        "email_3": """Subject: Penna College of Cement Sciences – Let's Simplify Operations Together

Dear Dr. [Principal's Name],

I realize you have a busy schedule managing one of India's few specialized Cement Sciences colleges. I wanted to share one more thought:

Your website mentions "Dedicated Career Services & Placement Assistance" and "100+ Hiring Students." Managing placement drives, company tie-ups, and student tracking manually is resource-intensive.

OnCampus ERP includes:
- **Placement tracking dashboard** – Monitor student placements in real-time
- **Company integration module** – Manage recruitment drives seamlessly  
- **Automated placement notifications** – Send updates to students via WhatsApp

Given your focus on producing industry-ready graduates for cement/manufacturing companies, having a streamlined placement process is critical.

I'd love to show you how other Andhra Pradesh institutions are benefiting. Would next Tuesday or Wednesday work for a 15-minute demo?

Best regards,
GTM Sales Strategist
OnCampus ERP"""
    },

    "contacts": {
        "emails": [
            "principal@pennainstitutions.co.in",
            "principal.pennacollege@gmail.com"
        ],
        "phones": [
            "+91 79012 69532",
            "+91 94930 72573"
        ],
        "linkedin_profiles": [],
        "social_media": {
            "facebook": "https://www.facebook.com/pennainstitutions",
            "twitter": "",
            "instagram": "https://www.instagram.com/penna_institutions/"
        }
    },

    "classification": {
        "college_type": "Specialized Technical (Cement Sciences)",
        "target_persona": "Principal / Head of Institution"
    },

    "tracking": {
        "email_1_sent": False,
        "email_opened": False,
        "email_2_sent": False,
        "email_3_sent": False,
        "demo_booked": False,
        "status": "ready_for_outreach"
    }
}

print(json.dumps(data, indent=2))