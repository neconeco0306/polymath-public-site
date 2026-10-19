/**
 * POLYMATH Open Lab: non-destructive homepage + separate 100-project index.
 * For this 2026-10-19 one-shot release, fetch the pinned *pre-navigation*
 * production alias after verified rollback. Deployment must fail on drift.
 * The result embeds full original page, not a reconstructed snippet.
 * Once a source-controlled canonical homepage exists, migrate to it.
 */
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
const BASE = 'https://polymath-open-lab.vercel.app/';
const PINNED = 'https://polymath-open-6m054519r-nilo17.vercel.app/'; // last known intact deployment
const anchor='<!-- POLYMATH_PRODUCT_DIRECTORY_v2_START -->';
const links=[
 ['MORPH','画像・ファイル加工','https://nilo-morph-lab.onrender.com/'],
 ['PLOTCRAFT','グラフ・可視化','https://nilo-plotcraft-lab.onrender.com/'],
 ['LINKLOOM','プロフィールサイト制作','https://nilo-linkloom-lab.onrender.com/']
];
const css=`<style id="polymath-products-style">
#polymath-product-entry{box-sizing:border-box;width:min(1060px,calc(100% - 36px));margin:28px auto 34px;border:1px solid #cbdccd;background:#fffdf8;color:#1a3b30;border-radius:12px;box-shadow:0 8px 26px #19362f09;padding:21px 25px;font:inherit}
#polymath-product-entry *{box-sizing:border-box}#polymath-product-entry .polybar{display:flex;align-items:center;gap:12px;justify-content:space-between;flex-wrap:wrap}
#polymath-product-entry .polykicker{font:800 11px/1.6 ui-monospace,monospace;letter-spacing:.08em;color:#3b735e}#polymath-product-entry h2{font-size:clamp(19px,2.4vw,25px);letter-spacing:-.035em;margin:5px 0 8px;line-height:1.5;color:#1a3b30}
#polymath-product-entry p{font-size:13px;line-height:1.75;color:#506c61;margin:0 0 15px}
#polymath-product-entry .polylist{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
#polymath-product-entry a.polytool{display:block;background:#f5f8f3;border:1px solid #dce8de;border-radius:8px;text-decoration:none;color:#1a4435;padding:12px 13px;line-height:1.5;min-width:0}
#polymath-product-entry a.polytool strong{display:block;font-size:14px;color:#1b533f}#polymath-product-entry a.polytool small{display:block;font-size:11px;color:#536f5d;margin-top:4px}
#polymath-product-entry a.polytool:hover{border-color:#82b49d;background:#eaf2e9}#polymath-product-entry a:focus-visible{outline:3px solid #bb5b2e;outline-offset:3px}
#polymath-product-entry .polydirectory{display:inline-block;font-size:12px;font-weight:800;color:#175b44;text-underline-offset:3px;white-space:normal}
@media(max-width:630px){#polymath-product-entry{padding:17px 16px;margin:19px auto 25px}#polymath-product-entry .polylist{grid-template-columns:1fr}}
</style>`;
const section=`${anchor}\n<section id="polymath-product-entry" aria-labelledby="poly-products-title"><div class="polybar"><div class="polykicker">NEW / FREE PRODUCT PROGRAM · 03 LIVE · 100 REFERENCES</div><a class="polydirectory" href="/creator-suite/">100件の開発計画を見る ↗</a></div><h2 id="poly-products-title">無料の制作ツールを公開中</h2><p>研究成果とは別に、3つのブラウザツールを制作しました。100件の候補から3件を公開デモ化し、残り97件は検討・開発待ちです。</p><div class="polylist">${links.map(([label,desc,url])=>`<a class="polytool" href="${url}" target="_blank" rel="noopener noreferrer" aria-label="${label}を新しいタブで開く"><strong>${label} ↗</strong><small>${desc}</small></a>`).join('')}</div></section><!-- POLYMATH_PRODUCT_DIRECTORY_v2_END -->`;
async function loadBase(){
 if(process.env.ORIGINAL_PATH)return readFile(process.env.ORIGINAL_PATH,'utf8');
 const errors=[];
 for (const url of [PINNED, BASE]){
  for(let attempt=1;attempt<=2;attempt++){
   const ctrl=new AbortController();const to=setTimeout(()=>ctrl.abort(),15000);
   try{
    const res=await fetch(url,{redirect:'follow',signal:ctrl.signal,cache:'no-store'});
    if(!res.ok)throw Error('HTTP '+res.status);
    const txt=await res.text();
    if(!txt.toLowerCase().startsWith('<!doctype html')||!txt.includes('POLYMATH')||!txt.includes('</html>')||Buffer.byteLength(txt,'utf8')<50000)throw Error('Unexpected original length or markup');
    console.log('ORIGIN_ACCEPTED',JSON.stringify({source:url,bytes:Buffer.byteLength(txt)}));
    return txt;
   }catch(e){errors.push(url+' attempt '+attempt+': '+String(e));}
   finally{clearTimeout(to)}
  }
 }
 throw Error('Unable to retrieve intact baseline: '+errors.join(' | '));
}
const original=await loadBase();
if(!original.toLowerCase().startsWith('<!doctype html')||!/<html\b/i.test(original)||!/<main\b/i.test(original)||!/<\/main>/i.test(original)||!/<\/body>/i.test(original)||!/<\/html>/i.test(original))throw Error('Original HTML structure mismatch');
if(!process.env.ORIGINAL_PATH && Buffer.byteLength(original,'utf8')<50000)throw Error('Original unexpectedly short; abort');
if(!/POLYMATH/i.test(original)||!/研究|制作|成果/.test(original))throw Error('Not the expected research site');
if(original.includes('creator-suite-links')||original.includes('polymath-product-entry'))throw Error('Origin is already patched. Refuse recursive copy');
const main=/<main\b[^>]*>/i.exec(original);if(!main)throw Error('main absent');
const insert=main.index+main[0].length;
let html=original.slice(0,insert)+'\n'+section+'\n'+original.slice(insert);
const head=/<\/head\s*>/i.exec(html);if(!head)throw Error('head absent');html=html.slice(0,head.index)+'\n'+css+'\n'+html.slice(head.index);
if((html.match(/<section id="polymath-product-entry"/g)||[]).length!==1)throw Error('Duplicate entry ID');
if(links.some(([, ,url])=>(section.split(url).length-1)!==1))throw Error('Broken tool navigation link');
if((html.match(/<main\b/gi)||[]).length !== (original.match(/<main\b/gi)||[]).length)throw Error('Main count modified');
const restore=html.replace('\n'+css+'\n','').replace('\n'+section+'\n','');
if(restore!==original)throw Error('Existing research content changed; abort');
const catalog=await readFile('catalog.html','utf8');
if((catalog.match(/data-entry data-stage=/g)||[]).length!==100 || !catalog.includes('公開デモ 3') || !catalog.includes('開発候補 97'))throw Error('Catalog validation failed');
await mkdir('dist/creator-suite',{recursive:true});
await writeFile('dist/index.html',html,'utf8');await writeFile('dist/creator-suite/index.html',catalog,'utf8');
await writeFile('dist/creator-suite/program.json',await readFile('catalog.json'));
const digest=s=>createHash('sha256').update(s).digest('hex');
const report={origin:BASE,originalBytes:Buffer.byteLength(original),originalSha256:digest(original),updatedSha256:digest(html),originalStructurePreserved:restore===original,catalogEntries:100,liveDemos:3,backlog:97,links:links.map(x=>x[2]),status:'HTML_AND_CATALOG_INTEGRITY_PASS',externalBrowserTest:'NOT_YET_RUN'};
await writeFile('dist/creator-suite/build-audit.json',JSON.stringify(report,null,2));
if(!process.env.ORIGINAL_PATH){try{const rob=await fetch(new URL('robots.txt',BASE),{signal:AbortSignal.timeout(7000)});if(rob.ok)await writeFile('dist/robots.txt',await rob.text())}catch(err){console.log('Robots fetch was skipped',String(err))}}
console.log('INTEGRITY_PASS '+JSON.stringify(report));