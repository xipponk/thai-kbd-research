"""
01_filter_th_domain.py  —  BreachCompilation format
Structure: data/[a-z0-9]/[aa-zz]/...  (nested, recursive)
Format:    email:password  (last colon = separator)
"""

import re
from pathlib import Path
from tqdm import tqdm

INPUT_DIR = Path("data/raw/CompilationOfManyBreaches/data")
OUTPUT = Path("data/filtered/th_domain_passwords.txt")

TH_PATTERN = re.compile(
    r"@.+\.(co\.th|ac\.th|go\.th|or\.th|net\.th|in\.th|th)$", re.IGNORECASE
)


def is_th_domain(email: str) -> bool:
    return bool(TH_PATTERN.search(email))


def process():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    # collect all files first
    all_files = [f for f in INPUT_DIR.rglob("*") if f.is_file()]
    print(f"Total files found: {len(all_files):,}")

    stats = {"lines": 0, "binary_skip": 0, "th_found": 0, "written": 0}

    with open(OUTPUT, "w", encoding="utf-8") as fout:
        for filepath in tqdm(all_files, desc="Scanning"):
            # skip binary files
            try:
                with open(filepath, "r", encoding="utf-8", errors="strict") as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                stats["binary_skip"] += 1
                continue

            for line in lines:
                stats["lines"] += 1
                line = line.strip()
                if ":" not in line:
                    continue

                # split on LAST colon
                email, _, password = line.rpartition(":")

                if not email or not password:
                    continue

                if not is_th_domain(email):
                    continue

                stats["th_found"] += 1

                # write PASSWORD ONLY — no email
                if 4 <= len(password) <= 64 and password.isprintable():
                    fout.write(password + "\n")
                    stats["written"] += 1

    return stats


if __name__ == "__main__":
    print("🔍 Filtering .th domain passwords from BreachCompilation...")
    stats = process()
    print(f"\n✅ Done!")
    print(f"   Lines scanned   : {stats['lines']:,}")
    print(f"   Binary skipped  : {stats['binary_skip']:,}")
    print(f"   .th found       : {stats['th_found']:,}")
    print(f"   Passwords written: {stats['written']:,}")
    print(f"\n📁 Output → {OUTPUT}")

