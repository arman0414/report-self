const el = (id) => document.getElementById(id);
const esc = (value) => String(value ?? '').replace(/[&<>'"]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[ch]));
async function api(url, options){ const res = await fetch(url, options); const data = await res.json().catch(()=>({detail:'Unexpected response'})); if(!res.ok) throw new Error(Array.isArray(data.detail) ? data.detail.map(d=>d.msg).join(', ') : data.detail || 'Request failed'); return data; }
function item(title, body, badges = []) { return `<div class="item"><strong>${esc(title)}</strong>${badges.join('')}<p>${esc(body)}</p></div>`; }
async function run(){
  try {
    const payload={topic:el('topic').value,audience:el('audience').value,depth:Number(el('depth').value)};
    const report=await api('/api/research',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    el('taskCount').textContent=report.tasks.length;
    el('claimCount').textContent=report.claims.length;
    el('critiqueCount').textContent=report.critiques.length;
    const avg=report.claims.reduce((s,c)=>s+c.confidence,0)/Math.max(report.claims.length,1);
    el('confidence').textContent=report.claims.length ? Math.round(avg*100)+'%' : 'n/a';
    el('claims').innerHTML=report.claims.length ? report.claims.slice(0,6).map(c=>item('Claim',c.text,[`<span class="badge">${Math.round(c.confidence*100)}%</span>`,`<span class="badge low">${esc(c.source_ids.join(', '))}</span>`])).join('') : item('No grounded claims', 'Try a topic related to AI systems, RAG, incidents, reliability, security, or event streaming.');
    el('report').textContent=report.markdown;
  } catch(err) {
    el('claims').innerHTML = item('Request failed', err.message);
    el('report').textContent = err.message;
  }
}
el('runResearch').onclick=run; el('example').onclick=()=>{el('topic').value='production-grade AI incident response platforms'; el('depth').value='4';};
