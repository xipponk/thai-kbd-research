# Thai Keyboard Layout Switching — Password Strength Analysis

**Full Title**: Analysing the Strength of Passwords Created Using Thai–English Keyboard Layout Switching  
**Author**: Asst. Prof. Tuul Triyason, Ph.D.  
**Affiliation**: School of Information Technology, KMUTT, Thailand  
**Target Journal**: Information Security Journal: A Global Perspective (Taylor & Francis, Scopus Q2)

---

## Research Overview

คนไทยจำนวนหนึ่งนิยมตั้ง password โดยพิมพ์คำภาษาไทยขณะที่ keyboard อยู่ใน English (QWERTY) layout ทำให้ได้ password ที่ดูเหมือน random English characters เช่น พิมพ์ `สวัสดี` แล้วได้ `l;ylfu`

งานวิจัยนี้ศึกษาว่า password ที่สร้างด้วยวิธีนี้ **แข็งแรงพอหรือไม่** โดยวัดจาก:
- Entropy (Peak + Shannon)
- zxcvbn password strength score
- Penetration testing (Hashcat — brute-force, dictionary, combiner attack)

และศึกษาว่า password แบบใดที่ **ยังเปราะบาง** แม้จะใช้ Thai keyboard switching

---

## Project Structure

```
thai-kbd-research/
├── data/
│   ├── raw/             # ⚠️ Breach data (ห้าม push to Git)
│   ├── filtered/        # Passwords จาก .th domains
│   ├── thai-dict/       # Thai wordlist สำหรับ validation
│   └── processed/       # Confirmed Thai keyboard-switched passwords + metrics
├── scripts/
│   ├── keyboard_map.py          # Kedmanee ↔ QWERTY mapping (TIS 820-2538)
│   ├── 01_filter_th_domain.py   # Filter .th domain passwords จาก COMB
│   ├── 02_reverse_mapping.py    # Detect Thai keyboard-switched candidates
│   ├── 03_validate_thai.py      # Validate ด้วย PyThaiNLP dictionary
│   ├── 04_entropy_zxcvbn.py     # Compute entropy + zxcvbn metrics
│   └── 05_analysis.py           # Pattern analysis (cracked vs not cracked)
├── results/
│   ├── figures/          # Charts และ plots สำหรับ paper
│   └── tables/           # Statistical tables
├── paper/
│   ├── draft/            # Paper draft
│   ├── references/       # .bib + related work PDFs
│   └── notes/            # Research notes
├── tests/                # Unit tests
├── .gitignore
└── README.md
```

---

## Pipeline

```
COMB / Collection #1 breach data
        ↓
[01] Filter .th domain emails  →  data/filtered/th_domain_passwords.txt
        ↓
[02] Reverse Kedmanee mapping  →  data/filtered/th_keyboard_switched_candidates.txt
        ↓
[03] Thai dictionary validation  →  data/processed/confirmed_thai_switched.txt
        ↓
[04] Entropy + zxcvbn metrics  →  data/processed/metrics.csv
        ↓
[05] Pattern analysis  →  results/tables/ + results/figures/
        ↓
Paper writing
```

---

## Setup

```bash
# Clone / เปิด project
cd ~/projects/thai-kbd-research

# Activate virtual environment
source .venv/bin/activate

# Install dependencies (ครั้งแรก)
pip install pythainlp zxcvbn tqdm pandas matplotlib seaborn
```

---

## Running the Pipeline

```bash
# Step 1: Filter .th domains จาก COMB
python scripts/01_filter_th_domain.py --input data/raw/<comb_file>

# Step 2: Detect Thai keyboard-switched candidates
python scripts/02_reverse_mapping.py

# Step 3: Validate ด้วย Thai dictionary
python scripts/03_validate_thai.py

# Step 4: Compute metrics
python scripts/04_entropy_zxcvbn.py

# Step 5: Pattern analysis
python scripts/05_analysis.py
```

---

## Key Concepts

**Kedmanee Layout**: มาตรฐาน TIS 820-2538 — keyboard ภาษาไทยที่ใช้ทั่วไปในไทย

**Keyboard Switching Password**: การพิมพ์คำภาษาไทยในขณะที่ OS/input method อยู่ใน English mode ทำให้ได้ string ที่ดูเหมือน random English characters แต่จริงๆ แล้วถอดรหัสได้จาก physical key mapping

**Threat Model**:
- *Uninformed attacker*: ใช้ standard dictionary (RockYou, LinkedIn) → crack ได้น้อยมาก
- *Informed attacker*: รู้ Thai keyboard pattern + มี Thai wordlist → crack ได้มากขึ้น

---

## Ethical Notes

- ใช้เฉพาะ **password strings** เท่านั้น — ไม่เก็บ email หรือ PII ใดๆ
- Secondary analysis ของ publicly available breach data
- ไม่ require IRB (computational analysis, no human subjects)
- Raw breach data **ไม่ถูก commit** ขึ้น repository (.gitignore ครอบคลุมแล้ว)

---

## Progress Tracker

- [x] Project structure setup
- [x] Keyboard mapping script (TIS 820-2538)
- [x] Filter script (01)
- [x] Reverse mapping script (02)
- [x] Thai validation script (03)
- [x] Metrics script (04)
- [ ] Download + inspect COMB format
- [ ] Run pipeline on real data
- [ ] Pattern analysis (05)
- [ ] Results visualization
- [ ] Paper draft

---

## Related Work (to be cited)

- Wheeler (2012) — zxcvbn: realistic password strength estimation
- Ur et al. (2015) — Measuring Password Guessability for an Entire University
- Li et al. (2014) — The Large-Scale Analysis of Chinese Passwords
- Thai & Tanaka (2024) — SMMl-PSM multilingual password strength model
- Hong et al. (2021) — Korean password security with integrated dictionaries

---

*Last updated: April 2026*