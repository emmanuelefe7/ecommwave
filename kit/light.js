// LIGHT look icons. Write >i:name< inside an element and call lightIcons() at the end of the page.
const LI_=(d,c='#152a59',w=30)=>`<svg width="${w}" height="${w}" viewBox="0 0 24 24" fill="none" stroke="${c}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">${d}</svg>`;
const LICONS={
  target:LI_('<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/>'),
  mail:LI_('<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 7l9 6 9-6"/>'),
  search:LI_('<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>'),
  trend:LI_('<path d="M4 16l6-6 4 4 6-6"/><path d="M15 8h5v5"/>'),
  phone:LI_('<rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M11 18.5h2"/>'),
  camera:LI_('<path d="M4 8h3l2-2.5h6L17 8h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>'),
  star:LI_('<path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.9l-5.2 2.7 1-5.8L3.5 9.7l5.9-.9z"/>'),
  truck:LI_('<path d="M3 6.5h11v9H3zM14 10h4l3 3v2.5h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17.5" cy="17.5" r="1.8"/>'),
  cart:LI_('<path d="M4.5 8.5h15l-1.3 11.2a1.5 1.5 0 01-1.5 1.3H7.3a1.5 1.5 0 01-1.5-1.3z"/><path d="M8.5 11V7a3.5 3.5 0 017 0v4"/>'),
  heart:LI_('<path d="M12 20s-7-4.4-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.6-7 10-7 10z"/>'),
  hand:LI_('<path d="M7 11V6.5a1.5 1.5 0 013 0V11M10 10V5a1.5 1.5 0 013 0v5M13 10V6a1.5 1.5 0 013 0v6M16 9.5a1.5 1.5 0 013 0V14a7 7 0 01-7 7h-.5A6.5 6.5 0 015 16.2L3.6 13a1.5 1.5 0 012.6-1.4L8 14"/>'),
  clock:LI_('<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>'),
  check:LI_('<path d="M5 12.5l4.5 4.5L19 7.5"/>','#152a59',24),
  arrowm:LI_('<path d="M5 12h14M13 6l6 6-6 6"/>','#152a59',32),
  arroww:LI_('<path d="M5 12h14M13 6l6 6-6 6"/>','#ffffff',26),
};
function lightIcons(){document.body.innerHTML=document.body.innerHTML.replace(/>i:(\w+)</g,(m,k)=>'>'+(LICONS[k]||k)+'<');}
