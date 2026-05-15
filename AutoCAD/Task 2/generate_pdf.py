"""
PDF Generator for Mechanical Drawing
Component: Flanged Shaft Coupling
Standard: ISO/ASME Y14.5
"""

from reportlab.lib.pagesizes import A1, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
import math

# A1 landscape: 841 x 594 mm → points
W_mm, H_mm = 841, 594
W = W_mm * mm
H = H_mm * mm

BORDER_M = 10 * mm

# Colors
C_OBJECT   = colors.black
C_HIDDEN   = colors.HexColor('#0000CC')
C_CENTER   = colors.HexColor('#CC0000')
C_DIM      = colors.HexColor('#888800')
C_ANNOT    = colors.HexColor('#007777')
C_HATCH    = colors.HexColor('#AA00AA')
C_TITLE    = colors.black
C_SECTION  = colors.HexColor('#444444')

def pt(v_mm):
    """mm to points"""
    return v_mm * mm

def draw_dashed_line(c, x1, y1, x2, y2, dash=(3*mm, 1.5*mm)):
    c.setDash(*dash)
    c.line(x1, y1, x2, y2)
    c.setDash()

def draw_center_line(c, x1, y1, x2, y2):
    c.setDash([6*mm, 1.5*mm, 0.5*mm, 1.5*mm], 0)
    c.line(x1, y1, x2, y2)
    c.setDash()

def draw_arrow(c, x1, y1, x2, y2, size=2.5*mm):
    """Draw arrowhead at (x2,y2) pointing from (x1,y1)"""
    angle = math.atan2(y2-y1, x2-x1)
    ax1 = x2 - size * math.cos(angle - math.radians(20))
    ay1 = y2 - size * math.sin(angle - math.radians(20))
    ax2 = x2 - size * math.cos(angle + math.radians(20))
    ay2 = y2 - size * math.sin(angle + math.radians(20))
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(ax1, ay1)
    p.lineTo(ax2, ay2)
    p.close()
    c.drawPath(p, fill=1, stroke=0)

def dim_horizontal(c, x1, y, x2, text, offset=8*mm, fs=3.5):
    """Draw horizontal linear dimension"""
    c.setStrokeColor(C_DIM)
    c.setFillColor(C_DIM)
    c.setLineWidth(0.25*mm)
    # Dim line
    c.line(x1, y, x2, y)
    draw_arrow(c, x2, y, x1, y)
    draw_arrow(c, x1, y, x2, y)
    # Ext lines
    c.line(x1, y - offset*0.3, x1, y + offset*0.15)
    c.line(x2, y - offset*0.3, x2, y + offset*0.15)
    # Text
    c.setFont('Helvetica', fs*mm)
    c.drawCentredString((x1+x2)/2, y + 1.5*mm, text)

def dim_vertical(c, x, y1, y2, text, offset=8*mm, fs=3.5):
    """Draw vertical linear dimension"""
    c.setStrokeColor(C_DIM)
    c.setFillColor(C_DIM)
    c.setLineWidth(0.25*mm)
    c.line(x, y1, x, y2)
    draw_arrow(c, x, y1, x, y2)
    draw_arrow(c, x, y2, x, y1)
    c.line(x - offset*0.15, y1, x + offset*0.3, y1)
    c.line(x - offset*0.15, y2, x + offset*0.3, y2)
    c.saveState()
    c.translate(x + 1.5*mm, (y1+y2)/2)
    c.rotate(90)
    c.setFont('Helvetica', fs*mm)
    c.drawCentredString(0, 0, text)
    c.restoreState()

def dim_diameter(c, cx, cy, r, angle_deg, text, fs=3.5):
    """Diameter dimension with leader"""
    c.setStrokeColor(C_DIM)
    c.setFillColor(C_DIM)
    c.setLineWidth(0.25*mm)
    rad = math.radians(angle_deg)
    x1 = cx + r * math.cos(rad)
    y1 = cy + r * math.sin(rad)
    x2 = cx - r * math.cos(rad)
    y2 = cy - r * math.sin(rad)
    c.line(x1, y1, x2, y2)
    draw_arrow(c, x2, y2, x1, y1)
    draw_arrow(c, x1, y1, x2, y2)
    # Text at center-ish
    tx = cx + (r * 0.1) * math.cos(rad + math.radians(90))
    ty = cy + (r * 0.1) * math.sin(rad + math.radians(90))
    c.setFont('Helvetica-Bold', fs*mm)
    c.drawCentredString(tx, ty + 1*mm, text)

def hatch_region(c, x1, y1, x2, y2, spacing=3*mm, angle=45):
    """Draw diagonal hatch lines in a rectangle"""
    c.saveState()
    c.setStrokeColor(C_HATCH)
    c.setLineWidth(0.15*mm)
    p = c.beginPath()
    p.rect(x1, y1, x2-x1, y2-y1)
    c.clipPath(p, stroke=0)
    rad = math.radians(angle)
    dx = spacing / math.cos(rad)
    W_box = x2 - x1
    H_box = y2 - y1
    diag = math.sqrt(W_box**2 + H_box**2)
    steps = int(diag / spacing) + 4
    for i in range(-steps, steps):
        sx = x1 + i * dx
        c.line(sx, y1, sx + H_box / math.tan(rad), y2)
    c.restoreState()

def leader_note(c, fx, fy, tx, ty, text, fs=2.8):
    """Leader with note"""
    c.setStrokeColor(C_ANNOT)
    c.setFillColor(C_ANNOT)
    c.setLineWidth(0.2*mm)
    c.line(fx, fy, tx, ty)
    draw_arrow(c, tx, ty, fx, fy)
    c.line(tx, ty, tx + 20*mm, ty)
    c.setFont('Helvetica', fs*mm)
    c.drawString(tx + 1*mm, ty + 1*mm, text)


def generate_pdf():
    fname = '/home/claude/MEC-001_Flanged_Shaft_Coupling.pdf'
    c = canvas.Canvas(fname, pagesize=(W, H))
    c.setTitle('MEC-001 Flanged Shaft Coupling — Mechanical Drawing')
    c.setAuthor('Mechanical Engineering Portfolio')
    c.setSubject('2D Orthographic Drawing — ISO Third Angle Projection')

    # ─── SHEET BORDER ──────────────────────────────────────────────────────────
    c.setStrokeColor(C_TITLE)
    c.setLineWidth(0.7*mm)
    c.rect(BORDER_M, BORDER_M, W - 2*BORDER_M, H - 2*BORDER_M)
    c.setLineWidth(0.35*mm)
    c.rect(BORDER_M + 2*mm, BORDER_M + 2*mm,
           W - 2*BORDER_M - 4*mm, H - 2*BORDER_M - 4*mm)

    # ─── VIEW ORIGINS (in points) ───────────────────────────────────────────────
    FVx, FVy = pt(175), pt(190)   # Front View centre
    TVx, TVy = pt(175), pt(370)   # Top View centre
    SVx, SVy = pt(360), pt(190)   # Side View centre

    # Component parameters (mm → pt)
    OD    = pt(60)   # outer radius
    HUB_R = pt(30)   # hub radius
    BORE_R= pt(15)   # bore radius
    PCD_R = pt(45)   # bolt PCD radius
    FH    = pt(20)   # flange thickness (height in front view)
    HH    = pt(40)   # hub height
    KW    = pt(6)    # keyway width
    KD    = pt(3)    # keyway depth

    # ═══════════════════════════════════════════════════════════════════════════
    # FRONT VIEW (Section A-A)
    # ═══════════════════════════════════════════════════════════════════════════
    c.setStrokeColor(C_OBJECT)
    c.setLineWidth(0.5*mm)

    # Flange rectangle
    c.rect(FVx - OD, FVy - FH/2, 2*OD, FH)
    # Hub rectangle
    c.rect(FVx - HUB_R, FVy - HH/2, 2*HUB_R, HH)
    # Keyway top of hub
    c.rect(FVx - KW/2, FVy + HH/2, KW, KD)

    # Section hatching
    hatch_region(c, FVx - OD, FVy - FH/2, FVx - HUB_R, FVy + FH/2)
    hatch_region(c, FVx + HUB_R, FVy - FH/2, FVx + OD, FVy + FH/2)
    # Hub walls hatch
    hatch_region(c, FVx - HUB_R, FVy - HH/2, FVx - BORE_R, FVy + HH/2)
    hatch_region(c, FVx + BORE_R, FVy - HH/2, FVx + HUB_R, FVy + HH/2)

    # Bore (hidden lines)
    c.setStrokeColor(C_HIDDEN)
    c.setLineWidth(0.18*mm)
    draw_dashed_line(c, FVx - BORE_R, FVy - HH/2, FVx - BORE_R, FVy + HH/2)
    draw_dashed_line(c, FVx + BORE_R, FVy - HH/2, FVx + BORE_R, FVy + HH/2)

    # Center lines — Front View
    c.setStrokeColor(C_CENTER)
    c.setLineWidth(0.18*mm)
    draw_center_line(c, FVx - pt(80), FVy, FVx + pt(80), FVy)
    draw_center_line(c, FVx, FVy - pt(35), FVx, FVy + pt(35))

    # Redraw object borders over hatch
    c.setStrokeColor(C_OBJECT)
    c.setLineWidth(0.5*mm)
    c.rect(FVx - OD, FVy - FH/2, 2*OD, FH, fill=0)
    c.rect(FVx - HUB_R, FVy - HH/2, 2*HUB_R, HH, fill=0)
    c.rect(FVx - KW/2, FVy + HH/2, KW, KD, fill=0)

    # Section cut arrows (A-A)
    c.setFillColor(C_SECTION)
    c.setStrokeColor(C_SECTION)
    c.setFont('Helvetica-Bold', 5*mm)
    c.drawString(FVx - OD - pt(12), FVy + pt(2), 'A')
    c.drawString(FVx + OD + pt(5), FVy + pt(2), 'A')
    c.setLineWidth(0.4*mm)
    c.line(FVx - OD - pt(10), FVy, FVx - OD - pt(3), FVy)
    draw_arrow(c, FVx - OD - pt(3), FVy, FVx - OD, FVy)
    c.line(FVx + OD + pt(3), FVy, FVx + OD + pt(10), FVy)
    draw_arrow(c, FVx + OD + pt(3), FVy, FVx + OD, FVy)

    # Surface finish symbol
    sf_x, sf_y = FVx + HUB_R + pt(5), FVy + pt(5)
    c.setStrokeColor(C_ANNOT)
    c.setLineWidth(0.2*mm)
    c.line(sf_x, sf_y, sf_x + pt(5), sf_y + pt(5))
    c.line(sf_x + pt(5), sf_y + pt(5), sf_x + pt(10), sf_y + pt(5))
    c.setFillColor(C_ANNOT)
    c.setFont('Helvetica', 2.5*mm)
    c.drawString(sf_x + pt(6), sf_y + pt(6), 'Ra 1.6')

    # FRONT VIEW DIMENSIONS
    # Overall width
    dim_horizontal(c, FVx - OD, FVy - FH/2 - pt(14), FVx + OD, '⌀120', fs=3.2)
    # Hub width
    dim_horizontal(c, FVx - HUB_R, FVy - HH/2 - pt(25), FVx + HUB_R, '⌀60', fs=3.2)
    # Bore width
    dim_horizontal(c, FVx - BORE_R, FVy + HH/2 + pt(10), FVx + BORE_R, '⌀30 BORE', fs=3.2)
    # Hub height
    dim_vertical(c, FVx + OD + pt(14), FVy - HH/2, FVy + HH/2, '40', fs=3.2)
    # Flange thickness
    dim_vertical(c, FVx + OD + pt(25), FVy - FH/2, FVy + FH/2, '20', fs=3.2)

    # VIEW LABEL
    c.setFillColor(C_ANNOT)
    c.setFont('Helvetica-Bold', 3.5*mm)
    c.drawCentredString(FVx, FVy - HH/2 - pt(38), 'FRONT VIEW (SECTION A-A)')

    # ═══════════════════════════════════════════════════════════════════════════
    # TOP VIEW
    # ═══════════════════════════════════════════════════════════════════════════
    c.setStrokeColor(C_OBJECT)
    c.setLineWidth(0.5*mm)

    # Outer flange circle
    c.circle(TVx, TVy, OD, stroke=1, fill=0)
    # Hub circle
    c.circle(TVx, TVy, HUB_R, stroke=1, fill=0)
    # PCD circle (center linetype)
    c.setStrokeColor(C_CENTER)
    c.setLineWidth(0.18*mm)
    draw_center_line(c, TVx - OD - pt(15), TVy, TVx + OD + pt(15), TVy)
    draw_center_line(c, TVx, TVy - OD - pt(15), TVx, TVy + OD + pt(15))

    # Draw PCD circle as center line (dashed circle sim)
    c.setDash(4*mm, 1.5*mm)
    c.circle(TVx, TVy, PCD_R, stroke=1, fill=0)
    c.setDash()

    # Bore circle (hidden)
    c.setStrokeColor(C_HIDDEN)
    c.setLineWidth(0.18*mm)
    c.setDash(3*mm, 1.5*mm)
    c.circle(TVx, TVy, BORE_R, stroke=1, fill=0)
    c.setDash()

    # 6 bolt holes on PCD
    num_bolts = 6
    bolt_r_draw = pt(5)
    for i in range(num_bolts):
        angle = i * 360/num_bolts
        rad = math.radians(angle)
        bx = TVx + PCD_R * math.cos(rad)
        by = TVy + PCD_R * math.sin(rad)
        c.setStrokeColor(C_OBJECT)
        c.setLineWidth(0.35*mm)
        c.circle(bx, by, bolt_r_draw, stroke=1, fill=0)
        # Center cross
        c.setStrokeColor(C_CENTER)
        c.setLineWidth(0.13*mm)
        draw_center_line(c, bx - pt(8), by, bx + pt(8), by)
        draw_center_line(c, bx, by - pt(8), bx, by + pt(8))

    # Keyway in top view
    c.setStrokeColor(C_OBJECT)
    c.setLineWidth(0.5*mm)
    c.rect(TVx - KW/2, TVy + HUB_R, KW, KD, fill=0)

    # TOP VIEW DIMENSIONS
    dim_diameter(c, TVx, TVy, OD, 50, '⌀120', fs=3.2)
    dim_diameter(c, TVx, TVy, HUB_R, 140, '⌀60', fs=3.2)
    dim_diameter(c, TVx, TVy, PCD_R, 230, 'PCD ⌀90', fs=3.2)
    dim_diameter(c, TVx, TVy, BORE_R, 315, '⌀30', fs=3.2)

    # Bolt hole leader note
    bx0 = TVx + PCD_R * math.cos(math.radians(0))
    by0 = TVy + PCD_R * math.sin(math.radians(0))
    leader_note(c, bx0 + bolt_r_draw, by0, TVx + OD + pt(12), by0,
                '6 x M10 EQUI-SP. ON PCD', fs=2.8)

    c.setFillColor(C_ANNOT)
    c.setFont('Helvetica-Bold', 3.5*mm)
    c.drawCentredString(TVx, TVy + OD + pt(8), 'TOP VIEW')

    # ═══════════════════════════════════════════════════════════════════════════
    # SIDE VIEW
    # ═══════════════════════════════════════════════════════════════════════════
    c.setStrokeColor(C_OBJECT)
    c.setLineWidth(0.5*mm)

    # Hub profile in side view
    c.rect(SVx - HUB_R, SVy - HH/2, 2*HUB_R, HH, fill=0)
    c.rect(SVx - KW/2, SVy + HH/2, KW, KD, fill=0)

    # Section hatching on hub walls
    hatch_region(c, SVx - HUB_R, SVy - HH/2, SVx - BORE_R, SVy + HH/2)
    hatch_region(c, SVx + BORE_R, SVy - HH/2, SVx + HUB_R, SVy + HH/2)

    # Bore (hidden in side view)
    c.setStrokeColor(C_HIDDEN)
    c.setLineWidth(0.18*mm)
    draw_dashed_line(c, SVx - BORE_R, SVy - HH/2, SVx - BORE_R, SVy + HH/2)
    draw_dashed_line(c, SVx + BORE_R, SVy - HH/2, SVx + BORE_R, SVy + HH/2)

    # Flange (behind hub, shown as hidden)
    FW_SIDE = pt(20)
    draw_dashed_line(c, SVx - HUB_R - FW_SIDE, SVy - OD, SVx - HUB_R, SVy - OD)
    draw_dashed_line(c, SVx - HUB_R - FW_SIDE, SVy + OD, SVx - HUB_R, SVy + OD)
    draw_dashed_line(c, SVx - HUB_R - FW_SIDE, SVy - OD, SVx - HUB_R - FW_SIDE, SVy + OD)

    # Center lines — Side View
    c.setStrokeColor(C_CENTER)
    c.setLineWidth(0.18*mm)
    draw_center_line(c, SVx - pt(50), SVy, SVx + pt(50), SVy)
    draw_center_line(c, SVx, SVy - pt(55), SVx, SVy + pt(55))

    # Redraw hub border over hatch
    c.setStrokeColor(C_OBJECT)
    c.setLineWidth(0.5*mm)
    c.rect(SVx - HUB_R, SVy - HH/2, 2*HUB_R, HH, fill=0)
    c.rect(SVx - KW/2, SVy + HH/2, KW, KD, fill=0)

    # SIDE VIEW DIMENSIONS
    dim_vertical(c, SVx + HUB_R + pt(14), SVy - HH/2, SVy + HH/2, '40', fs=3.2)
    dim_horizontal(c, SVx - HUB_R, SVy - HH/2 - pt(12), SVx + HUB_R, '60', fs=3.2)
    dim_horizontal(c, SVx - HUB_R - FW_SIDE, SVy + OD + pt(10), SVx - HUB_R, '20', fs=3.2)

    c.setFillColor(C_ANNOT)
    c.setFont('Helvetica-Bold', 3.5*mm)
    c.drawCentredString(SVx, SVy - HH/2 - pt(25), 'SIDE VIEW')

    # ─── PROJECTION LINES ──────────────────────────────────────────────────────
    c.setStrokeColor(colors.HexColor('#999999'))
    c.setLineWidth(0.1*mm)
    c.setDash(2*mm, 1.5*mm)
    # Front to Top (vertical)
    c.line(FVx - OD, FVy + HH/2 + pt(5), FVx - OD, TVy - OD - pt(5))
    c.line(FVx + OD, FVy + HH/2 + pt(5), FVx + OD, TVy - OD - pt(5))
    # Front to Side (horizontal)
    c.line(FVx + OD + pt(5), FVy - FH/2, SVx - HUB_R - FW_SIDE - pt(5), FVy - FH/2)
    c.line(FVx + OD + pt(5), FVy + FH/2, SVx - HUB_R - FW_SIDE - pt(5), FVy + FH/2)
    c.setDash()

    # ─── GENERAL NOTES BOX ─────────────────────────────────────────────────────
    notes_x = BORDER_M + pt(5)
    notes_y = BORDER_M + pt(5)
    notes_w = pt(175)
    notes_h = pt(80)

    c.setStrokeColor(C_TITLE)
    c.setLineWidth(0.3*mm)
    c.rect(notes_x, notes_y, notes_w, notes_h)

    c.setFillColor(colors.black)
    c.setFont('Helvetica-Bold', 3.5*mm)
    c.drawString(notes_x + pt(3), notes_y + notes_h - pt(7), 'GENERAL NOTES:')
    c.setLineWidth(0.2*mm)
    c.line(notes_x, notes_y + notes_h - pt(10), notes_x + notes_w, notes_y + notes_h - pt(10))

    notes = [
        '1. ALL DIMENSIONS IN MILLIMETRES UNLESS STATED.',
        '2. GENERAL TOLERANCES: ISO 2768-m (MEDIUM).',
        '3. MATERIAL: CAST IRON GRADE 250 (IS 210).',
        '4. SURFACE FINISH: Ra 1.6 ON ALL MACHINED SURFACES.',
        '5. BORE TOLERANCE: H7 (30+0.021/+0.000 mm).',
        '6. SHAFT TOLERANCE: k6 (INTERFERENCE FIT).',
        '7. BOLT HOLES: 6 x M10 THROUGH, EQUI-SPACED.',
        '8. KEYWAY: 6 x 6 x 22 mm (BS 46 PART 1).',
        '9. SURFACE TREATMENT: GREY PRIMER COAT.',
        '10. DRAWING STANDARD: BS 8888 / ISO 128.',
    ]
    c.setFont('Helvetica', 2.8*mm)
    for i, note in enumerate(notes):
        c.drawString(notes_x + pt(3), notes_y + notes_h - pt(16) - i * pt(6), note)

    # ─── TITLE BLOCK ───────────────────────────────────────────────────────────
    TB_W = pt(200)
    TB_H = pt(100)
    tb_x = W - BORDER_M - TB_W
    tb_y = BORDER_M

    c.setStrokeColor(C_TITLE)
    c.setLineWidth(0.7*mm)
    c.rect(tb_x, tb_y, TB_W, TB_H)
    c.setLineWidth(0.3*mm)

    # Component title area (top of title block)
    c.setFillColor(colors.HexColor('#1a1a2e'))
    c.rect(tb_x, tb_y + TB_H - pt(22), TB_W, pt(22), fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 5.5*mm)
    c.drawCentredString(tb_x + TB_W/2, tb_y + TB_H - pt(13), 'FLANGED SHAFT COUPLING')
    c.setFont('Helvetica', 3.5*mm)
    c.drawCentredString(tb_x + TB_W/2, tb_y + TB_H - pt(20), 'ORTHOGRAPHIC PROJECTION — 3rd ANGLE')

    # Grid rows inside title block
    row_labels = [
        ('DRAWN BY:', 'YOUR NAME'),
        ('DATE:', '2024-01-15'),
        ('CHECKED BY:', '—'),
        ('SCALE:', '1:2'),
        ('DWG NO:', 'MEC-001'),
        ('SHEET:', '1 OF 1'),
    ]
    row_h = pt(13)
    for i, (label, value) in enumerate(row_labels):
        ry = tb_y + TB_H - pt(22) - (i + 1) * row_h
        if i > 0:
            c.setStrokeColor(C_TITLE)
            c.setLineWidth(0.2*mm)
            c.line(tb_x, ry + row_h, tb_x + TB_W, ry + row_h)
        mid_x = tb_x + TB_W * 0.45
        c.line(mid_x, ry, mid_x, ry + row_h)
        c.setFillColor(colors.HexColor('#555555'))
        c.setFont('Helvetica', 2.5*mm)
        c.drawString(tb_x + pt(3), ry + pt(4), label)
        c.setFillColor(colors.black)
        c.setFont('Helvetica-Bold', 3.5*mm)
        c.drawString(mid_x + pt(3), ry + pt(4), value)

    # 3rd angle symbol (simplified)
    sym_x = tb_x + pt(150)
    sym_y = tb_y + pt(5)
    c.setStrokeColor(colors.HexColor('#555555'))
    c.setLineWidth(0.2*mm)
    c.setFillColor(colors.HexColor('#555555'))
    c.setFont('Helvetica', 2.5*mm)
    c.drawString(sym_x, sym_y, '[3rd ANGLE PROJ.]')

    # ─── REVISION BLOCK ────────────────────────────────────────────────────────
    rev_x = tb_x
    rev_y = tb_y + TB_H + pt(5)
    rev_w = TB_W
    rev_h = pt(30)

    c.setStrokeColor(C_TITLE)
    c.setLineWidth(0.35*mm)
    c.rect(rev_x, rev_y, rev_w, rev_h)

    c.setFillColor(colors.HexColor('#1a1a2e'))
    c.rect(rev_x, rev_y + rev_h - pt(10), rev_w, pt(10), fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 3.5*mm)
    c.drawCentredString(rev_x + rev_w/2, rev_y + rev_h - pt(8), 'REVISION HISTORY')

    c.setFillColor(colors.black)
    c.setFont('Helvetica-Bold', 2.8*mm)
    c.drawString(rev_x + pt(3), rev_y + rev_h - pt(15), 'REV   DATE            DESCRIPTION                        BY')
    c.setLineWidth(0.15*mm)
    c.line(rev_x, rev_y + rev_h - pt(17), rev_x + rev_w, rev_y + rev_h - pt(17))
    c.setFont('Helvetica', 2.8*mm)
    c.drawString(rev_x + pt(3), rev_y + rev_h - pt(22), 'A      2024-01-15    INITIAL RELEASE                       YN')
    c.drawString(rev_x + pt(3), rev_y + rev_h - pt(28), '—      —              —                                              —')

    # ─── DRAWING TITLE HEADER ──────────────────────────────────────────────────
    c.setFillColor(colors.HexColor('#1a1a2e'))
    c.rect(BORDER_M + pt(2), H - BORDER_M - pt(2) - pt(18),
           W - 2*BORDER_M - pt(4) - TB_W - pt(5), pt(18), fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 5*mm)
    c.drawString(BORDER_M + pt(8), H - BORDER_M - pt(13),
                 'MECHANICAL ENGINEERING — 2D ORTHOGRAPHIC DRAWING')
    c.setFont('Helvetica', 3*mm)
    c.drawString(BORDER_M + pt(8), H - BORDER_M - pt(18),
                 'Component: Flanged Shaft Coupling  |  Standard: BS 8888 / ISO 128  |  Units: mm')

    c.save()
    print(f"PDF saved: {fname}")
    return fname

generate_pdf()
