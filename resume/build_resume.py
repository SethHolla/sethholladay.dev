"""Builds seth-holladay.pdf. Edit the content below, then run: python resume/build_resume.py"""
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
OUT = ROOT / "seth-holladay.pdf"
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


header = table([[
    [Paragraph("Seth Holladay", name_style), Paragraph("Game Programmer", title_style)],
    Paragraph("<br/>".join([
        link("https://sethholladay.dev", "sethholladay.dev") + f" {dim('|')} " +
        link("https://sethholladay.itch.io", "sethholladay.itch.io"),
        link("mailto:sethholladay6@gmail.com", "sethholladay6@gmail.com") + f" {dim('|')} (435) 881-3791",
        link("https://github.com/SethHolla", "github.com/SethHolla") + f" {dim('|')} " +
        link("https://www.linkedin.com/in/t-seth-holladay/", "linkedin.com/in/t-seth-holladay"),
    ]), contact_style),
]], [WIDTH * 0.5, WIDTH * 0.5], [("VALIGN", (0, 0), (-1, -1), "BOTTOM")])

story = [
    header,
    HRFlowable(width="100%", thickness=1.4, color=INK, spaceBefore=8, spaceAfter=7),
    Paragraph(
        "Gameplay programmer specializing in character control and multiplayer systems. Spent five years building "
        "<i>It Was You</i>, an online murder mystery for 5–12 players coming to Steam, alongside four years of "
        "professional software engineering. Proficient in C# and C++ with Unity and Unreal Engine.", summary_style),

    *section("Game Development Experience"),
    entry(f"Snowfall Games {dim('|')} <i>It Was You</i> (Steam)", "Sep 2020 – Aug 2025", "Game Engineer",
          "Remote", [
              "Architected the player character controller from scratch for a first-person multiplayer murder "
              "mystery, using a modular design that drives animation across the game’s many items so new ones slot "
              "in cleanly.",
              "Co-developed core gameplay systems, including a targeting system built into the networking layer.",
          ], first=True),
    entry("Jetty Games", "Sep 2026 – Present", "Co-Founder &amp; Engineering Producer", "Salt Lake City, UT", [
        "Co-founded a 10-person indie team that ships complete games on jam deadlines, including <i>Attiction</i>.",
        "Program gameplay while also producing: set milestones and run meetings that keep art, design, and audio "
        "in sync.",
    ]),

    *section("Software Engineering Experience"),
    entry(f"Mappslab {dim('|')} Children’s Media Workshop", "Jul 2021 – Jan 2025", "Lead Developer",
          "Salt Lake City, UT", [
              "Led development of an interactive mapping platform used in classrooms, where students draw on maps, "
              "plot routes, collaborate, and present their work as slideshows (React, Next.js, PostgreSQL).",
              "Cut page load times by rebuilding data fetching and caching around React Query.",
              "Designed the PostgreSQL schema and tuned queries to keep data consistent and the app responsive.",
          ], first=True),
    entry("Place", "Jul 2023 – Jan 2024", "Software Engineer", "Draper, UT", [
        "Diagnosed and cleared a 3-month backlog of QA-escalated bugs within a month of joining.",
        "Led a performance push across thousands of client websites, auditing load times, optimizing asset "
        "delivery, and fixing slow-rendering elements to raise SEO scores.",
        "Led frontend development of a new Next.js analytics tool, including its data visualizations and reports.",
    ]),
    entry("Atomic Jolt", "Jul 2020 – Aug 2021", "Software Engineer", "Remote", [
        "Built and deployed learning tools adopted by 13 schools and organizations.",
        "Maintained client sites and tools, resolving security and email deliverability issues and shipping new "
        "features.",
    ]),

    *section("Game Jam Projects"),
    Paragraph("<b>Matter of Factory</b> – Engineer &amp; Producer, 1-Bit Jam 11. One of two engineers on a "
              "factory-automation game.", bullet_style, bulletText=BULLET),
    Paragraph("<b>Luci Forever</b> – Engineer &amp; Artist, Maxwell Rodgers Memorial Jam 2026. Coded and drew "
              "art for a cozy pet sim.", bullet_style, bulletText=BULLET),
    Paragraph("<b>One True Door</b> – Developer, week-long Unity game jam. Built a complete game from scratch with "
              "a team of three.", bullet_style, bulletText=BULLET),

    *section("Education"),
    table([[Paragraph(f"University of Utah {dim('|')} <font name='OpenSans'>B.S. Computer Science</font>",
                      org_style),
            Paragraph("Expected Spring 2028 · Salt Lake City, UT", meta_style)]],
          [WIDTH * 0.6, WIDTH * 0.4]),

    KeepTogether([*section("Skills"), table([[Paragraph(label, label_style), Paragraph(value, value_style)] for label, value in [
        ("Languages", "C#, C++, C, Lua, TypeScript, JavaScript, Python, Java, Rust, SQL, PHP"),
        ("Game Development", "Unity, Unreal Engine, gameplay systems, character controllers, animation, multiplayer"),
        ("Web &amp; Tools", "React, Next.js, PostgreSQL, Ruby on Rails, Git, JetBrains IDEs, Linux"),
    ]], [WIDTH * 0.2, WIDTH * 0.8], [("BOTTOMPADDING", (0, 0), (-1, -2), 2.5)])]),
]

doc = SimpleDocTemplate(str(OUT), pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
                        topMargin=0.5 * inch, bottomMargin=0.45 * inch, title="Seth Holladay \u2013 Resume",
                        author="Seth Holladay", subject="Game Programmer Resume")
doc.build(story)
print(f"Wrote {OUT}")
