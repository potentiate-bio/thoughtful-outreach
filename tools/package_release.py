#!/usr/bin/env python3
"""Zip the skill folder for upload to chat apps (Claude, ChatGPT, Gemini skill uploads).
Writes dist/target-list-research.zip with SKILL.md at the top of the skill folder."""
import os, zipfile
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILL = os.path.join(ROOT, "skills", "target-list-research")
os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
out = os.path.join(ROOT, "dist", "target-list-research.zip")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for d, _, files in os.walk(SKILL):
        for f in files:
            if f.endswith(".pyc") or "__pycache__" in d:
                continue
            p = os.path.join(d, f)
            z.write(p, os.path.join("target-list-research", os.path.relpath(p, SKILL)))
print("wrote", out)
