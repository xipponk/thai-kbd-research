"""
keyboard_map.py  —  Kedmanee (Thai) ↔ QWERTY keyboard mapping
==============================================================
Mapping verified against ground truth pairs from actual dataset:

  l;ylfu8iy[        → สวัสดีครับ        ✓ (10/10)
  mefuwfhfu         → ทำดีได้ดี          ✓ (9/9)
  z,iyd86I          → ผมรักคุณ           ✓ (8/8)
  ohe-7ho.shiu[9yd  → น้ำขึ้นให้รีบตัก    ✓ (16/16)
  souglnvxt0itg-h   → หนีเสือปะจระเข้    ✓ (15/15)

Keys marked [GT] = confirmed from ground truth pairs above
Keys marked [KM] = inferred from standard Kedmanee layout
Keys marked [SH] = shifted key (uppercase / special)
"""

# =============================================================
# QWERTY key → Thai character (Kedmanee layout)
# =============================================================

QWERTY_TO_KEDMANEE = {

    # --- Number row (unshifted) ---
    '`': 'ๅ',  # [KM]
    '1': '๑',  # [KM]
    '2': '๒',  # [KM]
    '3': '๓',  # [KM]
    '4': '๔',  # [KM]
    '5': 'ู',  # [KM] sara uu (long u below)
    '6': 'ุ',  # [GT] sara u (short u below) — from ผมรักคุณ
    '7': 'ึ',  # [GT] sara ue short — from น้ำขึ้น
    '8': 'ค',  # [GT] kho khwai — from ผมรักคุณ, สวัสดี
    '9': 'ต',  # [GT] to tao — from น้ำขึ้นให้รีบตัก
    '0': 'จ',  # [GT] cho chan — from หนีเสือปะจระเข้
    '-': 'ข',  # [GT] kho khai — from น้ำขึ้น
    '=': 'ช',  # [KM] cho chang

    # --- Row 2 (top letter row, unshifted) ---
    'q': 'ๆ',  # [KM]
    'w': 'ไ',  # [GT] from ทำดีได้ดี
    'e': 'ำ',  # [GT] from ทำดีได้ดี, น้ำขึ้น
    'r': 'พ',  # [KM]
    't': 'ะ',  # [GT] from หนีเสือปะจระเข้
    'y': 'ั',  # [GT] sara a (short a above) — from สวัสดีครับ, ผมรักคุณ
    'u': 'ี',  # [GT] sara ii (long i above) — from สวัสดีครับ, ทำดีได้ดี
    'i': 'ร',  # [GT] ro han — from ผมรักคุณ, น้ำขึ้นให้รีบตัก
    'o': 'น',  # [GT] no nu — from น้ำขึ้น, หนีเสือ
    'p': 'ย',  # [GT] yo yak — from หนีเสือปะจระเข้
    '[': 'บ',  # [GT] bo baimai — from สวัสดีครับ, น้ำขึ้น
    ']': 'ล',  # [KM]
    '\\': 'ฃ', # [KM]

    # --- Row 3 (home row, unshifted) ---
    'a': 'ฟ',  # [KM]
    's': 'ห',  # [GT] ho hip — from น้ำขึ้นให้รีบตัก, หนีเสือ
    'd': 'ก',  # [GT] ko kai — from ผมรักคุณ
    'f': 'ด',  # [GT] do dek — from สวัสดีครับ, ทำดีได้ดี
    'g': 'เ',  # [GT] sara e — from หนีเสือปะจระเข้
    'h': '้',  # [GT] mai tho (tone mark) — from สวัสดีครับ ทุกตัว
    'j': '่',  # [KM] mai ek (tone mark)
    'k': 'า',  # [KM] sara aa
    'l': 'ส',  # [GT] so suea — from สวัสดีครับ, หนีเสือ
    ';': 'ว',  # [GT] wo waen — from สวัสดีครับ
    "'": 'ง',  # [KM] ngo ngu

    # --- Row 4 (bottom row, unshifted) ---
    'z': 'ผ',  # [GT] pho phueng — from ผมรักคุณ
    'x': 'ป',  # [GT] po pla — from หนีเสือปะจระเข้
    'c': 'แ',  # [KM]
    'v': 'อ',  # [GT] o ang — from หนีเสือปะจระเข้
    'b': 'ิ',  # [KM] sara i (short i above)
    'n': 'ื',  # [GT] sara uea — from หนีเสือปะจระเข้
    'm': 'ท',  # [GT] tho thahan — from ทำดีได้ดี
    ',': 'ม',  # [GT] mo ma — from ผมรักคุณ
    '.': 'ใ',  # [GT] sara ai maimuan — from น้ำขึ้นให้รีบตัก
    '/': 'ฝ',  # [KM]

    # --- Shifted keys (uppercase letters) ---
    'A': 'ฤ',  # [KM]
    'B': 'ฮ',  # [KM]
    'C': 'ฃ',  # [KM]
    'D': 'ฏ',  # [KM]
    'E': 'ฎ',  # [KM]
    'F': 'โ',  # [KM]
    'G': 'ฌ',  # [KM]
    'H': '็',  # [KM] mai taikhu
    'I': 'ณ',  # [GT] no nen — from ผมรักคุณ (shift+i)
    'J': '๋',  # [KM] mai chattawa
    'K': 'ษ',  # [KM]
    'L': 'ศ',  # [KM]
    'M': 'ฒ',  # [KM]
    'N': 'ฺ',  # [KM] thanthakat
    'O': 'ฯ',  # [KM]
    'P': 'ญ',  # [KM]
    'Q': '๐',  # [KM] Thai digit 0
    'R': 'ฑ',  # [KM]
    'S': 'ฆ',  # [KM]
    'T': 'ธ',  # [KM]
    'U': '๊',  # [KM] mai tri
    'V': 'ฉ',  # [KM]
    'W': '"',  # [KM]
    'X': 'ฦ',  # [KM]
    'Y': 'ํ',  # [KM] nikhahit
    'Z': 'ฬ',  # [KM]

    # --- Shifted number row ---
    '~': 'ๆ',  # [KM]
    '!': '+',  # [KM]
    '@': '๑',  # [KM]
    '#': '๒',  # [KM]
    '$': '๓',  # [KM]
    '%': '๔',  # [KM]
    '^': 'ู',  # [KM]
    '&': '฿',  # [KM] baht sign
    '*': '๕',  # [KM]
    '(': '๖',  # [KM]
    ')': '๗',  # [KM]
    '_': '๘',  # [KM]
    '+': '๙',  # [KM]

    # --- Shifted brackets / punctuation ---
    '{': ',',  # [KM]
    '}': '.',  # [KM]
    '|': 'ฅ',  # [KM]
    ':': 'ซ',  # [KM]
    '"': '.',  # [KM]
    '<': 'ฬ',  # [KM]
    '>': 'ฦ',  # [KM]
    '?': '฿',  # [KM]
}

# Reverse mapping: Thai character → QWERTY key
KEDMANEE_TO_QWERTY = {v: k for k, v in QWERTY_TO_KEDMANEE.items()}


# =============================================================
# Core functions
# =============================================================

def eng_to_thai(text: str) -> str:
    """
    Decode: given a password typed in English (QWERTY) mode,
    reveal the Thai text the user intended (Kedmanee layout).

    Example: 'l;ylfu8iy[' → 'สวัสดีครับ'
    """
    return ''.join(QWERTY_TO_KEDMANEE.get(c, c) for c in text)


def thai_to_eng(text: str) -> str:
    """
    Encode: given Thai text, produce what would appear if typed
    while keyboard is in English (QWERTY) mode.

    Example: 'ผมรักคุณ' → 'z,iyd86I'  (approximately, shifted chars vary)
    """
    return ''.join(KEDMANEE_TO_QWERTY.get(c, c) for c in text)


def thai_ratio_after_decode(password: str) -> float:
    """
    Decode password as Kedmanee-switched, then measure what fraction
    of characters fall in the Thai Unicode block (U+0E00–U+0E7F).
    High ratio → likely a Thai keyboard-switched password.
    """
    if not password:
        return 0.0
    decoded = eng_to_thai(password)
    thai_count = sum(1 for c in decoded if '\u0e00' <= c <= '\u0e7f')
    return thai_count / len(password)


def is_likely_thai_switched(password: str, threshold: float = 0.6) -> bool:
    """Returns True if password is likely typed in Thai but shown as English."""
    return thai_ratio_after_decode(password) >= threshold


# =============================================================
# Self-test
# =============================================================

if __name__ == '__main__':
    ground_truth = [
        ('l;ylfu8iy[',       'สวัสดีครับ',        True),
        ('mefuwfhfu',        'ทำดีได้ดี',          True),
        ('z,iyd86I',         'ผมรักคุณ',           True),
        ('ohe-7ho.shiu[9yd', 'น้ำขึ้นให้รีบตัก',   True),
        ('souglnvxt0itg-h',  'หนีเสือปะจระเข้',   True),
        # Non-Thai passwords — should NOT be detected
        ('password123',      None,                  False),
        ('123456',           None,                  False),
        ('soccer2012',       None,                  False),
    ]

    print('=== keyboard_map.py self-test ===\n')
    all_pass = True
    for pw, expected_thai, expected_detected in ground_truth:
        decoded  = eng_to_thai(pw)
        detected = is_likely_thai_switched(pw)
        ratio    = thai_ratio_after_decode(pw)

        if expected_thai:
            ok = (decoded == expected_thai) and (detected == expected_detected)
        else:
            ok = (detected == expected_detected)

        status = '✅' if ok else '❌'
        if not ok:
            all_pass = False

        print(f'{status} {pw:25s}  detected={detected} ratio={ratio:.2f}')
        if expected_thai:
            match = '✓' if decoded == expected_thai else '✗'
            print(f'     decoded:  {decoded}')
            print(f'     expected: {expected_thai}  [{match}]')
        print()

    print('=' * 50)
    print(f'Result: {"ALL PASSED ✅" if all_pass else "SOME FAILED ❌"}')