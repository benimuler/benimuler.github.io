(function(){var R=window.RATES,d=document;
var nf=new Intl.NumberFormat("he-IL",{maximumFractionDigits:0}),n2=new Intl.NumberFormat("he-IL",{minimumFractionDigits:2,maximumFractionDigits:2});
function f0(x){return nf.format(Math.round(x))}function f2(x){return n2.format(x)}function ils(x){return f0(x)+" ₪"}function pc(x){return n2.format(x*100)+"%"}
function big(l,v,s){return '<div class="big"><span>'+l+'</span><b>'+v+'</b>'+(s?'<small>'+s+'</small>':'')+'</div>'}
function tbl(rows,head){return '<div class="tw" style="margin-top:10px"><table>'+(head?'<thead><tr>'+head.map(function(h){return '<th>'+h+'</th>'}).join("")+'</tr></thead>':'')+'<tbody>'+rows.map(function(r){return '<tr>'+r.map(function(c){return '<td>'+c+'</td>'}).join("")+'</tr>'}).join("")+'</tbody></table></div>'}
function warn(t){return '<div class="warn">'+t+'</div>'}
function btax(x,b){var t=0,p=0;for(var i=0;i<b.length;i++){if(x>p)t+=(Math.min(x,b[i][0])-p)*b[i][1];p=b[i][0]}return t}
function pmt(P,r,n){return r===0?P/n:P*r/(1-Math.pow(1+r,-n))}
function blEmp(g){var lo=Math.min(g,R.bl.low),hi=Math.max(0,Math.min(g,R.bl.max)-R.bl.low);return{bl:lo*R.bl.empBLlow+hi*R.bl.empBLhigh,h:lo*R.bl.empHlow+hi*R.bl.empHhigh}}
var C={
net:function(v){var g=v.gross,tax0=btax(g,R.taxM),cr=v.points*R.point,tax=Math.max(0,tax0-cr),b=blEmp(g),pen=g*v.pension/100,net=g-tax-b.bl-b.h-pen;
return big("שכר נטו משוער לחודש",ils(net),"מתוך ברוטו "+ils(g)+" · "+pc(net/g)+" מהברוטו")+tbl([["מס הכנסה (אחרי נקודות זיכוי)",ils(tax)],["ביטוח לאומי",ils(b.bl)],["ביטוח בריאות",ils(b.h)]].concat(pen?[["הפרשת עובד לפנסיה (כניכוי בלבד)",ils(pen)]]:[]),["רכיב","סכום לחודש"])+'<p class="meta">מס לפני זיכוי: '+ils(tax0)+" · שווי נקודות הזיכוי: "+ils(cr)+" · שיעור מס ממוצע: "+pc(tax/g)+"</p>"},
cpi:function(v){var a=R.cpi[v.from],b=R.cpi[v.to];if(!a||!b)return"";var out=v.amount*b/a,ch=b/a-1;
return big("הסכום אחרי הצמדה",ils(out),"שינוי של "+pc(ch)+" (מדד "+f2(a)+" ל-"+f2(b)+")")+tbl([["הסכום המקורי",ils(v.amount)],["הפרשי הצמדה",ils(out-v.amount)],["מדד בסיס (בסיס ממוצע 2024=100)",f2(a)],["מדד סיום",f2(b)]])+(a===b?"":"")},
vat:function(v){var r=v.rate/100,net,vat,gross;if(v.mode==="add"){net=v.amount;vat=net*r;gross=net+vat}else{gross=v.amount;net=gross/(1+r);vat=gross-net}
return big(v.mode==="add"?"הסכום כולל מע\"מ":"הסכום לפני מע\"מ",v.mode==="add"?f2(gross)+" ₪":f2(net)+" ₪","מע\"מ: "+f2(vat)+" ₪ ("+v.rate+"%)")+tbl([["לפני מע\"מ",f2(net)+" ₪"],["מע\"מ",f2(vat)+" ₪"],["כולל מע\"מ",f2(gross)+" ₪"]])},
sev:function(v){var ms=new Date(v.end)-new Date(v.start);if(!(ms>0))return warn("תאריך הסיום חייב להיות אחרי תאריך ההתחלה.");var yrs=ms/86400000/365.25,s=v.salary*yrs,ex=R.sevExempt*yrs;
return big("פיצויי פיטורים משוערים",ils(s),f2(yrs)+" שנות עבודה × שכר חודשי "+ils(v.salary))+tbl([["תקופת העבודה",f2(yrs)+" שנים"],["חישוב לפי סעיף 12(א): שכר חודש לכל שנת עבודה",ils(s)],["לידיעה: תקרת הפטור ממס לפי הלוח, 13,750 ₪ לשנת עבודה",ils(ex)]])+warn("זהו חישוב בסיסי למשכורת חודשית קבועה. הזכאות, הפקדות לפי סעיף 14, שכר משתנה וחישוב המס אינם נכללים.")},
ot:function(v){var thr=v.thr,tot125=0,tot150=0,tot=0;var h=v.hours,ot=Math.max(0,h-thr),a=Math.min(2,ot),b=Math.max(0,ot-2);var pay=v.rate*(a*1.25+b*1.5),day=v.rate*Math.min(h,thr)+pay;
var days=v.days;return big("תשלום בגין שעות נוספות בחודש",ils((pay)*days),f2(ot)+" שעות נוספות ביום × "+days+" ימים")+tbl([["שעות נוספות ב-125% ביום",f2(a)],["שעות נוספות ב-150% ביום",f2(b)],["תשלום על השעות הנוספות ביום",f2(a*v.rate*1.25+b*v.rate*1.5)+" ₪"],["שכר יומי כולל שעות נוספות",ils(day)],["שכר חודשי כולל שעות נוספות",ils(day*days)]])+(ot>4?warn("הדין אוסר העסקה ביותר מ-4 שעות נוספות ביום."):"")},
sh:function(v){var r=v.rate/100/12,n=v.years*12,p=pmt(v.amount,r,n);return mort(v,p,r,n)},
prime:function(v){var rate=v.prime+v.margin,r=rate/100/12,n=v.years*12,p=pmt(v.amount,r,n);var s1=pmt(v.amount,(rate+1)/100/12,n),s2=pmt(v.amount,(rate+2)/100/12,n);
return mort({amount:v.amount,rate:rate,years:v.years},p,r,n,"ריבית "+f2(rate)+"% (פריים "+f2(v.prime)+"% "+(v.margin>=0?"+":"")+f2(v.margin)+"%)")+tbl([["אם הפריים יעלה ב-1%",ils(s1)+" ("+(s1>p?"+":"")+f0(s1-p)+" ₪)"],["אם הפריים יעלה ב-2%",ils(s2)+" ("+(s2>p?"+":"")+f0(s2-p)+" ₪)"]],["תרחיש (החזר חודשי)","החזר חדש"])},
mcpi:function(v){var r=v.rate/100/12,n=v.years*12,im=Math.pow(1+v.infl/100,1/12)-1,B=v.amount,paid=0,first=pmt(B,r,n),rows=[];for(var m=1;m<=n;m++){B*=1+im;var p=pmt(B,r,n-m+1),i=B*r;B-=p-i;paid+=p;if(m%60===0||m===n)rows.push([m/12+" שנים",ils(p)])}
return big("החזר חודשי ראשון",ils(first),"סך תשלומים בהנחת מדד "+f2(v.infl)+"% בשנה: "+ils(paid))+tbl(rows,["אחרי","החזר חודשי"])+tbl([["סך התשלומים",ils(paid)],["סך הריבית וההצמדה",ils(paid-v.amount)]])+warn("זו הדגמה בהנחת אינפלציה קבועה. המדד בפועל משתנה.")},
op:function(v){var rev=v.rev*12,prof=Math.max(0,(v.rev-v.exp)*12),I=prof/12,bl=function(x){var lo=Math.min(x,R.bl.low),hi=Math.max(0,Math.min(x,R.bl.max)-R.bl.low);return{b:lo*R.bl.selfBLlow+hi*R.bl.selfBLhigh,h:lo*R.bl.selfHlow+hi*R.bl.selfHhigh}};
var base=I,i;for(i=0;i<8;i++){var t=bl(base);base=I-0.52*t.b}var x=bl(base),tax=Math.max(0,btax(prof,R.taxY)-v.points*R.point*12),net=prof-tax-(x.b+x.h)*12;
return big("הכנסה נטו משוערת לחודש",ils(net/12),"רווח לפני מס: "+ils(I)+" לחודש")+tbl([["מחזור שנתי",ils(rev)],["רווח שנתי",ils(prof)],["מס הכנסה שנתי",ils(tax)],["ביטוח לאומי ובריאות שנתי",ils((x.b+x.h)*12)],["נטו שנתי",ils(net)]])+(rev>R.osekCeil?warn("המחזור השנתי חורג מתקרת עוסק פטור ("+f0(R.osekCeil)+" ₪)."):"")+warn("הערכה גסה: אין בחישוב ניכוי הוצאות מוכרות מיוחדות, הפרשות לפנסיה, או ניכוי חלק מדמי הביטוח הלאומי במס.")},
fuel:function(v){var l=v.km*(v.trip==="2"?2:1)*v.l100/100,c=l*v.price;return big("עלות הדלק לנסיעה",f2(c)+" ₪",f2(l)+" ליטר × "+f2(v.price)+" ₪ לליטר")+tbl([["עלות לקילומטר",f2(c/(v.km*(v.trip==="2"?2:1)))+" ₪"],["מרחק כולל",f0(v.km*(v.trip==="2"?2:1))+" ק\"מ"]])},
ci:function(v){var r=Math.pow(1+v.rate/100,1/12)-1,B=v.p,dep=v.p,y=[];for(var m=1;m<=v.years*12;m++){B=B*(1+r)+v.m;dep+=v.m;if(m%12===0)y.push([m/12,ils(dep),ils(B)])}
return big("הסכום בסוף התקופה",ils(B),"הפקדות "+ils(dep)+" · רווח "+ils(B-dep))+tbl(y.filter(function(_,i,a){return a.length<=12||i%Math.ceil(a.length/10)===0||i===a.length-1}),["שנה","סך הפקדות","שווי"])}};
function mort(v,p,r,n,sub){var tot=p*n,B=v.amount,rows=[],ya=0,yi=0;for(var m=1;m<=n;m++){var i=B*r;B-=p-i;yi+=i;ya+=p-i;if(m%12===0||m===n){if((m/12)%5===0||m===n)rows.push([m/12,ils(Math.max(0,B))]);}}
return big("החזר חודשי",ils(p),sub||"ריבית "+f2(v.rate)+"% · "+v.years+" שנים")+tbl([["סכום ההלוואה",ils(v.amount)],["סך התשלומים",ils(tot)],["סך הריבית",ils(tot-v.amount)]])+tbl(rows,["אחרי שנים","יתרת קרן"])}
d.querySelectorAll("form.calc").forEach(function(f){var out=d.getElementById("out"),fn=C[f.dataset.calc];
function run(){var v={};f.querySelectorAll("input,select").forEach(function(e){v[e.name]=e.type==="number"?parseFloat(e.value)||0:e.value});try{out.innerHTML=fn(v)}catch(e){out.innerHTML=""}}
f.addEventListener("input",run);run()})})();
