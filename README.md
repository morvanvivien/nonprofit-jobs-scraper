# How to Scrape Nonprofit and Charity Job Boards (CharityJob, Idealist, Pro Bono Australia, HacesFalta)

> **Run it now, no code: [nonprofit-jobs-scraper on the Apify Store](https://apify.com/bibian/nonprofit-jobs-scraper)** &nbsp;|&nbsp; $3.00 per 1,000 job postings &nbsp;|&nbsp; no browser, no proxy, no login

Nonprofit and charity jobs are scattered across small, sector-specific boards with no shared format and no public API: CharityJob (United Kingdom), Idealist (United States), Pro Bono Australia and HacesFalta (Spain). This guide shows how to pull postings from all four in a single run, in one unified schema, with a free Apify Actor, from the console or from code.

Searches this page answers: nonprofit jobs scraper, charity jobs scraper, charityjob scraper, idealist scraper, pro bono australia scraper, hacesfalta scraper.

## What you get

- Every job posting from CharityJob, Idealist, Pro Bono Australia and HacesFalta, in one unified schema: title, company, location, remote policy, employment type, salary range and dates.
- Deduplicated across sources and across runs (`onlyNew`), with country, source host and native id kept on every row.
- Optional full description as plain text. No personal data (recruiter contact details) is ever exported.

Export the dataset as JSON, CSV or Excel, or read it through the Apify API. A real sample (five results, already public, no personal data) is in [`sample-output.json`](sample-output.json).

## Output fields

| Field | Type | Meaning |
|---|---|---|
| `id`, `url` | string | Stable identifier (`<source>:<native id>`) and public link |
| `title`, `companyName` | string | Job title and employer as displayed |
| `companyUrl` | string or null | Company page on the source site, when it exists |
| `locationLabel`, `city`, `region`, `postalCode`, `country` | string or null | Where the job is based |
| `remote` | string | `remote`, `hybrid`, `onsite` or `unknown` |
| `employmentType` | string | `full_time`, `part_time`, `contract`, `freelance`, `internship`, `apprenticeship`, `temporary` or `unknown` |
| `salaryMin`, `salaryMax`, `salaryCurrency`, `salaryPeriod` | number or null | Salary range, as numbers, in the site's own currency |
| `datePosted`, `validThrough` | string or null | ISO dates |
| `description` | string or null | Plain text, only when `includeDescriptions` is on. No personal data. |
| `experienceLevel`, `industry` | string or null | As named by the site |
| `skills` | string[] | Skills listed by the site, if any |
| `source`, `sourceId`, `scrapedAt` | string | Host name of the source site, its native id, extraction timestamp |
| `opportunityType` | string (HacesFalta only) | `paid` or `volunteer` — HacesFalta lists both paid nonprofit jobs and unpaid volunteering |

## Use cases

- **Watch four niche boards from one place.** No need to check CharityJob, Idealist, Pro Bono Australia and HacesFalta separately: one schema, one schedule.
- **Build a daily alert for a role or a region.** Schedule a run every morning with `publishedWithinDays: 1` and `onlyNew: true`, then send only the new postings to Slack, e-mail or a spreadsheet.
- **Track hiring in the nonprofit sector.** Group postings by `country`, `employmentType` or `industry` to see where charities and NGOs are recruiting right now.
- **Feed a niche job board or newsletter** for the nonprofit and social sector with structured, deduplicated data and the canonical `url` back to the original posting.

## Input

| Field | What it does |
|---|---|
| `keywords` | Job title or cause area, for example `fundraising` or `case manager`. Empty means every posting. |
| `location` | City or region, for example `London` or `Sydney`. Empty means all locations. |
| `countries` | Which countries to cover: `GB` (CharityJob), `US` (Idealist), `AU` (Pro Bono Australia), `ES` (HacesFalta). Defaults to all 4. |
| `sources` | Which of the four job boards to query in this run. Defaults to all 4. |
| `publishedWithinDays` | Keep only postings published in the last N days. Use `1` for a daily monitoring run. |
| `remote` | Keep only postings with this remote policy: `any`, `remote`, `hybrid` or `onsite`. |
| `maxItems` | The run stops once this many postings are saved, across all sources combined (default 50). |
| `includeDescriptions` | Add the job description as plain text (default on). |
| `onlyNew` | For scheduled runs: skip postings an earlier run of this same search already delivered. |

Example input:

```json
{
  "keywords": "fundraising",
  "countries": ["GB", "US", "AU", "ES"],
  "maxItems": 50,
  "includeDescriptions": false
}
```

## Four ways to use it

### 1. Apify console, no code

1. Open [the Actor page](https://apify.com/bibian/nonprofit-jobs-scraper) and click **Try for free** (a free Apify account is enough).
2. Fill in the input form (keywords, countries and the maximum number of results) and click **Start**.
3. When the run finishes, open the **Output** tab, check the table, then **Export** as CSV, Excel or JSON.
4. For a daily alert, open **Schedules**, create a daily schedule for the Actor, turn `onlyNew` on, and optionally add an integration that sends new results to Slack, e-mail or Google Sheets.

### 2. Apify API with JavaScript

```bash
npm install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
node examples/run.js
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('bibian/nonprofit-jobs-scraper').call({
    "keywords": "fundraising",
    "countries": ["GB", "US", "AU", "ES"],
    "maxItems": 50,
    "includeDescriptions": false
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const item of items) {
    console.log(`${item.title} | ${item.companyName} | ${item.locationLabel} | ${item.source}`);
}
```

The complete file is [`examples/run.js`](examples/run.js) (ES module, Node 18 or later).

### 3. Apify API with Python

```bash
pip install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
python examples/run.py
```

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("bibian/nonprofit-jobs-scraper").call(run_input={
    "keywords": "fundraising",
    "countries": ["GB", "US", "AU", "ES"],
    "maxItems": 50,
    "includeDescriptions": False,
})

for item in client.dataset(run.default_dataset_id).iterate_items():
    print(f"{item['title']} | {item.get('companyName')} | {item.get('locationLabel')} | {item.get('source')}")
```

The complete file is [`examples/run.py`](examples/run.py). Never put your token in the code: read it from the `APIFY_TOKEN` environment variable as above.

### 4. Schedule it for a daily alert

Create an Apify Schedule for the Actor, set `publishedWithinDays` to `1` and `onlyNew` to `true`, and attach an integration (Slack, e-mail, Google Sheets, Make, Zapier or a webhook) so only the new postings reach you, every day.

## Pricing

Pay per result: **$3.00 per 1,000 job postings** (that is $0.003 per job posting), plus a small start fee per run. You pay only for the postings saved to the dataset, deduplicated across all 4 sources before being counted or charged. Apify's free plan includes monthly credits, enough to try it on a few hundred results. Prices are those shown on the [Store page](https://apify.com/bibian/nonprofit-jobs-scraper) when this guide was written; the Store page is the reference.

## Limits and honest notes

- Only what each site publishes is collected: not every posting shows a salary, a region or an experience level, so those fields are often `null` (visible in `sample-output.json`).
- HacesFalta mixes paid jobs and unpaid volunteering on the same board: use `opportunityType` to tell them apart, or filter it out client-side. The other 3 boards are paid jobs only.
- The dataset contains job postings only. Recruiter contact details are never exported.
- Postings are the public ones: anything behind a login is out of scope.
- This is an unofficial tool, not affiliated with CharityJob, Idealist, Pro Bono Australia or HacesFalta. Check each site's terms and the data protection rules that apply to your use.

## Why this one

4 nonprofit and social-sector boards across 4 countries in one run, one schema, deduplicated across sources by URL and by (title, company, city). `source` and `country` on every row to filter or split by board or market. No connection, no login, no browser to configure.

## FAQ

**Does it need a browser or a proxy?**
No. All four sources are read directly over HTTP, so runs are fast and cheap.

**How do I only get new postings every day?**
Set `publishedWithinDays` to `1`, turn `onlyNew` on, and schedule the Actor once a day. Each source is deduplicated against what a previous run already delivered.

**Can I query just one source, like only Idealist?**
Yes, set `sources` to `["idealist"]` (or any subset) and `countries` to match.

**Does it include volunteering, or only paid jobs?**
Both are included from HacesFalta (tagged with `opportunityType`); the other 3 boards are paid jobs only.

**Can I get the data in Excel or Google Sheets?**
Yes. Export the dataset as CSV, Excel or JSON from the Apify console, or connect the Apify Google Sheets integration.

## Try it

**[Open nonprofit-jobs-scraper on the Apify Store](https://apify.com/bibian/nonprofit-jobs-scraper)**

The code in `examples/` is released under the MIT license (see [LICENSE](LICENSE)). The data belongs to its original publishers.
