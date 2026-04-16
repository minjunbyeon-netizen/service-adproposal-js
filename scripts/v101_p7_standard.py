# -*- coding: utf-8 -*-
"""V101 P7 (idx=6) - 오버레이 제거, 표준 슬라이드 레이아웃 + 서브스텝 유지."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179


# 표준 content-body 안에서 렌더링 (헤더/HIVE MEDIA/pagenum은 템플릿이 처리)
# morphWrap + expanded 클래스로 서브스텝 유지
P7 = """<!--PARENT:Ⅰ. 제안개요--><!--TAG:0825503 해독-->
<style>
.mg{display:inline-block;position:relative;font-size:var(--fs-display);font-weight:700;line-height:0.9;color:#1A1A1A;font-variant-numeric:tabular-nums;transition:all 1.2s cubic-bezier(.25,.46,.45,.94);margin:0 -2px}
.morph-wrap.expanded .mg{margin:0 64px}

@keyframes drawCircle7{from{stroke-dashoffset:500}to{stroke-dashoffset:0}}
@keyframes labelUp7{from{opacity:0;transform:translate(-50%,12px)}to{opacity:1;transform:translate(-50%,0)}}

.pc7{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);pointer-events:none;opacity:0;transition:opacity .3s}
.morph-wrap.expanded .pc7{opacity:1}
.morph-wrap.expanded .mg-08 .pc7 ellipse{stroke-dasharray:500;stroke-dashoffset:500;animation:drawCircle7 .7s ease 1.0s forwards}
.morph-wrap.expanded .mg-25 .pc7 ellipse{stroke-dasharray:500;stroke-dashoffset:500;animation:drawCircle7 .7s ease 1.3s forwards}
.morph-wrap.expanded .mg-55 .pc7 ellipse{stroke-dasharray:500;stroke-dashoffset:500;animation:drawCircle7 .7s ease 1.6s forwards}
.morph-wrap.expanded .mg-03 .pc7 ellipse{stroke-dasharray:500;stroke-dashoffset:500;animation:drawCircle7 .7s ease 1.9s forwards}

.ml7{position:absolute;bottom:calc(100% + 56px);left:50%;transform:translateX(-50%);white-space:nowrap;text-align:center;opacity:0;pointer-events:none}
.morph-wrap.expanded .mg-08 .ml7{animation:labelUp7 .5s ease 1.4s forwards}
.morph-wrap.expanded .mg-25 .ml7{animation:labelUp7 .5s ease 1.7s forwards}
.morph-wrap.expanded .mg-55 .ml7{animation:labelUp7 .5s ease 2.0s forwards}
.morph-wrap.expanded .mg-03 .ml7{animation:labelUp7 .5s ease 2.3s forwards}
</style>

<svg style="position:absolute;width:0;height:0"><defs><filter id="rough7"><feTurbulence type="turbulence" baseFrequency="0.035" numOctaves="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3" xChannelSelector="R" yChannelSelector="G"/></filter></defs></svg>

<div style="height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center">

<div style="font-size:14px;color:#A0A0A5;font-weight:700;margin-bottom:var(--s-2);letter-spacing:2px">SERIAL NO.</div>

<div class="morph-wrap" id="morphWrap">
<span class="mg mg-08">08<svg class="pc7" width="200" height="180" viewBox="0 0 200 180"><ellipse cx="100" cy="90" rx="88" ry="72" fill="none" stroke="#E84E10" stroke-width="4.5" stroke-linecap="round" opacity="0.85" style="filter:url(#rough7)"/></svg><div class="ml7"><div style="font-size:26px;font-weight:700;color:#1A1A1A;line-height:1.2">연구력 세계 8위</div><div style="font-size:14px;color:#6E6E73;margin-top:4px">국내 1위</div></div></span><span class="mg mg-25">25<svg class="pc7" width="200" height="180" viewBox="0 0 200 180"><ellipse cx="100" cy="90" rx="85" ry="70" fill="none" stroke="#E84E10" stroke-width="4.5" stroke-linecap="round" opacity="0.85" style="filter:url(#rough7)"/></svg><div class="ml7"><div style="font-size:26px;font-weight:700;color:#1A1A1A;line-height:1.2">총지배인 25명</div><div style="font-size:14px;color:#6E6E73;margin-top:4px">호텔업계 배출</div></div></span><span class="mg mg-55">55<svg class="pc7" width="200" height="180" viewBox="0 0 200 180"><ellipse cx="100" cy="90" rx="84" ry="69" fill="none" stroke="#E84E10" stroke-width="4.5" stroke-linecap="round" opacity="0.85" style="filter:url(#rough7)"/></svg><div class="ml7"><div style="font-size:26px;font-weight:700;color:#1A1A1A;line-height:1.2">QS 호스피탈리티</div><div style="font-size:14px;color:#6E6E73;margin-top:4px">세계 55위</div></div></span><span class="mg mg-03">03<svg class="pc7" width="200" height="180" viewBox="0 0 200 180"><ellipse cx="100" cy="90" rx="86" ry="71" fill="none" stroke="#E84E10" stroke-width="4.5" stroke-linecap="round" opacity="0.85" style="filter:url(#rough7)"/></svg><div class="ml7"><div style="font-size:26px;font-weight:700;color:#1A1A1A;line-height:1.2">한국 호텔관광</div><div style="font-size:14px;color:#6E6E73;margin-top:4px">TOP 3</div></div></span>
</div>

</div>"""


def main():
    conn = sqlite3.connect(str(DB))
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=6",
        (P7, PID),
    )
    conn.commit()
    conn.close()
    print("[P7] 표준 레이아웃 + 서브스텝 유지")


if __name__ == "__main__":
    main()
