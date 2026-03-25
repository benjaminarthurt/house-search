# Past Listing Recovery Attempts - 5707 Scenic Ave, Mexico, NY 13114

_Date:_ 2026-03-24

## Goal
Recover older listing snapshots or past-listing photos from public web archives / caches.

## Concrete public traces preserved
### Brave search snippet: Homes.com sold results
Observed via Brave search results for `"5707 Scenic Ave" Mexico NY` and related queries:
- Address: `5707 Scenic Ave, Mexico, NY 13114`
- Sold date shown in snippet: `Sold Sep 03, 2024`
- Price shown in snippet: `$255,000`
- Size shown in snippet: `2,184 Sq Ft`
- DOM shown in snippet: `54 Days On Market`
- Beds/baths shown in snippet: `4 Beds · 4 Baths`
- Listing remarks snippet captured:
  - `Welcome to this updated grand brick home in the Village of Mexico.`
  - `The current owners opened it up as a single family home but it can easily be turned back into a 2 unit by closing up two doors for income potential...`

This is currently the strongest publicly visible trace of the prior sale-cycle listing text from this environment.

## Exact URLs tried and results
### Direct listing / aggregator pages
- `https://www.homes.com/property/5707-scenic-ave-mexico-ny/`
  - Result: `403 Access Denied` from this environment.
- `https://www.homes.com/mexico-ny/sold/`
  - Result: `403 Access Denied` from this environment.
- `https://www.movoto.com/mexico-ny/5707-scenic-ave-mexico-ny-13114/pid_j81bu36qjh/`
  - Result: current page accessible, but this is the current/public page, not an archived prior listing cycle.
- `https://www.century21galloway.com/real-estate/new-york-state-alliance-mls/property/r1655848-5707-scenic-avenue-mexico-ny-13114/`
  - Result: current page accessible, but no archived older snapshot was recovered in this pass.

### Wayback Machine CDX / snapshot discovery probes
- `https://web.archive.org/cdx/search/cdx?url=https%3A%2F%2Fwww.homes.com%2Fproperty%2F5707-scenic-ave-mexico-ny%2F&output=json&fl=timestamp,original,statuscode,mimetype&filter=statuscode:200&limit=20&from=2023`
  - Result: `[]`
- `https://web.archive.org/cdx/search/cdx?url=https%3A%2F%2Fwww.movoto.com%2Fmexico-ny%2F5707-scenic-ave-mexico-ny-13114%2Fpid_j81bu36qjh%2F&output=json&fl=timestamp,original,statuscode,mimetype&filter=statuscode:200&limit=20&from=2023`
  - Result: `[]`
- `https://web.archive.org/cdx/search/cdx?url=www.homes.com/mexico-ny/sold/*&output=json&fl=timestamp,original,statuscode&filter=statuscode:200&limit=20&from=2024`
  - Result: `[]`
- `https://web.archive.org/cdx/search/cdx?url=www.century21galloway.com/mexico-real-estate*&output=json&fl=timestamp,original,statuscode&filter=statuscode:200&limit=20&from=2024`
  - Result: `[]`
- `https://web.archive.org/cdx/search/cdx?url=www.howardhanna.com/homes/new-york/mexico*&output=json&fl=timestamp,original,statuscode&filter=statuscode:200&limit=20&from=2024`
  - Result: `[]`

## Search angles tried
- Exact address searches with listing domains: Homes, Movoto, Zillow, Realtor, Redfin, Trulia, Century 21, Howard Hanna.
- Phrase search on the apparent listing remarks:
  - `"updated grand brick home in the Village of Mexico"`
  - `"The current owners opened it up as a single family home"`
- Archive targets:
  - `site:web.archive.org`
  - `site:archive.today OR site:archive.is OR site:archive.ph`

## Outcome
No concrete archived photo gallery or archived prior listing page was recoverable from public Wayback/CDX results in this pass.

## Best next leads if this needs another pass
1. Try manual browser-based archive services outside this environment (some are JS/challenge-sensitive).
2. Probe alternate syndication paths if an MLS-to-broker feed exposed the sold listing under a different brokerage URL in 2024.
3. Search image caches or social reposts using the exact listing remarks plus `Mexico NY`.
