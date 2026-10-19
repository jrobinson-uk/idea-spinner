"""Writes the Idea Spinner ingredient illustrations in one house style."""
import sys, pathlib

OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

INK = "#1f2440"
RED, ORANGE, YELLOW = "#e0302c", "#f29a4a", "#ffd23f"
TEAL, TEAL_L, BLUE = "#0d8a80", "#5fd3c4", "#4a8fe0"
PURPLE, PURPLE_L = "#7448c7", "#e3d8fa"
GREEN, GREY, GREY_D, WHITE = "#3aa35b", "#c9cbd6", "#9a9db0", "#ffffff"
BROWN, BROWN_D, BROWN_L = "#d9a066", "#c48a52", "#ecc28c"


def svg(body):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240">'
        '<rect x="6" y="6" width="228" height="228" rx="44" fill="#ffffff"/>'
        f'<g fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">'
        f"{body}</g></svg>\n"
    )


def grid(x0, y0, step, size, lit, on, off, radius=3):
    out = []
    for r in range(5):
        for c in range(5):
            fill = on if (r, c) in lit else off
            out.append(
                f'<rect x="{x0 + c * step}" y="{y0 + r * step}" width="{size}" height="{size}" rx="{radius}" fill="{fill}" stroke="none"/>'
            )
    return "".join(out)


HEART = {(0, 1), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3), (4, 2)}
SMILE = {(1, 1), (1, 3), (3, 0), (3, 4), (4, 1), (4, 2), (4, 3)}

art = {
    # ---------------- Inputs ----------------
    "button": f"""
      <path d="M78 76V52M162 76V52M78 184v24M162 184v24"/>
      <rect x="56" y="76" width="128" height="108" rx="16" fill="{GREY}"/>
      <circle cx="120" cy="130" r="36" fill="{RED}"/>
      <path d="M102 116a22 22 0 0 1 14-10" stroke="{WHITE}" stroke-width="6"/>""",
    "light-sensor": f"""
      <path d="M44 44l18 18M30 84h22M84 30v22" stroke="{ORANGE}"/>
      <path d="M110 160v50M138 160v50"/>
      <circle cx="124" cy="116" r="50" fill="{ORANGE}"/>
      <path d="M98 96h52v12H98v12h52v12H98" stroke="{RED}" stroke-width="5"/>""",
    "temperature-sensor": f"""
      <rect x="100" y="34" width="40" height="132" rx="20" fill="{WHITE}"/>
      <circle cx="120" cy="174" r="30" fill="{RED}"/>
      <rect x="112" y="90" width="16" height="70" fill="{RED}" stroke="none"/>
      <path d="M152 64h16M152 90h16M152 116h16M152 142h16"/>""",
    "accelerometer": f"""
      <g transform="rotate(-15 120 150)">
        <rect x="62" y="112" width="116" height="78" rx="12" fill="{TEAL_L}"/>
        <rect x="104" y="135" width="32" height="32" rx="5" fill="{INK}"/>
        <path d="M76 126h2M162 126h2M76 176h2M162 176h2"/>
      </g>
      <path d="M62 82A88 88 0 0 1 178 82" stroke="{ORANGE}"/>
      <path d="M50 92l20-2-8-18z" fill="{ORANGE}" stroke="{ORANGE}" stroke-width="4"/>
      <path d="M190 92l-20-2 8-18z" fill="{ORANGE}" stroke="{ORANGE}" stroke-width="4"/>""",
    "microphone": f"""
      <rect x="92" y="34" width="56" height="100" rx="28" fill="{GREY}"/>
      <path d="M106 66h28M106 84h28M106 102h28" stroke-width="5"/>
      <path d="M70 112a50 50 0 0 0 100 0"/>
      <path d="M120 162v28M92 196h56"/>""",
    "distance-sensor": f"""
      <rect x="22" y="80" width="58" height="96" rx="10" fill="{BLUE}"/>
      <circle cx="51" cy="106" r="15" fill="{GREY}"/>
      <circle cx="51" cy="150" r="15" fill="{GREY}"/>
      <circle cx="51" cy="106" r="5" fill="{INK}"/>
      <circle cx="51" cy="150" r="5" fill="{INK}"/>
      <path d="M96 110a22 22 0 0 1 0 36M114 98a40 40 0 0 1 0 60M132 86a58 58 0 0 1 0 84" stroke="{TEAL}"/>
      <rect x="168" y="70" width="48" height="116" rx="8" fill="{ORANGE}"/>
      <path d="M88 208h72" stroke-width="5"/>
      <path d="M84 208l14-8v16z" fill="{INK}" stroke-width="4"/>
      <path d="M164 208l-14-8v16z" fill="{INK}" stroke-width="4"/>""",
    "motion-sensor": f"""
      <path d="M112 136l38-36M120 154l46-22" stroke="{TEAL}" stroke-dasharray="2 12"/>
      <rect x="22" y="172" width="116" height="26" rx="6" fill="{GREEN}"/>
      <path d="M34 172a46 46 0 0 1 92 0z" fill="{WHITE}"/>
      <path d="M62 172l6-40M98 172l-6-40M42 150h76" stroke-width="4"/>
      <circle cx="182" cy="64" r="14" fill="{WHITE}"/>
      <path d="M180 80l-4 48M154 102l26-14 22 16M176 128l-18 36M176 128l22 32"/>
      <path d="M208 70h14M210 94h14M204 118h14" stroke="{ORANGE}"/>""",
    "soil-moisture": f"""
      <rect x="28" y="150" width="184" height="62" rx="14" fill="{BROWN_D}"/>
      <path d="M60 176h8M110 192h8M160 172h8M190 196h4" stroke="{BROWN_L}"/>
      <path d="M102 112v70M138 112v70" stroke-width="14"/>
      <path d="M102 112v70M138 112v70" stroke="{YELLOW}" stroke-width="4"/>
      <rect x="88" y="54" width="64" height="60" rx="8" fill="{GREEN}"/>
      <path d="M190 34c-14 18-20 28-20 38a20 20 0 0 0 40 0c0-10-6-20-20-38z" fill="#7cc4f2"/>""",
    "touch": f"""
      <ellipse cx="120" cy="170" rx="80" ry="26" stroke="{TEAL}" stroke-dasharray="2 14"/>
      <ellipse cx="120" cy="170" rx="54" ry="16" fill="{YELLOW}"/>
      <path d="M104 26v116a16 16 0 0 0 32 0V26" fill="#f6c9a0"/>
      <path d="M110 128a10 10 0 0 0 20 0v-12h-20z" fill="#fde3cc" stroke-width="4"/>""",
    "compass": f"""
      <circle cx="120" cy="120" r="78" fill="{WHITE}"/>
      <circle cx="120" cy="120" r="60" fill="#eef1f6"/>
      <path d="M120 54v8M120 178v8M54 120h8M178 120h8"/>
      <path d="M120 66l18 54h-36z" fill="{RED}"/>
      <path d="M120 174l18-54h-36z" fill="{GREY}"/>
      <circle cx="120" cy="120" r="7" fill="{INK}"/>""",
    "ai-classifier": f"""
      <path d="M40 68V44h24M176 44h24v24M40 172v24h24M200 172v24h-24" stroke="{PURPLE}"/>
      <path d="M44 120q76-68 152 0q-76 68-152 0z" fill="{WHITE}"/>
      <circle cx="120" cy="120" r="28" fill="{PURPLE}"/>
      <circle cx="120" cy="120" r="10" fill="{INK}"/>
      <path d="M128 106l4 4" stroke="{WHITE}" stroke-width="5"/>""",
    # ---------------- Outputs ----------------
    "led": f"""
      <path d="M120 26v14M74 46l10 10M166 46l-10 10M54 92h14M172 92h14" stroke="{ORANGE}"/>
      <path d="M108 154v56M132 154v44"/>
      <rect x="80" y="134" width="80" height="20" rx="4" fill="{RED}"/>
      <path d="M88 134V96a32 32 0 0 1 64 0v38z" fill="{RED}"/>
      <path d="M104 92a16 16 0 0 1 12-14" stroke="{WHITE}" stroke-width="6"/>""",
    "colour-leds": f"""
      <circle cx="120" cy="120" r="62" stroke-width="36"/>
      <circle cx="120" cy="120" r="62" stroke="#3a3d55" stroke-width="26"/>
      <circle cx="120.0" cy="58.0" r="13" fill="{RED}" stroke-width="4"/>
      <circle cx="163.8" cy="76.2" r="13" fill="{ORANGE}" stroke-width="4"/>
      <circle cx="182.0" cy="120.0" r="13" fill="{YELLOW}" stroke-width="4"/>
      <circle cx="163.8" cy="163.8" r="13" fill="{GREEN}" stroke-width="4"/>
      <circle cx="120.0" cy="182.0" r="13" fill="{TEAL_L}" stroke-width="4"/>
      <circle cx="76.2" cy="163.8" r="13" fill="{BLUE}" stroke-width="4"/>
      <circle cx="58.0" cy="120.0" r="13" fill="{PURPLE}" stroke-width="4"/>
      <circle cx="76.2" cy="76.2" r="13" fill="#ff7eb6" stroke-width="4"/>""",
    "speaker": f"""
      <path d="M44 96h32l44-34v116l-44-34H44z" fill="{GREY}"/>
      <path d="M146 100a30 30 0 0 1 0 40M166 82a56 56 0 0 1 0 76M186 64a82 82 0 0 1 0 112" stroke="{ORANGE}"/>""",
    "servo": f"""
      <path d="M141 67A64 64 0 0 0 59 67" stroke="{ORANGE}" stroke-dasharray="2 12"/>
      <rect x="28" y="124" width="184" height="30" rx="6" fill="{BLUE}"/>
      <rect x="52" y="100" width="136" height="88" rx="12" fill="{BLUE}"/>
      <path d="M104 118L134 80" stroke-width="22"/>
      <path d="M104 118L134 80" stroke="{WHITE}" stroke-width="10"/>
      <circle cx="104" cy="118" r="16" fill="{WHITE}"/>
      <circle cx="104" cy="118" r="4" fill="{INK}"/>""",
    "motor": f"""
      <path d="M66 80V60M98 80V60"/>
      <path d="M172 120h40"/>
      <rect x="34" y="80" width="124" height="84" rx="18" fill="{GREY}"/>
      <rect x="150" y="96" width="24" height="52" rx="6" fill="{GREY_D}"/>
      <path d="M58 104h70M58 140h70" stroke="{GREY_D}" stroke-width="4"/>
      <path d="M184 92A28 28 0 1 1 184 148" stroke="{ORANGE}"/>
      <path d="M168 148l16-9v18z" fill="{ORANGE}" stroke="{ORANGE}" stroke-width="4"/>""",
    "led-matrix": f"""
      <rect x="40" y="40" width="160" height="160" rx="18" fill="{INK}"/>
      {grid(60, 60, 26, 18, HEART, RED, "#3b4066")}""",
    "screen": f"""
      <path d="M120 164v24M86 194h68"/>
      <rect x="30" y="44" width="180" height="120" rx="14" fill="{INK}"/>
      <rect x="46" y="60" width="148" height="88" rx="6" fill="#c8f1ea" stroke="none"/>
      <path d="M64 84h70M64 104h104M64 124h52" stroke="{TEAL}"/>""",
    "generative-ai": f"""
      <path d="M48 52h144a16 16 0 0 1 16 16v84a16 16 0 0 1-16 16h-84l-34 28v-28H48a16 16 0 0 1-16-16V68a16 16 0 0 1 16-16z" fill="{PURPLE_L}"/>
      <path d="M112 72c4 20 10 26 30 30c-20 4-26 10-30 30c-4-20-10-26-30-30c20-4 26-10 30-30z" fill="{PURPLE}"/>
      <path d="M162 76c2 9 5 12 14 14c-9 2-12 5-14 14c-2-9-5-12-14-14c9-2 12-5 14-14z" fill="{YELLOW}" stroke-width="4"/>
      <path d="M162 124c1.5 6 3.5 8 9 9.5c-5.5 1.5-7.5 3.5-9 9.5c-1.5-6-3.5-8-9-9.5c5.5-1.5 7.5-3.5 9-9.5z" fill="{PURPLE}" stroke-width="4"/>""",
    # ---------------- Wildcards ----------------
    "microbit": f"""
      <rect x="22" y="54" width="196" height="132" rx="16" fill="#3a3d55"/>
      <path d="M22 160h196v10a16 16 0 0 1-16 16H38a16 16 0 0 1-16-16z" fill="#e6b84a"/>
      <circle cx="54" cy="168" r="8" fill="{WHITE}"/>
      <circle cx="120" cy="168" r="8" fill="{WHITE}"/>
      <circle cx="186" cy="168" r="8" fill="{WHITE}"/>
      {grid(83, 68, 15, 11, SMILE, RED, "#565b7c", 2)}
      <circle cx="54" cy="104" r="14" fill="{GREY}"/>
      <circle cx="54" cy="104" r="6" fill="{INK}"/>
      <circle cx="186" cy="104" r="14" fill="{GREY}"/>
      <circle cx="186" cy="104" r="6" fill="{INK}"/>""",
    "pico": f"""
      <rect x="16" y="102" width="26" height="36" rx="4" fill="{GREY}"/>
      <rect x="34" y="78" width="184" height="84" rx="8" fill="{GREEN}"/>
      {"".join(f'<circle cx="{x}" cy="78" r="5" fill="{WHITE}" stroke-width="4"/><circle cx="{x}" cy="162" r="5" fill="{WHITE}" stroke-width="4"/>' for x in range(52, 212, 20))}
      <rect x="112" y="102" width="36" height="36" rx="4" fill="{INK}"/>
      <circle cx="78" cy="120" r="9" fill="{WHITE}"/>
      <rect x="178" y="108" width="20" height="24" rx="3" fill="{GREY}"/>""",
    "raspberry-pi": f"""
      <rect x="18" y="52" width="190" height="136" rx="14" fill="{GREEN}"/>
      <rect x="44" y="62" width="138" height="20" rx="3" fill="{INK}"/>
      {"".join(f'<circle cx="{x}" cy="72" r="2.5" fill="#e6b84a" stroke="none"/>' for x in range(54, 176, 12))}
      <rect x="66" y="104" width="52" height="52" rx="6" fill="{GREY}"/>
      <rect x="132" y="112" width="26" height="30" rx="3" fill="{INK}"/>
      <rect x="186" y="96" width="38" height="28" rx="3" fill="{GREY}"/>
      <rect x="186" y="134" width="38" height="28" rx="3" fill="{GREY}"/>
      <circle cx="34" cy="68" r="5" fill="{WHITE}" stroke-width="4"/>
      <circle cx="34" cy="172" r="5" fill="{WHITE}" stroke-width="4"/>""",
    "cardboard": f"""
      <path d="M44 96l76 32v90l-76-32z" fill="{BROWN}"/>
      <path d="M120 128l76-32v90l-76 32z" fill="{BROWN_D}"/>
      <path d="M44 96l-18 30 76 32 18-30z" fill="{BROWN_L}"/>
      <path d="M196 96l18 30-76 32-18-30z" fill="{BROWN_L}"/>
      <path d="M44 96l76-32 76 32-76 32z" fill="#a8743f"/>
      <path d="M70 152l26 11" stroke-width="5"/>""",
    "tin-foil": f"""
      <path d="M44 72l42-14 30 18 42-16 38 22-10 40 14 38-44 18-34-12-38 16-38-18 10-42z" fill="#dfe3ea"/>
      <path d="M78 102l30 22 22-26 32 34M86 164l26-20 30 18M64 132l20-6" stroke="{GREY_D}" stroke-width="4"/>
      <path d="M176 52v18M167 61h18" stroke="{ORANGE}" stroke-width="5"/>""",
    "paperclips": f"""
      <g transform="rotate(-14 96 120)">
        <path d="M78 58v118a20 20 0 0 0 40 0V48a14 14 0 0 0-28 0v116" stroke-width="16"/>
        <path d="M78 58v118a20 20 0 0 0 40 0V48a14 14 0 0 0-28 0v116" stroke="{BLUE}" stroke-width="7"/>
      </g>
      <g transform="rotate(16 150 120)">
        <path d="M132 70v110a20 20 0 0 0 40 0V60a14 14 0 0 0-28 0v108" stroke-width="16"/>
        <path d="M132 70v110a20 20 0 0 0 40 0V60a14 14 0 0 0-28 0v108" stroke="{RED}" stroke-width="7"/>
      </g>""",
    "bricks": f"""
      {"".join(f'<rect x="{x}" y="128" width="26" height="18" rx="4" fill="{YELLOW}"/>' for x in (50, 88, 126, 164))}
      <rect x="36" y="144" width="168" height="58" rx="8" fill="{YELLOW}"/>
      {"".join(f'<rect x="{x}" y="58" width="26" height="18" rx="4" fill="{BLUE}"/>' for x in (82, 132))}
      <rect x="66" y="74" width="108" height="56" rx="8" fill="{BLUE}"/>""",
    "string": f"""
      <path d="M158 170c22 12 30 24 52 16" />
      <circle cx="110" cy="124" r="64" fill="{ORANGE}"/>
      <g stroke-width="4" stroke="#b5530f">
        <ellipse cx="110" cy="124" rx="64" ry="22" transform="rotate(-35 110 124)"/>
        <ellipse cx="110" cy="124" rx="64" ry="40" transform="rotate(-35 110 124)"/>
        <ellipse cx="110" cy="124" rx="64" ry="26" transform="rotate(40 110 124)"/>
        <ellipse cx="110" cy="124" rx="64" ry="14" transform="rotate(90 110 124)"/>
      </g>
      <circle cx="110" cy="124" r="64"/>""",
    "plastic-bottle": f"""
      <rect x="102" y="24" width="36" height="24" rx="5" fill="{BLUE}"/>
      <path d="M106 48h28v16l22 28v108a16 16 0 0 1-16 16h-40a16 16 0 0 1-16-16V92l22-28z" fill="#d6ecfa"/>
      <rect x="84" y="128" width="72" height="44" fill="{TEAL_L}"/>
      <path d="M100 104v14" stroke="{WHITE}" stroke-width="7"/>""",
}

for name, body in art.items():
    (OUT / f"{name}.svg").write_text(svg(body))

favicon = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
    '<circle cx="32" cy="36" r="26" fill="#9e1814"/>'
    '<circle cx="32" cy="30" r="26" fill="#e0302c"/>'
    '<path d="M20 22a14 14 0 0 1 10-8" stroke="#fff" stroke-width="5" stroke-linecap="round" fill="none"/></svg>\n'
)
(OUT.parent / "favicon.svg").write_text(favicon)
print(len(art), "illustrations written")
