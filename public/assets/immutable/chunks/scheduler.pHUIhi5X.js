function j(){}const lt=t=>t;function W(t,e){for(const n in e)t[n]=e[n];return t}function B(t){return t()}function at(){return Object.create(null)}function I(t){t.forEach(B)}function L(t){return typeof t=="function"}function ut(t,e){return t!=t?e==e:t!==e||t&&typeof t=="object"||typeof t=="function"}function ft(t){return Object.keys(t).length===0}function O(t,...e){if(t==null){for(const i of e)i(void 0);return j}const n=t.subscribe(...e);return n.unsubscribe?()=>n.unsubscribe():n}function _t(t){let e;return O(t,n=>e=n)(),e}function dt(t,e,n){t.$$.on_destroy.push(O(e,n))}function ht(t,e,n,i){if(t){const r=S(t,e,n,i);return t[0](r)}}function S(t,e,n,i){return t[1]&&i?W(n.ctx.slice(),t[1](i(e))):n.ctx}function mt(t,e,n,i){if(t[2]&&i){const r=t[2](i(n));if(e.dirty===void 0)return r;if(typeof r=="object"){const o=[],s=Math.max(e.dirty.length,r.length);for(let l=0;l<s;l+=1)o[l]=e.dirty[l]|r[l];return o}return e.dirty|r}return e.dirty}function pt(t,e,n,i,r,o){if(r){const s=S(e,n,i,o);t.p(s,r)}}function yt(t){if(t.ctx.length>32){const e=[],n=t.ctx.length/32;for(let i=0;i<n;i++)e[i]=-1;return e}return-1}function bt(t){const e={};for(const n in t)n[0]!=="$"&&(e[n]=t[n]);return e}function gt(t,e){const n={};e=new Set(e);for(const i in t)!e.has(i)&&i[0]!=="$"&&(n[i]=t[i]);return n}function wt(t,e,n){return t.set(n),e}function xt(t){return t&&L(t.destroy)?t.destroy:j}const q=["",!0,1,"true","contenteditable"];let y=!1;function vt(){y=!0}function kt(){y=!1}function H(t,e,n,i){for(;t<e;){const r=t+(e-t>>1);n(r)<=i?t=r+1:e=r}return t}function R(t){if(t.hydrate_init)return;t.hydrate_init=!0;let e=t.childNodes;if(t.nodeName==="HEAD"){const c=[];for(let a=0;a<e.length;a++){const u=e[a];u.claim_order!==void 0&&c.push(u)}e=c}const n=new Int32Array(e.length+1),i=new Int32Array(e.length);n[0]=-1;let r=0;for(let c=0;c<e.length;c++){const a=e[c].claim_order,u=(r>0&&e[n[r]].claim_order<=a?r+1:H(1,r,M=>e[n[M]].claim_order,a))-1;i[c]=n[u]+1;const N=u+1;n[N]=c,r=Math.max(N,r)}const o=[],s=[];let l=e.length-1;for(let c=n[r]+1;c!=0;c=i[c-1]){for(o.push(e[c-1]);l>=c;l--)s.push(e[l]);l--}for(;l>=0;l--)s.push(e[l]);o.reverse(),s.sort((c,a)=>c.claim_order-a.claim_order);for(let c=0,a=0;c<s.length;c++){for(;a<o.length&&s[c].claim_order>=o[a].claim_order;)a++;const u=a<o.length?o[a]:null;t.insertBefore(s[c],u)}}function D(t,e){t.appendChild(e)}function F(t){if(!t)return document;const e=t.getRootNode?t.getRootNode():t.ownerDocument;return e&&e.host?e:t.ownerDocument}function Et(t){const e=v("style");return e.textContent="/* empty */",U(F(t),e),e.sheet}function U(t,e){return D(t.head||t,e),e.sheet}function G(t,e){if(y){for(R(t),(t.actual_end_child===void 0||t.actual_end_child!==null&&t.actual_end_child.parentNode!==t)&&(t.actual_end_child=t.firstChild);t.actual_end_child!==null&&t.actual_end_child.claim_order===void 0;)t.actual_end_child=t.actual_end_child.nextSibling;e!==t.actual_end_child?(e.claim_order!==void 0||e.parentNode!==t)&&t.insertBefore(e,t.actual_end_child):t.actual_end_child=e.nextSibling}else(e.parentNode!==t||e.nextSibling!==null)&&t.appendChild(e)}function Nt(t,e,n){y&&!n?G(t,e):(e.parentNode!==t||e.nextSibling!=n)&&t.insertBefore(e,n||null)}function J(t){t.parentNode&&t.parentNode.removeChild(t)}function At(t,e){for(let n=0;n<t.length;n+=1)t[n]&&t[n].d(e)}function v(t){return document.createElement(t)}function K(t){return document.createElementNS("http://www.w3.org/2000/svg",t)}function k(t){return document.createTextNode(t)}function Ct(){return k(" ")}function jt(){return k("")}function A(t,e,n,i){return t.addEventListener(e,n,i),()=>t.removeEventListener(e,n,i)}function E(t,e,n){n==null?t.removeAttribute(e):t.getAttribute(e)!==n&&t.setAttribute(e,n)}const Q=["width","height"];function V(t,e){const n=Object.getOwnPropertyDescriptors(t.__proto__);for(const i in e)e[i]==null?t.removeAttribute(i):i==="style"?t.style.cssText=e[i]:i==="__value"?t.value=t[i]=e[i]:n[i]&&n[i].set&&Q.indexOf(i)===-1?t[i]=e[i]:E(t,i,e[i])}function Ot(t,e){for(const n in e)E(t,n,e[n])}function X(t,e){Object.keys(e).forEach(n=>{Y(t,n,e[n])})}function Y(t,e,n){const i=e.toLowerCase();i in t?t[i]=typeof t[i]=="boolean"&&n===""?!0:n:e in t?t[e]=typeof t[e]=="boolean"&&n===""?!0:n:E(t,e,n)}function St(t){return/-/.test(t)?X:V}function Dt(t){return t.dataset.svelteH}function zt(t){return Array.from(t.childNodes)}function Z(t){t.claim_info===void 0&&(t.claim_info={last_index:0,total_claimed:0})}function z(t,e,n,i,r=!1){Z(t);const o=(()=>{for(let s=t.claim_info.last_index;s<t.length;s++){const l=t[s];if(e(l)){const c=n(l);return c===void 0?t.splice(s,1):t[s]=c,r||(t.claim_info.last_index=s),l}}for(let s=t.claim_info.last_index-1;s>=0;s--){const l=t[s];if(e(l)){const c=n(l);return c===void 0?t.splice(s,1):t[s]=c,r?c===void 0&&t.claim_info.last_index--:t.claim_info.last_index=s,l}}return i()})();return o.claim_order=t.claim_info.total_claimed,t.claim_info.total_claimed+=1,o}function P(t,e,n,i){return z(t,r=>r.nodeName===e,r=>{const o=[];for(let s=0;s<r.attributes.length;s++){const l=r.attributes[s];n[l.name]||o.push(l.name)}o.forEach(s=>r.removeAttribute(s))},()=>i(e))}function Pt(t,e,n){return P(t,e,n,v)}function Tt(t,e,n){return P(t,e,n,K)}function $(t,e){return z(t,n=>n.nodeType===3,n=>{const i=""+e;if(n.data.startsWith(i)){if(n.data.length!==i.length)return n.splitText(i.length)}else n.data=i},()=>k(e),!0)}function Mt(t){return $(t," ")}function tt(t,e){e=""+e,t.data!==e&&(t.data=e)}function et(t,e){e=""+e,t.wholeText!==e&&(t.data=e)}function Wt(t,e,n){~q.indexOf(n)?et(t,e):tt(t,e)}function Bt(t,e){t.value=e??""}function It(t,e,n,i){n==null?t.style.removeProperty(e):t.style.setProperty(e,n,i?"important":"")}let m;function nt(){if(m===void 0){m=!1;try{typeof window<"u"&&window.parent&&window.parent.document}catch{m=!0}}return m}function Lt(t,e){getComputedStyle(t).position==="static"&&(t.style.position="relative");const i=v("iframe");i.setAttribute("style","display: block; position: absolute; top: 0; left: 0; width: 100%; height: 100%; overflow: hidden; border: 0; opacity: 0; pointer-events: none; z-index: -1;"),i.setAttribute("aria-hidden","true"),i.tabIndex=-1;const r=nt();let o;return r?(i.src="data:text/html,<script>onresize=function(){parent.postMessage(0,'*')}<\/script>",o=A(window,"message",s=>{s.source===i.contentWindow&&e()})):(i.src="about:blank",i.onload=()=>{o=A(i.contentWindow,"resize",e),e()}),D(t,i),()=>{(r||o&&i.contentWindow)&&o(),J(i)}}function it(t,e,{bubbles:n=!1,cancelable:i=!1}={}){return new CustomEvent(t,{detail:e,bubbles:n,cancelable:i})}function qt(t,e){return new t(e)}let p;function b(t){p=t}function d(){if(!p)throw new Error("Function called outside component initialization");return p}function Ht(t){d().$$.on_mount.push(t)}function Rt(t){d().$$.after_update.push(t)}function Ft(t){d().$$.on_destroy.push(t)}function Ut(){const t=d();return(e,n,{cancelable:i=!1}={})=>{const r=t.$$.callbacks[e];if(r){const o=it(e,n,{cancelable:i});return r.slice().forEach(s=>{s.call(t,o)}),!o.defaultPrevented}return!0}}function Gt(t,e){return d().$$.context.set(t,e),e}function Jt(t){return d().$$.context.get(t)}function Kt(t,e){const n=t.$$.callbacks[e.type];n&&n.slice().forEach(i=>i.call(this,e))}const h=[],C=[];let _=[];const w=[],T=Promise.resolve();let x=!1;function rt(){x||(x=!0,T.then(ct))}function Qt(){return rt(),T}function st(t){_.push(t)}function Vt(t){w.push(t)}const g=new Set;let f=0;function ct(){if(f!==0)return;const t=p;do{try{for(;f<h.length;){const e=h[f];f++,b(e),ot(e.$$)}}catch(e){throw h.length=0,f=0,e}for(b(null),h.length=0,f=0;C.length;)C.pop()();for(let e=0;e<_.length;e+=1){const n=_[e];g.has(n)||(g.add(n),n())}_.length=0}while(h.length);for(;w.length;)w.pop()();x=!1,g.clear(),b(t)}function ot(t){if(t.fragment!==null){t.update(),I(t.before_update);const e=t.dirty;t.dirty=[-1],t.fragment&&t.fragment.p(t.ctx,e),t.after_update.forEach(st)}}function Xt(t){const e=[],n=[];_.forEach(i=>t.indexOf(i)===-1?e.push(i):n.push(i)),n.forEach(i=>i()),_=e}export{Ft as $,It as A,C as B,qt as C,Qt as D,F as E,Et as F,st as G,it as H,lt as I,at as J,ct as K,ft as L,Xt as M,p as N,b as O,B as P,h as Q,rt as R,vt as S,kt as T,W as U,K as V,Tt as W,Ot as X,At as Y,gt as Z,bt as _,ut as a,_t as a0,Gt as a1,Jt as a2,wt as a3,V as a4,xt as a5,Wt as a6,Kt as a7,Bt as a8,A as a9,Vt as aa,Ut as ab,St as ac,Lt as ad,Ct as b,Pt as c,zt as d,v as e,$ as f,J as g,Mt as h,L as i,Nt as j,G as k,tt as l,dt as m,j as n,ht as o,Dt as p,E as q,I as r,O as s,k as t,pt as u,yt as v,mt as w,jt as x,Rt as y,Ht as z};