"""
02_reverse_mapping.py
---------------------
Step 2: Decode filtered passwords using reverse Kedmanee→QWERTY mapping
        Identify which passwords are likely Thai keyboard-switched

Input:  data/filtered/th_domain_passwords.txt
Output: data/filtered/th_keyboard_switched_candidates.txt
        data/filtered/th_decode_log.csv  (password, decoded_thai, thai_ratio)

Run:
    python scripts/02_reverse_mapping.py
"""

import csv
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from keyboard_map import eng_to_thai, thai_ratio_after_decode

THRESHOLD = 0.60  # 60% of chars decode to Thai → classified as Thai-switched

INPUT             = Path('data/filtered/th_domain_passwords.txt')
OUTPUT_CANDIDATES = Path('data/filtered/th_keyboard_switched_candidates.txt')
OUTPUT_LOG        = Path('data/filtered/th_decode_log.csv')


def process(input_path=INPUT, output_candidates=OUTPUT_CANDIDATES,
            output_log=OUTPUT_LOG, threshold=THRESHOLD):
    
    stats = {'total': 0, 'thai_switched': 0, 'not_switched': 0}
    
    output_candidates.parent.mkdir(parents=True, exist_ok=True)
    
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as fin, \
         open(output_candidates, 'w', encoding='utf-8') as fout_cand, \
         open(output_log, 'w', encoding='utf-8', newline='') as fout_log:
        
        writer = csv.writer(fout_log)
        writer.writerow(['password', 'decoded_thai', 'thai_ratio', 'is_thai_switched'])
        
        for line in fin:
            password = line.strip()
            if not password:
                continue
            
            stats['total'] += 1
            decoded = eng_to_thai(password)
            ratio   = thai_ratio_after_decode(password)
            is_thai = ratio >= threshold
            
            writer.writerow([password, decoded, f'{ratio:.3f}', is_thai])
            
            if is_thai:
                stats['thai_switched'] += 1
                fout_cand.write(password + '\n')
            else:
                stats['not_switched'] += 1
    
    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',  default=str(INPUT))
    parser.add_argument('--output', default=str(OUTPUT_CANDIDATES))
    parser.add_argument('--log',    default=str(OUTPUT_LOG))
    parser.add_argument('--threshold', type=float, default=THRESHOLD)
    args = parser.parse_args()

    print(f"🔑 Reverse mapping: QWERTY → Kedmanee (Thai)")
    print(f"   Input:     {args.input}")
    print(f"   Threshold: {args.threshold:.0%} Thai chars after decode")

    stats = process(
        input_path=Path(args.input),
        output_candidates=Path(args.output),
        output_log=Path(args.log),
        threshold=args.threshold
    )

    print(f"\n✅ Done!")
    print(f"   Total passwords     : {stats['total']:,}")
    print(f"   Thai-switched found : {stats['thai_switched']:,}  ({stats['thai_switched']/max(stats['total'],1)*100:.1f}%)")
    print(f"   Not switched        : {stats['not_switched']:,}")


if __name__ == '__main__':
    main()