"""
Floor Plan PDF Renderer
Renders a publication-quality PDF of the residential floor plan
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Arc, Rectangle, Circle, Ellipse
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe
import numpy as np

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
EW   = 0.230   # external wall m
IW   = 0.115   # internal wall m
HW   = 14.400  # house width m
HH   = 10.800  # house height m
V_DIV = 7.000
H_DIV = 4.700
R_COL = HW - 2*EW - V_DIV
KITCHEN_W = 4.200
BATH_W    = R_COL - KITCHEN_W
ix = EW; iy = EW
IW_SPACE = HW - 2*EW
IH_SPACE = HH - 2*EW

kbx = ix + V_DIV + IW + KITCHEN_W

# ── COLORS ───────────────────────────────────────────────────────────────────
C_WALL      = '#1a1a2e'
C_WALL_INT  = '#2d3561'
C_WALL_FILL = '#c8d3e8'
C_FLOOR     = '#f7f4ef'
C_FLOOR2    = '#eef0f8'
C_DOOR      = '#c0392b'
C_WINDOW    = '#2980b9'
C_FURN      = '#7f8c8d'
C_FURN_FILL = '#dfe6e9'
C_DIM       = '#27ae60'
C_TEXT      = '#2c3e50'
C_LABEL     = '#1a1a2e'
C_TITLE     = '#1a1a2e'
C_BORDER    = '#2c3e50'
C_NORTH     = '#c0392b'
C_GRID      = '#b2bec3'

# ── FIGURE SETUP ─────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(20, 15.5), facecolor='#f0ece4')
ax = fig.add_axes([0.05, 0.13, 0.68, 0.84])  # main drawing area
ax.set_facecolor(C_FLOOR)
ax.set_xlim(-1.5, HW+3.5)
ax.set_ylim(-2.8, HH+1.2)
ax.set_aspect('equal')
ax.axis('off')

# ── HELPERS ──────────────────────────────────────────────────────────────────
def rect_patch(ax, x, y, w, h, fc, ec, lw=1.2, alpha=1.0, zorder=1, ls='-'):
    p = Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, ls=ls, alpha=alpha, zorder=zorder)
    ax.add_patch(p)
    return p

def line(ax, x1, y1, x2, y2, color=C_WALL, lw=1.0, ls='-', zorder=2):
    ax.plot([x1,x2],[y1,y2], color=color, lw=lw, ls=ls, zorder=zorder, solid_capstyle='round')

def dim_line(ax, x1, y1, x2, y2, label, orient='h', offset=0.5):
    """Draw dimension line with arrows and text"""
    color = C_DIM
    lw = 0.9
    if orient == 'h':
        y = y1 - offset
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='<->', color=color, lw=lw))
        # Extension lines
        ax.plot([x1,x1],[y1,y-0.05], color=color, lw=0.7, ls='--')
        ax.plot([x2,x2],[y2,y-0.05], color=color, lw=0.7, ls='--')
        ax.text((x1+x2)/2, y-0.18, label, ha='center', va='top',
                fontsize=6.5, color=color, fontfamily='monospace',
                fontweight='bold')
    else:
        x = x1 + offset
        ax.annotate('', xy=(x, y2), xytext=(x, y1),
                    arrowprops=dict(arrowstyle='<->', color=color, lw=lw))
        ax.plot([x1,x+0.05],[y1,y1], color=color, lw=0.7, ls='--')
        ax.plot([x2,x+0.05],[y2,y2], color=color, lw=0.7, ls='--')
        ax.text(x+0.18, (y1+y2)/2, label, ha='left', va='center',
                fontsize=6.5, color=color, fontfamily='monospace',
                fontweight='bold', rotation=90)

def room_label(ax, name, area, cx, cy):
    ax.text(cx, cy+0.12, name, ha='center', va='center',
            fontsize=8.5, color=C_LABEL, fontweight='bold',
            fontfamily='DejaVu Sans')
    ax.text(cx, cy-0.18, area, ha='center', va='center',
            fontsize=7, color='#546e7a', fontfamily='monospace')

def furn_rect(ax, x, y, w, h, label=None):
    rect_patch(ax, x, y, w, h, fc=C_FURN_FILL, ec=C_FURN, lw=0.7, zorder=4)
    if label:
        ax.text(x+w/2, y+h/2, label, ha='center', va='center',
                fontsize=5.5, color=C_FURN, fontfamily='monospace', zorder=5)

# ═════════════════════════════════════════════════════════════════════════════
# DRAW FLOOR FILL
# ═════════════════════════════════════════════════════════════════════════════
# Interior floor
rect_patch(ax, ix, iy, IW_SPACE, IH_SPACE, fc=C_FLOOR, ec='none', zorder=0)

# Room tints
for (rx, ry, rw, rh, col) in [
    (ix, iy+H_DIV+IW,       V_DIV-IW/2, IH_SPACE-H_DIV-IW, '#e8f4f8'),   # bed1
    (ix+V_DIV+IW, iy+H_DIV+IW, R_COL-IW, IH_SPACE-H_DIV-IW,  '#fff3e0'), # bed2
    (ix, iy,                 V_DIV-IW/2, H_DIV,               '#f1f8e9'), # living
    (ix+V_DIV+IW, iy,        KITCHEN_W,  H_DIV,               '#fce4ec'), # kitchen
    (kbx+IW, iy,             BATH_W-IW,  H_DIV,               '#e8eaf6'), # bath
]:
    rect_patch(ax, rx, ry, rw, rh, fc=col, ec='none', zorder=1)

# ═════════════════════════════════════════════════════════════════════════════
# WALLS
# ═════════════════════════════════════════════════════════════════════════════
WLW = 3.5   # external wall line weight
IWL = 2.0   # internal wall line weight

# External wall (filled rectangles for solid walls)
for (x, y, w, h) in [
    (0, 0, HW, EW),               # bottom
    (0, HH-EW, HW, EW),           # top
    (0, 0, EW, HH),               # left
    (HW-EW, 0, EW, HH),           # right
]:
    rect_patch(ax, x, y, w, h, fc=C_WALL_FILL, ec=C_WALL, lw=WLW, zorder=3)

# Internal walls (horizontal divider)
rect_patch(ax, ix, iy+H_DIV, IW_SPACE, IW, fc=C_WALL_FILL, ec=C_WALL_INT, lw=IWL, zorder=3)
# Internal walls (vertical divider)
rect_patch(ax, ix+V_DIV, iy, IW, IH_SPACE, fc=C_WALL_FILL, ec=C_WALL_INT, lw=IWL, zorder=3)
# Kitchen/Bath divider
rect_patch(ax, kbx, iy, IW, H_DIV, fc=C_WALL_FILL, ec=C_WALL_INT, lw=IWL, zorder=3)

# ═════════════════════════════════════════════════════════════════════════════
# DOORS
# ═════════════════════════════════════════════════════════════════════════════
def draw_door(ax, hx, hy, width=0.9, swing='R', wall_orient='h'):
    """Draw door gap + swing arc"""
    w = width
    door_color = C_DOOR
    if wall_orient == 'h':
        if swing == 'R':
            arc = Arc((hx, hy), 2*w, 2*w, angle=0, theta1=0, theta2=90,
                      color=door_color, lw=1.0, zorder=6)
            ax.add_patch(arc)
            line(ax, hx, hy, hx, hy+w, color=door_color, lw=1.0, zorder=6)
            line(ax, hx, hy, hx+w, hy, color=door_color, lw=1.0, zorder=6)
        else:
            arc = Arc((hx+w, hy), 2*w, 2*w, angle=0, theta1=90, theta2=180,
                      color=door_color, lw=1.0, zorder=6)
            ax.add_patch(arc)
            line(ax, hx+w, hy, hx+w, hy+w, color=door_color, lw=1.0, zorder=6)
            line(ax, hx, hy, hx+w, hy, color=door_color, lw=1.0, zorder=6)
    else:  # vertical wall
        if swing == 'R':
            arc = Arc((hx, hy+w), 2*w, 2*w, angle=0, theta1=270, theta2=360,
                      color=door_color, lw=1.0, zorder=6)
            ax.add_patch(arc)
            line(ax, hx, hy, hx+w, hy, color=door_color, lw=1.0, zorder=6)
            line(ax, hx, hy+w, hx, hy, color=door_color, lw=1.0, zorder=6)
        else:
            arc = Arc((hx, hy), 2*w, 2*w, angle=0, theta1=0, theta2=90,
                      color=door_color, lw=1.0, zorder=6)
            ax.add_patch(arc)
            line(ax, hx, hy, hx+w, hy, color=door_color, lw=1.0, zorder=6)
            line(ax, hx, hy, hx, hy+w, color=door_color, lw=1.0, zorder=6)
    # White gap to show door opening in wall
    if wall_orient == 'h':
        rect_patch(ax, hx, hy-EW/2, w, EW, fc=C_FLOOR, ec='none', zorder=5)
    else:
        rect_patch(ax, hx-EW/2, hy, EW, w, fc=C_FLOOR, ec='none', zorder=5)

# Main entrance (bottom wall, living room side)
draw_door(ax, 1.2, 0, 0.9, swing='R', wall_orient='h')
# Living → Bedroom 1
draw_door(ax, ix+V_DIV, iy+H_DIV+IW+0.3, 0.8, swing='R', wall_orient='v')
# Living → Kitchen
draw_door(ax, ix+V_DIV+IW+0.2, iy+H_DIV, 0.8, swing='R', wall_orient='h')
# Bedroom 1 exterior door
draw_door(ax, 0, iy+H_DIV+IW+0.8, 0.8, swing='R', wall_orient='v')
# Bedroom 2 door
draw_door(ax, ix+V_DIV+IW+1.5, iy+H_DIV, 0.8, swing='L', wall_orient='h')
# Bathroom door
draw_door(ax, kbx, iy+0.3, 0.75, swing='R', wall_orient='v')

# ═════════════════════════════════════════════════════════════════════════════
# WINDOWS
# ═════════════════════════════════════════════════════════════════════════════
def draw_window(ax, x, y, length=1.2, wall='h'):
    wc = C_WINDOW
    if wall == 'h':
        rect_patch(ax, x, y, length, EW, fc='#d6eaf8', ec=wc, lw=1.5, zorder=6)
        line(ax, x, y+EW/2, x+length, y+EW/2, color=wc, lw=1.5, zorder=7)
    else:
        rect_patch(ax, x, y, EW, length, fc='#d6eaf8', ec=wc, lw=1.5, zorder=6)
        line(ax, x+EW/2, y, x+EW/2, y+length, color=wc, lw=1.5, zorder=7)

# Living room (bottom)
draw_window(ax, 2.5, 0, 1.5, wall='h')
# Bedroom 1 (top)
draw_window(ax, 1.0, HH-EW, 1.4, wall='h')
# Bedroom 2 (top)
draw_window(ax, 8.5, HH-EW, 1.4, wall='h')
# Bedroom 2 (right)
draw_window(ax, HW-EW, iy+H_DIV+IW+0.8, 1.2, wall='v')
# Kitchen (right)
draw_window(ax, HW-EW, iy+0.5, 1.0, wall='v')
# Bathroom (bottom, small)
draw_window(ax, kbx+IW+0.2, 0, 0.6, wall='h')

# ═════════════════════════════════════════════════════════════════════════════
# FURNITURE
# ═════════════════════════════════════════════════════════════════════════════
# ── LIVING ROOM ──
furn_rect(ax, ix+0.3, iy+0.3, 2.2, 0.9, 'SOFA')
furn_rect(ax, ix+0.3, iy+0.3, 0.9, 1.5)
furn_rect(ax, ix+0.8, iy+1.4, 1.0, 0.6)           # coffee table
furn_rect(ax, ix+0.3, iy+H_DIV-0.25, 2.5, 0.18, 'TV UNIT')
furn_rect(ax, ix+3.8, iy+0.3, 1.4, 0.8, 'DINING')
for ci in range(3): furn_rect(ax, ix+3.9+ci*0.4, iy+0.15, 0.35, 0.12)
for ci in range(3): furn_rect(ax, ix+3.9+ci*0.4, iy+1.12, 0.35, 0.12)

# ── BEDROOM 1 ──
b1y = iy + H_DIV + IW
b1h = IH_SPACE - H_DIV - IW
furn_rect(ax, ix+0.3, b1y+b1h-2.1, 1.8, 2.0, 'DOUBLE BED')
rect_patch(ax, ix+0.3, b1y+b1h-0.5, 1.8, 0.35, fc='#b2bec3', ec=C_FURN, lw=0.7, zorder=5)
furn_rect(ax, ix+0.3, b1y+0.2, 1.8, 0.6, 'WARDROBE')
furn_rect(ax, ix+3.5, b1y+0.2, 1.2, 0.6, 'DESK')
furn_rect(ax, ix+2.2, b1y+b1h-1.6, 0.5, 0.5)   # side table

# ── BEDROOM 2 ──
b2_ix = ix + V_DIV + IW
b2_iw = R_COL - IW
b2y = iy + H_DIV + IW
b2h = IH_SPACE - H_DIV - IW
furn_rect(ax, b2_ix+0.3, b2y+b2h-2.0, 1.0, 1.9, 'BED')
rect_patch(ax, b2_ix+0.3, b2y+b2h-0.5, 1.0, 0.35, fc='#b2bec3', ec=C_FURN, lw=0.7, zorder=5)
furn_rect(ax, b2_ix+1.5, b2y+b2h-2.0, 1.0, 1.9, 'BED')
rect_patch(ax, b2_ix+1.5, b2y+b2h-0.5, 1.0, 0.35, fc='#b2bec3', ec=C_FURN, lw=0.7, zorder=5)
furn_rect(ax, b2_ix+0.3, b2y+0.2, 2.0, 0.6, 'WARDROBE')
furn_rect(ax, b2_ix+b2_iw-1.4, b2y+0.2, 1.0, 0.6, 'DESK')

# ── KITCHEN ──
kt_ix = ix + V_DIV + IW
furn_rect(ax, kt_ix+0.1, iy+0.1, KITCHEN_W-0.2, 0.6, 'COUNTER')
furn_rect(ax, kt_ix+KITCHEN_W-0.6, iy+0.1, 0.6, 2.5)  # side counter
# Sink
rect_patch(ax, kt_ix+KITCHEN_W-0.56, iy+2.2, 0.46, 0.4, fc='#aed6f1', ec=C_WINDOW, lw=0.8, zorder=5)
c = Circle((kt_ix+KITCHEN_W-0.33, iy+2.4), 0.06, fc='none', ec=C_WINDOW, lw=0.8, zorder=6)
ax.add_patch(c)
ax.text(kt_ix+KITCHEN_W-0.33, iy+2.65, 'SINK', ha='center', va='bottom', fontsize=5, color=C_FURN, zorder=6)
# Stove
furn_rect(ax, kt_ix+0.2, iy+1.6, 0.8, 0.8, 'STOVE')
for bx in [kt_ix+0.37, kt_ix+0.57]:
    for by in [iy+1.75, iy+2.13]:
        c2 = Circle((bx, by), 0.07, fc='none', ec=C_FURN, lw=0.7, zorder=6)
        ax.add_patch(c2)
# Fridge
furn_rect(ax, kt_ix+1.5, iy+1.6, 0.7, 0.8, 'FRIDGE')

# ── BATHROOM ──
ba_ix = kbx + IW
ba_iw = BATH_W - IW
# Bathtub
rect_patch(ax, ba_ix+0.1, iy+H_DIV-1.7, ba_iw-0.2, 1.5, fc='#aed6f1', ec=C_WINDOW, lw=1.0, zorder=4)
rect_patch(ax, ba_ix+0.2, iy+H_DIV-1.6, ba_iw-0.4, 1.2, fc='#d6eaf8', ec=C_WINDOW, lw=0.7, zorder=5)
ax.text(ba_ix+ba_iw/2, iy+H_DIV-1.0, 'BATH', ha='center', va='center', fontsize=6, color=C_WINDOW, zorder=6)
# Toilet
rect_patch(ax, ba_ix+0.2, iy+0.2, 0.4, 0.6, fc=C_FURN_FILL, ec=C_FURN, lw=0.7, zorder=4)
e = Ellipse((ba_ix+0.4, iy+0.55), 0.34, 0.5, fc='white', ec=C_FURN, lw=0.7, zorder=5)
ax.add_patch(e)
ax.text(ba_ix+0.4, iy+0.85, 'WC', ha='center', va='bottom', fontsize=5.5, color=C_FURN, zorder=6)
# Basin
rect_patch(ax, ba_ix+0.1, iy+1.2, 0.5, 0.5, fc='#d6eaf8', ec=C_WINDOW, lw=0.7, zorder=4)
c3 = Circle((ba_ix+0.35, iy+1.45), 0.06, fc='none', ec=C_WINDOW, lw=0.7, zorder=5)
ax.add_patch(c3)
ax.text(ba_ix+0.35, iy+1.75, 'BASIN', ha='center', va='bottom', fontsize=5.5, color=C_FURN, zorder=6)

# ═════════════════════════════════════════════════════════════════════════════
# ROOM LABELS
# ═════════════════════════════════════════════════════════════════════════════
room_label(ax, 'LIVING ROOM',  f'{V_DIV*(H_DIV):.1f} m²',
           ix+V_DIV/2, iy+H_DIV/2)
room_label(ax, 'BEDROOM 1',    f'{V_DIV*(IH_SPACE-H_DIV-IW):.1f} m²',
           ix+V_DIV/2, iy+H_DIV+IW+(IH_SPACE-H_DIV-IW)/2)
room_label(ax, 'BEDROOM 2',    f'{(R_COL-IW)*(IH_SPACE-H_DIV-IW):.1f} m²',
           ix+V_DIV+IW+R_COL/2, iy+H_DIV+IW+(IH_SPACE-H_DIV-IW)/2)
room_label(ax, 'KITCHEN',      f'{KITCHEN_W*H_DIV:.1f} m²',
           ix+V_DIV+IW+KITCHEN_W/2, iy+H_DIV*0.5)
room_label(ax, 'BATHROOM',     f'{(BATH_W-IW)*H_DIV:.1f} m²',
           kbx+IW+(BATH_W-IW)/2, iy+H_DIV*0.5)

# ═════════════════════════════════════════════════════════════════════════════
# DIMENSIONS
# ═════════════════════════════════════════════════════════════════════════════
# Overall width (bottom)
dim_line(ax, 0, 0, HW, 0,    f'{HW*1000:.0f}', orient='h', offset=1.1)
# Left column
dim_line(ax, 0, 0, ix+V_DIV, 0, f'{(ix+V_DIV)*1000:.0f}', orient='h', offset=0.6)
# Right column
dim_line(ax, ix+V_DIV+IW, 0, HW, 0, f'{(HW-ix-V_DIV-IW)*1000:.0f}', orient='h', offset=0.6)
# Overall height (right)
dim_line(ax, HW, 0, HW, HH,  f'{HH*1000:.0f}', orient='v', offset=1.1)
# Bottom row height
dim_line(ax, HW, 0, HW, iy+H_DIV, f'{(iy+H_DIV)*1000:.0f}', orient='v', offset=0.55)
# Top row height
dim_line(ax, HW, iy+H_DIV+IW, HW, HH, f'{(HH-iy-H_DIV-IW)*1000:.0f}', orient='v', offset=0.55)

# ═════════════════════════════════════════════════════════════════════════════
# NORTH ARROW
# ═════════════════════════════════════════════════════════════════════════════
na_x = -0.8
na_y = HH - 1.5
circle_n = Circle((na_x, na_y), 0.5, fc='white', ec=C_NORTH, lw=1.5, zorder=10)
ax.add_patch(circle_n)
ax.annotate('', xy=(na_x, na_y+0.45), xytext=(na_x, na_y-0.1),
            arrowprops=dict(arrowstyle='->', color=C_NORTH, lw=2.0), zorder=11)
ax.text(na_x, na_y+0.62, 'N', ha='center', va='center',
        fontsize=11, color=C_NORTH, fontweight='bold', zorder=12)

# ═════════════════════════════════════════════════════════════════════════════
# TITLE BLOCK (bottom panel using separate axes)
# ═════════════════════════════════════════════════════════════════════════════
ax_tb = fig.add_axes([0.05, 0.01, 0.68, 0.10])
ax_tb.set_xlim(0, 10)
ax_tb.set_ylim(0, 1.6)
ax_tb.axis('off')
ax_tb.set_facecolor('white')

rect_patch(ax_tb, 0, 0, 10, 1.6, fc='white', ec=C_BORDER, lw=2.0)
line(ax_tb, 3.8, 0, 3.8, 1.6, color=C_BORDER, lw=1.5)
line(ax_tb, 0, 0.8, 10, 0.8, color=C_BORDER, lw=1.0)
line(ax_tb, 6.5, 0.8, 6.5, 1.6, color=C_BORDER, lw=1.0)
line(ax_tb, 8.2, 0.8, 8.2, 1.6, color=C_BORDER, lw=1.0)
line(ax_tb, 6.5, 0, 6.5, 0.8, color=C_BORDER, lw=1.0)

# Left cell – Project title
ax_tb.text(1.9, 1.1, 'RESIDENTIAL FLOOR PLAN', ha='center', va='center',
           fontsize=12, fontweight='bold', color=C_TITLE)
ax_tb.text(1.9, 0.35, '2-Bedroom House  |  Ground Floor  |  Scale 1:50',
           ha='center', va='center', fontsize=8, color='#546e7a')

# Info cells
cells = [
    (4.4, 1.35, 'PROJECT', '2BR Residential House'),
    (4.4, 0.45, 'DRAWN BY', 'AutoCAD Intern'),
    (7.35, 1.35, 'DATE', '2025'),
    (7.35, 0.45, 'SCALE', '1 : 50'),
    (9.1, 1.35, 'SHEET', '01 / 01'),
    (9.1, 0.45, 'REV', 'A'),
    (5.5, 0.45, 'DWG NO', 'RFP-2025-001'),
]
for cx, cy, lbl, val in cells:
    ax_tb.text(cx, cy+0.22, lbl, ha='left', va='center', fontsize=6,
               color='#546e7a', fontweight='bold')
    ax_tb.text(cx, cy, val, ha='left', va='center', fontsize=8, color=C_TITLE)

# ═════════════════════════════════════════════════════════════════════════════
# LEGEND PANEL (right side)
# ═════════════════════════════════════════════════════════════════════════════
ax_leg = fig.add_axes([0.75, 0.13, 0.23, 0.84])
ax_leg.set_xlim(0, 10)
ax_leg.set_ylim(0, 30)
ax_leg.axis('off')
ax_leg.set_facecolor('#f0ece4')

ax_leg.text(5, 29.2, 'LEGEND', ha='center', va='center',
            fontsize=11, fontweight='bold', color=C_TITLE)

legend_items = [
    (C_WALL_FILL, C_WALL, 3.0, 'External Wall (230mm)'),
    (C_WALL_FILL, C_WALL_INT, 1.5, 'Internal Wall (115mm)'),
    (C_FURN_FILL, C_FURN, 1.0, 'Furniture'),
    ('#d6eaf8', C_WINDOW, 1.0, 'Window'),
    ('white', C_DOOR, 1.0, 'Door / Swing'),
]
y0 = 27.5
for fc, ec, lw, label in legend_items:
    rect_patch(ax_leg, 0.5, y0-0.4, 2.0, 0.8, fc=fc, ec=ec, lw=lw, zorder=2)
    ax_leg.text(3.0, y0, label, ha='left', va='center',
                fontsize=8, color=C_TEXT)
    y0 -= 1.8

# Room areas summary
ax_leg.text(5, 17.5, 'ROOM SCHEDULE', ha='center', va='center',
            fontsize=10, fontweight='bold', color=C_TITLE)
rooms_data = [
    ('Living Room',    f'{V_DIV*(H_DIV):.1f} m²'),
    ('Bedroom 1',      f'{V_DIV*(IH_SPACE-H_DIV-IW):.1f} m²'),
    ('Bedroom 2',      f'{(R_COL-IW)*(IH_SPACE-H_DIV-IW):.1f} m²'),
    ('Kitchen',        f'{KITCHEN_W*H_DIV:.1f} m²'),
    ('Bathroom',       f'{(BATH_W-IW)*H_DIV:.1f} m²'),
    ('─────────────', '──────'),
    ('TOTAL (GFA)',     f'{HW*HH:.1f} m²'),
]
y0 = 16.5
for rm, area in rooms_data:
    ax_leg.text(0.5, y0, rm,   ha='left',  va='center', fontsize=8, color=C_TEXT)
    ax_leg.text(9.5, y0, area, ha='right', va='center', fontsize=8, color=C_TEXT,
                fontfamily='monospace')
    y0 -= 1.6

# Notes
ax_leg.text(5, 5.5, 'GENERAL NOTES', ha='center', va='center',
            fontsize=10, fontweight='bold', color=C_TITLE)
notes = [
    '1. All dims in millimetres',
    '2. Do not scale from drawing',
    '3. Verify on site before work',
    '4. Wall finish not shown',
    '5. Drawing scale: 1:50 @ A1',
]
y0 = 4.5
for note in notes:
    ax_leg.text(0.5, y0, note, ha='left', va='center', fontsize=7.5, color='#546e7a')
    y0 -= 1.0

# Project info box
rect_patch(ax_leg, 0, -0.5, 10, 1.2, fc='#1a1a2e', ec='none', zorder=2)
ax_leg.text(5, 0.2, 'RFP-2025-001  |  FOR REVIEW  |  REV A',
            ha='center', va='center', fontsize=7.5, color='white',
            fontfamily='monospace', zorder=3)

# ═════════════════════════════════════════════════════════════════════════════
# MAIN FIGURE BORDER
# ═════════════════════════════════════════════════════════════════════════════
for spine in ['top','bottom','left','right']:
    fig.patch.set_linewidth(0)

# Save
out = '/mnt/user-data/outputs/residential_floor_plan.pdf'
plt.savefig(out, dpi=200, bbox_inches='tight', facecolor='#f0ece4')
print(f"PDF saved: {out}")
