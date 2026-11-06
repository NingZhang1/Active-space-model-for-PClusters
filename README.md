# Active space models for P-clusters in nitrogenase

For details, see supplementary materials in the following reference:

"Electronic landscape of the P-cluster of nitrogenase as revealed through many-electron quantum wavefunction simulations"
Zhendong Li, Sheng Guo, Qiming Sun & Garnet Kin-Lic Chan, Nature Chemistry 11, 1026–1033 (2019).
doi: 10.1038/s41557-019-0337-3

## Orbital reordering: atom-contiguous active spaces

The active orbitals are reclassified from the orbital pictures of the
supplementary PDF `41557_2019_337_MOESM1_ESM.pdf` (Supplementary Figs. 11/12,
18/19, 30/31).  The new order is the concatenation of the atomic groups given
below; inside each group the original orbital order is kept, so that all
orbitals of the same atom become consecutive.  All orbital labels are
**1-based**, exactly as in the PDF and in the FCIDUMP.

Integrals are transformed with `new k <-> old PERM[k]`:

```text
h'[I,J]    = h[p_I, p_J]
(I J|K L)' = (p_I p_J | p_K p_L),      p_X = PERM[X]
```

The nuclear energy, `NORB`, `NELEC`, `MS2`, `ORBSYM` and all numerical
values are unchanged.  Each transformation was verified by re-reading both
files and comparing every two- and one-electron integral.

### PN cluster — CAS(114e,73o)

`FCIDUMP_pN.zip` — NORB=73, NELEC=114, MS2=0, ECORE=-16416.7064728

The order below follows the atom-level classification read off the orbital
plots.  There are thirteen sulfur groups: the six terminal (cysteine) S
atoms contribute two orbitals each, the seven S atoms of the [Fe8S7] core
three each.  They alternate with the eight Fe 3d groups.

**Groups (original orbital labels)**

| Group | Character | Old orbital indices | Count |
|:------|:----------|:--------------------|------:|
| S1 | S 3p | 1–2 | 2 |
| S2 | S 3p | 3, 9 | 2 |
| Fe1 | Fe 3d | 4–8 | 5 |
| S3 | S 3p | 10–12 | 3 |
| S4 | S 3p | 13–15 | 3 |
| Fe2 | Fe 3d | 16–20 | 5 |
| S5 | S 3p | 21–23 | 3 |
| Fe3 | Fe 3d | 24–28 | 5 |
| Fe4 | Fe 3d | 29–33 | 5 |
| S6 | S 3p | 34–35, 38 | 3 |
| S7 | S 3p | 36, 40 | 2 |
| S8 | S 3p | 37, 39 | 2 |
| Fe5 | Fe 3d | 41–45 | 5 |
| Fe6 | Fe 3d | 46–50 | 5 |
| S9 | S 3p | 51–53 | 3 |
| S10 | S 3p | 54, 56, 58 | 3 |
| S11 | S 3p | 55, 57, 59 | 3 |
| Fe7 | Fe 3d | 60–64 | 5 |
| Fe8 | Fe 3d | 65–69 | 5 |
| S12 | S 3p | 70–71 | 2 |
| S13 | S 3p | 72–73 | 2 |

**New order**

| New indices | Group | Character | Old orbital indices |
|:------------|:------|:----------|:--------------------|
| 1–2 | S1 | S 3p | 1–2 |
| 3–4 | S2 | S 3p | 3, 9 |
| 5–9 | Fe1 | Fe 3d | 4–8 |
| 10–12 | S3 | S 3p | 10–12 |
| 13–15 | S4 | S 3p | 13–15 |
| 16–20 | Fe2 | Fe 3d | 16–20 |
| 21–23 | S5 | S 3p | 21–23 |
| 24–28 | Fe3 | Fe 3d | 24–28 |
| 29–33 | Fe4 | Fe 3d | 29–33 |
| 34–36 | S6 | S 3p | 34–35, 38 |
| 37–38 | S7 | S 3p | 36, 40 |
| 39–40 | S8 | S 3p | 37, 39 |
| 41–45 | Fe5 | Fe 3d | 41–45 |
| 46–50 | Fe6 | Fe 3d | 46–50 |
| 51–53 | S9 | S 3p | 51–53 |
| 54–56 | S10 | S 3p | 54, 56, 58 |
| 57–59 | S11 | S 3p | 55, 57, 59 |
| 60–64 | Fe7 | Fe 3d | 60–64 |
| 65–69 | Fe8 | Fe 3d | 65–69 |
| 70–71 | S12 | S 3p | 70–71 |
| 72–73 | S13 | S 3p | 72–73 |

`PERM` (new → old, 1-based):

```text
PERM = [
    1, 2, 3, 9, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16,
    17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
    33, 34, 35, 38, 36, 40, 37, 39, 41, 42, 43, 44, 45, 46, 47, 48,
    49, 50, 51, 52, 53, 54, 56, 58, 55, 57, 59, 60, 61, 62, 63, 64,
    65, 66, 67, 68, 69, 70, 71, 72, 73
]
```

### P1+ cluster — CAS(117e,75o)

`FCIDUMP_p+.zip` — NORB=75, NELEC=117, MS2=1, ECORE=-16352.0242933

The order below follows the atom-level classification read off the orbital
plots.  There are fourteen sulfur groups: the seven terminal (cysteine) S
atoms contribute two orbitals each, the seven S atoms of the [Fe8S7] core
three each.  They alternate with the eight Fe 3d groups.

**Groups (original orbital labels)**

| Group | Character | Old orbital indices | Count |
|:------|:----------|:--------------------|------:|
| S1 | S 3p | 1–2 | 2 |
| S2 | S 3p | 3–4 | 2 |
| Fe1 | Fe 3d | 5–9 | 5 |
| S3 | S 3p | 10, 12, 14 | 3 |
| S4 | S 3p | 11, 13, 16 | 3 |
| S5 | S 3p | 15, 22–23 | 3 |
| Fe2 | Fe 3d | 17–21 | 5 |
| Fe3 | Fe 3d | 24–28 | 5 |
| Fe4 | Fe 3d | 29–33 | 5 |
| S6 | S 3p | 34–36 | 3 |
| S7 | S 3p | 37, 39 | 2 |
| S8 | S 3p | 38, 40 | 2 |
| Fe5 | Fe 3d | 41–45 | 5 |
| Fe6 | Fe 3d | 46–50 | 5 |
| S9 | S 3p | 51–53 | 3 |
| S10 | S 3p | 54, 56–57 | 3 |
| S11 | S 3p | 55, 58–59 | 3 |
| Fe7 | Fe 3d | 60–64 | 5 |
| Fe8 | Fe 3d | 67–71 | 5 |
| S12 | S 3p | 65–66 | 2 |
| S13 | S 3p | 72–73 | 2 |
| S14 | S 3p | 74–75 | 2 |

**New order**

| New indices | Group | Character | Old orbital indices |
|:------------|:------|:----------|:--------------------|
| 1–2 | S1 | S 3p | 1–2 |
| 3–4 | S2 | S 3p | 3–4 |
| 5–9 | Fe1 | Fe 3d | 5–9 |
| 10–12 | S3 | S 3p | 10, 12, 14 |
| 13–15 | S4 | S 3p | 11, 13, 16 |
| 16–18 | S5 | S 3p | 15, 22–23 |
| 19–23 | Fe2 | Fe 3d | 17–21 |
| 24–28 | Fe3 | Fe 3d | 24–28 |
| 29–33 | Fe4 | Fe 3d | 29–33 |
| 34–36 | S6 | S 3p | 34–36 |
| 37–38 | S7 | S 3p | 37, 39 |
| 39–40 | S8 | S 3p | 38, 40 |
| 41–45 | Fe5 | Fe 3d | 41–45 |
| 46–50 | Fe6 | Fe 3d | 46–50 |
| 51–53 | S9 | S 3p | 51–53 |
| 54–56 | S10 | S 3p | 54, 56–57 |
| 57–59 | S11 | S 3p | 55, 58–59 |
| 60–64 | Fe7 | Fe 3d | 60–64 |
| 65–69 | Fe8 | Fe 3d | 67–71 |
| 70–71 | S12 | S 3p | 65–66 |
| 72–73 | S13 | S 3p | 72–73 |
| 74–75 | S14 | S 3p | 74–75 |

`PERM` (new → old, 1-based):

```text
PERM = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 11, 13, 16, 15,
    22, 23, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28, 29, 30, 31, 32,
    33, 34, 35, 36, 37, 39, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48,
    49, 50, 51, 52, 53, 54, 56, 57, 55, 58, 59, 60, 61, 62, 63, 64,
    67, 68, 69, 70, 71, 65, 66, 72, 73, 74, 75
]
```

### POX cluster — CAS(120e,77o)

`FCIDUMP_pOX.zip` — NORB=77, NELEC=120, MS2=0, ECORE=-16379.4031668

The order below follows the atom-level classification read off the orbital
plots.  There are fifteen sulfur groups: the eight terminal (cysteine) S
atoms contribute two orbitals each, the seven S atoms of the [Fe8S7] core
three each.  They alternate with the eight Fe 3d groups.

**Groups (original orbital labels)**

| Group | Character | Old orbital indices | Count |
|:------|:----------|:--------------------|------:|
| S1 | S 3p | 1–2 | 2 |
| S2 | S 3p | 3, 9 | 2 |
| Fe1 | Fe 3d | 4–8 | 5 |
| S3 | S 3p | 10, 12, 14 | 3 |
| S4 | S 3p | 11, 13, 15 | 3 |
| S5 | S 3p | 21–23 | 3 |
| Fe2 | Fe 3d | 16–20 | 5 |
| Fe3 | Fe 3d | 24–28 | 5 |
| Fe4 | Fe 3d | 29–33 | 5 |
| S6 | S 3p | 34–36 | 3 |
| S7 | S 3p | 37, 39 | 2 |
| S8 | S 3p | 38, 40 | 2 |
| S9 | S 3p | 41–42 | 2 |
| Fe5 | Fe 3d | 43–47 | 5 |
| Fe6 | Fe 3d | 48–52 | 5 |
| S10 | S 3p | 53–55 | 3 |
| S11 | S 3p | 56–58 | 3 |
| S12 | S 3p | 59, 65–66 | 3 |
| Fe7 | Fe 3d | 60–64 | 5 |
| Fe8 | Fe 3d | 68–72 | 5 |
| S13 | S 3p | 67, 73 | 2 |
| S14 | S 3p | 74–75 | 2 |
| S15 | S 3p | 76–77 | 2 |

**New order**

| New indices | Group | Character | Old orbital indices |
|:------------|:------|:----------|:--------------------|
| 1–2 | S1 | S 3p | 1–2 |
| 3–4 | S2 | S 3p | 3, 9 |
| 5–9 | Fe1 | Fe 3d | 4–8 |
| 10–12 | S3 | S 3p | 10, 12, 14 |
| 13–15 | S4 | S 3p | 11, 13, 15 |
| 16–18 | S5 | S 3p | 21–23 |
| 19–23 | Fe2 | Fe 3d | 16–20 |
| 24–28 | Fe3 | Fe 3d | 24–28 |
| 29–33 | Fe4 | Fe 3d | 29–33 |
| 34–36 | S6 | S 3p | 34–36 |
| 37–38 | S7 | S 3p | 37, 39 |
| 39–40 | S8 | S 3p | 38, 40 |
| 41–42 | S9 | S 3p | 41–42 |
| 43–47 | Fe5 | Fe 3d | 43–47 |
| 48–52 | Fe6 | Fe 3d | 48–52 |
| 53–55 | S10 | S 3p | 53–55 |
| 56–58 | S11 | S 3p | 56–58 |
| 59–61 | S12 | S 3p | 59, 65–66 |
| 62–66 | Fe7 | Fe 3d | 60–64 |
| 67–71 | Fe8 | Fe 3d | 68–72 |
| 72–73 | S13 | S 3p | 67, 73 |
| 74–75 | S14 | S 3p | 74–75 |
| 76–77 | S15 | S 3p | 76–77 |

`PERM` (new → old, 1-based):

```text
PERM = [
    1, 2, 3, 9, 4, 5, 6, 7, 8, 10, 12, 14, 11, 13, 15, 21,
    22, 23, 16, 17, 18, 19, 20, 24, 25, 26, 27, 28, 29, 30, 31, 32,
    33, 34, 35, 36, 37, 39, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48,
    49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 65, 66, 60, 61, 62,
    63, 64, 68, 69, 70, 71, 72, 67, 73, 74, 75, 76, 77
]
```

### Files and script

[`reorder_orbitals.py`](<reorder_orbitals.py>) performs the transformations:

```bash
python3 reorder_orbitals.py --molecule pN  --verify
python3 reorder_orbitals.py --molecule p+  --verify
python3 reorder_orbitals.py --molecule pOX --verify
python3 reorder_orbitals.py --verify                 # all three
python3 reorder_orbitals.py --print-map              # new -> old table
```

| File | System | Description |
|:-----|:-------|:------------|
| [`FCIDUMP_pN.zip`](<FCIDUMP_pN.zip>) | PN | original FCIDUMP |
| [`FCIDUMP_pN_reordered`](<FCIDUMP_pN_reordered>) | PN | reordered FCIDUMP, 73 orbitals |
| [`FCIDUMP_pN_reordered.zip`](<FCIDUMP_pN_reordered.zip>) | PN | the same file, zipped |
| [`FCIDUMP_p+.zip`](<FCIDUMP_p+.zip>) | P1+ | original FCIDUMP |
| [`FCIDUMP_p+_reordered`](<FCIDUMP_p+_reordered>) | P1+ | reordered FCIDUMP, 75 orbitals |
| [`FCIDUMP_p+_reordered.zip`](<FCIDUMP_p+_reordered.zip>) | P1+ | the same file, zipped |
| [`FCIDUMP_pOX.zip`](<FCIDUMP_pOX.zip>) | POX | original FCIDUMP |
| [`FCIDUMP_pOX_reordered`](<FCIDUMP_pOX_reordered>) | POX | reordered FCIDUMP, 77 orbitals |
| [`FCIDUMP_pOX_reordered.zip`](<FCIDUMP_pOX_reordered.zip>) | POX | the same file, zipped |
