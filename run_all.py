"""Run every script and report whether all claims are confirmed (a few seconds in total)."""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SCRIPTS = ["example_3_2.py", "examples_C12_C13.py", "appendix_D4.py", "proposition_6_1_iii.py"]

failed = []
for name in SCRIPTS:
    result = subprocess.run([sys.executable, str(ROOT / name)], cwd=str(ROOT), capture_output=True, text=True)
    print(f"{'ok  ' if result.returncode == 0 else 'FAIL'}  {name}")
    if result.returncode != 0:
        failed.append(name)
        print(result.stdout + result.stderr)
print(f"{len(SCRIPTS) - len(failed)}/{len(SCRIPTS)} scripts confirmed all their claims")
sys.exit(1 if failed else 0)
