"""
Fills Agile_Template_v0.1.xls (Sprint Backlog / User Stories) for
AI Code Review & Security Analysis Agent — Milestones 1 & 2
Run: python fill_agile_template.py

Uses xlwt for .xls format. Install if needed:
  pip install xlwt xlrd xlutils
"""
import os
import sys

# ── Try to import xlutils (handles both reading & writing .xls) ────────────
try:
    import xlrd
    from xlutils.copy import copy as xl_copy
    USE_XLUTILS = True
except ImportError:
    USE_XLUTILS = False

try:
    import xlwt
    HAS_XLWT = True
except ImportError:
    HAS_XLWT = False

FILE_PATH = r"C:\Users\Siddu Vinayaka\Downloads\Agile_Template_v0.1.xls"

# ── User Story data ────────────────────────────────────────────────────────
# (Planned Sprint, Actual Sprint, US ID, User Story Description,
#  MOSCOW, Dependency, Assignee, Status)
user_stories = [
    (
        "Sprint 1", "Sprint 1", "US-001",
        "As a developer, I want to paste Python or Java code directly into the portal "
        "so I can get an automated AI review without uploading a file.",
        "Must Have", "None", "Developer", "Completed"
    ),
    (
        "Sprint 1", "Sprint 1", "US-002",
        "As a developer, I want to upload a .py or .java source file so I can review "
        "real project code from my local machine.",
        "Must Have", "US-001", "Developer", "Completed"
    ),
    (
        "Sprint 1", "Sprint 1", "US-003",
        "As a developer, I want the system to automatically detect whether my code is "
        "Python or Java so I don't have to select the language manually.",
        "Must Have", "US-001", "Developer", "Completed"
    ),
    (
        "Sprint 1", "Sprint 1", "US-004",
        "As a developer, I want the system to validate my code's syntax before running "
        "AI analysis so I receive meaningful feedback on broken code and avoid wasting API credits.",
        "Must Have", "US-003", "Developer", "Completed"
    ),
    (
        "Sprint 1", "Sprint 1", "US-005",
        "As a developer, I want OWASP guidelines and secure coding standards indexed "
        "into a RAG pipeline so the Security Agent has authoritative, up-to-date "
        "context when scanning my code.",
        "Must Have", "None", "Developer", "Completed"
    ),
    (
        "Sprint 2", "Sprint 2", "US-006",
        "As a developer, I want a Code Analysis Agent to identify code smells, "
        "complexity issues, and design anti-patterns with severity scoring (High / "
        "Medium / Low) so I can improve code quality systematically.",
        "Must Have", "US-003", "Developer", "Completed"
    ),
    (
        "Sprint 2", "Sprint 2", "US-007",
        "As a developer, I want a Security Vulnerability Agent to scan my code for "
        "OWASP-standard vulnerabilities (SQL Injection, XSS, Hardcoded Secrets, Weak "
        "Cryptography, etc.) and classify them by type and severity with "
        "location-specific flagging.",
        "Must Have", "US-005", "Developer", "Completed"
    ),
    (
        "Sprint 2", "Sprint 2", "US-008",
        "As a developer, I want the Code Analysis and Security Vulnerability agents "
        "to run in parallel via a LangGraph orchestrator so that overall analysis "
        "time is minimised.",
        "Must Have", "US-006, US-007", "Developer", "Completed"
    ),
    (
        "Sprint 2", "Sprint 2", "US-009",
        "As a developer, I want all agent findings merged into a single unified list "
        "sorted by severity (High → Medium → Low) so I can prioritise the most "
        "critical issues first.",
        "Must Have", "US-008", "Developer", "Completed"
    ),
    (
        "Sprint 2", "Sprint 2", "US-010",
        "As a developer, I want the system's detection accuracy validated against "
        "sample Python and Java codebases containing known quality issues and "
        "vulnerabilities, so I can confirm the agents are working correctly.",
        "Must Have", "US-006, US-007", "Developer", "Completed"
    ),
]

# ══════════════════════════════════════════════════════════════════════════
#  APPROACH 1: Use xlutils to copy existing template and write into it
# ══════════════════════════════════════════════════════════════════════════
if USE_XLUTILS:
    print("Using xlutils to preserve template formatting...")

    rb = xlrd.open_workbook(FILE_PATH, formatting_info=True)
    wb = xl_copy(rb)

    # Find the first sheet
    sheet_name = rb.sheet_names()[0]
    print(f"Sheet name: '{sheet_name}'")
    ws = wb.get_sheet(0)

    # ── Styles ──────────────────────────────────────────────────────────
    font_body = xlwt.Font()
    font_body.name = "Arial"
    font_body.height = 200   # 10pt

    font_done = xlwt.Font()
    font_done.name = "Arial"
    font_done.bold = True
    font_done.height = 200
    font_done.colour_index = xlwt.Style.colour_map.get("dark_green", 0x3A)

    al_wrap = xlwt.Alignment()
    al_wrap.wrap = xlwt.Alignment.WRAP_AT_RIGHT
    al_wrap.vert = xlwt.Alignment.VERT_CENTER

    al_center = xlwt.Alignment()
    al_center.horz = xlwt.Alignment.HORZ_CENTER
    al_center.vert = xlwt.Alignment.VERT_CENTER

    thin = xlwt.Borders()
    thin.left   = xlwt.Borders.THIN
    thin.right  = xlwt.Borders.THIN
    thin.top    = xlwt.Borders.THIN
    thin.bottom = xlwt.Borders.THIN

    def make_style(font, alignment):
        s = xlwt.XFStyle()
        s.font      = font
        s.alignment = alignment
        s.borders   = thin
        return s

    style_body   = make_style(font_body, al_wrap)
    style_center = make_style(font_body, al_center)
    style_done   = make_style(font_done, al_center)

    # ── Write rows starting at row index 1 (row 2 in WPS) ───────────────
    for idx, us in enumerate(user_stories):
        row = idx + 1   # 0-indexed; row 0 = header
        ws.row(row).height_mismatch = True
        ws.row(row).height = 1200  # ~60pt

        for col, val in enumerate(us):
            if col in (0, 1, 2, 4, 5, 6):   # centred columns
                ws.write(row, col, val, style_center)
            elif col == 7:                    # Status — coloured
                ws.write(row, col, val, style_done)
            else:
                ws.write(row, col, val, style_body)

    wb.save(FILE_PATH)
    print("\n" + "=" * 55)
    print("  Agile_Template_v0.1.xls — FILLED SUCCESSFULLY!")
    print("=" * 55)
    print(f"\n  Location: {FILE_PATH}")
    print(f"  User stories written: {len(user_stories)}")

# ══════════════════════════════════════════════════════════════════════════
#  APPROACH 2: xlutils not available — create fresh with xlwt
# ══════════════════════════════════════════════════════════════════════════
elif HAS_XLWT:
    print("xlutils not found — creating fresh .xls file with xlwt...")

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Sprint Backlog")

    # Header style
    h_font = xlwt.Font()
    h_font.bold = True
    h_font.name = "Arial"
    h_font.height = 220
    h_font.colour_index = 0x01  # white — will be on orange bg

    h_pat = xlwt.Pattern()
    h_pat.pattern       = xlwt.Pattern.SOLID_PATTERN
    h_pat.pattern_colour = 0x34   # orange

    h_al = xlwt.Alignment()
    h_al.horz = xlwt.Alignment.HORZ_CENTER
    h_al.vert = xlwt.Alignment.VERT_CENTER
    h_al.wrap = xlwt.Alignment.WRAP_AT_RIGHT

    h_borders = xlwt.Borders()
    h_borders.left = h_borders.right = h_borders.top = h_borders.bottom = xlwt.Borders.THIN

    h_style = xlwt.XFStyle()
    h_style.font      = h_font
    h_style.pattern   = h_pat
    h_style.alignment = h_al
    h_style.borders   = h_borders

    # Write headers
    headers = [
        "Planned Sprint", "Actual Sprint", "US ID",
        "User Story Description", "MOSCOW", "Dependency", "Assignee", "Status"
    ]
    col_widths = [18, 18, 12, 65, 14, 18, 14, 14]

    ws.row(0).height_mismatch = True
    ws.row(0).height = 800
    for col, (h, w) in enumerate(zip(headers, col_widths)):
        ws.write(0, col, h, h_style)
        ws.col(col).width = w * 256

    # Body styles
    al_wrap = xlwt.Alignment()
    al_wrap.wrap = xlwt.Alignment.WRAP_AT_RIGHT
    al_wrap.vert = xlwt.Alignment.VERT_CENTER

    al_center = xlwt.Alignment()
    al_center.horz = xlwt.Alignment.HORZ_CENTER
    al_center.vert = xlwt.Alignment.VERT_CENTER

    thin = xlwt.Borders()
    thin.left = thin.right = thin.top = thin.bottom = xlwt.Borders.THIN

    pat_alt = xlwt.Pattern()
    pat_alt.pattern       = xlwt.Pattern.SOLID_PATTERN
    pat_alt.pattern_colour = 0x2C  # light blue

    pat_white = xlwt.Pattern()
    pat_white.pattern       = xlwt.Pattern.SOLID_PATTERN
    pat_white.pattern_colour = 0x01  # white

    def body_style(alt, center=False, done=False):
        s = xlwt.XFStyle()
        f = xlwt.Font(); f.name = "Arial"; f.height = 200
        if done:
            f.bold = True
        s.font      = f
        s.borders   = thin
        s.pattern   = pat_alt if alt else pat_white
        al = al_center if center else al_wrap
        s.alignment = al
        return s

    for idx, us in enumerate(user_stories):
        row  = idx + 1
        alt  = (idx % 2 == 1)
        ws.row(row).height_mismatch = True
        ws.row(row).height = 1400

        for col, val in enumerate(us):
            center = col in (0, 1, 2, 4, 5, 6)
            done   = (col == 7)
            ws.write(row, col, val, body_style(alt, center, done))

    wb.save(FILE_PATH)
    print("\n" + "=" * 55)
    print("  Agile_Template_v0.1.xls — FILLED SUCCESSFULLY!")
    print("=" * 55)
    print(f"\n  Location: {FILE_PATH}")
    print(f"  User stories written: {len(user_stories)}")

# ══════════════════════════════════════════════════════════════════════════
#  APPROACH 3: Nothing available — guide user to install
# ══════════════════════════════════════════════════════════════════════════
else:
    print("ERROR: Required packages not found.")
    print("Please run:  pip install xlwt xlrd xlutils")
    print("Then re-run: python fill_agile_template.py")
    sys.exit(1)

print("\n  Open the file in WPS to review!")
print("\n  All 3 files are now complete! ✅")
