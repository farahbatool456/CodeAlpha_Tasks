"""
Residential Floor Plan Generator
Generates a professional 2D AutoCAD-compatible DXF floor plan
"""

import ezdxf
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment
import math

def create_floor_plan():
    doc = ezdxf.new(dxfversion='R2010')
    doc.header['$INSUNITS'] = 4  # mm
    doc.header['$LUNITS'] = 2    # decimal
    doc.header['$LUPREC'] = 0
    doc.header['$AUNITS'] = 0
    doc.header['$AUPREC'] = 0
    doc.header['$LIMMIN'] = (0, 0)
    doc.header['$LIMMAX'] = (20000, 15000)
    doc.header['$EXTMIN'] = (-500, -500, 0)
    doc.header['$EXTMAX'] = (20500, 15500, 0)

    msp = doc.modelspace()

    # ─── LAYER DEFINITIONS ────────────────────────────────────────────────────
    layers = {
        'A-WALL':        {'color': colors.WHITE,   'ltype': 'Continuous', 'lw': 50},
        'A-WALL-INT':    {'color': 8,               'ltype': 'Continuous', 'lw': 30},
        'A-DOOR':        {'color': colors.CYAN,     'ltype': 'Continuous', 'lw': 18},
        'A-WINDOW':      {'color': colors.CYAN,     'ltype': 'Continuous', 'lw': 18},
        'A-FURN':        {'color': colors.MAGENTA,  'ltype': 'Continuous', 'lw': 9},
        'A-ANNO-TEXT':   {'color': colors.YELLOW,   'ltype': 'Continuous', 'lw': 9},
        'A-ANNO-DIM':    {'color': colors.GREEN,    'ltype': 'Continuous', 'lw': 9},
        'A-HATCH':       {'color': 251,             'ltype': 'Continuous', 'lw': 9},
        'A-GRID':        {'color': 8,               'ltype': 'DASHED',     'lw': 9},
        'TITLEBLOCK':    {'color': colors.WHITE,    'ltype': 'Continuous', 'lw': 35},
    }

    # Ensure DASHED linetype exists
    if 'DASHED' not in doc.linetypes:
        doc.linetypes.add('DASHED', pattern=[0.5, -0.25])

    for name, props in layers.items():
        if name not in doc.layers:
            layer = doc.layers.add(name)
        else:
            layer = doc.layers.get(name)
        layer.color = props['color']
        layer.linetype = props['ltype']
        layer.lineweight = props['lw']

    # ─── TEXT STYLES ──────────────────────────────────────────────────────────
    if 'ARCH' not in doc.styles:
        doc.styles.add('ARCH', font='romans.shx')
    if 'ARCH-BOLD' not in doc.styles:
        doc.styles.add('ARCH-BOLD', font='romand.shx')

    # ─── DIMENSIONS ───────────────────────────────────────────────────────────
    dim_style = doc.dimstyles.new('ARCH-DIM')
    dim_style.dxf.dimasz = 100     # arrow size
    dim_style.dxf.dimtxt = 120     # text height
    dim_style.dxf.dimgap = 50
    dim_style.dxf.dimexo = 60      # extension line offset
    dim_style.dxf.dimexe = 80      # extension line extension
    dim_style.dxf.dimdli = 350
    dim_style.dxf.dimclrd = colors.GREEN
    dim_style.dxf.dimclre = colors.GREEN
    dim_style.dxf.dimclrt = colors.GREEN

    # ═══════════════════════════════════════════════════════════════════════════
    # FLOOR PLAN GEOMETRY
    # House: 14,400 wide × 10,800 tall  (exterior, to outside of walls)
    # Wall thickness: external = 230mm, internal = 115mm
    # Origin at bottom-left exterior corner
    # ═══════════════════════════════════════════════════════════════════════════
    ORIGIN_X, ORIGIN_Y = 1000, 1500   # drawing origin
    EW = 230    # external wall thickness
    IW = 115    # internal wall thickness
    HW = 14400  # house width (exterior)
    HH = 10800  # house height (exterior)

    # ── helpers ──────────────────────────────────────────────────────────────
    def rect(layer, x, y, w, h, closed=True):
        pts = [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]
        if closed:
            pts.append((x,y))
        msp.add_lwpolyline(pts, dxfattribs={'layer': layer, 'closed': True})

    def line(layer, x1, y1, x2, y2):
        msp.add_line((x1,y1,0),(x2,y2,0), dxfattribs={'layer':layer})

    def text(layer, txt, x, y, height=100, style='ARCH', align=TextEntityAlignment.MIDDLE_CENTER, rotation=0):
        msp.add_text(
            txt,
            dxfattribs={'layer':layer, 'height':height, 'style':style, 'rotation':rotation}
        ).set_placement((x,y), align=align)

    def room_label(name, area_str, cx, cy):
        text('A-ANNO-TEXT', name,     cx, cy+80,  height=140, style='ARCH-BOLD')
        text('A-ANNO-TEXT', area_str, cx, cy-80,  height=90,  style='ARCH')

    # ─── EXTERNAL WALLS (thick outline) ───────────────────────────────────────
    ox, oy = ORIGIN_X, ORIGIN_Y
    # Outer boundary
    rect('A-WALL', ox, oy, HW, HH)
    # Inner boundary
    rect('A-WALL', ox+EW, oy+EW, HW-2*EW, HH-2*EW)

    # Fill top/bottom walls
    # Bottom wall
    pts_b = [(ox,oy),(ox+HW,oy),(ox+HW,oy+EW),(ox,oy+EW),(ox,oy)]
    msp.add_lwpolyline(pts_b, dxfattribs={'layer':'A-WALL','closed':True})
    # Top wall
    pts_t = [(ox,oy+HH-EW),(ox+HW,oy+HH-EW),(ox+HW,oy+HH),(ox,oy+HH),(ox,oy+HH-EW)]
    msp.add_lwpolyline(pts_t, dxfattribs={'layer':'A-WALL','closed':True})
    # Left wall
    pts_l = [(ox,oy),(ox+EW,oy),(ox+EW,oy+HH),(ox,oy+HH),(ox,oy)]
    msp.add_lwpolyline(pts_l, dxfattribs={'layer':'A-WALL','closed':True})
    # Right wall
    pts_r = [(ox+HW-EW,oy),(ox+HW,oy),(ox+HW,oy+HH),(ox+HW-EW,oy+HH),(ox+HW-EW,oy)]
    msp.add_lwpolyline(pts_r, dxfattribs={'layer':'A-WALL','closed':True})

    # ═══════════════════════════════════════════════════════════════════════════
    # ROOM LAYOUT (coordinates relative to interior: ix, iy = ox+EW, oy+EW)
    #
    #  Interior space: 13940 × 10340
    #  ┌────────────────────────────────────────┐
    #  │   BEDROOM 1     │    BEDROOM 2         │  ← top row (H=4700)
    #  ├─────────────────┼──────────────────────┤
    #  │  LIVING ROOM    │ KITCHEN │ BATHROOM   │  ← bottom row (H=5640)
    #  └────────────────────────────────────────┘
    #  Vertical divider at X=7000 from interior left
    #  Horizontal divider at Y=4700 from interior bottom
    # ═══════════════════════════════════════════════════════════════════════════
    ix = ox + EW   # interior left
    iy = oy + EW   # interior bottom
    IW_SPACE = HW - 2*EW   # 13940
    IH_SPACE = HH - 2*EW   # 10340

    V_DIV  = 7000   # vertical divider x from ix (left/right split)
    H_DIV  = 4700   # horizontal divider y from iy (top/bottom split)

    # ── bottom right sub-division ─────────────────────────────────────────────
    # Kitchen and Bathroom share the right column bottom
    # Kitchen width = 4200, Bathroom = right column - 4200
    R_COL = IW_SPACE - V_DIV   # 6940
    KITCHEN_W = 4200
    BATH_W    = R_COL - KITCHEN_W  # 2740

    # ─── INTERNAL WALLS ───────────────────────────────────────────────────────
    # Horizontal divider (separates bedrooms from living/kitchen/bath)
    line('A-WALL-INT', ix,         iy+H_DIV, ix+IW_SPACE, iy+H_DIV)
    line('A-WALL-INT', ix,         iy+H_DIV+IW, ix+IW_SPACE, iy+H_DIV+IW)

    # Vertical main divider (separates left rooms from right rooms)
    line('A-WALL-INT', ix+V_DIV,   iy, ix+V_DIV, iy+IH_SPACE)
    line('A-WALL-INT', ix+V_DIV+IW,iy, ix+V_DIV+IW, iy+IH_SPACE)

    # Kitchen / Bathroom divider (right bottom column)
    kbx = ix + V_DIV + IW + KITCHEN_W
    line('A-WALL-INT', kbx,        iy, kbx, iy+H_DIV)
    line('A-WALL-INT', kbx+IW,     iy, kbx+IW, iy+H_DIV)

    # ─── ROOM CENTRES (for labels) ────────────────────────────────────────────
    # Living Room: left bottom
    lr_cx = ix + V_DIV/2
    lr_cy = iy + H_DIV/2
    # Bedroom 1: left top
    b1_cx = ix + V_DIV/2
    b1_cy = iy + H_DIV + IW + (IH_SPACE - H_DIV - IW)/2
    # Bedroom 2: right top
    b2_cx = ix + V_DIV + IW + R_COL/2
    b2_cy = b1_cy
    # Kitchen: right bottom left portion
    kt_cx = ix + V_DIV + IW + KITCHEN_W/2
    kt_cy = iy + H_DIV/2
    # Bathroom: right bottom right portion
    ba_cx = kbx + IW + BATH_W/2
    ba_cy = iy + H_DIV/2

    # ─── ROOM LABELS ─────────────────────────────────────────────────────────
    # Areas in m²
    def sq_m(w_mm, h_mm):
        return f"{(w_mm/1000)*(h_mm/1000):.1f} m²"

    room_label("LIVING ROOM",  sq_m(V_DIV, H_DIV),             lr_cx, lr_cy)
    room_label("BEDROOM 1",    sq_m(V_DIV, IH_SPACE-H_DIV-IW), b1_cx, b1_cy)
    room_label("BEDROOM 2",    sq_m(R_COL-IW, IH_SPACE-H_DIV-IW), b2_cx, b2_cy)
    room_label("KITCHEN",      sq_m(KITCHEN_W, H_DIV),         kt_cx, kt_cy)
    room_label("BATHROOM",     sq_m(BATH_W-IW, H_DIV),         ba_cx, ba_cy)

    # ─── DOORS ────────────────────────────────────────────────────────────────
    # Door helper: swing arc + gap
    def door(x, y, width=900, swing_dir='right', wall='h', rotation=0):
        """Draw a door symbol: clear gap + swing arc"""
        # gap in wall (shown as empty space — we just draw swing symbol)
        if wall == 'h':
            if swing_dir == 'right':
                # hinge at x, swing to x+width
                msp.add_arc(
                    center=(x, y, 0), radius=width,
                    start_angle=0, end_angle=90,
                    dxfattribs={'layer':'A-DOOR'}
                )
                line('A-DOOR', x, y, x, y+width)
                line('A-DOOR', x, y, x+width, y)
            else:
                msp.add_arc(
                    center=(x+width, y, 0), radius=width,
                    start_angle=90, end_angle=180,
                    dxfattribs={'layer':'A-DOOR'}
                )
                line('A-DOOR', x+width, y, x+width, y+width)
                line('A-DOOR', x, y, x+width, y)
        else:  # vertical wall
            if swing_dir == 'right':
                msp.add_arc(
                    center=(x, y+width, 0), radius=width,
                    start_angle=270, end_angle=360,
                    dxfattribs={'layer':'A-DOOR'}
                )
                line('A-DOOR', x, y, x+width, y)
                line('A-DOOR', x, y+width, x, y)
            else:
                msp.add_arc(
                    center=(x, y, 0), radius=width,
                    start_angle=0, end_angle=90,
                    dxfattribs={'layer':'A-DOOR'}
                )
                line('A-DOOR', x, y, x+width, y)
                line('A-DOOR', x, y, x, y+width)

    # Main entrance door (bottom wall, living room side)
    door_entrance_x = ox + 1200
    door(door_entrance_x, oy, width=900, swing_dir='right', wall='h')

    # Living → Bedroom 1 (vertical divider top)
    door(ix + V_DIV, iy + H_DIV + IW + 300, width=800, swing_dir='right', wall='v')

    # Living → Kitchen (horizontal divider, right side)
    door(ix + V_DIV + IW + 200, iy + H_DIV, width=800, swing_dir='right', wall='h')

    # Bedroom 1 private door (left wall, upper)
    door(ox, iy + H_DIV + IW + 800, width=800, swing_dir='right', wall='v')

    # Bedroom 2 door (horizontal divider, right column)
    door(ix + V_DIV + IW + 1500, iy + H_DIV, width=800, swing_dir='left', wall='h')

    # Bathroom door (kitchen/bath divider)
    door(kbx, iy + 300, width=750, swing_dir='right', wall='v')

    # ─── WINDOWS ──────────────────────────────────────────────────────────────
    def window(x, y, width=1200, wall='h'):
        if wall == 'h':
            # three lines: frame + glazing
            line('A-WINDOW', x, y, x+width, y)
            line('A-WINDOW', x, y+EW/2, x+width, y+EW/2)
            line('A-WINDOW', x, y+EW, x+width, y+EW)
            line('A-WINDOW', x, y, x, y+EW)
            line('A-WINDOW', x+width, y, x+width, y+EW)
        else:
            line('A-WINDOW', x, y, x, y+width)
            line('A-WINDOW', x+EW/2, y, x+EW/2, y+width)
            line('A-WINDOW', x+EW, y, x+EW, y+width)
            line('A-WINDOW', x, y, x+EW, y)
            line('A-WINDOW', x, y+width, x+EW, y+width)

    # Living room window (bottom wall)
    window(ox+2500, oy, width=1500, wall='h')
    # Bedroom 1 window (top wall)
    window(ox+1000, oy+HH-EW, width=1400, wall='h')
    # Bedroom 2 window (top wall)
    window(ox+8500, oy+HH-EW, width=1400, wall='h')
    # Bedroom 2 window (right wall)
    window(ox+HW-EW, iy+H_DIV+IW+800, width=1200, wall='v')
    # Kitchen window (right wall)
    window(ox+HW-EW, iy+500, width=1000, wall='v')
    # Bathroom window (bottom wall, small)
    window(kbx+IW+200, oy, width=600, wall='h')

    # ─── FURNITURE ────────────────────────────────────────────────────────────
    # ── Living Room ──
    # Sofa (L-shape): 2200×900 + 900×900
    rect('A-FURN', ix+300, iy+300, 2200, 900)
    rect('A-FURN', ix+300, iy+300, 900, 900+600)
    text('A-ANNO-TEXT', 'SOFA', ix+300+1100, iy+300+450, height=80)
    # Coffee table
    rect('A-FURN', ix+1000, iy+1400, 1000, 600)
    # TV unit
    rect('A-FURN', ix+300, iy+H_DIV-200, 2500, 150)
    text('A-ANNO-TEXT', 'TV UNIT', ix+300+1250, iy+H_DIV-125, height=80)
    # Dining table (4-seater)
    rect('A-FURN', ix+3500, iy+300, 1400, 800)
    text('A-ANNO-TEXT', 'DINING', ix+3500+700, iy+300+400, height=80)
    # Chairs around dining
    for cx_off in [0, 500, 1000]:
        rect('A-FURN', ix+3500+cx_off*0.5+150, iy+150, 450, 120)  # front
        rect('A-FURN', ix+3500+cx_off*0.5+150, iy+1020, 450, 120) # back

    # ── Bedroom 1 ──
    b1y = iy + H_DIV + IW
    b1h = IH_SPACE - H_DIV - IW
    # Double bed: 1800×2000
    bed_x = ix + 300
    bed_y = b1y + b1h - 2200
    rect('A-FURN', bed_x, bed_y, 1800, 2000)
    rect('A-FURN', bed_x, bed_y+1600, 1800, 400)  # headboard
    text('A-ANNO-TEXT', 'BED (DOUBLE)', bed_x+900, bed_y+1000, height=80)
    # Wardrobe
    rect('A-FURN', ix+300, b1y+200, 1800, 600)
    text('A-ANNO-TEXT', 'WARDROBE', ix+300+900, b1y+500, height=80)
    # Side table
    rect('A-FURN', ix+2200, bed_y+800, 500, 500)
    # Study desk
    rect('A-FURN', ix+3500, b1y+200, 1200, 600)
    text('A-ANNO-TEXT', 'DESK', ix+3500+600, b1y+500, height=80)

    # ── Bedroom 2 ──
    b2_ix = ix + V_DIV + IW
    b2_iw = R_COL - IW
    b2y = iy + H_DIV + IW
    b2h = IH_SPACE - H_DIV - IW
    # Single beds (twin)
    rect('A-FURN', b2_ix+300, b2y+b2h-2000, 1000, 1900)
    rect('A-FURN', b2_ix+300, b2y+b2h-2000+1500, 1000, 380)  # headboard
    text('A-ANNO-TEXT', 'BED', b2_ix+300+500, b2y+b2h-1000, height=80)
    rect('A-FURN', b2_ix+1500, b2y+b2h-2000, 1000, 1900)
    rect('A-FURN', b2_ix+1500, b2y+b2h-2000+1500, 1000, 380)
    text('A-ANNO-TEXT', 'BED', b2_ix+1500+500, b2y+b2h-1000, height=80)
    # Wardrobe
    rect('A-FURN', b2_ix+300, b2y+200, 2000, 600)
    text('A-ANNO-TEXT', 'WARDROBE', b2_ix+300+1000, b2y+500, height=80)
    # Desk
    rect('A-FURN', b2_ix+b2_iw-1400, b2y+200, 1000, 600)
    text('A-ANNO-TEXT', 'DESK', b2_ix+b2_iw-900, b2y+500, height=80)

    # ── Kitchen ──
    kt_ix = ix + V_DIV + IW
    # Counter along bottom wall: 400 deep
    rect('A-FURN', kt_ix+100, iy+100, KITCHEN_W-200, 600)
    text('A-ANNO-TEXT', 'COUNTER', kt_ix+100+KITCHEN_W/2-100, iy+400, height=80)
    # Counter along right
    rect('A-FURN', kt_ix+KITCHEN_W-600, iy+100, 600, 2500)
    # Sink symbol
    rect('A-FURN', kt_ix+KITCHEN_W-550, iy+2200, 450, 400)
    msp.add_circle((kt_ix+KITCHEN_W-325, iy+2400, 0), radius=80, dxfattribs={'layer':'A-FURN'})
    text('A-ANNO-TEXT', 'SINK', kt_ix+KITCHEN_W-325, iy+2600, height=75)
    # Stove (4 burners)
    rect('A-FURN', kt_ix+200, iy+1600, 800, 800)
    for bx in [kt_ix+370, kt_ix+570]:
        for by in [iy+1750, iy+1950+180]:
            msp.add_circle((bx, by, 0), radius=80, dxfattribs={'layer':'A-FURN'})
    text('A-ANNO-TEXT', 'STOVE', kt_ix+600, iy+2000, height=75)
    # Fridge
    rect('A-FURN', kt_ix+1500, iy+1600, 700, 800)
    text('A-ANNO-TEXT', 'FRIDGE', kt_ix+1850, iy+2000, height=75)

    # ── Bathroom ──
    ba_ix = kbx + IW
    ba_iw = BATH_W - IW
    # Bathtub
    rect('A-FURN', ba_ix+100, iy+H_DIV-1700, ba_iw-200, 1500)
    rect('A-FURN', ba_ix+200, iy+H_DIV-1600, ba_iw-400, 1200)
    text('A-ANNO-TEXT', 'BATHTUB', ba_ix+ba_iw/2, iy+H_DIV-1000, height=80)
    # Toilet
    rect('A-FURN', ba_ix+200, iy+200, 400, 600)
    msp.add_ellipse(
        center=(ba_ix+400, iy+550, 0),
        major_axis=(0, 350, 0),
        ratio=0.6,
        dxfattribs={'layer':'A-FURN'}
    )
    text('A-ANNO-TEXT', 'WC', ba_ix+400, iy+850, height=75)
    # Wash basin
    rect('A-FURN', ba_ix+100, iy+1200, 500, 500)
    msp.add_circle((ba_ix+350, iy+1450, 0), radius=60, dxfattribs={'layer':'A-FURN'})
    text('A-ANNO-TEXT', 'BASIN', ba_ix+350, iy+1800, height=75)

    # ─── DIMENSIONS ───────────────────────────────────────────────────────────
    dim_gap = 500
    dim_gap2 = 950

    # Overall width (bottom)
    dimmer = msp.add_linear_dim(
        base=(ox, oy - dim_gap2),
        p1=(ox, oy),
        p2=(ox+HW, oy),
        dimstyle='ARCH-DIM',
        dxfattribs={'layer': 'A-ANNO-DIM'}
    )
    dimmer.render()

    # Overall height (right)
    dimmer2 = msp.add_linear_dim(
        base=(ox+HW + dim_gap2, oy),
        p1=(ox+HW, oy),
        p2=(ox+HW, oy+HH),
        angle=90,
        dimstyle='ARCH-DIM',
        dxfattribs={'layer': 'A-ANNO-DIM'}
    )
    dimmer2.render()

    # Left column width (bottom)
    dimmer3 = msp.add_linear_dim(
        base=(ox, oy - dim_gap),
        p1=(ox, oy),
        p2=(ix+V_DIV, oy),
        dimstyle='ARCH-DIM',
        dxfattribs={'layer': 'A-ANNO-DIM'}
    )
    dimmer3.render()

    # Right column width
    dimmer4 = msp.add_linear_dim(
        base=(ix+V_DIV+IW, oy - dim_gap),
        p1=(ix+V_DIV+IW, oy),
        p2=(ox+HW, oy),
        dimstyle='ARCH-DIM',
        dxfattribs={'layer': 'A-ANNO-DIM'}
    )
    dimmer4.render()

    # Bottom row height (left side)
    dimmer5 = msp.add_linear_dim(
        base=(ox - dim_gap, oy),
        p1=(ox, oy),
        p2=(ox, iy+H_DIV),
        angle=90,
        dimstyle='ARCH-DIM',
        dxfattribs={'layer': 'A-ANNO-DIM'}
    )
    dimmer5.render()

    # Top row height
    dimmer6 = msp.add_linear_dim(
        base=(ox - dim_gap, iy+H_DIV+IW),
        p1=(ox, iy+H_DIV+IW),
        p2=(ox, oy+HH),
        angle=90,
        dimstyle='ARCH-DIM',
        dxfattribs={'layer': 'A-ANNO-DIM'}
    )
    dimmer6.render()

    # ─── NORTH ARROW ──────────────────────────────────────────────────────────
    na_x = ox + HW + 1800
    na_y = oy + HH - 1200
    # Arrow
    msp.add_arrow(
        name=ezdxf.ARROWS.closed_filled,
        insert=(na_x, na_y+600, 0),
        size=300,
        rotation=90,
        dxfattribs={'layer': 'TITLEBLOCK'}
    )
    msp.add_circle((na_x, na_y, 0), radius=400, dxfattribs={'layer': 'TITLEBLOCK'})
    text('TITLEBLOCK', 'N', na_x, na_y+200, height=220, style='ARCH-BOLD')

    # ─── TITLE BLOCK ──────────────────────────────────────────────────────────
    tb_x = ox
    tb_y = oy - 2200
    tb_w = HW
    tb_h = 1600

    # Border
    rect('TITLEBLOCK', tb_x, tb_y, tb_w, tb_h)
    # Dividers
    line('TITLEBLOCK', tb_x + tb_w*0.4, tb_y, tb_x + tb_w*0.4, tb_y + tb_h)
    line('TITLEBLOCK', tb_x + tb_w*0.4, tb_y + tb_h*0.5, tb_x + tb_w, tb_y + tb_h*0.5)

    # Title
    text('TITLEBLOCK', 'RESIDENTIAL FLOOR PLAN',
         tb_x + tb_w*0.2, tb_y + tb_h*0.6, height=220, style='ARCH-BOLD')
    text('TITLEBLOCK', '2-BEDROOM HOUSE  |  GROUND FLOOR',
         tb_x + tb_w*0.2, tb_y + tb_h*0.25, height=120, style='ARCH')

    # Info cells
    info = [
        ('PROJECT:', 'Residential House Design', tb_x + tb_w*0.45, tb_y + tb_h*0.78),
        ('DRAWN BY:', 'AutoCAD Intern',          tb_x + tb_w*0.45, tb_y + tb_h*0.58),
        ('DATE:',     '2025',                    tb_x + tb_w*0.72, tb_y + tb_h*0.78),
        ('SCALE:',    '1:50',                    tb_x + tb_w*0.72, tb_y + tb_h*0.58),
        ('SHEET:',    '01 of 01',                tb_x + tb_w*0.88, tb_y + tb_h*0.78),
        ('REV:',      'A',                       tb_x + tb_w*0.88, tb_y + tb_h*0.58),
        ('DRAWING NO:', 'RFP-2025-001',          tb_x + tb_w*0.58, tb_y + tb_h*0.25),
        ('STATUS:',   'FOR REVIEW',              tb_x + tb_w*0.80, tb_y + tb_h*0.25),
    ]
    for label, val, lx, ly in info:
        text('TITLEBLOCK', label, lx, ly+60,  height=80,  style='ARCH-BOLD',
             align=TextEntityAlignment.BOTTOM_LEFT)
        text('TITLEBLOCK', val,   lx, ly-40,  height=100, style='ARCH',
             align=TextEntityAlignment.BOTTOM_LEFT)

    # ─── DRAWING BORDER ───────────────────────────────────────────────────────
    border_margin = 200
    rect('TITLEBLOCK',
         ox - border_margin,
         tb_y - border_margin,
         HW + 2*border_margin + 2200,
         HH + tb_h + 2200 + 2*border_margin)

    # ─── LEGEND / NOTES ───────────────────────────────────────────────────────
    leg_x = ox + HW + 400
    leg_y = oy + 400
    text('TITLEBLOCK', 'LEGEND:', leg_x, leg_y + 2200, height=130, style='ARCH-BOLD',
         align=TextEntityAlignment.BOTTOM_LEFT)
    legend_items = [
        '── EXTERNAL WALL (230mm)',
        '── INTERNAL WALL (115mm)',
        '─ ─ DOOR SWING',
        '═══ WINDOW',
        '─── DIMENSION LINE',
    ]
    for i, item in enumerate(legend_items):
        text('A-ANNO-TEXT', item, leg_x, leg_y + 1900 - i*200, height=90, style='ARCH',
             align=TextEntityAlignment.BOTTOM_LEFT)

    text('TITLEBLOCK', 'NOTES:', leg_x, leg_y - 200, height=130, style='ARCH-BOLD',
         align=TextEntityAlignment.BOTTOM_LEFT)
    notes = [
        '1. ALL DIMENSIONS IN MILLIMETRES',
        '2. DO NOT SCALE FROM DRAWING',
        '3. VERIFY ON SITE BEFORE CONSTRUCTION',
        '4. WALL FINISH NOT SHOWN',
        '5. DRAWING SCALE: 1:50 @ A1',
    ]
    for i, note in enumerate(notes):
        text('A-ANNO-TEXT', note, leg_x, leg_y - 500 - i*200, height=90, style='ARCH',
             align=TextEntityAlignment.BOTTOM_LEFT)

    return doc

# ── SAVE ──────────────────────────────────────────────────────────────────────
doc = create_floor_plan()
out_path = '/mnt/user-data/outputs/residential_floor_plan.dxf'
doc.saveas(out_path)
print(f"DXF saved: {out_path}")
