const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const P=(t,s,d)=>clamp((t-s)/d);                 // linear progress
const eo=x=>1-Math.pow(1-x,3);                   // ease out cubic
const eo5=x=>1-Math.pow(1-x,5);                  // ease out quint
const eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2; // ease in-out cubic
const back=x=>{const c1=1.3,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const lerp=(a,b,x)=>a+(b-a)*x;
const $=s=>document.querySelector(s);
const $$=s=>[...document.querySelectorAll(s)];

// split an element's text nodes into masked words; keeps inline wrappers (e.g. .serif, .accent)
function splitWords(el){
  const out=[];
  const walk=(node,wrapClass)=>{
    [...node.childNodes].forEach(n=>{
      if(n.nodeType===3){
        const frag=document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(tok=>{
          if(!tok) return;
          if(/^\s+$/.test(tok)){frag.appendChild(document.createTextNode(' '));return;}
          const w=document.createElement('span');w.className='w';
          const i=document.createElement('span');i.textContent=tok;
          if(wrapClass) i.className=wrapClass;
          w.appendChild(i);frag.appendChild(w);out.push(i);
        });
        n.replaceWith(frag);
      } else if(n.nodeType===1 && n.tagName==='BR'){ }
      else if(n.nodeType===1){ const cls=n.className; const kids=document.createDocumentFragment();
        walk(n,cls); while(n.firstChild) kids.appendChild(n.firstChild); n.replaceWith(kids); }
    });
  };
  walk(el,'');
  return out;
}
// animate words in (t local), stagger s, duration d
function wordsIn(words,t,start,stagger=.07,d=.6){
  words.forEach((w,i)=>{const x=eo5(P(t,start+i*stagger,d));
    w.style.transform=`translateY(${(1-x)*110}%)`;});
}
function wordsOut(words,t,start,stagger=.03,d=.4){
  if(t<start) return;
  words.forEach((w,i)=>{const x=eio(P(t,start+i*stagger,d));
    w.style.transform=`translateY(${-x*110}%)`;});
}
function op(el,v){el.style.opacity=v}
function tf(el,s){el.style.transform=s}
const CHECK='<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#34d5a0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
const ARROW='<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#34d5a0" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
const CURSOR='<svg viewBox="0 0 24 24" width="40" height="40"><path d="M4 2l15 11.2-6.6 1 3.9 7.6-2.9 1.5-3.9-7.7L4 20.5z" fill="#fff" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/></svg>';
const BAG='<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#34d5a0" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 8.5h15l-1.3 11.2a1.5 1.5 0 01-1.5 1.3H7.3a1.5 1.5 0 01-1.5-1.3z"/><path d="M8.5 11V7a3.5 3.5 0 017 0v4"/></svg>';
const LOCK='<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2.4"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/></svg>';
const PLUS='<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>';
const SEARCH='<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0f1f4d" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>';
const CART='<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0f1f4d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 8.5h15l-1.3 11.2a1.5 1.5 0 01-1.5 1.3H7.3a1.5 1.5 0 01-1.5-1.3z"/><path d="M8.5 11V7a3.5 3.5 0 017 0v4"/></svg>';
const STATUS='<svg width="78" height="14" viewBox="0 0 78 14"><rect x="0" y="9" width="3.5" height="5" rx="1" fill="#0f172a"/><rect x="5.5" y="6" width="3.5" height="8" rx="1" fill="#0f172a"/><rect x="11" y="3" width="3.5" height="11" rx="1" fill="#0f172a"/><rect x="16.5" y="0" width="3.5" height="14" rx="1" fill="#0f172a"/><path d="M29 5.5a10 10 0 0114 0M31.5 8.3a6.3 6.3 0 019 0M34.2 11a2.6 2.6 0 013.6 0" stroke="#0f172a" stroke-width="2" fill="none" stroke-linecap="round"/><rect x="50" y="1" width="24" height="12" rx="3.5" stroke="#0f172a" stroke-opacity=".4" fill="none"/><rect x="52" y="3" width="18" height="8" rx="2" fill="#0f172a"/><rect x="75.5" y="4.5" width="2" height="5" rx="1" fill="#0f172a" fill-opacity=".4"/></svg>';
function browserHTML(url,inner,w,h){
  return `<div class="bbar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i>
  <div class="url">${LOCK}<span>${url}</span></div></div><div class="view" style="width:${w}px;height:${h-58}px">${inner}</div>`;
}
const PRODUCTS=[['p_serum','Glow Serum Set','$48','$64'],['p_sneaker','Court Sneaker','$89',''],['p_bag','Tan Satchel','$129','$159'],['p_dress','Linen Dress','$75','']];
function novaHTML(){
  return `<div class="nova"><div class="ann">Free shipping over $50 · 30-day returns</div>
  <div class="nav"><div class="logo">NOVA</div><div class="links"><span>Shop</span><span>New</span><span>About</span><span>Journal</span></div>
  <div class="icons">${SEARCH}<span style="position:relative">${CART}<b class="cartn" style="position:absolute;right:-9px;top:-7px;width:20px;height:20px;border-radius:50%;background:#12b886;color:#fff;font:700 12px Inter;display:grid;place-items:center;opacity:0">1</b></span></div></div>
  <div class="hero"><img src="assets/hero_woman.png"><h2>The Summer <em>Edit</em></h2><div class="btn">Shop now</div></div>
  <div class="sec"><h3>Best sellers</h3><div class="grid">${PRODUCTS.map(p=>`<div class="card"><div class="im"><img src="assets/${p[0]}.png"><div class="plus">${PLUS}</div></div><div class="nm">${p[1]}</div><div class="pr">★★★★★ ${p[2]}${p[3]?`<s>${p[3]}</s>`:''}</div></div>`).join('')}</div></div></div>`;
}
function junkHTML(){
  const txt='★★ FREE SHIPPING?? ★★ BUY NOW!!! ★★ LIMITED TIME ★★ HOT HOT HOT ★★ DON\'T MISS OUT ★★ ';
  return `<div class="junk"><div class="top">MEGA SALE!!! 70% OFF EVERYTHING – HURRY!!!</div>
  <div class="nav"><span>Home</span><span>Sale</span><span>New</span><span>Hot</span><span>Deals</span><span>Info</span><span>Blog</span><span>FAQ</span><span>More</span></div>
  <img class="heroimg" src="assets/hero_woman.png">
  <div class="bd">BEST DEALS EVER!!!</div><div class="ch">CLICK HERE NOW &gt;&gt;</div>
  <div class="marq"><span class="mq">${txt+txt+txt}</span></div>
  <div class="prods">${PRODUCTS.map((p,i)=>`<div class="p"><img src="assets/${p[0]}.png"><b>$${[99,49,19,29][i]}!!!</b><u>BUY NOW BUY NOW</u></div>`).join('')}</div>
  <div class="pop"><span class="x">✕</span>WAIT!!! DON'T LEAVE!!!<small>Enter your email for 5% off maybe</small></div></div>`;
}

// ---- Voiceover sync ----
// Author the animation on any "design" timeline, then lock it to the voice:
//   const T = voWarp([0.15, 1.9, 3.7, 6.4, 9.9, 12.0]);   // design time where each VO line's moment begins
//   window.DUR = VO.dur;  function render(t){ draw(T(t)); }   // draw(d) = your animation in design time
// Line i's design moment lands exactly when line i starts being spoken; the end of the design
// timeline (designEnd, default last anchor + 3) lands on VO.dur. Requires <script src="vo/timing.js">.
function voWarp(anchors, designEnd){
  const L=window.VO.lines; const xs=[0], ys=[0];
  anchors.forEach((d,i)=>{ if(L[i]){ xs.push(L[i].start); ys.push(d); } });
  xs.push(window.VO.dur); ys.push(designEnd ?? anchors[anchors.length-1]+3);
  return t=>{ for(let i=1;i<xs.length;i++){ if(t<=xs[i]){ const f=(t-xs[i-1])/Math.max(1e-6,xs[i]-xs[i-1]); return ys[i-1]+(ys[i]-ys[i-1])*f; } } return ys[ys.length-1]; };
}
