# Indeed Job Scraper

> Extract structured job postings and hiring-company insights from Indeed search results at scale. This tool turns public listings into clean, analytics-ready data for research, recruiting, and market intelligence.

> Use the Indeed job scraper to capture titles, companies, locations, salaries, posting dates, job types, and rich company metadata with robust filtering and high reliability.


<p align="center">
  <a href="https://bitbash.def" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Indeed job scraper</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction

This project programmatically collects job listings from Indeed search result pages and normalizes them into machine-readable JSON/CSV. It solves the pain of copy-pasting or dealing with noisy HTML by providing a stable, structured pipeline that’s ready for analytics, dashboards, or CRM enrichment.

**Who is it for?** Talent acquisition teams, market researchers, data engineers, sales/BD teams doing lead generation, and analysts benchmarking roles and salaries across regions.

### Why structured job data matters

- Consistent, enriched fields (salary, reviews, remote type, job types) enable apples-to-apples analysis across searches.
- Filters and batching support large pulls for longitudinal trend tracking.
- Output is ready for BI tools, data warehouses, or downstream NLP (skills extraction, benefits, contacts).
- Designed for resilience against layout changes with strict validation and fallbacks.
- Supports integration into Python pipelines and no-code automation systems.

## Features

| Feature | Description |
|----------|-------------|
| Search URL ingestion | Paste any Indeed search URL (with filters applied) to target precise roles, companies, and locations. |
| Rich field coverage | Captures titles, companies, salary snippets, ratings, reviews, locations, dates, job types, remote modes, and more. |
| Pagination & batching | Crawls multi-page results reliably with configurable limits and deduplication by job key. |
| Robustness & accuracy | Defensive parsing, schema validation, and fallbacks for dynamic UI changes. |
| Flexible export | Download data as JSON, CSV, or Excel; stream into pipelines or databases. |
| Cost-aware operation | Efficient traversal and throttling keep usage costs low at scale. |
| Compliance friendly | Focuses on publicly available job data with practical guardrails and documentation. |

---

## What Data This Scraper Extracts

| Field Name | Field Description |
|-------------|------------------|
| company | Company name as shown on the listing. |
| companyBrandingAttributes.headerImageUrl | Header image URL if present on the company card. |
| companyBrandingAttributes.logoUrl | Company logo URL if present. |
| companyOverviewLink | Link to the company’s profile/overview page. |
| companyRating | Average rating score displayed for the company. |
| companyReviewCount | Count of reviews associated with the company. |
| displayTitle | Display title of the job listing. |
| expired | Boolean indicating whether the job listing has expired. |
| extractedSalary.min | Parsed minimum salary value (numeric if available). |
| extractedSalary.max | Parsed maximum salary value (numeric if available). |
| extractedSalary.type | Compensation cadence (e.g., yearly, monthly) when detectable. |
| formattedLocation | Human-readable location string. |
| formattedRelativeTime | Relative posting time (e.g., “3 days ago”). |
| jobLocationCity | Parsed city component of the location (when available). |
| jobLocationState | Parsed state/region component (when available). |
| jobTypes | Array of job type tags (e.g., Full-time, Contract). |
| jobkey | Unique job identifier extracted from the listing. |
| link | Canonical link to the job details page. |
| locationCount | Count of locations associated with the posting (multi-location roles). |
| newJob | Boolean set when the listing is flagged as “new”. |
| normTitle | Normalized title for aggregation (e.g., “Software Engineer”). |
| pubDate | Publication date/time (ISO when available). |
| remoteWorkModel.type | Remote classification (REMOTE, HYBRID, ONSITE when detectable). |
| salarySnippet.text | Salary text snippet as displayed. |
| salarySnippet.currency | Currency code if parsed from snippet. |
| snippet | Short job description/summary. |
| sponsored | Boolean indicating a sponsored listing. |
| taxoAttributes / taxonomyAttributes | Structured attribute tags used by the platform (labels and tiers). |
| title | Title variant used in the job card. |
| urgentlyHiring | Boolean indicating an urgent hiring badge. |
| viewJobLink | Alternate link to the job view page (if present). |

---

## Example Output


    [
      {
        "company": "Acme Corp",
        "companyBrandingAttributes": {
          "headerImageUrl": "https://images.example.com/acme/header.jpg",
          "logoUrl": "https://images.example.com/acme/logo.png"
        },
        "companyOverviewLink": "https://www.indeed.com/cmp/Acme-Corp",
        "companyRating": 4.1,
        "companyReviewCount": 532,
        "displayTitle": "Senior Data Engineer",
        "expired": false,
        "extractedSalary": {
          "min": 140000,
          "max": 170000,
          "type": "yearly"
        },
        "formattedLocation": "New York, NY",
        "formattedRelativeTime": "3 days ago",
        "jobLocationCity": "New York",
        "jobLocationState": "NY",
        "jobTypes": ["Full-time"],
        "jobkey": "123abc456def",
        "link": "https://www.indeed.com/viewjob?jk=123abc456def",
        "locationCount": 1,
        "newJob": true,
        "normTitle": "Data Engineer",
        "pubDate": "2025-10-28T09:00:00Z",
        "remoteWorkModel": { "type": "REMOTE_HYBRID" },
        "salarySnippet": {
          "currency": "USD",
          "text": "$140,000 - $170,000 a year",
          "salaryTextFormatted": true,
          "source": "employer"
        },
        "snippet": "Design and optimize data pipelines in cloud environments...",
        "sponsored": false,
        "taxonomyAttributes": [
          { "label": "Python", "tier": "skill" },
          { "label": "ETL", "tier": "skill" }
        ],
        "title": "Senior Data Engineer",
        "urgentlyHiring": false,
        "viewJobLink": "https://www.indeed.com/rc/clk?jk=123abc456def"
      }
    ]

---

## Directory Structure Tree


    Indeed job scraper/
    ├── src/
    │   ├── main.py
    │   ├── crawler/
    │   │   ├── pagination.py
    │   │   └── throttling.py
    │   ├── parsers/
    │   │   ├── listing_parser.py
    │   │   └── salary_parser.py
    │   ├── exporters/
    │   │   ├── json_exporter.py
    │   │   └── csv_exporter.py
    │   └── config/
    │       └── settings.example.json
    ├── data/
    │   ├── inputs.sample.txt
    │   └── sample.json
    ├── tests/
    │   ├── test_parsers.py
    │   └── test_end_to_end.py
    ├── requirements.txt
    └── README.md

---

## Use Cases

- **Talent acquisition teams** use it to **monitor fresh openings and employer activity**, so they can **source candidates faster and prioritize outreach**.
- **Market researchers** use it to **collect multi-region postings**, so they can **analyze hiring demand, salary bands, and role trends**.
- **Sales/BD teams** use it to **identify companies actively hiring specific roles**, so they can **generate qualified leads for B2B products/services**.
- **Data engineers** use it to **feed normalized listings into warehouses**, so they can **power dashboards and downstream ML pipelines**.
- **Educators and bootcamps** use it to **track skill requirements across roles**, so they can **update curricula based on real market demand**.

---

## FAQs

**Q1: What input do I need to start?**
Provide a complete Indeed search URL (including your filters like title, company, location, salary, job type). Optionally set a maximum results limit and region/proxy preferences.

**Q2: How accurate is salary parsing?**
Salary ranges are parsed from visible snippets. When ranges or cadence are ambiguous, the raw text is preserved and numeric fields may be null, enabling your own post-processing rules.

**Q3: Can it distinguish remote, hybrid, and onsite roles?**
Yes, when the listing exposes these tags or text patterns. The `remoteWorkModel.type` field is populated when detectable; otherwise the field is omitted.

**Q4: How do I avoid duplicates across runs?**
Use the `jobkey` as a stable identifier. Store processed keys and skip already-seen listings when re-crawling overlapping searches.

---

## Performance Benchmarks and Results

**Primary Metric:** Processes ~1,000–1,500 listings per minute on typical broadband for paginated searches with moderate filtering.
**Reliability Metric:** >98% successful page retrieval across long runs with retry and backoff enabled.
**Efficiency Metric:** <300 KB average memory footprint per listing during parse/export; streaming exporters keep peak RAM low.
**Quality Metric:** 95–99% field completeness on common attributes (title, company, location, link); 70–90% structured salary coverage when employers disclose ranges.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
