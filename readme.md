# Paris Food Map

An interactive web app with 178 curated Paris restaurants, cafés, and bistros.

**Live URL:** https://peytonsherlin.github.io/paris-food-map/paris-food-map.html

---

## Files

| File | Purpose |
|------|---------|
| `paris-food-map.html` | The entire app — map, data, filters, UI |
| `sw.js` | Service worker — enables offline use after first visit |
| `scripts/scrape.py` | Bi-weekly scraper — checks Les Frenchies for new places |
| `.github/workflows/scrape.yml` | GitHub Actions scheduler — runs scraper automatically |

---

## Accounts & Services

| Service | Purpose | Cost |
|---------|---------|------|
| **GitHub** (github.com/peytonsherlin) | Hosts files, runs automation, issues alerts | Free |
| **GitHub Pages** | Serves the live public URL over HTTPS | Free |
| **YouTube RSS Feed** | Monitors Les Frenchies channel for new videos | Free |
| **Les Frenchies Travel** (youtube.com/@LesFrenchiesTravel) | Source channel for all place data | N/A |

---

## Features

- **Interactive map** — filter by arrondissement, price, meal type, experience level, locals' picks
- **Smart search** — type and hit Enter to filter places by keyword, vibe, or food type
- **Mobile view** — bottom pill bar with Filters, List, and Saved panels
- **Deep linking** — URL updates with active filters so views are shareable
- **PWA / offline** — works without internet after first load
- **Les Frenchies Channel button** — every place links to the YouTube channel playlists
- **Saved places** — users can heart places and export them
- **Image fallbacks** — broken photos show a warm placeholder instead of broken icons

---

## Bi-Weekly Automation

1. GitHub Actions fires on the **1st and 15th of every month**
2. Scraper fetches the Les Frenchies Travel YouTube RSS feed
3. Checks video descriptions for place names not already in the map
4. If new places found → opens a **GitHub Issue** for review
5. Check the **Issues tab**, verify the places, and add confirmed ones to the map

---

## Next Steps

- B2B distribution — share live URL with hotel and tour operator partners
- Paywall / access control once demand is validated
