#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
Demo 12 — PAXECT Core One-Minute Stress Test
---------------------------------------------
Continuously encodes and decodes files for 60 s to
validate deterministic stability and zero-error throughput.
"""

import subprocess, time, shutil
from pathlib import Path

BASE = Path("/tmp/paxect_demo12")
SRC = BASE / "src.txt"
ENC = BASE / "enc.freq"
DEC = BASE / "dec.txt"
LOG = BASE / "core_stress.jsonl"

shutil.rmtree(BASE, ignore_errors=True)
BASE.mkdir(parents=True)
LOG.write_text("")

def run_cycle(i:int)->bool:
    SRC.write_text(f"cycle={i} paxect core test\n",encoding="utf-8")
    e = subprocess.run(["python3","paxect_core.py","encode","-i",str(SRC),"-o",str(ENC),"--verify"],
                       stderr=subprocess.PIPE,text=True)
    if e.returncode!=0:
        LOG.write_text(LOG.read_text()+f'{{"cycle":{i},"phase":"encode","err":"{e.stderr.strip()}"}}\n')
        return False
    d = subprocess.run(["python3","paxect_core.py","decode","-i",str(ENC),"-o",str(DEC),"--verify"],
                       stderr=subprocess.PIPE,text=True)
    if d.returncode!=0:
        LOG.write_text(LOG.read_text()+f'{{"cycle":{i},"phase":"decode","err":"{d.stderr.strip()}"}}\n')
        return False
    return SRC.read_text()==DEC.read_text()

print("=== Demo 12 — PAXECT Core One-Minute Stress Test ===")
start=time.time();cycles=0;errors=0
while time.time()-start<60:
    cycles+=1
    if not run_cycle(cycles): errors+=1
print(f"\nCompleted cycles: {cycles}")
print(f"Errors detected : {errors}")
print(f"Reliability    : {(1-errors/cycles)*100:.4f}%")
print(f"Log           : {LOG}")

if errors==0:
    print("✅ Core engine passed 1-minute stress test without errors.")
else:
    print("⚠️ Core engine detected recoverable errors; see log for details.")
