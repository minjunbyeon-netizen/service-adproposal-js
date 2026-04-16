"""로컬 vs Railway 스크린샷 바이트 비교 -- 픽셀 단위 diff."""
import hashlib
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).parent
LOCAL = ROOT / "local_shots"
RW = ROOT / "rw_shots"

FOCUS = [1, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 27, 28, 43]


def md5(p: Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()[:12]


def png_size(p: Path) -> tuple[int, int]:
    data = p.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return (0, 0)
    # IHDR chunk starts at offset 8, length=13, type="IHDR"
    width = struct.unpack(">I", data[16:20])[0]
    height = struct.unpack(">I", data[20:24])[0]
    return (width, height)


def diff_pct(a: Path, b: Path) -> float:
    """간단 diff -- 파일 크기 차이를 % 로 출력."""
    sa = a.stat().st_size
    sb = b.stat().st_size
    if max(sa, sb) == 0:
        return 0.0
    return abs(sa - sb) / max(sa, sb) * 100


print(f"{'idx':>4} {'local sz':>10} {'rw sz':>10} {'sz %':>6}  {'local dim':>12} {'rw dim':>12}  same?")
print("-" * 80)

total_mismatch = 0
for idx in FOCUS:
    local = LOCAL / f"local_{idx:02d}.png"
    rw = RW / f"rw_{idx:02d}.png"
    if not local.exists() or not rw.exists():
        print(f"{idx:>4}  MISSING")
        continue
    ls = local.stat().st_size
    rs = rw.stat().st_size
    d = diff_pct(local, rw)
    ldim = png_size(local)
    rdim = png_size(rw)
    same = md5(local) == md5(rw)
    flag = "==" if same else ("~=" if d < 5 else "!=")
    if not same:
        total_mismatch += 1
    print(f"{idx:>4} {ls:>10} {rs:>10} {d:>5.1f}%  {ldim[0]}x{ldim[1]:<5}  {rdim[0]}x{rdim[1]:<5}  {flag}")

print("-" * 80)
print(f"mismatches: {total_mismatch}/{len(FOCUS)}")
