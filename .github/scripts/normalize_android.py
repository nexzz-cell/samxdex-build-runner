#!/usr/bin/env python3
from pathlib import Path
import re
import sys

AGP = "8.11.1"
GRADLE = "8.13"
VERSION_RE = re.compile(r"(?:[1-9]|10)(?:\.0)?")

root = Path(sys.argv[1]).resolve()
version = sys.argv[2] if len(sys.argv) > 2 else "1.0"
if not VERSION_RE.fullmatch(version):
    raise SystemExit("VERSION_NAME harus 1.0 sampai 10.0")

android = root / "android"
if not android.is_dir():
    raise SystemExit("Folder android tidak ditemukan setelah project preparation")

for name in ("settings.gradle", "build.gradle"):
    p = android / name
    if not p.exists():
        continue
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"(id\s+[\"\']com\.android\.application[\"\']\s+version\s+[\"\'])[0-9.]+([\"\'])", rf"\g<1>{AGP}\2", s)
    s = re.sub(r"(id\s+[\"\']com\.android\.library[\"\']\s+version\s+[\"\'])[0-9.]+([\"\'])", rf"\g<1>{AGP}\2", s)
    s = re.sub(r"(com\.android\.tools\.build:gradle:)[0-9.]+", rf"\g<1>{AGP}", s)
    p.write_text(s, encoding="utf-8")

for name in ("settings.gradle.kts", "build.gradle.kts"):
    p = android / name
    if not p.exists():
        continue
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"(id\(\"com\.android\.application\"\)\s+version\s+\")[0-9.]+(\")", rf"\g<1>{AGP}\2", s)
    s = re.sub(r"(id\(\"com\.android\.library\"\)\s+version\s+\")[0-9.]+(\")", rf"\g<1>{AGP}\2", s)
    s = re.sub(r"(com\.android\.tools\.build:gradle:)[0-9.]+", rf"\g<1>{AGP}", s)
    p.write_text(s, encoding="utf-8")

wrapper = android / "gradle/wrapper/gradle-wrapper.properties"
wrapper.parent.mkdir(parents=True, exist_ok=True)
wrapper.write_text(
    "distributionBase=GRADLE_USER_HOME\n"
    "distributionPath=wrapper/dists\n"
    f"distributionUrl=https\\://services.gradle.org/distributions/gradle-{GRADLE}-bin.zip\n"
    "zipStoreBase=GRADLE_USER_HOME\n"
    "zipStorePath=wrapper/dists\n",
    encoding="utf-8",
)

app = android / "app/build.gradle"
if app.exists():
    s = app.read_text(encoding="utf-8")
    s = re.sub(r'versionName\s+["\'][^"\']+["\']', f'versionName "{version}"', s, count=1)
    app.write_text(s, encoding="utf-8")

appk = android / "app/build.gradle.kts"
if appk.exists():
    s = appk.read_text(encoding="utf-8")
    s = re.sub(r'versionName\s*=\s*["\'][^"\']+["\']', f'versionName = "{version}"', s, count=1)
    appk.write_text(s, encoding="utf-8")
