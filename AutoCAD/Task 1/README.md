# Residential Floor Plan — AutoCAD 2D Project

**Drawing No:** RFP-2025-001 | **Rev:** A | **Scale:** 1:50 @ A1 | **Status:** For Review

---

## Project Overview

A complete 2D residential floor plan of a single-storey, 2-bedroom house produced to professional AutoCAD drafting standards. Designed as an internship submission and portfolio piece demonstrating core architectural drafting skills: layering, dimensioning, wall construction, door/window symbols, and furniture layout.

The house covers a **14,400 mm × 10,800 mm** footprint and is divided into five rooms across two zones.

---

## Floor Plan Layout

```
┌─────────────────────┬──────────────────────────┐
│                     │                          │
│    BEDROOM 1        │       BEDROOM 2          │
│    ~32.2 m²         │       ~37.8 m²           │
│                     │                          │
├─────────────────────┼──────────────┬───────────┤
│                     │              │           │
│    LIVING ROOM      │   KITCHEN    │ BATHROOM  │
│    ~32.9 m²         │   ~19.7 m²   │  ~12.9 m²│
│                     │              │           │
└─────────────────────┴──────────────┴───────────┘
         14,400 mm wide × 10,800 mm tall
```

---

## Features

### Drafting Standards
- **Wall thickness:** External 230 mm | Internal 115 mm (standard masonry)
- **Layer system:** 9 named layers (A-WALL, A-WALL-INT, A-DOOR, A-WINDOW, A-FURN, A-ANNO-TEXT, A-ANNO-DIM, A-HATCH, TITLEBLOCK)
- **Dimension style:** ARCH-DIM with extension lines, arrow heads, 1:50 scale
- **Text styles:** ARCH (romans.shx) and ARCH-BOLD (romand.shx) — standard AutoCAD drafting fonts
- **DXF version:** R2010 (AutoCAD 2010+), widely compatible

### Room Details
| Room | Width | Depth | Area |
|------|-------|-------|------|
| Living Room | 7,000 mm | 4,700 mm | ~32.9 m² |
| Bedroom 1 | 7,000 mm | 5,525 mm | ~38.7 m² |
| Bedroom 2 | 6,825 mm | 5,525 mm | ~37.7 m² |
| Kitchen | 4,200 mm | 4,700 mm | ~19.7 m² |
| Bathroom | 2,625 mm | 4,700 mm | ~12.3 m² |
| **Total GFA** | | | **~155.5 m²** |

### Elements Included
- Exterior and interior walls with correct thickness
- 6 doors with swing arcs (standard architectural symbol)
- 6 windows (glazing line + frame)
- Full furniture layout: sofa, dining table, beds, wardrobes, desks, kitchen appliances, bathroom fixtures
- Room labels with area calculations
- Linear dimensions (overall + sub-dimensions)
- North arrow
- Professional title block (project name, drawn by, date, scale, drawing number, revision, sheet number)
- General notes and legend

---

## Files in This Project

| File | Description |
|------|-------------|
| `residential_floor_plan.dxf` | AutoCAD-compatible source file (open in AutoCAD, BricsCAD, LibreCAD, etc.) |
| `residential_floor_plan.pdf` | Print-ready PDF with full title block and legend |
| `README.md` | This file |
| `generate_floorplan.py` | Python script that generates the DXF using ezdxf |
| `render_pdf.py` | Python script that renders the PDF using matplotlib |

---

## Software Used

| Tool | Purpose |
|------|---------|
| **AutoCAD 2021+** | Primary CAD software for opening/editing DXF |
| **ezdxf (Python)** | Programmatic DXF generation |
| **matplotlib (Python)** | PDF rendering and visual export |
| **BricsCAD / LibreCAD** | Free alternatives to open the DXF |

---

## How to Open the DXF in AutoCAD

1. Open AutoCAD
2. `File → Open → residential_floor_plan.dxf`
3. Type `ZOOM` → `E` (Extents) to fit the drawing on screen
4. Use the **Layer Manager** (`LA`) to toggle layers on/off

### Recommended Layer Visibility for Plotting
| Layer | Print |
|-------|-------|
| A-WALL | ✅ Yes |
| A-WALL-INT | ✅ Yes |
| A-DOOR | ✅ Yes |
| A-WINDOW | ✅ Yes |
| A-ANNO-DIM | ✅ Yes |
| A-ANNO-TEXT | ✅ Yes |
| TITLEBLOCK | ✅ Yes |
| A-FURN | Optional |
| A-HATCH | Optional |

---

## How to Export from AutoCAD

### Export as PDF (from AutoCAD)
1. `File → Plot` (or `Ctrl+P`)
2. Printer/Plotter: `DWG To PDF.pc3`
3. Paper size: `ISO A1 (841 × 594 mm)`
4. Plot area: `Extents`
5. Scale: `1:50`
6. Click **OK**

### Save as DWG (from DXF)
1. Open the `.dxf` file in AutoCAD
2. `File → Save As`
3. Format: `AutoCAD 2018 Drawing (*.dwg)`
4. Save

---

## Drawing Standards Reference

| Property | Value |
|----------|-------|
| Units | Millimetres |
| Scale | 1:50 |
| Wall (external) | 230 mm |
| Wall (internal) | 115 mm |
| Door (standard) | 900 mm |
| Door (bedroom) | 800 mm |
| Door (bathroom) | 750 mm |
| Window (typical) | 1,200–1,500 mm |
| Ceiling height | 2,700 mm (not shown in 2D plan) |
| DXF version | R2010 |

---

## Skills Demonstrated

- 2D architectural drafting
- AutoCAD layer management
- Wall construction and room planning
- Door and window symbols (BS/ISO standard)
- Furniture layout and space planning
- Linear dimensioning with extension lines
- Title block and drawing annotation
- PDF and DXF export workflow

---

## Notes

- All dimensions are in **millimetres**
- Do **not** scale from this drawing — verify on site
- Wall finishes, structural elements, and MEP (mechanical, electrical, plumbing) are **not** shown
- This drawing is for portfolio/internship purposes only and does not constitute a construction document

---

*Drawing No: RFP-2025-001 | Rev A | 2025*
