(function(){var d=document,r=d.documentElement;
var t=localStorage.getItem("theme");if(t)r.dataset.theme=t;
d.addEventListener("DOMContentLoaded",function(){
var b=d.getElementById("tbtn");if(b)b.onclick=function(){var n=r.dataset.theme==="dark"?"light":"dark";r.dataset.theme=n;localStorage.setItem("theme",n)};
var i=d.getElementById("q"),o=d.getElementById("sres"),idx=null;if(!i)return;
function load(c){if(idx)return c();fetch("/search.json").then(function(x){return x.json()}).then(function(j){idx=j;c()})}
function norm(s){return s.replace(/["'״׳,]/g,"").toLowerCase()}
i.addEventListener("input",function(){var q=norm(i.value.trim());if(q.length<2){o.style.display="none";return}
load(function(){var w=q.split(/\s+/),h=idx.filter(function(e){var s=norm(e.t+" "+e.k);return w.every(function(x){return s.indexOf(x)>-1})}).slice(0,7);
o.innerHTML=h.length?h.map(function(e){return '<a href="'+e.u+'">'+e.t+'<small>'+e.d+'</small></a>'}).join(""):'<a href="#">לא נמצאו תוצאות</a>';o.style.display="block"})});
i.addEventListener("keydown",function(e){if(e.key==="Enter"){var a=o.querySelector("a");if(a&&a.getAttribute("href")!=="#")location.href=a.href}if(e.key==="Escape")o.style.display="none"});
d.addEventListener("click",function(e){if(!e.target.closest(".sbox"))o.style.display="none"})})})();
