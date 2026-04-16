# -*- coding: utf-8 -*-
"""V101 P16 (idx=14 now after P13 delete) - 동그라미 위치 보정 + HIVE MEDIA + pagenum."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "adproposal.db"
PID = 179

P16 = """<!--PARENT:Ⅲ. 세부 과업 수행 계획--><!--TAG:숫자를 기억으로-->
<style>
@keyframes drawC16{from{stroke-dashoffset:400}to{stroke-dashoffset:0}}
@keyframes lIn16{from{opacity:0;transform:translateX(-16px)}to{opacity:1;transform:translateX(0)}}
@keyframes tSwap16{from{opacity:0}to{opacity:1}}

.rf-wrap .rf-row{transition:all 1s cubic-bezier(.25,.46,.45,.94);padding-left:0;padding-right:0}
.rf-wrap.expanded .rf-row{padding-left:40px;padding-right:40px}

.rf-circle-wrap{position:relative;display:inline-block}
.rf-circle-svg{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);pointer-events:none;opacity:0}
.rf-wrap.expanded .rf-r1 .rf-circle-svg{opacity:1}
.rf-wrap.expanded .rf-r1 .rf-circle-svg ellipse{stroke-dasharray:400;stroke-dashoffset:400;animation:drawC16 .7s ease .8s forwards}
.rf-wrap.expanded .rf-r2 .rf-circle-svg{opacity:1}
.rf-wrap.expanded .rf-r2 .rf-circle-svg ellipse{stroke-dasharray:400;stroke-dashoffset:400;animation:drawC16 .7s ease 1.1s forwards}
.rf-wrap.expanded .rf-r3 .rf-circle-svg{opacity:1}
.rf-wrap.expanded .rf-r3 .rf-circle-svg ellipse{stroke-dasharray:400;stroke-dashoffset:400;animation:drawC16 .7s ease 1.4s forwards}

.rf-after{opacity:0}
.rf-wrap.expanded .rf-r1 .rf-after{animation:lIn16 .5s ease 1.2s forwards}
.rf-wrap.expanded .rf-r2 .rf-after{animation:lIn16 .5s ease 1.5s forwards}
.rf-wrap.expanded .rf-r3 .rf-after{animation:lIn16 .5s ease 1.8s forwards}

.rf-num-text{transition:transform 1s cubic-bezier(.25,.46,.45,.94)}
.rf-wrap.expanded .rf-num-text{transform:scale(1.2)}

.rf-title-after{display:none}
.rf-title-before{display:inline}
.rf-wrap.expanded .rf-title-before{display:none}
.rf-wrap.expanded .rf-title-after{display:inline;animation:tSwap16 .5s ease forwards}

.rf-desc{transition:color .8s ease}
.rf-wrap.expanded .rf-desc{color:#6E6E73}
</style>

<div id="morphPhase1" style="position:absolute;top:0;left:0;right:0;bottom:0;background:#fff;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:var(--s-3) 0;z-index:5">

<svg style="position:absolute;width:0;height:0"><defs><filter id="rough16"><feTurbulence type="turbulence" baseFrequency="0.035" numOctaves="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3" xChannelSelector="R" yChannelSelector="G"/></filter></defs></svg>

<div style="position:absolute;top:80px;right:120px;font-size:14px;color:#1A1A1A;font-weight:700">HIVE MEDIA</div>

<div class="rf-wrap" id="morphWrap">

<div class="t-heading" style="margin-bottom:var(--s-4)">
<span class="rf-title-before"><span class="w-bold">3가지 숫자</span></span>
<span class="rf-title-after">숫자를 <span style="font-weight:700;color:#E84E10">기억</span>으로</span>
</div>

<div style="display:flex;flex-direction:column;gap:0;max-width:1100px;width:94%;margin:0 auto var(--s-4)">

<div class="rf-row rf-r1" style="display:grid;grid-template-columns:80px 1fr 280px;gap:var(--s-3);align-items:center;padding:var(--s-3) var(--s-2);border-top:1px solid #E8E8E8">
<div style="font-size:24px;font-weight:700;text-align:center"><span class="rf-circle-wrap"><span class="rf-num-text">01</span><svg class="rf-circle-svg" width="64" height="52" viewBox="0 0 64 52"><ellipse cx="32" cy="26" rx="28" ry="22" fill="none" stroke="#E84E10" stroke-width="3" stroke-linecap="round" opacity="0.85" style="filter:url(#rough16)"/></svg></span></div>
<div class="rf-desc" style="font-size:20px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:left">총지배인 25명 · 승무원 동남권 최다 · 셰프 4명</div>
<div class="rf-after" style="font-size:22px;font-weight:700;color:#E84E10;text-align:right">산업이 선택한 대학</div>
</div>

<div class="rf-row rf-r2" style="display:grid;grid-template-columns:80px 1fr 280px;gap:var(--s-3);align-items:center;padding:var(--s-3) var(--s-2);border-top:1px solid #E8E8E8">
<div style="font-size:24px;font-weight:700;text-align:center"><span class="rf-circle-wrap"><span class="rf-num-text">02</span><svg class="rf-circle-svg" width="64" height="52" viewBox="0 0 64 52"><ellipse cx="32" cy="26" rx="28" ry="22" fill="none" stroke="#E84E10" stroke-width="3" stroke-linecap="round" opacity="0.85" style="filter:url(#rough16)"/></svg></span></div>
<div class="rf-desc" style="font-size:20px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:left">QS 호스피탈리티 세계 55위 · 국내 3위</div>
<div class="rf-after" style="font-size:22px;font-weight:700;color:#E84E10;text-align:right">글로벌 1위가 될 때까지</div>
</div>

<div class="rf-row rf-r3" style="display:grid;grid-template-columns:80px 1fr 280px;gap:var(--s-3);align-items:center;padding:var(--s-3) var(--s-2);border-top:1px solid #E8E8E8;border-bottom:1px solid #E8E8E8">
<div style="font-size:24px;font-weight:700;text-align:center"><span class="rf-circle-wrap"><span class="rf-num-text">03</span><svg class="rf-circle-svg" width="64" height="52" viewBox="0 0 64 52"><ellipse cx="32" cy="26" rx="28" ry="22" fill="none" stroke="#E84E10" stroke-width="3" stroke-linecap="round" opacity="0.85" style="filter:url(#rough16)"/></svg></span></div>
<div class="rf-desc" style="font-size:20px;color:#1A1A1A;font-weight:700;line-height:1.5;text-align:left">호텔 총지배인 25명 배출</div>
<div class="rf-after" style="font-size:22px;font-weight:700;color:#E84E10;text-align:right">26번째가 당신</div>
</div>

</div>
</div>

<div style="position:absolute;bottom:28px;right:40px;font-size:14px;font-weight:700;color:#6E6E73">15</div>

</div>"""


def main():
    conn = sqlite3.connect(str(DB))
    # After P13 deleted, P16 shifted to idx=14
    conn.execute(
        "UPDATE sections SET content=? WHERE proposal_id=? AND order_idx=14",
        (P16, PID),
    )
    conn.commit()
    conn.close()
    print("[P16] 동그라미 중앙 보정 + HIVE MEDIA + pagenum 추가")


if __name__ == "__main__":
    main()
