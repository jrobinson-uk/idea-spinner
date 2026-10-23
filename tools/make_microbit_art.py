"""Builds the micro:bit sub-site's pictures.

1. Board variants from the Micro:bit Educational Foundation's drawing
   (microbit/img/source/microbit-drawing-2.svg, CC BY-NC-SA 4.0,
   https://github.com/microbit-foundation/microbit-svg), with the green
   fringe and a square canvas so highlights can sit around the board.
2. One highlight layer per feature, drawn on the same canvas, which the page
   stacks on top of the board.

Usage: python3 tools/make_microbit_art.py
"""
import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "microbit/img/source/microbit-drawing-2.svg"
OUT = ROOT / "microbit/img"

# Square canvas around the 208.9 x 168.1 board, with room above and below.
VIEWBOX = "-15.5 -36 240 240"

INK = "#1f2440"
GLOW = "#ffd23f"
RED, ORANGE, YELLOW = "#e0302c", "#f29a4a", "#ffd23f"
TEAL, TEAL_L, BLUE = "#0d8a80", "#5fd3c4", "#4a8fe0"
GREY, WHITE = "#c9cbd6", "#ffffff"

# Where things are on the board, in drawing units.
BUTTON_A, BUTTON_B = (28.75, 82.25), (179.75, 82.25)
LOGO = (103.75, 34.25)
MIC = (132.2, 42)
PINS = {"0": (23.25, 132), "1": (61.25, 132), "2": (103.75, 132)}
LED_X = [73.75, 88.75, 103.75, 118.75, 133.75]
LED_Y = [56.25, 71, 85.75, 100.25, 114.25]
USB = (104, 3)
BADGE = (196, -6)


# ---------------------------------------------------------------- board variants

def set_layer(svg, label, show):
    pat = re.compile(r'(<g\b[^>]*?inkscape:label="%s"[^>]*?style=")([^"]*)(")' % re.escape(label), re.S)
    m = pat.search(svg)
    if not m:
        pat = re.compile(r'(<g\b[^>]*?style=")([^"]*)("[^>]*?inkscape:label="%s")' % re.escape(label), re.S)
        m = pat.search(svg)
    assert m, label
    style = re.sub(r"display:[a-z]+;?", "", m.group(2)).strip(";")
    disp = "display:inline" if show else "display:none"
    return svg[: m.start()] + m.group(1) + ";".join(filter(None, [disp, style])) + m.group(3) + svg[m.end():]


def board(out_name, show=(), hide=()):
    svg = SRC.read_text()
    for label in show:
        svg = set_layer(svg, label, True)
    for label in hide:
        svg = set_layer(svg, label, False)
    svg = re.sub(r'viewBox="[^"]*"', f'viewBox="{VIEWBOX}"', svg, count=1)
    svg = re.sub(r'\bheight="[0-9.]+mm"', 'height="240"', svg, count=1)
    svg = re.sub(r'\bwidth="[0-9.]+mm"', 'width="240"', svg, count=1)
    svg = re.sub(r"<sodipodi:namedview.*?</sodipodi:namedview>|<sodipodi:namedview[^>]*/>", "", svg, flags=re.S)
    (OUT / out_name).write_text(svg)


OTHER_FRINGES = ["ColourFringeBlue", "ColourFringeYellow", "ColourFringeRed"]
board("board.svg", show=["ColourFringeGreen"], hide=OTHER_FRINGES + ["LEDsON", "LEDsHeart"])
board("board-mic.svg", show=["ColourFringeGreen", "MicrophoneON"],
      hide=OTHER_FRINGES + ["LEDsON", "LEDsHeart", "Microphone"])


# ---------------------------------------------------------------- drawing helpers

def layer(body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VIEWBOX}" width="240" height="240">'
        '<defs><filter id="glow" x="-50%" y="-50%" width="200%" height="200%">'
        '<feGaussianBlur stdDeviation="1.6"/></filter></defs>'
        f'<g fill="none" stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>\n'
    )


def glow_path(d):
    """A yellow line with a dark edge, readable on the black board and on light backgrounds."""
    return f'<path d="{d}" stroke="{INK}" stroke-width="6.5"/><path d="{d}" stroke="{GLOW}" stroke-width="3"/>'


def ring(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{INK}" stroke-width="6.5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{GLOW}" stroke-width="3"/>')


def rounded_ring(x, y, w, h, rx):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" stroke="{INK}" stroke-width="6.5"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" stroke="{GLOW}" stroke-width="3"/>')


def rays(cx, cy, r1, r2, angles):
    d = ""
    for a in angles:
        t = math.radians(a)
        d += f"M{cx + r1 * math.cos(t):.1f} {cy + r1 * math.sin(t):.1f}L{cx + r2 * math.cos(t):.1f} {cy + r2 * math.sin(t):.1f}"
    return glow_path(d)


def arrow(x1, y1, x2, y2, head=7):
    """A glowing arrow from (x1, y1) to (x2, y2)."""
    t = math.atan2(y2 - y1, x2 - x1)
    a1, a2 = t + math.radians(150), t - math.radians(150)
    d = (f"M{x1} {y1}L{x2} {y2}"
         f"M{x2 + head * math.cos(a1):.1f} {y2 + head * math.sin(a1):.1f}L{x2} {y2}"
         f"L{x2 + head * math.cos(a2):.1f} {y2 + head * math.sin(a2):.1f}")
    return glow_path(d)


def leds(pattern):
    """Light LEDs on the 5x5 display. `pattern` is five strings of '#' and '.'."""
    out = ""
    for r, row in enumerate(pattern):
        for c, ch in enumerate(row):
            if ch != "#":
                continue
            x, y = LED_X[c], LED_Y[r]
            out += (f'<rect x="{x - 3.2}" y="{y - 4.2}" width="6.4" height="8.4" rx="2" fill="#ff3b30" '
                    f'opacity="0.75" filter="url(#glow)"/>'
                    f'<rect x="{x - 1.6}" y="{y - 2.8}" width="3.2" height="5.6" rx="0.8" fill="#ff4a3d"/>')
    return out


def badge(icon, cx=BADGE[0], cy=BADGE[1]):
    """A round white badge with an icon drawn in a -15..15 box."""
    return (f'<circle cx="{cx}" cy="{cy}" r="25" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>'
            f'<g transform="translate({cx} {cy})" stroke="{INK}" stroke-width="3.2">{icon}</g>')


# Badge icons, centred on 0,0.
SUN = ('<circle r="7" fill="%s"/>' % YELLOW
       + "".join(f'<path d="M{10 * math.cos(math.radians(a)):.1f} {10 * math.sin(math.radians(a)):.1f}'
                 f'L{15 * math.cos(math.radians(a)):.1f} {15 * math.sin(math.radians(a)):.1f}" stroke="{ORANGE}"/>'
                 for a in range(0, 360, 45)))
THERMOMETER = (f'<rect x="-4.5" y="-16" width="9" height="22" rx="4.5" fill="{WHITE}"/>'
               f'<circle cy="9" r="7" fill="{RED}"/><rect x="-1.8" y="-6" width="3.6" height="12" fill="{RED}" stroke="none"/>')
COMPASS = (f'<circle r="14" fill="#eef1f6"/><path d="M0 -11L4.5 0H-4.5Z" fill="{RED}" stroke-width="2.4"/>'
           f'<path d="M0 11L4.5 0H-4.5Z" fill="{GREY}" stroke-width="2.4"/>')
MAGNET = ('<path d="M-9 -13v11a9 9 0 0 0 18 0v-11" stroke-width="11"/>'
          f'<path d="M-9 -13v11a9 9 0 0 0 18 0v-11" stroke="{RED}" stroke-width="6"/>'
          f'<path d="M-9 -13v4M9 -13v4" stroke="{GREY}" stroke-width="6" stroke-linecap="butt"/>')
SIGNAL = "".join(f'<rect x="{x}" y="{10 - h}" width="5" height="{h}" rx="1" fill="{TEAL_L}" stroke-width="2.4"/>'
                 for x, h in [(-13, 6), (-6, 11), (1, 16), (8, 21)])
PHONE = (f'<rect x="-9" y="-15" width="18" height="30" rx="3.5" fill="{WHITE}"/>'
         f'<rect x="-5.5" y="-10" width="11" height="17" rx="1" fill="{TEAL_L}" stroke-width="2"/>'
         f'<circle cy="11" r="1.2" fill="{INK}" stroke="none"/>')
NOTES = (f'<path d="M-6 8V-10L9 -13V5" stroke-width="3"/>'
         f'<ellipse cx="-9.5" cy="8.5" rx="4.5" ry="3.5" fill="{INK}"/><ellipse cx="5.5" cy="5.5" rx="4.5" ry="3.5" fill="{INK}"/>')
SPEAKER = (f'<path d="M-14 -5h6l7 -7v24l-7 -7h-6z" fill="{GREY}"/>'
           f'<path d="M4 -5a7 7 0 0 1 0 10M8 -10a13 13 0 0 1 0 20" stroke="{ORANGE}"/>'
           f'<path d="M12 -15l1.2 3 3 1.2 -3 1.2 -1.2 3 -1.2 -3 -3 -1.2 3 -1.2z" fill="{YELLOW}" stroke-width="1.6"/>')
CHART = (f'<rect x="-13" y="-13" width="26" height="26" rx="3" fill="{WHITE}"/>'
         f'<path d="M-8 7L-3 0 2 3 8 -7" stroke="{TEAL}"/>')
BROADCAST = (f'<circle r="3.5" fill="{INK}"/>'
             f'<path d="M-7 -7a10 10 0 0 0 0 14M7 -7a10 10 0 0 1 0 14M-12 -12a17 17 0 0 0 0 24M12 -12a17 17 0 0 1 0 24" stroke="{TEAL}"/>')
LAPTOP = (f'<rect x="-12" y="-12" width="24" height="16" rx="2" fill="{INK}"/>'
          f'<rect x="-9" y="-9" width="18" height="10" fill="{TEAL_L}" stroke="none"/>'
          f'<path d="M-16 6h32l-3 5h-26z" fill="{GREY}" stroke-width="2.6"/>')


def waves(cx, cy, start, end, radii=(14, 24, 34)):
    """Radio-style arcs around a point, between two angles in degrees."""
    d = ""
    for r in radii:
        a, b = math.radians(start), math.radians(end)
        d += (f"M{cx + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f}"
              f"A{r} {r} 0 0 1 {cx + r * math.cos(b):.1f} {cy + r * math.sin(b):.1f}")
    return glow_path(d)


HEART = [".#.#.", "#####", "#####", ".###.", "..#.."]
LETTER_A = [".###.", "#...#", "#####", "#...#", "#...#"]
ALL_ON = ["#####"] * 5

# ---------------------------------------------------------------- highlights

H = {}
# Inputs
H["buttons"] = (ring(*BUTTON_A, 15) + ring(*BUTTON_B, 15)
                + rays(*BUTTON_A, 21, 29, [150, 180, 210]) + rays(*BUTTON_B, 21, 29, [-30, 0, 30]))
H["touch-logo"] = rounded_ring(LOGO[0] - 21, LOGO[1] - 13, 42, 26, 13) + rays(*LOGO, 22, 32, [-150, -120, -90, -60, -30])
H["touch-pins"] = "".join(ring(x, y, 11) + rays(x, y, 17, 26, [60, 90, 120]) for x, y in PINS.values())
H["light-level"] = rounded_ring(64, 46, 80, 78, 10) + badge(SUN)
H["temperature"] = badge(THERMOMETER)
H["microphone"] = ring(*MIC, 8) + waves(MIC[0] + 2, MIC[1], -40, 40, radii=(16, 24))
H["tilt"] = (glow_path("M16 -6A150 150 0 0 1 192 -6")
             + glow_path("M24 -18L14 -5 30 -1") + glow_path("M184 -18L194 -5 178 -1"))
H["shake"] = (glow_path("M3 58a50 50 0 0 0 0 54M-4 50a60 60 0 0 0 0 70")
              + glow_path("M205 58a50 50 0 0 1 0 54M212 50a60 60 0 0 1 0 70"))
H["free-fall"] = (arrow(60, 166, 60, 196) + arrow(104, 166, 104, 200) + arrow(148, 166, 148, 196))
H["compass"] = badge(COMPASS)
H["magnet"] = badge(MAGNET)
H["radio-receive"] = badge(BROADCAST) + arrow(174, 14, 150, 34)
H["signal-strength"] = badge(SIGNAL)
H["phone-control"] = badge(PHONE) + arrow(174, 14, 150, 34)
# Outputs
H["led-pictures"] = leds(HEART)
H["scrolling-text"] = leds(LETTER_A) + arrow(130, -16, 78, -16)
H["music"] = badge(NOTES)
H["sound-effects"] = badge(SPEAKER)
H["radio-send"] = badge(BROADCAST) + arrow(150, 34, 174, 14)
H["phone-send"] = badge(PHONE) + arrow(150, 34, 174, 14)
H["data-logging"] = badge(CHART)
H["send-to-computer"] = glow_path(f"M{USB[0]} {USB[1] - 2}V-14Q104 -24 114 -24H170") + badge(LAPTOP)

(OUT / "highlights").mkdir(exist_ok=True)
for name, body in H.items():
    (OUT / "highlights" / f"{name}.svg").write_text(layer(body))
print(f"2 boards and {len(H)} highlights written")
