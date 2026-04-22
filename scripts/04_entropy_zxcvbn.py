"""
04_entropy_zxcvbn.py
--------------------
Step 4: Calculate entropy metrics + zxcvbn scores
        for confirmed Thai keyboard-switched passwords

Input:  data/processed/confirmed_thai_switched.txt
Output: data/processed/metrics.csv

Metrics:
    - Password length
    - Peak entropy (bits)  = len * log2(charset_size)
    - Shannon entropy (per symbol)
    - Total Shannon entropy
    - zxcvbn score (0-4)
    - zxcvbn guesses (log10)

Requires:
    pip install zxcvbn

Run:
    python scripts/04_entropy_zxcvbn.py
"""

import csv
import math
import argparse
from pathlib import Path

INPUT  = Path('data/processed/confirmed_thai_switched.txt')
OUTPUT = Path('data/processed/metrics.csv')

CHARSET_FULL = 95  # printable ASCII


def peak_entropy(password: str) -> float:
    """E = L * log2(R) where R = charset size"""
    if not password:
        return 0.0
    return len(password) * math.log2(CHARSET_FULL)


def shannon_entropy_per_symbol(password: str) -> float:
    """Shannon entropy per character"""
    if not password:
        return 0.0
    from collections import Counter
    freq = Counter(password)
    n = len(password)
    return -sum((c/n) * math.log2(c/n) for c in freq.values())


def get_zxcvbn(password: str) -> tuple[int, float]:
    """Returns (score 0-4, log10 guesses)"""
    try:
        import zxcvbn as zx
        result = zx.zxcvbn(password)
        guesses = result['guesses']
        log10 = math.log10(guesses) if guesses > 0 else 0
        return result['score'], log10
    except ImportError:
        return -1, -1  # zxcvbn not installed


def compute_metrics(input_path=INPUT, output_path=OUTPUT):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    count = 0
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as fin, \
         open(output_path, 'w', encoding='utf-8', newline='') as fout:
        
        writer = csv.writer(fout)
        writer.writerow([
            'password', 'length',
            'peak_entropy_bits', 'shannon_per_symbol', 'shannon_total',
            'zxcvbn_score', 'zxcvbn_log10_guesses'
        ])
        
        for line in fin:
            pw = line.strip()
            if not pw:
                continue
            
            pe = peak_entropy(pw)
            sh = shannon_entropy_per_symbol(pw)
            sh_total = sh * len(pw)
            zx_score, zx_log10 = get_zxcvbn(pw)
            
            writer.writerow([
                pw, len(pw),
                f'{pe:.4f}', f'{sh:.6f}', f'{sh_total:.4f}',
                zx_score, f'{zx_log10:.4f}'
            ])
            count += 1
    
    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=str(INPUT))
    parser.add_argument('--output', default=str(OUTPUT))
    args = parser.parse_args()

    print("📊 Computing entropy + zxcvbn metrics...")
    n = compute_metrics(
        input_path=Path(args.input),
        output_path=Path(args.output)
    )
    print(f"✅ Done! Processed {n:,} passwords → {args.output}")


if __name__ == '__main__':
    main()