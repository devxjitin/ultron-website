"""One-off helper: reads the Android app's ConnectorRegistry.kt and DeviceTool.kt and writes data/connectors.json
(connectors, their tools with plain labels, access and privacy facts). Use-case text is written by hand afterwards
in data/usecases.json, so re-running this never overwrites it.

Usage: python scripts/extract_connectors.py <path to android/app/src/main/java/com/assistant/app/data>
"""
import json
import re
import sys
from pathlib import Path

APP = Path(sys.argv[1])
reg = (APP / "ConnectorRegistry.kt").read_text(encoding="utf-8")
tools_src = (APP / "DeviceTool.kt").read_text(encoding="utf-8")

STR = r'"((?:[^"\\]|\\.)*)"'

tools = {}
for m in re.finditer(r'^\s{4}([A-Z_]+)\(\s*"(\w+)",\s*' + STR + r',\s*' + STR, tools_src, re.M):
    tools[m.group(1)] = {"fn": m.group(2), "label": m.group(3), "hint": m.group(4)}

cats = {"ESSENTIALS": "Essentials", "SEARCH_MEDIA": "Search and media", "PERSONAL": "Personal data", "PHONE_CONTROL": "Phone control"}
conns = []
spec = re.compile(
    r'ConnectorSpec\(\s*id = "(\w+)", name = "([^"]+)", description = "([^"]+)",\s*subtitle = "([^"]+)", '
    r'category = ConnectorCategory\.(\w+), kind = ConnectorKind\.(\w+),\s*permissions = (.*?), '
    r'access = SpecialAccess\.(\w+), defaultOn = (\w+),\s*tools = listOf\((.*?)\)\s*\)', re.S)
for m in spec.finditer(reg):
    ids = re.findall(r'DeviceTool\.(\w+)', m.group(10))
    conns.append({"id": m.group(1), "name": m.group(2), "desc": m.group(3), "sub": m.group(4), "cat": cats[m.group(5)],
                  "kind": m.group(6).lower(), "access": m.group(8), "on": m.group(9) == "true",
                  "tools": [dict(tools[t], key=t) for t in ids]})
infos = {}
info = re.compile(r'"(\w+)" to ConnectorInfo\(\s*' + STR + r',\s*' + STR + r',\s*' + STR + r'(?:,\s*' + STR + r')?')
for m in info.finditer(reg):
    infos[m.group(1)] = {"about": m.group(2), "needs": m.group(3), "privacy": m.group(4), "runs": m.group(5) or "Your phone"}
for c in conns:
    c.update(infos[c["id"]])
Path("data").mkdir(exist_ok=True)
Path("data/connectors.json").write_text(json.dumps(conns, indent=1, ensure_ascii=False), encoding="utf-8")
print(len(conns), "connectors,", sum(len(c["tools"]) for c in conns), "tools")
