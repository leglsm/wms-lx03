# WMS LX03 Viewer

**Live demo:** https://leglsm.github.io/wms-lx03/ · no login, opens with sample data

A browser-based viewer that turns a flat SAP WM bin-stock report (LX03) into a warehouse map, so you can see **where every part is, how many storage units it has, and how old it is** at a glance.

![WMS LX03 Viewer screenshot](docs/screenshot.png)

> All data in this demo is fictional (plant, warehouse, materials, programs, quantities). It is generated with a fixed seed by `scripts/generate_sample.py`. The tool was inspired by real warehouse work. No company data is included.

---

## Problem

The warehouse held **2,000+ SKUs**, but SAP only gave us LX03 as a long flat list. Nothing showed the stock spatially, so basic questions took slow, manual digging:

- Where is this part physically, and in which bins?
- How many handling units (HU) does a part have, and are they full pallets or pick units (PU)?
- Which rows are in **dynamic (random) locations** and which are in **fixed picking locations**? The raw export mixes both, and telling them apart relied on tribal knowledge.

## Approach

- **Input:** the standard LX03 export (storage type, storage bin, storage unit, material, quantities, GR date).
- **Bin parsing:** structured bins (`AISLE-BAY-LEVEL`, e.g. `01-05-02`) are laid out as rack faces. Free-form bins such as floor staging are shown as tiles.
- **Map:** each bin is colored by its oldest storage unit's age. Empty bins and blocked stock (0 available) are marked separately.
- **Aging and action list:** stock is bucketed by days since goods receipt. Anything older than 180 days or blocked goes to a short list with its bin location.
- **Search:** find any material, description, bin or storage unit and sort by any column.
- **Single self-contained HTML file:** no server and no install. It opens in any browser.

## Result

- Answering "where is it, how many HUs, how old is it" went from reading a flat report to **one look at the map**.
- In daily use it felt **about 10× faster** to locate parts, count HUs per part and spot problem stock. This is a hands-on estimate, not a timed study.

## What this demo includes

| Area | Demo |
|---|---|
| Storage types | 001 Pallet Racking, 002 Overflow Racking, 003 High Bay, 900 Floor Staging |
| Size | 727 bins, 586 storage units, 112 materials (scaled down from the real 2,000+ SKUs) |
| Views | KPI cards, bin map with bin detail, aging distribution, action list, searchable LX03 table |

SAP-style material number ranges are imitated (e.g. 2xxxxxxx components, 5xxxxxxx semi-finished, 45xxxxxx finished goods, 6xxxxxxx returnable packaging). None of them are real part numbers.

## Repository

```
index.html                  # the demo (data embedded)
template.html               # same page with a __DATA__ placeholder
data/sample_lx03.xlsx       # fictional LX03-style export
data/sample.json            # same data as JSON
scripts/generate_sample.py  # fixed-seed sample generator
scripts/build_demo.py       # embeds data/sample.json into template.html -> index.html
docs/screenshot.png
```

Rebuild: `pip install openpyxl`, then `python scripts/generate_sample.py && python scripts/build_demo.py`

## Author

Daniel Eunggu Lee · Warehouse & Material Flow Optimization Engineer · [github.com/leglsm](https://github.com/leglsm)
