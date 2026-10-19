"use strict";
(function(){
const models=[
["cost",1000,300,"追加収容費（公費）","仮に年間1,000人年の収容増×年300万円。実際の単価・服役延長件数は不明。"],
["cost",500,100,"追加送還・審査費（公費）","仮に500件の追加送還×100万円。送還者全体と重大犯罪者は別集団。"],
["cost",65229*.05,100,"送還手続費（公費）","不法残留者65,229人の5%を仮の対象×100万円。摘発成功者数の予測ではない。"],
["labor",268450*.10,.50,"年間労働者増加の10%が減少","仮に外国人就業者の年間増加268,450人が10%鈍化し、50%を他の労働で代替。",-1],
["labor",268450*.10,.30,"年間労働者増加の10%が減少","仮に外国人就業者の年間増加268,450人が10%鈍化し、30%を代替。非熟練者の実数ではない。",-1],
["labor",2000,0,"高度専門人材が2,000人純増","純追加就業2,000人と仮定。高度人材固有のGDP/人は把握できないため国内平均で代用。",1],
["cost",2571037*.10,5,"追加日本語研修費（民間等）","外国人労働者の10%相当に一人5万円の研修費を仮定。研修効果は未推計。"],
["cost",961342*.01,4,"追加審査費（公費）","既存永住者961,342人の1%相当に一件4万円と仮定。実際の再審査対象ではない。"],
["cost",9258*.10,10,"追加審査費（公費）","帰化許可者9,258人の10%相当に一件10万円を仮定。申請者の実際の総数ではない。"],
["recover",10000,10,"保険料等の徴収増","仮に一万件×10万円を追加徴収し、事務費3億円。外国籍の未納総額を測った値ではない。",3],
["transfer",1000,120,"公的給付支出の変化","仮に一千世帯×年120万円の支給変更を想定。対象者数・影響・妥当性は未検証。"],
["cost",68,20,"土地取得審査費（公費）","特定条件の届出68件×一件20万円の追加審査と仮定。国内全土地取引の件数ではない。"],
["cost",10000,.5,"免許切替の追加事務費（公費）","仮に一万件×5,000円の追加確認を行う条件。事故抑止効果の金銭価値は未推計。"],
["cost",11298,5,"難民審査追加費（公費）","難民申請11,298件と同数に一件5万円追加。処理短縮による節減は未算入。"],
["cost",457509*.10,10,"追加研修・移行費（民間）","技能実習者の10%相当に一人10万円の追加教育費を仮定。効果は未算入。"],
["tourism",94549,-.01,"訪日旅行消費の変化","2025年の旅行消費9兆4,549億円が仮に1%減少。GDP・税収の減少と同一ではない。"],
["statusquo",0,0,"現状維持の制度変更費","現在の制度を変更しなければ直接の制度移行費は0円。長期的なGDP影響が0と証明したのではない。"],
["cost",4281026*.10,2,"多言語支援費（自治体等）","在留外国人の10%相当に一人2万円の追加支援と仮定。トラブル減少効果は未算入。"]
];
const official={nominalGdpTrillion:672.7,employment:68280000,nationalTaxTrillion:84.2226};
const refs=[
["内閣府GDP","https://www.esri.cao.go.jp/jp/sna/menu.html"],
["総務省就業者数","https://www.stat.go.jp/data/roudou/sokuhou/nen/ft/pdf/gaiyou.pdf"],
["財務省税収","https://www.mof.go.jp/tax_policy/reference/fy2025k_budget_and_settlement.pdf"]
];
let scale=1;
const roundOku=n=>Math.abs(n)<1?Math.abs(n).toFixed(2):Math.abs(n)<10?Math.abs(n).toFixed(1):Math.round(Math.abs(n)).toLocaleString("ja-JP");
const money=n=>(n<0?"−":n>0?"＋":"±")+roundOku(n)+"億円";
const html=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function card(index){
 const m=models[index];if(!m)throw Error("invalid-policy-index");
 const kind=m[0];let headline="",gross="算定根拠なし",tax="算定根拠なし",other="―",formula="";
 if(kind==="labor"){
   const effective=m[1]*(1-m[2])*scale;
   const grossOku=m[5]*effective*(official.nominalGdpTrillion*1e12/official.employment)/1e8;
   headline="GDP粗参考 "+money(grossOku)+"/年";gross=money(grossOku)+"/年";
   tax=money(grossOku*official.nationalTaxTrillion/official.nominalGdpTrillion)+"/年";
   other="就業者数の仮定差："+Math.round(effective).toLocaleString("ja-JP")+"人";
   formula="GDP粗参考＝就業者の仮定差×（名目GDP672.7兆円÷就業者6,828万人）。国税参考＝GDP粗参考×（国税84.2226兆円÷GDP672.7兆円）。";
 }else if(kind==="cost"){
   const amount=m[1]*m[2]*scale/10000;
   headline=m[3]+" "+money(amount)+"/年";other=money(amount)+"/年";
   formula="仮定した件数 "+Math.round(m[1]).toLocaleString("ja-JP")+"件相当×一件あたり"+m[2]+"万円×"+scale+"倍÷10,000。";
 }else if(kind==="recover"){
   const collected=m[1]*m[2]*scale/10000,admin=m[5]*scale;
   headline="保険料等の追加徴収 "+money(collected)+"/年";
   other="追加徴収 "+money(collected)+"／行政費 "+money(admin)+"（差額 "+money(collected-admin)+"）";
   formula="仮の徴収10,000件×10万円。行政費3億円。両方を規模倍率で調整。保険料は国税に含めない。";
 }else if(kind==="transfer"){
   const amount=-m[1]*m[2]*scale/10000;
   headline="公的給付支出 "+money(amount)+"/年";other=money(amount)+"/年";
   formula="一千世帯×年間120万円×規模倍率。給付削減はGDP増加ではなく所得移転の変化。";
 }else if(kind==="tourism"){
   const amount=m[1]*m[2]*scale;headline="訪日旅行消費 "+money(amount)+"/年";other=money(amount)+"/年";
   formula="2025年旅行消費94,549億円×仮の1%減少×規模倍率。国内付加価値や税収とは別。";
 }else{
   headline="制度変更費 0円（現状維持の仮定）";other="0円（制度移行費のみ）";
   formula="現状維持なら制度変更に伴う直接の移行費は0円。経済・社会的効果を0円とみなしていない。";
 }
 const links=refs.map(r=>'<a href="'+r[1]+'" target="_blank" rel="noopener noreferrer">'+r[0]+' ↗</a>').join(" ／ ");
 return '<section class="impact-estimate"><div class="impact-tag">試算・仮定のシナリオ｜1年</div><strong class="impact-main">'+html(headline)+'</strong><div class="impact-trio"><div><b>GDP</b><span>'+html(gross)+'</span></div><div><b>国税</b><span>'+html(tax)+'</span></div><div><b>その他</b><span>'+html(other)+'</span></div></div><details class="impact-formula"><summary>推定の計算式・仮定を見る ＋</summary><p><b>対象の条件：</b>'+html(m[4])+'</p><p><b>計算式：</b>'+html(formula)+'</p><p>費用の単価・政策の影響人数・代替率は<strong>例示した仮定</strong>であり、実際の政策効果の予測ではありません。GDP/人は就業者全体の平均で、外国人に固有の生産性でも納税額でもありません。2025年度GDPと2025年平均就業者は対象期間が異なります。</p><p>'+links+'</p></details></section>';
}
window.PolicyImpact={card,setScale:v=>{if(!Number.isFinite(v)||v<.5||v>2)throw Error("scale-out-of-range");scale=v;},getModels:()=>models.length};
})();
