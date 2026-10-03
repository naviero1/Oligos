#!/usr/bin/env python3
"""Render the Phase 2 submission PDFs, substituting live dataset numbers.

The documents quote dozens of counts. Hand-maintaining them guarantees drift — a
stale table is indistinguishable from a fresh one, and these documents went out of
date once inside a single working session. So the HTML sources carry {{placeholders}}
and every number is filled from the data at render time.

Any placeholder without a value is a hard error: shipping a document containing a
literal "{{n_meas}}" would be worse than shipping a stale number, and silently
leaving it blank would be worse still.

Page limits are enforced here rather than left to a reviewer.

Usage:  python3 scripts/render_submission.py
"""
import os, re, subprocess, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from submission_stats import stats

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUB = os.path.join(ENDPOINT, "submission")
LIMITS = {"narrative": 12, "methodology": 5, "padp": 5}


def chrome():
    for c in ("/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
              shutil.which("chromium"), shutil.which("google-chrome")):
        if c and os.path.exists(c):
            return c
    sys.exit("no Chromium found to render PDFs")


def main():
    d = stats()
    # derived percentages the documents quote in prose
    hu = int(d["n_human"].replace(",", ""))
    tot = int(d["n_meas"].replace(",", ""))
    d.setdefault("pct_human", str(round(100 * hu / tot)))

    ch, fail = chrome(), 0
    for doc, limit in LIMITS.items():
        src = os.path.join(SUB, f"{doc}.html")
        html = open(src, encoding="utf-8").read()

        missing = sorted(set(re.findall(r"\{\{(\w+)\}\}", html)) - set(d))
        if missing:
            sys.exit(f"{doc}.html references placeholders with no value: {missing}")
        rendered = re.sub(r"\{\{(\w+)\}\}", lambda m: str(d[m.group(1)]), html)

        tmp = os.path.join(SUB, f".{doc}.rendered.html")
        open(tmp, "w", encoding="utf-8").write(rendered)
        out = os.path.join(SUB, f"{doc}.pdf")
        subprocess.run([ch, "--headless", "--disable-gpu", "--no-sandbox",
                        "--no-pdf-header-footer", f"--print-to-pdf={out}", tmp],
                       capture_output=True)
        os.remove(tmp)

        import pymupdf
        n = len(pymupdf.open(out))
        if n > limit:
            print(f"  FAIL {doc}.pdf: {n} pages exceeds the {limit}-page limit")
            fail = 1
        else:
            print(f"  ok   {doc}.pdf: {n} / {limit} pages")
    if fail:
        sys.exit(1)
    print(f"\nrendered with live figures: {d['n_meas']} measurements · {d['n_oligos']} oligos "
          f"· {d['n_human']} human · {d['n_bridge']} bridge compounds")


if __name__ == "__main__":
    main()
