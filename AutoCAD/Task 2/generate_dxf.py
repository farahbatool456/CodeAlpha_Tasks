"""
AutoCAD-Compatible DXF Generator
Component: Flanged Shaft Coupling (2D Mechanical Drawing)
Standard: ISO/ASME Y14.5 Dimensioning Practices
"""

import ezdxf
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment
import math

def create_mechanical_drawing():
    doc = ezdxf.new(dxfversion='R2010')
    doc.header['$INSUNITS'] = 4  # mm
    doc.header['$MEASUREMENT'] = 1  # metric

    # ─── LAYERS ────────────────────────────────────────────────────────────────
    layers = {
        'OBJECT':       {'color': colors.WHITE,      'ltype': 'Continuous', 'lw': 50},
        'HIDDEN':       {'color': colors.BLUE,        'ltype': 'DASHED',     'lw': 18},
        'CENTER':       {'color': colors.RED,         'ltype': 'CENTER',     'lw': 18},
        'DIMENSION':    {'color': colors.YELLOW,      'ltype': 'Continuous', 'lw': 18},
        'ANNOTATION':   {'color': colors.CYAN,        'ltype': 'Continuous', 'lw': 18},
        'TITLEBLOCK':   {'color': colors.WHITE,       'ltype': 'Continuous', 'lw': 70},
        'HATCH':        {'color': colors.MAGENTA,     'ltype': 'Continuous', 'lw': 13},
        'VIEWPORT':     {'color': colors.GREEN,       'ltype': 'Continuous', 'lw': 18},
        'BORDER':       {'color': colors.WHITE,       'ltype': 'Continuous', 'lw': 70},
    }

    # Load linetype definitions
    for ltype in ['DASHED', 'CENTER']:
        if ltype not in doc.linetypes:
            try:
                doc.linetypes.add(ltype, pattern=[0.5, -0.25] if ltype == 'DASHED' else [1.0, -0.25, 0.0, -0.25])
            except Exception:
                pass

    for name, props in layers.items():
        if name not in doc.layers:
            layer = doc.layers.add(name)
            layer.color = props['color']
            layer.linetype = props.get('ltype', 'Continuous')
            layer.lineweight = props['lw']

    msp = doc.modelspace()

    # ─── DIMSTYLE ──────────────────────────────────────────────────────────────
    if 'MECH_DIM' not in doc.dimstyles:
        dimstyle = doc.dimstyles.new('MECH_DIM')
    else:
        dimstyle = doc.dimstyles.get('MECH_DIM')
    dimstyle.dxf.dimtxt = 3.5
    dimstyle.dxf.dimasz = 3.0
    dimstyle.dxf.dimexo = 1.5
    dimstyle.dxf.dimexe = 2.5
    dimstyle.dxf.dimgap = 1.0
    dimstyle.dxf.dimdec = 1

    # ═══════════════════════════════════════════════════════════════════════════
    # COMPONENT: FLANGED SHAFT COUPLING
    # Dimensions (mm): OD=120, Hub OD=60, Bore=30, PCD=90, BoltHoles=6xM10
    # ═══════════════════════════════════════════════════════════════════════════

    # ─── VIEW ORIGINS ──────────────────────────────────────────────────────────
    FV = (160, 200)   # Front View centre
    TV = (160, 380)   # Top View centre  (above front)
    SV = (340, 200)   # Side View centre (right of front)

    # ─── FRONT VIEW ────────────────────────────────────────────────────────────
    # Outer flange rectangle (120mm dia → width=120, height=20 thick)
    fw, fh = 120, 20
    flange_rect = [
        (FV[0]-fw/2, FV[1]-fh/2),
        (FV[0]+fw/2, FV[1]-fh/2),
        (FV[0]+fw/2, FV[1]+fh/2),
        (FV[0]-fw/2, FV[1]+fh/2),
        (FV[0]-fw/2, FV[1]-fh/2),
    ]
    msp.add_lwpolyline(flange_rect, dxfattribs={'layer': 'OBJECT', 'lineweight': 50})

    # Hub (dia=60, height=40 total protruding 20mm beyond flange)
    hw, hh = 60, 40
    hub_rect = [
        (FV[0]-hw/2, FV[1]-hh/2),
        (FV[0]+hw/2, FV[1]-hh/2),
        (FV[0]+hw/2, FV[1]+hh/2),
        (FV[0]-hw/2, FV[1]+hh/2),
        (FV[0]-hw/2, FV[1]-hh/2),
    ]
    msp.add_lwpolyline(hub_rect, dxfattribs={'layer': 'OBJECT', 'lineweight': 50})

    # Bore hole (dia=30, shown as hidden in front view)
    bw = 30
    bore_lines_fv = [
        [(FV[0]-bw/2, FV[1]-hh/2), (FV[0]-bw/2, FV[1]+hh/2)],
        [(FV[0]+bw/2, FV[1]-hh/2), (FV[0]+bw/2, FV[1]+hh/2)],
    ]
    for line in bore_lines_fv:
        msp.add_line(line[0], line[1], dxfattribs={'layer': 'HIDDEN', 'lineweight': 18, 'linetype': 'DASHED'})

    # Center lines - Front View
    msp.add_line((FV[0]-75, FV[1]), (FV[0]+75, FV[1]),
                 dxfattribs={'layer': 'CENTER', 'linetype': 'CENTER', 'lineweight': 18})
    msp.add_line((FV[0], FV[1]-35), (FV[0], FV[1]+35),
                 dxfattribs={'layer': 'CENTER', 'linetype': 'CENTER', 'lineweight': 18})

    # Keyway in hub (6mm wide, 3mm deep) - front view
    kw, kd = 6, 3
    keyway_fv = [
        (FV[0]-kw/2, FV[1]+hh/2),
        (FV[0]-kw/2, FV[1]+hh/2+kd),
        (FV[0]+kw/2, FV[1]+hh/2+kd),
        (FV[0]+kw/2, FV[1]+hh/2),
    ]
    msp.add_lwpolyline(keyway_fv, dxfattribs={'layer': 'OBJECT', 'lineweight': 50})

    # Section hatch lines on flange in front view (indicate cut section)
    hatch_fv = msp.add_hatch(color=colors.MAGENTA, dxfattribs={'layer': 'HATCH'})
    hatch_fv.set_pattern_fill('ANSI31', scale=2.0, angle=45)
    hatch_fv.paths.add_polyline_path(
        [(FV[0]-fw/2, FV[1]-fh/2), (FV[0]-hw/2, FV[1]-fh/2),
         (FV[0]-hw/2, FV[1]+fh/2), (FV[0]-fw/2, FV[1]+fh/2)], is_closed=True)
    # Right flange section  
    hatch_fv2 = msp.add_hatch(color=colors.MAGENTA, dxfattribs={'layer': 'HATCH'})
    hatch_fv2.set_pattern_fill('ANSI31', scale=2.0, angle=45)
    hatch_fv2.paths.add_polyline_path(
        [(FV[0]+hw/2, FV[1]-fh/2), (FV[0]+fw/2, FV[1]-fh/2),
         (FV[0]+fw/2, FV[1]+fh/2), (FV[0]+hw/2, FV[1]+fh/2)], is_closed=True)

    # ─── FRONT VIEW DIMENSIONS ─────────────────────────────────────────────────
    # Overall width (OD = 120)
    dim1 = msp.add_linear_dim(
        base=(FV[0], FV[1]-fh/2-15),
        p1=(FV[0]-fw/2, FV[1]-fh/2),
        p2=(FV[0]+fw/2, FV[1]-fh/2),
        dimstyle='MECH_DIM',
        override={'dimpost': '%%C<>', 'dimupt': 0},
        dxfattribs={'layer': 'DIMENSION'}
    )
    dim1.set_text('%%C120')
    dim1.render()

    # Hub width (60mm)
    dim2 = msp.add_linear_dim(
        base=(FV[0], FV[1]-hh/2-30),
        p1=(FV[0]-hw/2, FV[1]-hh/2),
        p2=(FV[0]+hw/2, FV[1]-hh/2),
        dimstyle='MECH_DIM',
        dxfattribs={'layer': 'DIMENSION'}
    )
    dim2.set_text('%%C60')
    dim2.render()

    # Overall height (40mm hub)
    dim3 = msp.add_linear_dim(
        base=(FV[0]+fw/2+18, FV[1]),
        p1=(FV[0]+hw/2, FV[1]-hh/2),
        p2=(FV[0]+hw/2, FV[1]+hh/2),
        angle=90,
        dimstyle='MECH_DIM',
        dxfattribs={'layer': 'DIMENSION'}
    )
    dim3.set_text('40')
    dim3.render()

    # Flange thickness (20mm)
    dim4 = msp.add_linear_dim(
        base=(FV[0]+fw/2+35, FV[1]),
        p1=(FV[0]+fw/2, FV[1]-fh/2),
        p2=(FV[0]+fw/2, FV[1]+fh/2),
        angle=90,
        dimstyle='MECH_DIM',
        dxfattribs={'layer': 'DIMENSION'}
    )
    dim4.set_text('20')
    dim4.render()

    # Bore diameter (hidden dim)
    dim5 = msp.add_linear_dim(
        base=(FV[0], FV[1]+hh/2+18),
        p1=(FV[0]-bw/2, FV[1]+hh/2),
        p2=(FV[0]+bw/2, FV[1]+hh/2),
        dimstyle='MECH_DIM',
        dxfattribs={'layer': 'DIMENSION'}
    )
    dim5.set_text('%%C30 BORE')
    dim5.render()

    # VIEW LABEL
    msp.add_text('FRONT VIEW (SECTION A-A)',
                 dxfattribs={'layer': 'ANNOTATION', 'height': 4,
                             'insert': (FV[0]-30, FV[1]-hh/2-50),
                             'style': 'Standard'})

    # ─── TOP VIEW ──────────────────────────────────────────────────────────────
    # Flange face (circular view) — outer circle OD=120
    msp.add_circle(TV, 60, dxfattribs={'layer': 'OBJECT', 'lineweight': 50})
    # Hub circle OD=60
    msp.add_circle(TV, 30, dxfattribs={'layer': 'OBJECT', 'lineweight': 50})
    # Bore circle OD=30 (hidden)
    msp.add_circle(TV, 15, dxfattribs={'layer': 'HIDDEN', 'lineweight': 18, 'linetype': 'DASHED'})

    # PCD circle (pitch circle dia=90) — 6 bolt holes
    msp.add_circle(TV, 45, dxfattribs={'layer': 'CENTER', 'linetype': 'CENTER', 'lineweight': 13})

    # 6 bolt holes (M10 = dia 10) on PCD=90
    num_bolts = 6
    bolt_r = 5  # hole radius
    pcd_r = 45
    bolt_angles = [i * 360/num_bolts for i in range(num_bolts)]
    for angle in bolt_angles:
        rad = math.radians(angle)
        cx = TV[0] + pcd_r * math.cos(rad)
        cy = TV[1] + pcd_r * math.sin(rad)
        msp.add_circle((cx, cy), bolt_r, dxfattribs={'layer': 'OBJECT', 'lineweight': 35})
        # small center cross for each bolt hole
        msp.add_line((cx-7, cy), (cx+7, cy),
                     dxfattribs={'layer': 'CENTER', 'linetype': 'CENTER', 'lineweight': 13})
        msp.add_line((cx, cy-7), (cx, cy+7),
                     dxfattribs={'layer': 'CENTER', 'linetype': 'CENTER', 'lineweight': 13})

    # Center lines — Top View
    msp.add_line((TV[0]-80, TV[1]), (TV[0]+80, TV[1]),
                 dxfattribs={'layer': 'CENTER', 'linetype': 'CENTER', 'lineweight': 18})
    msp.add_line((TV[0], TV[1]-80), (TV[0], TV[1]+80),
                 dxfattribs={'layer': 'CENTER', 'linetype': 'CENTER', 'lineweight': 18})

    # Keyway in top view (at 90 deg, top)
    msp.add_line((TV[0]-kw/2, TV[1]+30), (TV[0]-kw/2, TV[1]+30+kd),
                 dxfattribs={'layer': 'OBJECT', 'lineweight': 50})
    msp.add_line((TV[0]+kw/2, TV[1]+30), (TV[0]+kw/2, TV[1]+30+kd),
                 dxfattribs={'layer': 'OBJECT', 'lineweight': 50})
    msp.add_line((TV[0]-kw/2, TV[1]+30+kd), (TV[0]+kw/2, TV[1]+30+kd),
                 dxfattribs={'layer': 'OBJECT', 'lineweight': 50})

    # TOP VIEW DIMENSIONS
    # OD dimension
    dim_tv1 = msp.add_diameter_dim(
        center=TV,
        radius=60,
        angle=45,
        dimstyle='MECH_DIM',
        dxfattribs={'layer': 'DIMENSION'}
    )
    dim_tv1.set_text('%%C120')
    dim_tv1.render()

    # Hub OD
    dim_tv2 = msp.add_diameter_dim(
        center=TV,
        radius=30,
        angle=135,
        dimstyle='MECH_DIM',
        dxfattribs={'layer': 'DIMENSION'}
    )
    dim_tv2.set_text('%%C60')
    dim_tv2.render()

    # PCD
    dim_tv3 = msp.add_diameter_dim(
        center=TV,
        radius=45,
        angle=225,
        dimstyle='MECH_DIM',
        dxfattribs={'layer': 'DIMENSION'}
    )
    dim_tv3.set_text('PCD %%C90')
    dim_tv3.render()

    # Bore
    dim_tv4 = msp.add_diameter_dim(
        center=TV,
        radius=15,
        angle=315,
        dimstyle='MECH_DIM',
        dxfattribs={'layer': 'DIMENSION'}
    )
    dim_tv4.set_text('%%C30 BORE')
    dim_tv4.render()

    msp.add_text('TOP VIEW',
                 dxfattribs={'layer': 'ANNOTATION', 'height': 4,
                             'insert': (TV[0]-10, TV[1]+75),
                             'style': 'Standard'})

    # Bolt hole note
    msp.add_text('6 x M10 HOLES EQUI-SPACED ON PCD',
                 dxfattribs={'layer': 'ANNOTATION', 'height': 3,
                             'insert': (TV[0]+65, TV[1]+20),
                             'style': 'Standard'})
    # Leader line for note
    msp.add_line((TV[0]+65, TV[1]+22), (TV[0]+pcd_r+bolt_r+2, TV[1]+5),
                 dxfattribs={'layer': 'ANNOTATION'})

    # ─── SIDE VIEW (RIGHT SIDE) ────────────────────────────────────────────────
    # Side view shows hub profile + bore
    # Hub: 60 wide, 40 tall
    sv_hw, sv_hh = 60, 40
    hub_side = [
        (SV[0]-sv_hw/2, SV[1]-sv_hh/2),
        (SV[0]+sv_hw/2, SV[1]-sv_hh/2),
        (SV[0]+sv_hw/2, SV[1]+sv_hh/2),
        (SV[0]-sv_hw/2, SV[1]+sv_hh/2),
        (SV[0]-sv_hw/2, SV[1]-sv_hh/2),
    ]
    msp.add_lwpolyline(hub_side, dxfattribs={'layer': 'OBJECT', 'lineweight': 50})

    # Flange shown as hidden lines (behind hub in side view, 20mm thick)
    sv_fw, sv_fh = 20, 120
    for y in [SV[1]-sv_fh/2, SV[1]+sv_fh/2]:
        msp.add_line((SV[0]-sv_hw/2, y), (SV[0]-sv_hw/2-sv_fw, y),
                     dxfattribs={'layer': 'HIDDEN', 'linetype': 'DASHED', 'lineweight': 18})
    msp.add_line((SV[0]-sv_hw/2-sv_fw, SV[1]-sv_fh/2),
                 (SV[0]-sv_hw/2-sv_fw, SV[1]+sv_fh/2),
                 dxfattribs={'layer': 'HIDDEN', 'linetype': 'DASHED', 'lineweight': 18})

    # Bore hidden lines in side view
    bore_off = 15
    for x in [SV[0]-bore_off, SV[0]+bore_off]:
        msp.add_line((x, SV[1]-sv_hh/2), (x, SV[1]+sv_hh/2),
                     dxfattribs={'layer': 'HIDDEN', 'linetype': 'DASHED', 'lineweight': 18})

    # Keyway top of hub side view
    msp.add_line((SV[0]-kw/2, SV[1]+sv_hh/2), (SV[0]-kw/2, SV[1]+sv_hh/2+kd),
                 dxfattribs={'layer': 'OBJECT', 'lineweight': 50})
    msp.add_line((SV[0]+kw/2, SV[1]+sv_hh/2), (SV[0]+kw/2, SV[1]+sv_hh/2+kd),
                 dxfattribs={'layer': 'OBJECT', 'lineweight': 50})
    msp.add_line((SV[0]-kw/2, SV[1]+sv_hh/2+kd), (SV[0]+kw/2, SV[1]+sv_hh/2+kd),
                 dxfattribs={'layer': 'OBJECT', 'lineweight': 50})

    # Center lines — Side View
    msp.add_line((SV[0]-45, SV[1]), (SV[0]+45, SV[1]),
                 dxfattribs={'layer': 'CENTER', 'linetype': 'CENTER', 'lineweight': 18})
    msp.add_line((SV[0], SV[1]-50), (SV[0], SV[1]+50),
                 dxfattribs={'layer': 'CENTER', 'linetype': 'CENTER', 'lineweight': 18})

    # Section hatch on hub in side view
    hatch_sv = msp.add_hatch(color=colors.MAGENTA, dxfattribs={'layer': 'HATCH'})
    hatch_sv.set_pattern_fill('ANSI31', scale=2.0, angle=45)
    hatch_sv.paths.add_polyline_path(
        [(SV[0]-sv_hw/2, SV[1]-sv_hh/2), (SV[0]-bore_off, SV[1]-sv_hh/2),
         (SV[0]-bore_off, SV[1]+sv_hh/2), (SV[0]-sv_hw/2, SV[1]+sv_hh/2)], is_closed=True)
    hatch_sv2 = msp.add_hatch(color=colors.MAGENTA, dxfattribs={'layer': 'HATCH'})
    hatch_sv2.set_pattern_fill('ANSI31', scale=2.0, angle=45)
    hatch_sv2.paths.add_polyline_path(
        [(SV[0]+bore_off, SV[1]-sv_hh/2), (SV[0]+sv_hw/2, SV[1]-sv_hh/2),
         (SV[0]+sv_hw/2, SV[1]+sv_hh/2), (SV[0]+bore_off, SV[1]+sv_hh/2)], is_closed=True)

    # Side view dimensions
    dim_sv1 = msp.add_linear_dim(
        base=(SV[0]+sv_hw/2+18, SV[1]),
        p1=(SV[0]+sv_hw/2, SV[1]-sv_hh/2),
        p2=(SV[0]+sv_hw/2, SV[1]+sv_hh/2),
        angle=90,
        dimstyle='MECH_DIM',
        dxfattribs={'layer': 'DIMENSION'}
    )
    dim_sv1.set_text('40')
    dim_sv1.render()

    dim_sv2 = msp.add_linear_dim(
        base=(SV[0], SV[1]-sv_hh/2-15),
        p1=(SV[0]-sv_hw/2, SV[1]-sv_hh/2),
        p2=(SV[0]+sv_hw/2, SV[1]-sv_hh/2),
        dimstyle='MECH_DIM',
        dxfattribs={'layer': 'DIMENSION'}
    )
    dim_sv2.set_text('60')
    dim_sv2.render()

    msp.add_text('SIDE VIEW',
                 dxfattribs={'layer': 'ANNOTATION', 'height': 4,
                             'insert': (SV[0]-12, SV[1]-sv_hh/2-50),
                             'style': 'Standard'})

    # ─── PROJECTION LINES ──────────────────────────────────────────────────────
    # Vertical from Front View to Top View
    for x in [FV[0]-fw/2, FV[0]+fw/2]:
        msp.add_line((x, FV[1]+fh/2+5), (x, TV[1]-70),
                     dxfattribs={'layer': 'VIEWPORT', 'linetype': 'DASHED', 'lineweight': 13})
    # Horizontal from Front View to Side View
    for y in [FV[1]-fh/2, FV[1]+fh/2]:
        msp.add_line((FV[0]+fw/2+5, y), (SV[0]-sv_hw/2-sv_fw-5, y),
                     dxfattribs={'layer': 'VIEWPORT', 'linetype': 'DASHED', 'lineweight': 13})

    # ─── SECTION CUT LINE (A-A) ────────────────────────────────────────────────
    cut_y = TV[1]
    msp.add_line((TV[0]-90, cut_y), (TV[0]-65, cut_y),
                 dxfattribs={'layer': 'ANNOTATION', 'lineweight': 50})
    msp.add_line((TV[0]+65, cut_y), (TV[0]+90, cut_y),
                 dxfattribs={'layer': 'ANNOTATION', 'lineweight': 50})
    msp.add_text('A', dxfattribs={'layer': 'ANNOTATION', 'height': 5,
                                  'insert': (TV[0]-95, cut_y-3), 'style': 'Standard'})
    msp.add_text('A', dxfattribs={'layer': 'ANNOTATION', 'height': 5,
                                  'insert': (TV[0]+90, cut_y-3), 'style': 'Standard'})

    # ─── SURFACE FINISH SYMBOL ─────────────────────────────────────────────────
    # On bore surface (right side of front view hub)
    sf_x, sf_y = FV[0]+hw/2+5, FV[1]+5
    msp.add_line((sf_x, sf_y), (sf_x+8, sf_y+8), dxfattribs={'layer': 'ANNOTATION'})
    msp.add_line((sf_x+8, sf_y+8), (sf_x+15, sf_y+8), dxfattribs={'layer': 'ANNOTATION'})
    msp.add_text('Ra 1.6', dxfattribs={'layer': 'ANNOTATION', 'height': 2.5,
                                        'insert': (sf_x+10, sf_y+9), 'style': 'Standard'})

    # ─── GENERAL TOLERANCE NOTE ────────────────────────────────────────────────
    msp.add_text('GENERAL TOLERANCES: ISO 2768-m',
                 dxfattribs={'layer': 'ANNOTATION', 'height': 3,
                             'insert': (50, 90), 'style': 'Standard'})
    msp.add_text('UNLESS OTHERWISE STATED, ALL DIM IN mm',
                 dxfattribs={'layer': 'ANNOTATION', 'height': 3,
                             'insert': (50, 83), 'style': 'Standard'})
    msp.add_text('MATERIAL: CAST IRON (GRADE 250)',
                 dxfattribs={'layer': 'ANNOTATION', 'height': 3,
                             'insert': (50, 76), 'style': 'Standard'})
    msp.add_text('FINISH: MACHINED SURFACES Ra 1.6',
                 dxfattribs={'layer': 'ANNOTATION', 'height': 3,
                             'insert': (50, 69), 'style': 'Standard'})
    msp.add_text('TREATMENT: GREY PRIMER COAT',
                 dxfattribs={'layer': 'ANNOTATION', 'height': 3,
                             'insert': (50, 62), 'style': 'Standard'})

    # ─── TITLE BLOCK ───────────────────────────────────────────────────────────
    # A1 sheet border (841 x 594)
    W, H = 841, 594

    # Sheet border (outer)
    msp.add_lwpolyline(
        [(0,0),(W,0),(W,H),(0,H),(0,0)],
        dxfattribs={'layer': 'BORDER', 'lineweight': 70}
    )
    # Inner margin
    msp.add_lwpolyline(
        [(10,10),(W-10,10),(W-10,H-10),(10,H-10),(10,10)],
        dxfattribs={'layer': 'BORDER', 'lineweight': 35}
    )

    # Title block box (bottom right)
    tb_x, tb_y = W-10-200, 10
    tb_w, tb_h = 200, 100

    title_block = [
        (tb_x, tb_y), (tb_x+tb_w, tb_y),
        (tb_x+tb_w, tb_y+tb_h), (tb_x, tb_y+tb_h), (tb_x, tb_y)
    ]
    msp.add_lwpolyline(title_block, dxfattribs={'layer': 'TITLEBLOCK', 'lineweight': 70})

    # Title block internal dividers
    rows = [tb_y+20, tb_y+35, tb_y+50, tb_y+65, tb_y+80]
    for ry in rows:
        msp.add_line((tb_x, ry), (tb_x+tb_w, ry), dxfattribs={'layer': 'TITLEBLOCK', 'lineweight': 18})

    # Vertical divider
    msp.add_line((tb_x+90, tb_y), (tb_x+90, tb_y+80), dxfattribs={'layer': 'TITLEBLOCK', 'lineweight': 18})

    # Title block content
    entries = [
        # (x_offset_from_tb_x, y_offset_from_tb_y, text, height)
        (5, 83, 'DRAWN BY:', 2.5),
        (95, 83, 'YOUR NAME', 3.5),
        (5, 68, 'CHECKED BY:', 2.5),
        (95, 68, '—', 3.5),
        (5, 53, 'DATE:', 2.5),
        (95, 53, '2024-01-15', 3.5),
        (5, 38, 'SCALE:', 2.5),
        (95, 38, '1:2', 3.5),
        (5, 23, 'DWG NO:', 2.5),
        (95, 23, 'MEC-001', 3.5),
        (5, 8, 'SHEET:', 2.5),
        (95, 8, '1 OF 1', 3.5),
    ]
    for ex, ey, et, eh in entries:
        msp.add_text(et, dxfattribs={'layer': 'TITLEBLOCK', 'height': eh,
                                     'insert': (tb_x+ex, tb_y+ey), 'style': 'Standard'})

    # Component name (large text above title block)
    msp.add_text('FLANGED SHAFT COUPLING',
                 dxfattribs={'layer': 'TITLEBLOCK', 'height': 7,
                             'insert': (tb_x+5, tb_y+tb_h+15), 'style': 'Standard'})
    msp.add_text('ORTHOGRAPHIC PROJECTION — 3rd ANGLE',
                 dxfattribs={'layer': 'TITLEBLOCK', 'height': 4,
                             'insert': (tb_x+5, tb_y+tb_h+5), 'style': 'Standard'})

    # 3rd angle projection symbol (simple text representation)
    msp.add_text('[3rd ANGLE]',
                 dxfattribs={'layer': 'TITLEBLOCK', 'height': 3.5,
                             'insert': (tb_x+130, tb_y+tb_h+8), 'style': 'Standard'})

    # ─── REVISION BLOCK ────────────────────────────────────────────────────────
    rev_x, rev_y = W-10-200, 10+tb_h+30
    msp.add_lwpolyline(
        [(rev_x, rev_y),(rev_x+200, rev_y),(rev_x+200, rev_y+35),(rev_x, rev_y+35),(rev_x, rev_y)],
        dxfattribs={'layer': 'TITLEBLOCK', 'lineweight': 35}
    )
    msp.add_text('REVISION HISTORY',
                 dxfattribs={'layer': 'TITLEBLOCK', 'height': 4,
                             'insert': (rev_x+55, rev_y+27), 'style': 'Standard'})
    msp.add_line((rev_x, rev_y+20), (rev_x+200, rev_y+20),
                 dxfattribs={'layer': 'TITLEBLOCK', 'lineweight': 13})
    msp.add_text('REV  DATE           DESCRIPTION              BY',
                 dxfattribs={'layer': 'TITLEBLOCK', 'height': 2.5,
                             'insert': (rev_x+3, rev_y+14), 'style': 'Standard'})
    msp.add_text('A    2024-01-15    INITIAL RELEASE          YN',
                 dxfattribs={'layer': 'TITLEBLOCK', 'height': 2.5,
                             'insert': (rev_x+3, rev_y+6), 'style': 'Standard'})

    return doc

# ─── SAVE ──────────────────────────────────────────────────────────────────────
doc = create_mechanical_drawing()
doc.saveas('/home/claude/MEC-001_Flanged_Shaft_Coupling.dxf')
print("DXF saved successfully.")
