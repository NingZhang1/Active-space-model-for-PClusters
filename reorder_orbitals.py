#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reorder_orbitals.py
===================

Reorder the active-space orbitals of the P-cluster FCIDUMP files so that the
orbitals belonging to the same atom are contiguous.

The classification used for each molecule follows the atom-level regrouping
obtained from the active-orbital pictures of the supplementary material of

    Z. Li, S. Guo, Q. Sun, G. K.-L. Chan,
    "Electronic landscape of the P-cluster of nitrogenase as revealed through
     many-electron quantum wavefunction simulations",
    Nature Chemistry 11, 1026-1033 (2019).  doi:10.1038/s41557-019-0337-3

(``41557_2019_337_MOESM1_ESM.pdf``; Supplementary Figs. 11/12, 18/19, 30/31).
For every molecule each S atom (both the S atoms of the [Fe8S7] core and the
terminal cysteine S atoms) and each Fe atom form one contiguous group.

All orbital labels are 1-based, exactly as in the PDF and in the FCIDUMP.
Within a group the order of the original orbitals is kept.

Integrals are transformed with  new_orbital k <-> old_orbital PERM[k]
(0-based internally), i.e.

    h'[I,J]    = h[p_I, p_J]
    (I J|K L)' = (p_I p_J | p_K p_L),      p_X = PERM[X] + 1

The output keeps the canonical FCIDUMP layout (header, two-electron block,
one-electron block, 0 0 0 0 nuclear-energy line); the numerical values are
copied verbatim from the input file.

Usage
-----
    python3 reorder_orbitals.py                 # all three molecules, with .zip
    python3 reorder_orbitals.py --molecule pN --verify
    python3 reorder_orbitals.py --print-map --molecule pOX
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
import zipfile

# --------------------------------------------------------------------------
# 1. Published classification (1-based orbital labels, as printed in the PDF)
# --------------------------------------------------------------------------
# Each group: (label, chemical character, [old 1-based orbital indices]).
# The order of the orbitals inside a group is the order of the paper.

MOLECULES = {
    # ------------------------------------------------------------------
    # PN cluster, CAS(114e,73o), Supplementary Sec. 4.2 (page 40)
    # ------------------------------------------------------------------
    "pN": dict(
        source="FCIDUMP_pN.zip",
        output="FCIDUMP_pN_reordered",
        norb=73,
        groups=[
            ("S1", "S 3p", [1, 2]),
            ("S2", "S 3p", [3, 9]),
            ("Fe1", "Fe 3d", [4, 5, 6, 7, 8]),
            ("S3", "S 3p", [10, 11, 12]),
            ("S4", "S 3p", [13, 14, 15]),
            ("Fe2", "Fe 3d", [16, 17, 18, 19, 20]),
            ("S5", "S 3p", [21, 22, 23]),
            ("Fe3", "Fe 3d", [24, 25, 26, 27, 28]),
            ("Fe4", "Fe 3d", [29, 30, 31, 32, 33]),
            ("S6", "S 3p", [34, 35, 38]),
            ("S7", "S 3p", [36, 40]),
            ("S8", "S 3p", [37, 39]),
            ("Fe5", "Fe 3d", [41, 42, 43, 44, 45]),
            ("Fe6", "Fe 3d", [46, 47, 48, 49, 50]),
            ("S9", "S 3p", [51, 52, 53]),
            ("S10", "S 3p", [54, 56, 58]),
            ("S11", "S 3p", [55, 57, 59]),
            ("Fe7", "Fe 3d", [60, 61, 62, 63, 64]),
            ("Fe8", "Fe 3d", [65, 66, 67, 68, 69]),
            ("S12", "S 3p", [70, 71]),
            ("S13", "S 3p", [72, 73]),
        ],
    ),
    # ------------------------------------------------------------------
    # P1+ cluster, CAS(117e,75o), Supplementary Sec. 5.2 (page 54)
    # ------------------------------------------------------------------
    "p+": dict(
        source="FCIDUMP_p+.zip",
        output="FCIDUMP_p+_reordered",
        norb=75,
        groups=[
            ("S1", "S 3p", [1, 2]),
            ("S2", "S 3p", [3, 4]),
            ("Fe1", "Fe 3d", [5, 6, 7, 8, 9]),
            ("S3", "S 3p", [10, 12, 14]),
            ("S4", "S 3p", [11, 13, 16]),
            ("S5", "S 3p", [15, 22, 23]),
            ("Fe2", "Fe 3d", [17, 18, 19, 20, 21]),
            ("Fe3", "Fe 3d", [24, 25, 26, 27, 28]),
            ("Fe4", "Fe 3d", [29, 30, 31, 32, 33]),
            ("S6", "S 3p", [34, 35, 36]),
            ("S7", "S 3p", [37, 39]),
            ("S8", "S 3p", [38, 40]),
            ("Fe5", "Fe 3d", [41, 42, 43, 44, 45]),
            ("Fe6", "Fe 3d", [46, 47, 48, 49, 50]),
            ("S9", "S 3p", [51, 52, 53]),
            ("S10", "S 3p", [54, 56, 57]),
            ("S11", "S 3p", [55, 58, 59]),
            ("Fe7", "Fe 3d", [60, 61, 62, 63, 64]),
            ("Fe8", "Fe 3d", [67, 68, 69, 70, 71]),
            ("S12", "S 3p", [65, 66]),
            ("S13", "S 3p", [72, 73]),
            ("S14", "S 3p", [74, 75]),
        ],
    ),
    # ------------------------------------------------------------------
    # POX cluster, CAS(120e,77o), Supplementary Sec. 6.2 (page 77)
    # ------------------------------------------------------------------
    "pOX": dict(
        source="FCIDUMP_pOX.zip",
        output="FCIDUMP_pOX_reordered",
        norb=77,
        groups=[
            ("S1", "S 3p", [1, 2]),
            ("S2", "S 3p", [3, 9]),
            ("Fe1", "Fe 3d", [4, 5, 6, 7, 8]),
            ("S3", "S 3p", [10, 12, 14]),
            ("S4", "S 3p", [11, 13, 15]),
            ("S5", "S 3p", [21, 22, 23]),
            ("Fe2", "Fe 3d", [16, 17, 18, 19, 20]),
            ("Fe3", "Fe 3d", [24, 25, 26, 27, 28]),
            ("Fe4", "Fe 3d", [29, 30, 31, 32, 33]),
            ("S6", "S 3p", [34, 35, 36]),
            ("S7", "S 3p", [37, 39]),
            ("S8", "S 3p", [38, 40]),
            ("S9", "S 3p", [41, 42]),
            ("Fe5", "Fe 3d", [43, 44, 45, 46, 47]),
            ("Fe6", "Fe 3d", [48, 49, 50, 51, 52]),
            ("S10", "S 3p", [53, 54, 55]),
            ("S11", "S 3p", [56, 57, 58]),
            ("S12", "S 3p", [59, 65, 66]),
            ("Fe7", "Fe 3d", [60, 61, 62, 63, 64]),
            ("Fe8", "Fe 3d", [68, 69, 70, 71, 72]),
            ("S13", "S 3p", [67, 73]),
            ("S14", "S 3p", [74, 75]),
            ("S15", "S 3p", [76, 77]),
        ],
    ),
}


def permutation_of(name: str):
    """0-based permutation (new -> old) and the group table of a molecule."""
    spec = MOLECULES[name]
    groups = [(label, char, [i - 1 for i in idxs])
              for label, char, idxs in spec["groups"]]
    perm = [old for _label, _char, idxs in groups for old in idxs]
    if sorted(perm) != list(range(spec["norb"])):
        raise ValueError(f"{name}: the published lists are not a permutation "
                         f"of 1..{spec['norb']}")
    return perm, groups


# --------------------------------------------------------------------------
# 2. Small helpers
# --------------------------------------------------------------------------

HEADER_KEYS = ("NORB", "NELEC", "MS2", "ORBSYM", "ISYM")


def read_source(path: str) -> str:
    """Return the text of an FCIDUMP, either a plain file or a .zip archive."""
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as zf:
            names = [n for n in zf.namelist() if not n.endswith("/")]
            if len(names) != 1:
                raise RuntimeError(
                    f"{path}: expected exactly one file in the archive, got {names}")
            raw = zf.read(names[0])
            print(f"[read] {path} :: {names[0]}  ({len(raw)/1e6:.1f} MB)")
            return raw.decode("ascii", errors="strict")
    with open(path, "r", encoding="ascii") as fh:
        text = fh.read()
    print(f"[read] {path}  ({len(text)/1e6:.1f} MB)")
    return text


def split_header(text: str):
    m = re.search(r"&END[^\n]*\n?", text, re.IGNORECASE)
    if not m:
        raise RuntimeError("FCIDUMP header does not contain &END")
    return text[:m.end()], text[m.end():]


def parse_header(header: str) -> dict:
    info = {}
    for key in HEADER_KEYS:
        m = re.search(rf"{key}\s*=\s*([^\n,]+)", header, re.IGNORECASE)
        if m:
            info[key] = m.group(1).strip()
    info["NORB"] = int(info["NORB"])
    info["NELEC"] = int(info["NELEC"])
    info["MS2"] = int(info.get("MS2", 0))
    info["ISYM"] = int(info.get("ISYM", 1))
    info["ORBSYM"] = [int(x) for x in re.findall(r"-?\d+", info.get("ORBSYM", ""))]
    if len(info["ORBSYM"]) != info["NORB"]:
        info["ORBSYM"] = [1] * info["NORB"]
    return info


def fmt_header(info: dict) -> str:
    return "".join([
        " &FCI NORB=%4d,NELEC=%3d,MS2=%d,\n"
        % (info["NORB"], info["NELEC"], info["MS2"]),
        "  ORBSYM=%s,\n" % ",".join(str(x) for x in info["ORBSYM"]),
        "  ISYM=%d,\n" % info["ISYM"],
        " &END\n",
    ])


def pair_index(p: int, q: int) -> int:
    if p < q:
        p, q = q, p
    return p * (p + 1) // 2 + q


def pair_table(norb: int):
    ii, jj = [], []
    for i in range(norb):
        for j in range(i + 1):
            ii.append(i)
            jj.append(j)
    return ii, jj


# --------------------------------------------------------------------------
# 3. Reordering
# --------------------------------------------------------------------------

def reorder(text: str, perm):
    """Return (new_text, stats).  ``perm[new] = old`` (0-based)."""
    header, body = split_header(text)
    info = parse_header(header)
    norb = info["NORB"]

    if len(perm) != norb:
        raise ValueError(f"permutation has {len(perm)} entries, but NORB={norb}")
    if sorted(perm) != list(range(norb)):
        raise ValueError("PERM is not a permutation of 0..NORB-1")

    inv = [0] * norb
    for new, old in enumerate(perm):
        inv[old] = new

    info["ORBSYM"] = [info["ORBSYM"][old] for old in perm]

    npair = norb * (norb + 1) // 2
    nint2 = npair * (npair + 1) // 2

    two = [None] * nint2
    one = [None] * npair
    ecore = None

    n_read = n_two = n_one = 0

    for line in body.splitlines():
        if not line.strip():
            continue
        tok = line.split()
        if len(tok) != 5:
            raise RuntimeError(f"malformed FCIDUMP line: {line!r}")
        v = tok[0]
        i, j, k, l = (int(t) for t in tok[1:5])
        n_read += 1

        if k != 0:  # two-electron integral
            b1 = pair_index(inv[i - 1], inv[j - 1])
            b2 = pair_index(inv[k - 1], inv[l - 1])
            if b1 < b2:
                b1, b2 = b2, b1
            pos = b1 * (b1 + 1) // 2 + b2
            if two[pos] is not None:
                raise RuntimeError(
                    f"duplicate two-electron integral at canonical position {pos}")
            two[pos] = v
            n_two += 1
        elif j != 0:  # one-electron integral (k == l == 0)
            b = pair_index(inv[i - 1], inv[j - 1])
            if one[b] is not None:
                raise RuntimeError(f"duplicate one-electron integral at block {b}")
            one[b] = v
            n_one += 1
        else:  # nuclear energy
            ecore = v

    if ecore is None:
        raise RuntimeError("no nuclear-energy line (0 0 0 0) found")
    missing2 = sum(1 for x in two if x is None)
    missing1 = sum(1 for x in one if x is None)
    if missing2 or missing1:
        raise RuntimeError(
            f"incomplete FCIDUMP: {missing2} two-electron and {missing1} "
            f"one-electron integrals missing")

    # ---- write in canonical FCIDUMP order --------------------------------
    ii, jj = pair_table(norb)
    pstr = ["%d %d" % (ii[b] + 1, jj[b] + 1) for b in range(npair)]

    chunks = [fmt_header(info)]
    buf = []
    pos = 0
    for b1 in range(npair):
        head = pstr[b1]
        for b2 in range(b1 + 1):
            buf.append(two[pos] + " " + head + " " + pstr[b2] + "\n")
            pos += 1
            if len(buf) >= 200_000:
                chunks.append("".join(buf))
                buf.clear()
    chunks.append("".join(buf))
    buf.clear()

    for b in range(npair):
        buf.append(one[b] + "  " + pstr[b] + "  0  0\n")
    chunks.append("".join(buf))

    chunks.append(ecore + " 0 0 0 0\n")
    new_text = "".join(chunks)

    stats = dict(norb=norb, npair=npair, nint2=nint2, n_read=n_read,
                 n_two=n_two, n_one=n_one, ecore=ecore)
    return new_text, stats


# --------------------------------------------------------------------------
# 4. Optional verification
# --------------------------------------------------------------------------

def _collect(path: str, mapping=None):
    """Read an FCIDUMP and return canonical integral arrays in a common
    (target) orbital numbering."""
    import numpy as np

    text = read_source(path)
    header, body = split_header(text)
    info = parse_header(header)
    norb = info["NORB"]
    if mapping is None:
        mapping = list(range(norb))
    if len(mapping) != norb:
        raise RuntimeError(f"mapping length {len(mapping)} != NORB {norb}")

    k2, v2, k1, v1 = [], [], [], []
    ecore = None
    for line in body.splitlines():
        tok = line.split()
        if len(tok) != 5:
            continue
        i, j, k, l = (int(t) - 1 for t in tok[1:5])
        if k >= 0:
            b1 = pair_index(mapping[i], mapping[j])
            b2 = pair_index(mapping[k], mapping[l])
            if b1 < b2:
                b1, b2 = b2, b1
            k2.append(b1 * (b1 + 1) // 2 + b2)
            v2.append(float(tok[0]))
        elif j >= 0:
            k1.append(pair_index(mapping[i], mapping[j]))
            v1.append(float(tok[0]))
        else:
            ecore = tok[0]

    return (np.asarray(k2, dtype=np.int64), np.asarray(v2, dtype=np.float64),
            np.asarray(k1, dtype=np.int64), np.asarray(v1, dtype=np.float64),
            ecore, norb)


def verify(old_path: str, new_path: str, perm):
    import numpy as np

    inv = [0] * len(perm)
    for new, old in enumerate(perm):
        inv[old] = new

    print("[verify] reading original ...")
    k2o, v2o, k1o, v1o, eo, norb = _collect(old_path, mapping=inv)
    print("[verify] reading reordered ...")
    k2n, v2n, k1n, v1n, en, _ = _collect(new_path)

    npair = norb * (norb + 1) // 2
    nint2 = npair * (npair + 1) // 2
    if eo != en:
        raise SystemExit(f"[verify] FAILED: ECORE {eo} != {en}")
    if len(k2o) != nint2:
        raise SystemExit(
            f"[verify] FAILED: {len(k2o)} two-electron integrals, expected {nint2}")
    if len(k1o) != npair:
        raise SystemExit(
            f"[verify] FAILED: {len(k1o)} one-electron integrals, expected {npair}")

    for name, ko, vo, kn, vn in (
        ("two-electron", k2o, v2o, k2n, v2n),
        ("one-electron", k1o, v1o, k1n, v1n),
    ):
        o = np.argsort(ko, kind="stable")
        p = np.argsort(kn, kind="stable")
        if not np.array_equal(ko[o], kn[p]):
            raise SystemExit(f"[verify] FAILED: {name} key mismatch")
        if not np.array_equal(vo[o], vn[p]):
            bad = np.flatnonzero(vo[o] != vn[p])[:5]
            raise SystemExit(f"[verify] FAILED: {name} value mismatch at {bad}")

    print("[verify] OK: %d two-electron + %d one-electron integrals, ECORE=%s"
          % (len(k2o), len(k1o), eo))


# --------------------------------------------------------------------------
# 5. Command line
# --------------------------------------------------------------------------

def print_map(name: str):
    perm, groups = permutation_of(name)
    print(f"# {name}: NORB={MOLECULES[name]['norb']}")
    print("# new  old  group      character")
    new = 0
    for label, char, idxs in groups:
        for old in idxs:
            print(f"{new+1:4d} {old+1:4d}  {label:<10s} {char}")
            new += 1


def run_one(name: str, do_zip: bool, do_verify: bool):
    spec = MOLECULES[name]
    perm, _groups = permutation_of(name)
    src, out = spec["source"], spec["output"]
    if not os.path.exists(src):
        print(f"[skip] {name}: {src} not found")
        return False

    t0 = time.time()
    text = read_source(src)
    new_text, stats = reorder(text, perm)
    with open(out, "w", encoding="ascii", newline="\n") as fh:
        fh.write(new_text)
    print("[write] %s  (%.1f MB, %d two-electron + %d one-electron, ECORE=%s)"
          " in %.1f s" % (out, len(new_text) / 1e6, stats["n_two"],
                          stats["n_one"], stats["ecore"], time.time() - t0))

    if do_verify:
        verify(src, out, perm)

    if do_zip:
        zpath = out + ".zip"
        with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_DEFLATED,
                             compresslevel=9) as zf:
            zf.write(out, arcname=os.path.basename(out))
        print(f"[zip]   {zpath}  ({os.path.getsize(zpath)/1e6:.1f} MB)")
    return True


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Make the P-cluster active orbitals atom-contiguous.")
    p.add_argument("--molecule", default="all",
                   choices=["all"] + list(MOLECULES),
                   help="which FCIDUMP to process (default: all)")
    p.add_argument("--no-zip", action="store_true")
    p.add_argument("--verify", action="store_true")
    p.add_argument("--print-map", action="store_true")
    args = p.parse_args(argv)

    names = list(MOLECULES) if args.molecule == "all" else [args.molecule]

    if args.print_map:
        for name in names:
            print_map(name)
            print()
        return 0

    ok = True
    for name in names:
        ok = run_one(name, not args.no_zip, args.verify) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
