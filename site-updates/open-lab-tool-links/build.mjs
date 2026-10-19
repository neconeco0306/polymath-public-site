/** Add three production-ready tool links near the site's opening index.
 * Uses the existing live site as the *build-time only* source to avoid
 * overwriting its research archive. Fails closed on source or layout drift.
 */
import {mkdir,writeFile} from 'node:fs/promises';
const source='https://polymath-open-lab.vercel.app/';
const links=[
  ['MORPH','画像・PDF・ファイルをまとめて加工','https://nilo-morph-lab.onrender.com/'],
  ['PLOTCRAFT','グラフ・データ可視化を自由に制作','https://nilo-plotcraft-lab.onrender.com/'],
  ['LINKLOOM','プロフィールサイトを編集して書き出す','https://nilo-linkloom-lab.onrender.com/'],
];
const style=`<style id="creator-suite-nav-style">
#creator-suite-links{width:min(1060px,calc(100% - 38px));margin:26px auto 34px;padding:24px 26px;border:1px solid #dce6df;border-radius:15px;background:#fffefb;color:#19352f;box-shadow:0 7px 24px #18372c0a}
#creator-suite-links .cst-eyebrow{color:#346958;font-size:11px;font-weight:800;letter-spacing:.14em}
#creator-suite-links h2{font-size:clamp(19px,3vw,25px);letter-spacing:-.03em;line-height:1.4;margin:7px 0 6px}
#creator-suite-links p{margin:0 0 19px;color:#536961;font-size:13px;line-height:1.75}
#creator-suite-links .cst-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
#creator-suite-links .cst-card{display:flex;flex-direction:column;gap:7px;min-width:0;padding:17px 17px 15px;background:#f7faf7;border:1px solid #e1e9e2;border-radius:11px;color:#1b3930;text-decoration:none!important;transition:background .15s,border-color .15s}
#creator-suite-links .cst-card:hover{background:#e9f3eb;border-color:#9bbda8}
#creator-suite-links .cst-card:focus-visible{outline:3px solid #a14b2c;outline-offset:3px}
#creator-suite-links .cst-card strong{font-size:17px;letter-spacing:.025em}
#creator-suite-links .cst-card small{font-size:12px;line-height:1.65;color:#49675c}
#creator-suite-links .cst-card span{margin-top:auto;padding-top:3px;font-size:12px;font-weight:800;color:#23684d}
@media(max-width:680px){#creator-suite-links{padding:19px 17px;margin:16px auto 24px}#creator-suite-links .cst-grid{grid-template-columns:1fr}#creator-suite-links .cst-card{padding:13px 15px;gap:4px}}
@media(prefers-reduced-motion:reduce){#creator-suite-links .cst-card{transition:none}}
</style>`;
const section=`<section id="creator-suite-links" aria-labelledby="creator-suite-title">
<div class="cst-eyebrow">NEW / FREE CREATOR TOOLS</div>
<h2 id="creator-suite-title">公開ツールを使ってみる</h2>
<p>研究とは別に、ブラウザで使える無料の制作ツールも公開しています。各サイトへ直接移動できます。</p>
<div class="cst-grid">${links.map(([title,description,url])=>`<a class="cst-card" href="${url}" target="_blank" rel="noopener noreferrer" aria-label="${title}：${description}（新しいタブで開く）"><strong>${title}</strong><small>${description}</small><span>サイトを開く ↗</span></a>`).join('')}</div>
</section>`;
const res=await fetch(source,{redirect:'follow',signal:AbortSignal.timeout(20000)});
if(!res.ok)throw Error('Source website unavailable '+res.status);
const orig=await res.text();
if(orig.length<10000||!orig.includes('POLYMATH')||!orig.includes('</html>'))throw Error('Unexpected source content, aborting');
if(orig.includes('creator-suite-links'))throw Error('New navigation already present in original, abort to avoid duplicate');
const targets=[...orig.matchAll(/<nav\b[^>]*>[\s\S]*?<\/nav>/gi)];
let point=-1,position='';
const toc=targets.find(m=>/目次|INDEX|一覧|作品|成果|ツール|CONTENTS/i.test(m[0]));
if(toc){point=toc.index+toc[0].length;position='toc-nav'}
else if(targets.length){point=targets[0].index+targets[0][0].length;position='first-nav'}
else{
 const main=/<main\b[^>]*>/i.exec(orig);
 if(!main)throw Error('Neither navigation nor main found; abort rather than modifying unknown layout');
 point=main.index+main[0].length;position='main-start';
}
if(point<0||point>orig.length-1000)throw Error('Insertion point failed validation');
const headClose=orig.indexOf('</head>');if(headClose<0)throw Error('No </head>');
const withSection=orig.slice(0,point)+'\n'+section+'\n'+orig.slice(point);
const html=withSection.slice(0,withSection.indexOf('</head>'))+style+'\n'+withSection.slice(withSection.indexOf('</head>'));
if(!html.includes(section)||!html.includes(style)||links.some(([, ,url])=>html.split(url).length!==2))throw Error('Link insertion integrity mismatch');
for(const s of [orig,html]){if((s.match(/<main\b/gi)||[]).length<1)throw Error('Lost main landmark')}
await mkdir('dist',{recursive:true});await writeFile('dist/index.html',html,'utf8');
const rob=await fetch(new URL('robots.txt',source),{signal:AbortSignal.timeout(10000)});if(rob.ok)await writeFile('dist/robots.txt',await rob.text());
const proof={source,origBytes:Buffer.byteLength(orig),newBytes:Buffer.byteLength(html),insertion:position,links:links.map(x=>x[2]),unchangedSourcePreserved:true};
await writeFile('dist/update-audit.json',JSON.stringify(proof,null,2));
console.log('NAV_ADDED',JSON.stringify(proof));