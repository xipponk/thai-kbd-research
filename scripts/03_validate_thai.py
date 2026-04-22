"""
03_validate_thai.py
-------------------
Step 3: Validate candidates against Thai dictionary
        Confirm that decoded Thai text contains real Thai words
        (not just random Thai characters)

Input:  data/filtered/th_keyboard_switched_candidates.txt
        data/thai-dict/thai_wordlist.txt  (one word per line)
Output: data/processed/confirmed_thai_switched.txt
        data/processed/validation_report.csv

Requires:
    pip install pythainlp

Run:
    python scripts/03_validate_thai.py
"""

import csv
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from keyboard_map import eng_to_thai

INPUT      = Path('data/filtered/th_keyboard_switched_candidates.txt')
DICT_PATH  = Path('data/thai-dict/thai_wordlist.txt')
OUTPUT     = Path('data/processed/confirmed_thai_switched.txt')
REPORT     = Path('data/processed/validation_report.csv')


def load_thai_dict(dict_path: Path) -> set:
    """Load Thai wordlist. Falls back to PyThaiNLP if file not found."""
    if dict_path.exists():
        with open(dict_path, 'r', encoding='utf-8') as f:
            words = {line.strip() for line in f if line.strip()}
        print(f"📚 Loaded Thai dict: {len(words):,} words from {dict_path}")
        return words
    
    # Fallback: use PyThaiNLP built-in dictionary
    try:
        from pythainlp.corpus import thai_words
        words = thai_words()
        print(f"📚 Using PyThaiNLP dict: {len(words):,} words")
        return set(words)
    except ImportError:
        print("⚠️  PyThaiNLP not found. Install: pip install pythainlp")
        print("   Will use Unicode-only validation (less accurate)")
        return set()


def contains_thai_word(decoded_text: str, thai_dict: set,
                       min_word_length: int = 4) -> tuple[bool, list]:
    """
    Flip the loop: extract substrings from decoded text,
    check against dict (O(1) lookup) — much faster
    """
    thai_portion = ''.join(c for c in decoded_text if '\u0e00' <= c <= '\u0e7f')
    if len(thai_portion) < min_word_length:
        return False, []

    matched = []
    n = len(thai_portion)
    for length in range(min_word_length, n + 1):
        for start in range(n - length + 1):
            substr = thai_portion[start:start + length]
            if substr in thai_dict:
                matched.append(substr)
                if len(matched) >= 3:
                    return True, matched
    
    matched.sort(key=len, reverse=True)
    return len(matched) > 0, matched[:5]


def validate(input_path=INPUT, dict_path=DICT_PATH, 
             output_path=OUTPUT, report_path=REPORT):
    
    thai_dict = load_thai_dict(dict_path)
    stats = {'total': 0, 'confirmed': 0, 'rejected': 0}
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as fin, \
         open(output_path, 'w', encoding='utf-8') as fout, \
         open(report_path, 'w', encoding='utf-8', newline='') as frep:
        
        writer = csv.writer(frep)
        writer.writerow(['password', 'decoded_thai', 'confirmed', 'matched_words'])
        
        for line in fin:
            password = line.strip()
            if not password:
                continue
            
            stats['total'] += 1
            decoded = eng_to_thai(password)
            confirmed, matched = contains_thai_word(decoded, thai_dict)
            
            writer.writerow([password, decoded, confirmed, '|'.join(matched)])
            
            if confirmed:
                stats['confirmed'] += 1
                fout.write(password + '\n')
            else:
                stats['rejected'] += 1
    
    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=str(INPUT))
    parser.add_argument('--output', default=str(OUTPUT))
    parser.add_argument('--report', default=str(REPORT))
    args = parser.parse_args()

    print("🔍 Validating candidates against Thai dictionary...")
    stats = validate(
        input_path=Path(args.input),
        output_path=Path(args.output),
        report_path=Path(args.report)
    )
    
    print(f"\n✅ Done!")
    print(f"   Total candidates  : {stats['total']:,}")
    print(f"   Confirmed Thai    : {stats['confirmed']:,}  ({stats['confirmed']/max(stats['total'],1)*100:.1f}%)")
    print(f"   Rejected          : {stats['rejected']:,}")
    print(f"\n📁 Confirmed → {OUTPUT}")
    print(f"📁 Report    → {REPORT}")


if __name__ == '__main__':
    main()