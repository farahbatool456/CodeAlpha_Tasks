# MEC-001 — Flanged Shaft Coupling
## 2D Mechanical Engineering Drawing | Portfolio & Internship Submission

---

## Project Overview

This project is a professional **2D orthographic mechanical drawing** of a **Flanged Shaft Coupling** — a standard machine element used to connect rotating shafts while transmitting torque. The drawing follows industry-standard drafting practices and is suitable for manufacturing, academic, and internship portfolio submission.

The project includes:
- A fully annotated **DXF file** (native AutoCAD format, import-ready)
- A print-ready **PDF drawing sheet** (A1 landscape)
- Complete **layer management**, dimensioning, and notation

---

## Component Specifications

| Parameter              | Value                         |
|------------------------|-------------------------------|
| Component              | Flanged Shaft Coupling        |
| Drawing Number         | MEC-001                       |
| Overall Diameter (OD)  | ⌀120 mm                       |
| Hub Diameter           | ⌀60 mm                        |
| Bore Diameter          | ⌀30 mm (H7 tolerance)         |
| Flange Thickness       | 20 mm                         |
| Hub Length             | 40 mm                         |
| Bolt Hole Circle (PCD) | ⌀90 mm                        |
| Bolt Holes             | 6 × M10, equally spaced       |
| Keyway                 | 6 × 6 × 22 mm (BS 46 Part 1) |
| Material               | Cast Iron Grade 250 (IS 210)  |
| Surface Finish         | Ra 1.6 (machined surfaces)    |
| Bore Fit               | H7/k6 (interference fit)      |
| Scale                  | 1:2                           |
| Sheet Size             | A1 (841 × 594 mm)             |

---

## Files in This Repository

```
MEC-001_Flanged_Shaft_Coupling/
│
├── MEC-001_Flanged_Shaft_Coupling.dxf   ← AutoCAD DXF (R2010 format)
├── MEC-001_Flanged_Shaft_Coupling.pdf   ← Print-ready PDF drawing
├── generate_dxf.py                       ← Python script: DXF generator
├── generate_pdf.py                       ← Python script: PDF generator
└── README.md                             ← This file
```

---

## Views Included

### 1. Front View (Section A-A)
- Full sectional view cut along the central axis
- Shows flange profile, hub, bore, and keyway
- Section hatching (ANSI31 pattern at 45°) on all solid material regions
- Hidden lines for bore diameter shown in dashed linetype

### 2. Top View
- Circular face view of the flange
- Shows all concentric circles: OD, Hub OD, PCD, and Bore
- 6 × M10 bolt holes positioned on PCD with centre marks
- Keyway slot visible at top of hub circle

### 3. Side View
- Profile view of the hub
- Bore shown as hidden (dashed) lines
- Flange depth shown as hidden lines behind hub
- Section hatching on hub walls

---

## Drafting Standards Followed

| Standard | Description |
|----------|-------------|
| **BS 8888 / ISO 128** | Technical drawing general principles |
| **ISO 2768-m** | General tolerances (medium class) |
| **ASME Y14.5** | Dimensioning and tolerancing practices |
| **BS 46 Part 1** | Keyway dimensions |
| **3rd Angle Projection** | View arrangement convention |
| **ISO 128-34** | Section views and hatching |

---

## Layer Structure (AutoCAD / DXF)

| Layer Name   | Color    | Linetype   | Use                          |
|--------------|----------|------------|------------------------------|
| `OBJECT`     | White    | Continuous | Visible outlines (0.5 mm)    |
| `HIDDEN`     | Blue     | DASHED     | Hidden edges (0.18 mm)       |
| `CENTER`     | Red      | CENTER     | Centrelines (0.18 mm)        |
| `DIMENSION`  | Yellow   | Continuous | All dimension entities       |
| `ANNOTATION` | Cyan     | Continuous | Notes, labels, leaders       |
| `HATCH`      | Magenta  | Continuous | Section fill patterns        |
| `TITLEBLOCK` | White    | Continuous | Border, title, revision      |
| `VIEWPORT`   | Green    | DASHED     | Projection alignment lines   |
| `BORDER`     | White    | Continuous | Sheet border (0.7 mm)        |

---

## Dimensions & Annotations

The drawing includes:
- **Linear dimensions** — overall, hub, bore widths and heights
- **Diameter callouts** — using ⌀ symbol (⌀120, ⌀60, ⌀30, ⌀90 PCD)
- **Bolt hole note** — `6 × M10 EQUI-SPACED ON PCD` with leader line
- **Tolerance callout** — Bore H7, shaft k6 interference fit
- **Surface finish symbol** — Ra 1.6 on machined bore surface
- **Section cut markers** — A-A arrows on top view
- **Keyway dimensions** — width and depth
- **Projection lines** — dashed alignment lines between views

---

## Title Block Contents

| Field        | Value                  |
|--------------|------------------------|
| Drawn By     | YOUR NAME              |
| Date         | 2024-01-15             |
| Checked By   | —                      |
| Scale        | 1:2                    |
| Drawing No.  | MEC-001                |
| Sheet        | 1 of 1                 |
| Revision     | A — Initial Release    |

---

## Software & Tools Used

| Tool                  | Purpose                            |
|-----------------------|------------------------------------|
| **AutoCAD 2021+**     | Open/edit the DXF drawing          |
| **ezdxf (Python)**    | Programmatic DXF generation        |
| **ReportLab (Python)**| PDF drawing output                 |
| **Python 3.10+**      | Script execution environment       |

> **Note on DXF vs DWG:** DXF (Drawing Exchange Format) is the open standard developed by Autodesk. AutoCAD opens DXF files natively. To save as DWG (AutoCAD binary format), open the DXF in AutoCAD and use **File → Save As → DWG**. DXF is preferable for GitHub because it is text-based and version-control friendly.

---

## How to Open the DXF in AutoCAD

1. Launch **AutoCAD** (2018 or later recommended)
2. `File → Open → Browse to MEC-001_Flanged_Shaft_Coupling.dxf`
3. Type `ZOOM` → `E` (Zoom Extents) to fit the drawing
4. Switch to `MODEL` space to see the full drawing
5. Use **Layer Manager** to toggle individual layers

### To Export DWG from AutoCAD:
```
File → Save As → AutoCAD Drawing (*.dwg) → Save
```

### To Export PDF from AutoCAD:
```
File → Plot → Printer: DWG to PDF.pc3 → Paper size: ISO A1
Plot area: Extents → Fit to paper → Plot
```

---

## How to Regenerate the Files

Requires Python 3.10+ and the following packages:

```bash
pip install ezdxf reportlab
```

Then run:

```bash
# Regenerate DXF
python generate_dxf.py

# Regenerate PDF
python generate_pdf.py
```

---

## Skills Demonstrated

- Orthographic projection (3rd angle) with 3 views
- Standard mechanical component drawing
- Sectional views with correct ANSI31 hatch patterns
- ISO/ASME dimensioning: linear, diameter, tolerance callouts
- Surface finish and fit specification (H7/k6)
- Proper use of linetypes (object, hidden, centre)
- Layer-based organisation for professional CAD workflow
- Title block and revision block formatting
- Engineering notes and general tolerance specification

---

## Why a Flanged Shaft Coupling?

It was chosen deliberately — not because it is the flashiest component, but because it tests a wide range of drafting skills in a single drawing:

- **Circular features** → requires diameter dimensions and PCD notation
- **Sectional view** → requires correct hatch and hidden line handling
- **Fits and tolerances** → demonstrates understanding of engineering fits
- **Repeated features** → bolt holes on PCD, keyway standardisation
- **Multiple views** → orthographic projection coherence

This is a real component used in industrial drive systems, which makes it directly relevant for mechanical engineering internship applications.

---

## License

This project is submitted as an academic and portfolio piece. You are free to use, modify, and adapt the drawing for educational purposes with attribution.

---

*Drawing prepared in accordance with BS 8888 and ISO 128 standards.*
