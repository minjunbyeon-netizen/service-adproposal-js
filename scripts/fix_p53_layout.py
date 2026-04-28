import sqlite3

DB = r"C:/dev/services/adproposal-js/data/adproposal.db"

# Q1 answer: 3 lines, accent on leading noun/subject only
# Q2 answer: 3 lines, accent on numbers only
NEW = """<!--PARENT:Epilogue--><!--TAG:Bookend-->
<style>
@keyframes ansIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.ans{opacity:0}
.morph-wrap.expanded .ans-1{animation:ansIn .6s ease .3s forwards}
.morph-wrap.expanded .ans-2{animation:ansIn .6s ease .8s forwards}
</style>
<div style="width:100%;height:100%;background:#fff;display:flex;justify-content:center;align-items:center">
<div class="morph-wrap" id="morphWrap" style="display:flex;flex-direction:column;gap:var(--s-5);max-width:1100px;width:92%;align-items:stretch;text-align:center">

<div style="display:flex;flex-direction:column;gap:var(--s-3);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8">
<div style="font-size:30px;font-weight:400;color:#1A1A1A;line-height:1.3"><span style="font-weight:700;color:#E84E10">무엇을</span> 기억시킬 것인가</div>
<div class="ans ans-1" style="font-size:36px;font-weight:700;color:#1A1A1A;line-height:1.5">
<span style="color:#E84E10">산업</span>이 먼저 찾아온 대학<br>
<span style="color:#E84E10">세계</span>가 증명한 숫자<br>
재학 중부터 <span style="color:#E84E10">업계인</span>
</div>
</div>

<div style="display:flex;flex-direction:column;gap:var(--s-3);padding:var(--s-3) 0;border-bottom:1px solid #E8E8E8">
<div style="font-size:30px;font-weight:400;color:#1A1A1A;line-height:1.3"><span style="font-weight:700;color:#E84E10">어떻게</span> 많이 팔 것인가</div>
<div class="ans ans-2" style="font-size:36px;font-weight:700;color:#1A1A1A;line-height:1.5">
<span style="color:#E84E10">3</span>타겟으로<br>
<span style="color:#E84E10">6</span>채널로<br>
<span style="color:#E84E10">1.25억</span> 제대로
</div>
</div>

</div>
</div>"""

c = sqlite3.connect(DB)
c.execute("UPDATE sections SET content=?, updated_at=CURRENT_TIMESTAMP WHERE id=5236", (NEW,))
c.commit()
print("P53 updated — answers line-broken, accent on keywords/numbers only")
