# Past Listing Recovery - Other Public Sites Sweep (2026-03-24)

## Goal
Search non-primary public real-estate traces for older listings / older photos for **5707 Scenic Ave, Mexico, NY 13114**.

## Highest-value concrete recovery
The already-saved current Movoto detail HTML contains a buried historical timeline for this exact property, with prior MLS numbers and dates.

### Source used
- `assets/raw-html/movoto-5707-detail-current.html`
- Extracted from Movoto page JSON / property-history panel for current page:
  - `https://www.movoto.com/mexico-ny/5707-scenic-ave-mexico-ny-13114/pid_j81bu36qjh/`

### Recovered prior listing timeline from Movoto
- **2026-01-01** — Listed at **$345,000** — MLS **R1655848**
- **2026-02-25** — Price change to **$339,900** — MLS **R1655848**
- **2024-04-15** — Listed at **$269,900** — MLS **S1531925**
- **2024-06-09** — Pending — MLS **S1531925**
- **2024-09-05** — Sold at **$255,000** — MLS **S1531925**
- **2024-04-15** — Listed at **$269,900** — MLS **S1531559**
- **2024-06-09** — Pending — MLS **S1531559**
- **2019-12-19** — Listed at **$170,000** — MLS **S1242723**
- **2020-01-30** — Continue Show — MLS **S1242723**
- **2020-04-05** — S-Closed — MLS **S1242723**
- **2018-03-12** — Listed at **$155,000** — MLS **S1103832**
- **2018-05-15** — Continue Show — MLS **S1103832**
- **2018-07-12** — Pending Sale — MLS **S1103832**
- **2018-08-02** — S-Closed — MLS **S1103832**
- **2015-04-29** — Listed at **$199,900** — MLS **S330862**
- **2016-10-20** — Price change to **$174,900** — MLS **S330862**
- **2017-07-24** — Price change to **$169,900** — MLS **S330862**

## Public search-result traces recovered this pass

### Homes.com sold snippet
Brave search returned a sold-page snippet for the property from Homes.com:
- `5707 Scenic Ave, Mexico, NY 13114 · /38 · $270,000 Sold Aug 30, 2024`
- snippet also exposed two-unit language:
  - `be turned back into a 2 unit by closing up two doors for income potential.`
  - `The large lower main unit is 2 bedroom 2 1/2 baths and the upper unit is 2 bedrooms`

### Redfin search-result snippet
Brave search on a Redfin zipcode page returned an embedded property snippet:
- `5707 Scenic Ave, Mexico, NY 13114 · $345,000 · 5 beds 4 baths 2,184 sq ft`
- listing broker snippet: `L Wilson Realty, (315) 664-0026`
- This appears to be a search-result trace, not a directly retrievable property detail page from this environment.

### Realtor.com trace
A Brave search result for Mexico, NY Realtor.com results included a snippet that mentions:
- `Property detail for 5707 Scenic Ave Mexico, NY 13114`
- No direct Realtor detail page was surfaced / fetched successfully in this pass.

## Archive / cache checks
### Wayback CDX checks against likely direct property URLs
Checked likely direct property URLs; all returned empty snapshot arrays (`[]`) except Movoto, which timed out during one direct CDX request:
- Realtor guessed detail URL → `[]`
- Howard Hanna guessed detail URL → `[]`
- Redfin guessed detail URL → `[]`
- Onjax guessed detail URL → `[]`
- Movoto guessed detail URL → timed out during CDX query from this environment

## Photo recovery status
- **No older photo gallery recovered** from Realtor.com, Howard Hanna, Redfin, Onjax, or Wayback in this pass.
- Current-listing photos were already harvested earlier, but this sweep did **not** recover prior-cycle photos for MLS **S1531925 / S1531559 / S1242723 / S1103832 / S330862**.

## Best next manual / browser-assisted leads
1. Search MLS history or brokerage IDX pages directly by old MLS IDs:
   - `S1531925`
   - `S1531559`
   - `S1242723`
   - `S1103832`
   - `S330862`
2. Ask listing office / local agent for archived print sheets or prior MLS photo sheets.
3. Browser-assisted search on Google/Bing image cache using the old MLS numbers may still surface image-host remnants.
4. If Onjax / IDX pages once existed for the old MLS IDs, a browser session may expose JS-loaded image URLs not visible here.
