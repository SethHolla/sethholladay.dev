"""Builds both resumes. Run: python resume/build_resume.py  (add "game" or "software" to build just one)"""
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

ROOT = Path(__file__).resolve().parent.parent
FONTS = Path("C:/Windows/Fonts")

# Montserrat for the name and headings, Open Sans for body text
pdfmetrics.registerFont(TTFont("Montserrat", FONTS / "Montserrat-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Montserrat-Bold", FONTS / "Montserrat-Bold.ttf"))
pdfmetrics.registerFont(TTFont("OpenSans", FONTS / "OpenSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("OpenSans-Bold", FONTS / "OpenSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("OpenSans-Italic", FONTS / "OpenSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("OpenSans-BoldItalic", FONTS / "OpenSans-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("SegoeSymbol", FONTS / "seguisym.ttf"))
pdfmetrics.registerFontFamily("OpenSans", normal="OpenSans", bold="OpenSans-Bold", italic="OpenSans-Italic",
                              boldItalic="OpenSans-BoldItalic")

# Neutral charcoal palette
INK = HexColor("#1a1a1a")
MUTED = HexColor("#5c5c5c")
SOFT = HexColor("#8a8a8a")
RULE = HexColor("#c8c8c8")
BODY = 9.4

MARGIN = 0.6 * inch
# frame width: page minus margins minus the frame's 6pt padding on each side
WIDTH = letter[0] - 2 * MARGIN - 12

name_style = ParagraphStyle("name", fontName="Montserrat-Bold", fontSize=25, leading=27, textColor=INK)
title_style = ParagraphStyle("title", fontName="Montserrat", fontSize=11.5, leading=15, textColor=MUTED)
contact_style = ParagraphStyle("contact", fontName="OpenSans", fontSize=8.6, leading=12.4, textColor=MUTED,
                               alignment=TA_RIGHT)
summary_style = ParagraphStyle("summary", fontName="OpenSans", fontSize=BODY, leading=13.6, textColor=INK)
section_style = ParagraphStyle("section", fontName="Montserrat-Bold", fontSize=10, leading=12, textColor=INK)
org_style = ParagraphStyle("org", fontName="OpenSans-Bold", fontSize=9.8, leading=12.6, textColor=INK)
role_style = ParagraphStyle("role", fontName="OpenSans-Italic", fontSize=BODY, leading=12.6, textColor=MUTED)
meta_style = ParagraphStyle("meta", fontName="OpenSans", fontSize=8.6, leading=12.6, textColor=MUTED,
                            alignment=TA_RIGHT)
bullet_style = ParagraphStyle("bullet", fontName="OpenSans", fontSize=BODY, leading=12.7, textColor=INK,
                              leftIndent=13, bulletIndent=2, bulletFontName="SegoeSymbol", bulletFontSize=8,
                              bulletColor=SOFT, spaceBefore=1.6)
label_style = ParagraphStyle("label", fontName="OpenSans-Bold", fontSize=BODY, leading=12.6, textColor=INK)
value_style = ParagraphStyle("value", fontName="OpenSans", fontSize=BODY, leading=12.6, textColor=INK)

BULLET = "\u25AA"
TIGHT = [("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
         ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
         ("VALIGN", (0, 0), (-1, -1), "TOP")]


def link(url, text):
    return f'<link href="{url}" color="#1a1a1a">{text}</link>'


def dim(text):
    return f'<font color="#b0b0b0">{text}</font>'


# Placeholder numbers to replace with real ones. They print highlighted in yellow and the build warns about them
# so a made-up figure never goes out by accident. Swap tbd("40%") for plain "40%" once it's accurate.
PLACEHOLDERS = []


def tbd(text):
    PLACEHOLDERS.append(text)
    return f'<span backColor="#fff176">{text}</span>'


def table(rows, widths, extra=()):
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle(TIGHT + list(extra)))
    return t


def section(title):
    # heading on the left, hairline running out to the right edge
    text = title.upper()
    text_w = pdfmetrics.stringWidth(text, "Montserrat-Bold", 10) + 7
    rule = HRFlowable(width="100%", thickness=0.6, color=RULE, spaceBefore=0, spaceAfter=0)
    head = table([[Paragraph(text, section_style), rule]], [text_w, WIDTH - text_w],
                 [("VALIGN", (1, 0), (1, 0), "MIDDLE")])
    return [Spacer(1, 11), head, Spacer(1, 5)]


def entry(org, dates, role, place, bullets, first=False):
    head = table([[Paragraph(org, org_style), Paragraph(dates, meta_style)],
                  [Paragraph(role, role_style), Paragraph(place, meta_style)]],
                 [WIDTH * 0.72, WIDTH * 0.28])
    parts = [] if first else [Spacer(1, 6)]
    parts += [head] + [Paragraph(b, bullet_style, bulletText=BULLET) for b in bullets]
    return KeepTogether(parts)


def header(title):
    return table([[
        [Paragraph("Seth Holladay", name_style), Paragraph(title, title_style)],
        Paragraph("<br/>".join([
            link("https://sethholladay.dev", "sethholladay.dev") + f" {dim('|')} " +
            link("https://sethholladay.itch.io", "sethholladay.itch.io"),
            link("mailto:sethholladay6@gmail.com", "sethholladay6@gmail.com") + f" {dim('|')} (435) 881-3791",
            link("https://github.com/SethHolla", "github.com/SethHolla") + f" {dim('|')} " +
            link("https://www.linkedin.com/in/t-seth-holladay/", "linkedin.com/in/t-seth-holladay"),
        ]), contact_style),
    ]], [WIDTH * 0.5, WIDTH * 0.5], [("VALIGN", (0, 0), (-1, -1), "BOTTOM")])


# ---- Shared content: edit once, both resumes update ----

def game_development():
    return [
        *section("Game Development"),
        entry(f"Snowfall Games {dim('|')} " + link("https://store.steampowered.com/app/1967050/It_Was_You/",
                                                    "<i>It Was You</i> (upcoming on Steam)"),
              "Sep 2020 – Aug 2025", "Game Engineer · Volunteer, indie studio", "Remote", [
                  f"Architected the first-person character controller in Unity (C#) from scratch, with a modular "
                  f"design that drives animation across 20+ items so new ones slot in cleanly.",
                  "Co-developed core gameplay systems on Mirror, including a targeting system synced across 12 players.",
              ], first=True),
        entry("Jetty Games", "Mar 2026 – Present", "Co-Founder &amp; Lead Programmer · Indie team",
              "Salt Lake City, UT", [
                  "Co-founded a 10-person indie team that shipped 5+ games in game jams over summer 2026.",
                  "Led programming on every project, setting up each codebase and coordinating engineers to hit "
                  "jam deadlines.",
              ]),
    ]


def software_experience():
    return [
        *section("Software Engineering Experience"),
        entry(f"Mappslab {dim('|')} Children’s Media Workshop", "Jul 2021 – Jan 2025",
              "Lead Developer (Contract)", "Salt Lake City, UT", [
                  "Led development of an interactive mapping platform used in classrooms, where students draw on "
                  "maps, plot routes, collaborate, and present their work as slideshows (React, Next.js, PostgreSQL).",
                  f"Cut page load times by 40% by rebuilding data fetching and caching around React Query.",
                  f"Designed the PostgreSQL schema and tuned slow queries from 2s to under 200ms.",
              ], first=True),
        entry("Place", "Jul 2023 – Jan 2024", "Software Engineer", "Draper, UT", [
            "Diagnosed and cleared a 3-month backlog of QA-escalated bugs within a month of joining.",
            "Led a performance push across thousands of client websites, optimizing asset delivery and slow-rendering "
            f"elements to raise average Lighthouse scores from 60 to 90.",
            "Led frontend development of a new Next.js analytics tool, including its data visualizations and reports.",
        ]),
        entry("Atomic Jolt", "Jul 2020 – Aug 2021", "Software Engineer", "Remote", [
            "Built and deployed learning tools adopted by 13 schools and organizations.",
            "Maintained client sites and tools, resolving security and email deliverability issues and shipping new "
            "features.",
        ]),
    ]


def game_jams():
    return [
        *section("Game Jam Projects"),
        Paragraph(f"<b>{link('https://spacetuna.itch.io/matter-of-factory', 'Matter of Factory')}</b> – Engineer "
                  "&amp; Producer, 1-Bit Jam 11. One of two programmers on a factory builder about refining "
                  "Dark Matter into energy.",
                  bullet_style, bulletText=BULLET),
        Paragraph(f"<b>{link('https://sethholladay.itch.io/luci-forever', 'Luci Forever')}</b> – Engineer &amp; "
                  "Artist, Maxwell Rodgers Memorial Jam 2026. Programmed gameplay and drew pixel art for a cozy "
                  "browser pet sim about raising a shrimp that arrives in a mystery package.",
                  bullet_style, bulletText=BULLET),
        Paragraph(f"<b>{link('https://kirill-malyshko.itch.io/attiction', 'Attiction')}</b> – Engineer &amp; "
                  "Producer, Anomaly Horror Jam. An anomaly-hunting escape room set in a looping attic.",
                  bullet_style, bulletText=BULLET),
    ]


def education():
    return [
        *section("Education"),
        table([[Paragraph(f"University of Utah {dim('|')} <font name='OpenSans'>B.S. Computer Science</font>",
                          org_style),
                Paragraph("Expected Spring 2028 · Salt Lake City, UT", meta_style)]],
              [WIDTH * 0.6, WIDTH * 0.4]),
    ]


def skills(rows):
    return [KeepTogether([*section("Skills"), table(
        [[Paragraph(label, label_style), Paragraph(value, value_style)] for label, value in rows],
        [WIDTH * 0.2, WIDTH * 0.8], [("BOTTOMPADDING", (0, 0), (-1, -2), 2.5)])])]


GAME_SKILLS = ("Game Development", "Unity, Mirror networking, gameplay systems, character controllers, animation")
WEB_SKILLS = ("Web &amp; Tools", "React, Next.js, React Query, PostgreSQL, Git, JetBrains IDEs, Linux")

# ---- The two versions: same content, different title, summary, and order ----

VARIANTS = {
    "game": dict(
        out="seth-holladay.pdf",
        title="Game Programmer",
        summary="Game programmer specializing in gameplay systems, character controllers, and multiplayer in Unity "
                "with C# and C++. Brings four years of professional software engineering and a habit of shipping on "
                "deadline.",
        sections=lambda: game_development() + software_experience() + game_jams() + education() + skills([
            ("Languages", "C#, C++, TypeScript, JavaScript, Python, SQL"),
            GAME_SKILLS, WEB_SKILLS]),
    ),
    "software": dict(
        out="seth-holladay-software.pdf",
        title="Software Engineer",
        summary="Full-stack engineer with four years of professional experience building React, Next.js, and "
                "PostgreSQL apps, with a track record of speeding up slow pages and clearing bug backlogs. Also builds "
                "multiplayer games in Unity and C#.",
        sections=lambda: software_experience() + game_development() + game_jams() + education() + skills([
            ("Languages", "TypeScript, JavaScript, SQL, Python, C#, C++"),
            WEB_SKILLS, GAME_SKILLS]),
    ),
}


def build(name):
    v = VARIANTS[name]
    out = ROOT / v["out"]
    PLACEHOLDERS.clear()
    story = [
        header(v["title"]),
        HRFlowable(width="100%", thickness=1.4, color=INK, spaceBefore=8, spaceAfter=7),
        Paragraph(v["summary"], summary_style),
        *v["sections"](),
    ]
    doc = SimpleDocTemplate(str(out), pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=0.5 * inch, bottomMargin=0.45 * inch, title="Seth Holladay – Resume",
                            author="Seth Holladay", subject=f"{v['title']} Resume")
    doc.build(story)
    print(f"Wrote {out}")
    if PLACEHOLDERS:
        print(f"  WARNING: {len(PLACEHOLDERS)} placeholder numbers still highlighted: {', '.join(PLACEHOLDERS)}")


if __name__ == "__main__":
    import sys
    for name in (sys.argv[1:] or VARIANTS):
        build(name)
