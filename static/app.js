/* adproposal-js frontend */
let currentProposalId = null;
let currentSectionId = null;
let proposalData = null;

function esc(t) { const d = document.createElement('div'); d.textContent = t; return d.innerHTML; }
function md(t) {
    if (typeof marked !== 'undefined' && marked.parse && typeof DOMPurify !== 'undefined') {
        return DOMPurify.sanitize(marked.parse(t));
    }
    return '<pre style="white-space:pre-wrap">' + esc(t) + '</pre>';
}

// ===== Proposals =====

async function loadProposals() {
    try {
        const res = await fetch('/api/proposals');
        const json = await res.json();
        if (!json.ok) return;
        renderProposalList(json.data);
    } catch (e) {
        console.error('loadProposals:', e);
    }
}

function renderProposalList(list) {
    var el = document.getElementById('proposalList');
    if (!list.length) {
        el.innerHTML = '<div class="empty-state">제안서가 없습니다</div>';
        return;
    }

    // 버전별 그룹핑
    var groups = {};
    var noVersion = [];
    list.forEach(function(p) {
        if (!p.version) { noVersion.push(p); return; }
        var major = p.version.split('-')[0]; // "V4-1" -> "V4"
        if (!groups[major]) groups[major] = [];
        groups[major].push(p);
    });

    // 메이저 버전 내림차순 정렬
    var majors = Object.keys(groups).sort(function(a, b) {
        return parseInt(b.replace('V', '')) - parseInt(a.replace('V', ''));
    });

    var h = '<div class="version-tree">';
    majors.forEach(function(major) {
        var items = groups[major];
        if (items.length === 1 && items[0].version === major) {
            // 단독 버전 (V1, V2, V3, V5)
            var p = items[0];
            var active = p.id === currentProposalId ? ' active' : '';
            h += '<div class="vt-item' + active + '" onclick="selectProposal(' + p.id + ')">' +
                '<span class="vt-label">' + esc(p.version) + '</span>' +
                '<span class="vt-title">' + esc(p.title) + '</span>' +
                '<span class="vt-pt" onclick="event.stopPropagation();openPT(' + p.id + ')" title="PT 열기">PT</span>' +
                '</div>';
        } else {
            // 그룹 (V4 -> 4-1, 4-2, ...)
            var groupOpen = items.some(function(p) { return p.id === currentProposalId; });
            h += '<div class="vt-group" onclick="toggleVGroup(this)">' +
                '<span class="vt-arrow">' + (groupOpen ? '&#9660;' : '&#9654;') + '</span>' +
                '<span class="vt-label">' + esc(major) + '</span>' +
                '<span class="vt-count">' + items.length + '</span>' +
                '</div>';
            h += '<div class="vt-sub" style="display:' + (groupOpen ? 'block' : 'none') + '">';
            // 서브 아이템 정렬 (V4-1, V4-2, ...)
            items.sort(function(a, b) {
                var na = parseInt((a.version.split('-')[1] || '0'));
                var nb = parseInt((b.version.split('-')[1] || '0'));
                return na - nb;
            });
            items.forEach(function(p) {
                var sub = p.version.replace(major + '-', '');
                var active = p.id === currentProposalId ? ' active' : '';
                h += '<div class="vt-sub-item' + active + '" onclick="selectProposal(' + p.id + ')">' +
                    '<span class="vt-sub-label">' + esc(sub) + '</span>' +
                    '<span class="vt-title">' + esc(p.title) + '</span>' +
                    '<span class="vt-pt" onclick="event.stopPropagation();openPT(' + p.id + ')" title="PT 열기">PT</span>' +
                    '</div>';
            });
            h += '</div>';
        }
    });

    // 버전 없는 항목
    noVersion.forEach(function(p) {
        var active = p.id === currentProposalId ? ' active' : '';
        h += '<div class="vt-item' + active + '" onclick="selectProposal(' + p.id + ')">' +
            '<span class="vt-title" style="flex:1">' + esc(p.title) + '</span>' +
            '</div>';
    });

    h += '</div>';
    el.innerHTML = h;
}

function toggleVGroup(el) {
    var sub = el.nextElementSibling;
    var arrow = el.querySelector('.vt-arrow');
    if (sub.style.display === 'none') {
        sub.style.display = 'block';
        arrow.innerHTML = '&#9660;';
    } else {
        sub.style.display = 'none';
        arrow.innerHTML = '&#9654;';
    }
}

async function selectProposal(id) {
    currentProposalId = id;
    currentSectionId = null;
    document.getElementById('centerEmpty').style.display = 'none';
    document.getElementById('centerContent').style.display = 'block';
    document.getElementById('rightEmpty').style.display = 'block';
    document.getElementById('rightContent').style.display = 'none';
    document.getElementById('btnExport').disabled = false;
    var btnPT = document.getElementById('btnPT');
    if (btnPT) btnPT.disabled = false;

    try {
        const res = await fetch('/api/proposals/' + id);
        const json = await res.json();
        if (!json.ok) return;
        proposalData = json.data;
        document.getElementById('proposalTitle').textContent = proposalData.title;

        if (proposalData.rfp_json) {
            renderRfpSummary(proposalData.rfp_json);
        } else {
            document.getElementById('rfpSummary').innerHTML = '';
        }

        if (proposalData.sections && proposalData.sections.length) {
            renderToc(proposalData.sections);
            document.getElementById('btnAnalyze').textContent = '재분석';
            document.getElementById('btnAutoGen').disabled = false;
            document.getElementById('conceptArea').style.display = 'block';
            loadConcepts(id);
        } else {
            document.getElementById('tocTree').innerHTML = '';
            document.getElementById('btnAnalyze').textContent = '분석 시작';
            document.getElementById('btnAutoGen').disabled = true;
            document.getElementById('conceptArea').style.display = 'none';
        }

        loadProposals();
    } catch (e) {
        console.error('selectProposal:', e);
    }
}

// ===== Upload =====

async function handleUpload() {
    const title = document.getElementById('inputTitle').value.trim();
    const files = document.getElementById('inputFiles').files;
    const text = document.getElementById('inputText').value.trim();

    if (!title) { alert('제목을 입력해주세요'); return; }
    if (!files.length && !text) { alert('파일 또는 텍스트를 입력해주세요'); return; }

    const fd = new FormData();
    fd.append('title', title);
    fd.append('text', text);
    for (const f of files) fd.append('files[]', f);

    const btn = document.getElementById('btnUpload');
    btn.disabled = true; btn.textContent = '업로드 중...';

    try {
        const res = await fetch('/api/proposals/upload', { method: 'POST', body: fd });
        const json = await res.json();
        if (!json.ok) { alert(json.error); return; }
        document.getElementById('inputTitle').value = '';
        document.getElementById('inputFiles').value = '';
        document.getElementById('inputText').value = '';
        await loadProposals();
        selectProposal(json.data.proposal_id);
    } catch (e) {
        alert('업로드 실패: ' + e.message);
    } finally {
        btn.disabled = false; btn.textContent = '업로드';
    }
}

// ===== Analysis =====

async function startAnalysis() {
    if (!currentProposalId) return;
    const btn = document.getElementById('btnAnalyze');
    const loading = document.getElementById('analysisLoading');
    btn.disabled = true;
    loading.style.display = 'block';

    try {
        const res = await fetch('/api/proposals/' + currentProposalId + '/analyze', { method: 'POST' });
        const json = await res.json();
        if (!json.ok) { alert(json.error); return; }

        renderRfpSummary(json.data.rfp_json);
        renderToc(json.data.toc);
        document.getElementById('btnAutoGen').disabled = false;
        btn.textContent = '재분석';
        loadProposals();
    } catch (e) {
        alert('분석 실패: ' + e.message);
    } finally {
        btn.disabled = false;
        loading.style.display = 'none';
    }
}

function renderRfpSummary(rfp) {
    const el = document.getElementById('rfpSummary');
    const fields = [
        ['발주처', rfp.client_name],
        ['사업명', rfp.project_name],
        ['예산', rfp.budget],
        ['수행기간', rfp.duration],
        ['제출기한', rfp.deadline],
    ].filter(f => f[1]);

    let h = '<div class="rfp-summary">';
    for (const [k, v] of fields) {
        h += `<div class="rfp-field"><span class="rfp-key">${k}</span><span class="rfp-val">${esc(v)}</span></div>`;
    }
    if (rfp.tasks && rfp.tasks.length) {
        h += `<div class="rfp-field"><span class="rfp-key">과업항목</span><span class="rfp-val">${rfp.tasks.map(t => esc(t)).join(', ')}</span></div>`;
    }
    h += '</div>';
    el.innerHTML = h;
}

function renderToc(sections) {
    const el = document.getElementById('tocTree');
    el.innerHTML = '<div class="toc-tree">' + sections.map(s => `
        <div class="toc-item level-${s.level}${s.id === currentSectionId ? ' active' : ''}" onclick="selectSection(${s.id})">
            <span class="toc-status ${s.status}">${s.status}</span>
            <span>${esc(s.title)}</span>
        </div>
    `).join('') + '</div>';
}

// ===== Section =====

async function selectSection(sid) {
    currentSectionId = sid;
    document.getElementById('rightEmpty').style.display = 'none';
    document.getElementById('rightContent').style.display = 'block';

    // highlight in TOC
    document.querySelectorAll('.toc-item').forEach(el => el.classList.remove('active'));
    const items = document.querySelectorAll('.toc-item');
    // find the section data
    const section = proposalData.sections.find(s => s.id === sid);
    if (section) {
        document.getElementById('sectionTitle').textContent = section.title;
        document.getElementById('sectionContent').innerHTML = section.content ? md(section.content) : '<span style="color:#6E6E73">아직 생성되지 않았습니다</span>';
    }

    // reload sections to get latest
    try {
        const res = await fetch('/api/proposals/' + currentProposalId + '/sections');
        const json = await res.json();
        if (json.ok) {
            proposalData.sections = json.data;
            renderToc(json.data);
            const latest = json.data.find(s => s.id === sid);
            if (latest) {
                document.getElementById('sectionContent').innerHTML = latest.content ? md(latest.content) : '<span style="color:#6E6E73">아직 생성되지 않았습니다</span>';
            }
        }
    } catch (e) { /* ignore */ }

    loadMessages(sid);
}

async function generateSection() {
    if (!currentSectionId) return;
    const btn = document.getElementById('btnGenerate');
    const loading = document.getElementById('genLoading');
    btn.disabled = true;
    loading.style.display = 'block';

    try {
        const res = await fetch('/api/chat/sections/' + currentSectionId + '/generate', { method: 'POST' });
        const json = await res.json();
        if (!json.ok) { alert(json.error); return; }
        document.getElementById('sectionContent').innerHTML = md(json.data.content);
        // update section data
        const s = proposalData.sections.find(s => s.id === currentSectionId);
        if (s) { s.content = json.data.content; s.status = 'done'; }
        renderToc(proposalData.sections);
        loadMessages(currentSectionId);
    } catch (e) {
        alert('생성 실패: ' + e.message);
    } finally {
        btn.disabled = false;
        loading.style.display = 'none';
    }
}

// ===== Auto Generate =====

async function autoGenerate() {
    const btn = document.getElementById('btnAutoGen');
    btn.disabled = true;
    btn.textContent = '생성 중...';

    const pending = proposalData.sections.filter(s => s.status === 'pending');
    for (const s of pending) {
        try {
            await selectSection(s.id);
            const res = await fetch('/api/chat/sections/' + s.id + '/generate', { method: 'POST' });
            const json = await res.json();
            if (json.ok) {
                const sec = proposalData.sections.find(x => x.id === s.id);
                if (sec) { sec.content = json.data.content; sec.status = 'done'; }
                renderToc(proposalData.sections);
                document.getElementById('sectionContent').innerHTML = md(json.data.content);
            }
        } catch (e) {
            console.error('autoGenerate section', s.id, e);
        }
    }

    btn.disabled = false;
    btn.textContent = '전체 자동 생성';
    alert('전체 섹션 생성이 완료되었습니다.');
}

// ===== Chat =====

async function loadMessages(sid) {
    const el = document.getElementById('chatMessages');
    try {
        const res = await fetch('/api/chat/sections/' + sid + '/messages');
        const json = await res.json();
        if (!json.ok) return;
        el.innerHTML = json.data.map(m => `
            <div class="chat-msg ${m.role}">
                <div class="chat-role">${m.role === 'user' ? 'CEO' : 'AI'}</div>
                ${m.role === 'assistant' ? md(m.content) : esc(m.content)}
            </div>
        `).join('');
        el.scrollTop = el.scrollHeight;
    } catch (e) { /* ignore */ }
}

async function sendChat() {
    if (!currentSectionId) return;
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    if (!text) return;

    input.value = '';
    const btn = document.getElementById('btnChat');
    btn.disabled = true;
    btn.textContent = '응답 대기...';

    // add user message to chat immediately
    const chatEl = document.getElementById('chatMessages');
    chatEl.innerHTML += `<div class="chat-msg user"><div class="chat-role">CEO</div>${esc(text)}</div>`;
    chatEl.scrollTop = chatEl.scrollHeight;

    try {
        const res = await fetch('/api/chat/sections/' + currentSectionId + '/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: text }),
        });
        const json = await res.json();
        if (!json.ok) { alert(json.error); return; }

        // update section content
        document.getElementById('sectionContent').innerHTML = md(json.data.content);
        const s = proposalData.sections.find(s => s.id === currentSectionId);
        if (s) { s.content = json.data.content; s.status = 'done'; }

        // add AI response to chat
        chatEl.innerHTML += `<div class="chat-msg assistant"><div class="chat-role">AI</div>${md(json.data.content)}</div>`;
        chatEl.scrollTop = chatEl.scrollHeight;
    } catch (e) {
        alert('응답 실패: ' + e.message);
    } finally {
        btn.disabled = false;
        btn.textContent = '전송';
    }
}

// ===== Concepts A/B/C =====

async function loadConcepts(pid) {
    try {
        var res = await fetch('/api/proposals/' + pid + '/concepts');
        var json = await res.json();
        if (!json.ok) return;
        renderConceptCards(json.data);
    } catch (e) {
        console.error('loadConcepts:', e);
    }
}

function renderConceptCards(concepts) {
    var el = document.getElementById('conceptCards');
    if (!concepts || !concepts.length) {
        el.innerHTML = '<div style="color:#6E6E73;font-size:12px;padding:8px 0">컨셉이 아직 없습니다. "컨셉 생성" 버튼을 클릭하세요.</div>';
        return;
    }
    var selected = proposalData && proposalData.selected_concept;
    el.innerHTML = '<div class="concept-grid">' + concepts.map(function(c) {
        var isActive = c.label === selected;
        return '<div class="concept-card-mini' + (isActive ? ' active' : '') + '" onclick="selectConcept(\'' + c.label + '\')">' +
            '<div class="concept-tag-mini">' + esc(c.label) + '</div>' +
            '<div class="concept-card-title">' + esc(c.title) + '</div>' +
            '<div class="concept-card-body">' + esc(c.body) + '</div>' +
            '</div>';
    }).join('') + '</div>';
}

async function generateConcepts() {
    if (!currentProposalId) return;
    var btn = document.getElementById('btnConceptGen');
    var loading = document.getElementById('conceptLoading');
    btn.disabled = true;
    loading.style.display = 'block';

    try {
        var res = await fetch('/api/proposals/' + currentProposalId + '/concepts/generate', { method: 'POST' });
        var json = await res.json();
        if (!json.ok) { alert(json.error); return; }
        renderConceptCards(json.data);
    } catch (e) {
        alert('컨셉 생성 실패: ' + e.message);
    } finally {
        btn.disabled = false;
        loading.style.display = 'none';
    }
}

async function selectConcept(label) {
    if (!currentProposalId) return;
    try {
        var res = await fetch('/api/proposals/' + currentProposalId + '/concepts/select', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ label: label }),
        });
        var json = await res.json();
        if (!json.ok) { alert(json.error); return; }
        if (proposalData) proposalData.selected_concept = label;
        loadConcepts(currentProposalId);
    } catch (e) {
        alert('컨셉 선택 실패: ' + e.message);
    }
}

// ===== Export =====

function exportMd() {
    if (!currentProposalId) return;
    window.location.href = '/api/proposals/' + currentProposalId + '/export';
}

function openPresentation() {
    if (!currentProposalId) return;
    window.open('/api/proposals/' + currentProposalId + '/export-html', '_blank');
}

function openPT(pid) {
    window.open('/api/proposals/' + pid + '/export-html', '_blank');
}

// ===== Init =====

document.addEventListener('DOMContentLoaded', function() {
    loadProposals();
});
