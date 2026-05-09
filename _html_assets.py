
CSS = """
*{box-sizing:border-box;}
body{font-family:'Inter',sans-serif;background:#f0f2f5;color:#222;margin:0;padding:2rem 1rem;transition:background .3s,color .3s;}
.wrap{max-width:1280px;margin:0 auto;}
h1{font-size:1.6rem;font-weight:700;margin-bottom:.2rem;}
.sub{font-size:.82rem;color:#888;margin-bottom:1.5rem;}
/* dark mode */
body.dark{background:#0f1117;color:#e0e0e0;}
body.dark .stat,body.dark .lang-wrap,body.dark .table-wrap{background:#1a1d2e;border-color:#2a2d3e;}
body.dark thead{background:#1e2133;}
body.dark td{border-top-color:#2a2d3e;}
body.dark tr.ok{background:#0f2218;}
body.dark tr.check{background:#231c06;}
body.dark tr.review{background:#230a0a;}
body.dark .fbtn{background:#1a1d2e;border-color:#2a2d3e;color:#ccc;}
body.dark .fbtn.active{background:#fff;color:#111;}
body.dark .note-cell{background:#1e2133;color:#ccc;}
/* header row */
.hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:.25rem;}
.hdr-btns{display:flex;gap:.5rem;}
.icon-btn{background:none;border:1px solid #ddd;border-radius:6px;padding:.3rem .65rem;cursor:pointer;font-size:.82rem;}
body.dark .icon-btn{border-color:#3a3d4e;color:#ccc;}
/* stat cards */
.summary{display:flex;gap:1rem;margin-bottom:1.5rem;flex-wrap:wrap;align-items:flex-start;}
.stat{background:#fff;border:1px solid #e2e2e2;border-radius:10px;padding:1rem 1.4rem;min-width:115px;box-shadow:0 1px 4px rgba(0,0,0,.06);}
.stat-label{font-size:.68rem;text-transform:uppercase;letter-spacing:.07em;color:#aaa;margin-bottom:.3rem;}
.stat-value{font-size:1.7rem;font-weight:700;color:#111;line-height:1;}
body.dark .stat-value{color:#e0e0e0;}
.stat.ok .stat-value{color:#27ae60;}
.stat.chk .stat-value{color:#e67e22;}
.stat.rev .stat-value{color:#c0392b;}
/* donut */
.donut-wrap{display:flex;flex-direction:column;align-items:center;justify-content:center;}
.donut-legend{font-size:.72rem;margin-top:.4rem;display:flex;gap:.75rem;}
.donut-legend span{display:flex;align-items:center;gap:.25rem;}
.dot{width:8px;height:8px;border-radius:50%;}
/* sliders */
.sliders{background:#fff;border:1px solid #e2e2e2;border-radius:10px;padding:.85rem 1.25rem;margin-bottom:1.25rem;box-shadow:0 1px 4px rgba(0,0,0,.06);}
body.dark .sliders{background:#1a1d2e;border-color:#2a2d3e;}
.sliders h3{font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:#888;margin:0 0 .6rem;}
.slider-row{display:flex;align-items:center;gap:.75rem;margin-bottom:.4rem;font-size:.8rem;}
.slider-row label{width:140px;color:#666;}
body.dark .slider-row label{color:#aaa;}
input[type=range]{flex:1;max-width:200px;accent-color:#2563eb;}
.slider-val{font-weight:700;width:36px;text-align:right;}
/* language table */
.section-title{font-size:.78rem;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:#777;margin-bottom:.5rem;}
.lang-wrap{background:#fff;border:1px solid #e2e2e2;border-radius:10px;padding:.85rem 1.25rem;margin-bottom:1.25rem;display:inline-block;box-shadow:0 1px 4px rgba(0,0,0,.06);}
.lt{border-collapse:collapse;font-size:.82rem;}
.lt th{padding:.3rem .9rem;text-align:left;font-size:.68rem;font-weight:600;text-transform:uppercase;color:#aaa;}
.lt td{padding:.3rem .9rem;border-top:1px solid #f0f0f0;}
body.dark .lt td{border-top-color:#2a2d3e;}
.ok-text{color:#27ae60;font-weight:600;}
.chk-text{color:#e67e22;font-weight:600;}
.rev-text{color:#c0392b;font-weight:600;}
/* toolbar */
.toolbar{display:flex;gap:.5rem;align-items:center;margin-bottom:.75rem;flex-wrap:wrap;}
.toolbar>span{font-size:.78rem;color:#999;}
.fbtn{padding:.3rem .8rem;border-radius:20px;font-size:.76rem;font-weight:500;border:1px solid #ddd;background:#fff;cursor:pointer;transition:all .15s;}
.fbtn:hover{border-color:#999;}
.fbtn.active{background:#111;color:#fff;border-color:#111;}
body.dark .fbtn.active{background:#e0e0e0;color:#111;}
.search-box{padding:.3rem .7rem;border-radius:6px;border:1px solid #ddd;font-size:.8rem;width:200px;background:#fff;color:#222;}
body.dark .search-box{background:#1a1d2e;border-color:#2a2d3e;color:#e0e0e0;}
.ml-auto{margin-left:auto;display:flex;gap:.5rem;}
.action-btn{padding:.32rem .85rem;border-radius:6px;font-size:.76rem;font-weight:600;border:none;cursor:pointer;transition:background .15s;}
.btn-blue{background:#2563eb;color:#fff;}
.btn-blue:hover{background:#1d4ed8;}
.btn-red{background:#e74c3c;color:#fff;}
.btn-red:hover{background:#c0392b;}
.btn-gray{background:#6b7280;color:#fff;}
.btn-gray:hover{background:#4b5563;}
/* table */
.table-wrap{background:#fff;border:1px solid #e2e2e2;border-radius:10px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.06);margin-bottom:1rem;}
table{width:100%;border-collapse:collapse;font-size:.875rem;}
thead{position:sticky;top:0;background:#fafafa;border-bottom:2px solid #e0e0e0;z-index:10;}
th{padding:.7rem .85rem;text-align:left;font-size:.7rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em;color:#666;}
th.sortable{cursor:pointer;user-select:none;}
th.sortable:hover{color:#111;}
td{padding:.68rem .85rem;border-top:1px solid #f0f0f0;vertical-align:top;color:#333;}
body.dark td{color:#d0d0d0;}
tbody tr{cursor:pointer;}
tbody tr:focus{outline:2px solid #2563eb;outline-offset:-2px;}
.ts{font-family:monospace;font-size:.8rem;color:#aaa;white-space:nowrap;}
.lang{font-size:.75rem;color:#888;white-space:nowrap;}
.src{font-size:.72rem;color:#bbb;font-family:monospace;}
/* score bar */
.sc-cell{white-space:nowrap;}
.sc-num{font-weight:600;font-size:.85rem;margin-bottom:4px;}
.sc-bar-wrap{background:#f0f0f0;border-radius:4px;height:5px;width:72px;}
.sc-bar{height:5px;border-radius:4px;}
/* row colors */
tr.ok{background:#f0faf4;}
tr.check{background:#fffbf0;}
tr.review{background:#fff5f5;}
tr:hover{filter:brightness(.97);}
tr.hidden{display:none!important;}
/* badges */
.badge{display:inline-block;padding:.18rem .48rem;border-radius:4px;font-size:.68rem;font-weight:700;letter-spacing:.04em;}
.badge.ok{background:#d4edda;color:#1a5e1a;}
.badge.check{background:#fff3cd;color:#7a5500;}
.badge.review{background:#f8d7da;color:#a11;}
.badge.drift{background:#e8eaf6;color:#3949ab;margin-left:4px;}
/* mismatch type badges */
.badge.t-ls{background:#ede7f6;color:#6a1b9a;}
.badge.t-cm{background:#ffebee;color:#b71c1c;}
.badge.t-tr{background:#fff3e0;color:#e65100;}
.badge.t-at{background:#fce4ec;color:#880e4f;}
.badge.t-ws{background:#fff8e1;color:#f57f17;}
.badge.t-mv{background:#f5f5f5;color:#757575;}
.badge.t-ok{background:#e8f5e9;color:#1b5e20;}
/* diff */
mark.diff-del{background:#ffd6d6;color:#900;border-radius:2px;padding:0 2px;}
mark.diff-ins{background:#d6ffe0;color:#060;border-radius:2px;padding:0 2px;}
/* note cell */
.note-cell{min-width:130px;font-size:.78rem;color:#555;border:1px dashed #ddd;border-radius:4px;padding:2px 5px;min-height:28px;}
.note-cell:focus{outline:2px solid #2563eb;border-color:transparent;}
/* footer */
.footer{font-size:.74rem;color:#bbb;text-align:right;padding:.25rem 0 1rem;}
/* print */
@media print{
  .toolbar,.sliders,.hdr-btns,.donut-wrap{display:none!important;}
  tr.hidden{display:table-row!important;}
  body{background:#fff!important;padding:0;}
  .table-wrap,.stat,.lang-wrap{box-shadow:none;border-color:#ccc;}
  thead{background:#f5f5f5!important;}
  @page{margin:1.5cm;}
}
"""

JS = """
// ── URL hash filter ──────────────────────────────────────────────────────────
window.addEventListener('load', () => {
  loadNotes();
  const h = location.hash.replace('#','');
  if (['ok','check','review'].includes(h)) {
    const btn = document.getElementById('btn-'+h);
    if (btn) filterTable(h, btn);
  }
  if (localStorage.getItem('theme')==='dark') enableDark();
});

// ── dark mode ────────────────────────────────────────────────────────────────
function enableDark(){ document.body.classList.add('dark'); }
function toggleDark(){
  document.body.classList.toggle('dark');
  localStorage.setItem('theme', document.body.classList.contains('dark')?'dark':'light');
}

// ── filter ───────────────────────────────────────────────────────────────────
function filterTable(status, btn) {
  document.querySelectorAll('.fbtn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('#tbody tr').forEach(row=>{
    row.classList.toggle('hidden', status!=='all' && row.dataset.status!==status);
  });
  location.hash = status==='all' ? '' : status;
}

// ── search ───────────────────────────────────────────────────────────────────
function searchTable(q) {
  const t = q.toLowerCase();
  document.querySelectorAll('#tbody tr').forEach(row=>{
    row.classList.toggle('hidden', t.length>0 && !row.innerText.toLowerCase().includes(t));
  });
}

// ── sort ─────────────────────────────────────────────────────────────────────
const _sd = {};
function sortTable(col) {
  const tbody = document.getElementById('tbody');
  const rows  = Array.from(tbody.querySelectorAll('tr'));
  const dir   = _sd[col]==='asc'?'desc':'asc';
  _sd[col]    = dir;
  rows.sort((a,b)=>{
    const av=a.cells[col]?.innerText.trim()||'', bv=b.cells[col]?.innerText.trim()||'';
    const an=parseFloat(av), bn=parseFloat(bv);
    if (!isNaN(an)&&!isNaN(bn)) return dir==='asc'?an-bn:bn-an;
    return dir==='asc'?av.localeCompare(bv):bv.localeCompare(av);
  });
  rows.forEach(r=>tbody.appendChild(r));
}

// ── live threshold reclassify ────────────────────────────────────────────────
function reclassify() {
  const okT  = parseFloat(document.getElementById('okSlider').value);
  const chkT = parseFloat(document.getElementById('chkSlider').value);
  document.getElementById('okVal').textContent  = okT.toFixed(2);
  document.getElementById('chkVal').textContent = chkT.toFixed(2);
  let ok=0, chk=0, rev=0;
  document.querySelectorAll('#tbody tr').forEach(row=>{
    const sc = parseFloat(row.dataset.score);
    const ns = sc>=okT?'ok': sc>=chkT?'check':'review';
    if (ns==='ok') ok++; else if (ns==='check') chk++; else rev++;
    row.className = row.className.replace(/\\bok\\b|\\bcheck\\b|\\breview\\b/g, ns);
    row.dataset.status = ns;
    const sb = row.querySelector('.sb');
    if (sb){ sb.className=`badge sb ${ns}`; sb.textContent=ns.toUpperCase(); }
    const bar = row.querySelector('.sc-bar');
    const col = ns==='ok'?'#27ae60':ns==='check'?'#e67e22':'#e74c3c';
    if (bar){ bar.style.background=col; bar.style.width=(parseFloat(row.dataset.score)*100)+'%'; }
  });
  const tot = ok+chk+rev;
  document.getElementById('cnt-ok').textContent  = ok;
  document.getElementById('cnt-chk').textContent = chk;
  document.getElementById('cnt-rev').textContent = rev;
  document.getElementById('btn-all').textContent   = `All (${tot})`;
  document.getElementById('btn-ok').textContent    = `OK (${ok})`;
  document.getElementById('btn-check').textContent = `Check (${chk})`;
  document.getElementById('btn-review').textContent= `Review (${rev})`;
  updateDonut(ok, chk, rev, tot);
}

// ── donut chart update ───────────────────────────────────────────────────────
function updateDonut(ok, chk, rev, tot) {
  if (!tot) return;
  const okP=ok/tot*100, chkP=chk/tot*100, revP=rev/tot*100;
  const set = (id, pct, off)=>{
    const el=document.getElementById(id);
    if (el){ el.setAttribute('stroke-dasharray',`${pct} ${100-pct}`);
             el.setAttribute('stroke-dashoffset',off); }
  };
  set('donut-ok',  okP,  25);
  set('donut-chk', chkP, 25-okP);
  set('donut-rev', revP, 25-okP-chkP);
  const lbl = document.getElementById('donut-lbl');
  if (lbl) lbl.textContent = Math.round(ok/tot*100)+'% OK';
}

// ── jump to worst ────────────────────────────────────────────────────────────
function jumpToWorst() {
  const rows = Array.from(document.querySelectorAll('#tbody tr:not(.hidden)'));
  if (!rows.length) return;
  const worst = rows.reduce((a,b)=>
    parseFloat(a.dataset.score)<parseFloat(b.dataset.score)?a:b);
  worst.scrollIntoView({behavior:'smooth',block:'center'});
  worst.style.outline='3px solid #e74c3c';
  worst.focus();
  setTimeout(()=>worst.style.outline='',2000);
}

// ── export CSV (respects active filter) ─────────────────────────────────────
function exportCSV() {
  const rows  = Array.from(document.querySelectorAll('#tbody tr:not(.hidden)'));
  const heads = Array.from(document.querySelectorAll('#mainTable thead th'))
                     .map(h=>h.innerText.replace(' ↕',''));
  const esc = v=>'"'+String(v).replace(/"/g,'""')+'"';
  const lines=[heads.map(esc).join(',')];
  rows.forEach(row=>{
    lines.push(Array.from(row.cells).map(c=>esc(c.innerText.trim())).join(','));
  });
  const blob=new Blob(['\\uFEFF'+lines.join('\\n')],{type:'text/csv;charset=utf-8;'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob); a.download='report_filtered.csv'; a.click();
}

// ── inline annotations (localStorage) ───────────────────────────────────────
function loadNotes() {
  document.querySelectorAll('.note-cell').forEach(cell=>{
    const key='note_'+cell.dataset.ts;
    cell.textContent=localStorage.getItem(key)||'';
    cell.addEventListener('input',()=>localStorage.setItem(key, cell.textContent));
  });
}

// ── keyboard navigation (arrow keys between rows) ───────────────────────────
document.addEventListener('keydown', e=>{
  if (!['ArrowDown','ArrowUp'].includes(e.key)) return;
  const focused = document.querySelector('#tbody tr:focus');
  const rows    = Array.from(document.querySelectorAll('#tbody tr:not(.hidden)'));
  const idx     = rows.indexOf(focused);
  const next    = e.key==='ArrowDown'?rows[idx+1]:rows[idx-1];
  if (next){ e.preventDefault(); next.focus(); next.scrollIntoView({block:'nearest'}); }
});
"""
