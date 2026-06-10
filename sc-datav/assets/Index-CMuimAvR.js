import{l as e,n as t,o as n,r,t as i}from"./styled-components.browser.esm-Ck8nA2i9.js";import{n as a}from"./index-BIZdDuW7.js";import{A as o,C as s,Cn as c,H as l,Ht as u,Jt as d,St as f,Tn as p,c as m,fn as h,n as g,s as _,t as v,u as y,w as b,wn as x,wt as S}from"./extends-DMrSfMvz.js";import{n as C,t as w}from"./constants-DZB49JWi.js";import{t as T}from"./Texture-9D4FxYDa.js";function E(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function D(e,t){return D=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},D(e,t)}function ee(){if(typeof Reflect>`u`||!Reflect.construct||Reflect.construct.sham)return!1;if(typeof Proxy==`function`)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],function(){})),!0}catch{return!1}}function O(e,t){(t==null||t>e.length)&&(t=e.length);for(var n=0,r=Array(t);n<t;n++)r[n]=e[n];return r}function te(e,t){if(e){if(typeof e==`string`)return O(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);if(n===`Object`&&e.constructor&&(n=e.constructor.name),n===`Map`||n===`Set`)return Array.from(e);if(n===`Arguments`||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return O(e,t)}}function ne(e){if(Array.isArray(e))return O(e)}function re(e){if(typeof Symbol<`u`&&e[Symbol.iterator]!=null||e[`@@iterator`]!=null)return Array.from(e)}function ie(){throw TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function ae(e){return ne(e)||re(e)||te(e)||ie()}new c,new c;function oe(e,t,n){return Math.max(t,Math.min(n,e))}function se(e,t){return oe(e-Math.floor(e/t)*t,0,t)}function ce(e,t){var n=se(t-e,Math.PI*2);return n>Math.PI&&(n-=Math.PI*2),n}function k(e,t){if(!(e instanceof t))throw TypeError(`Cannot call a class as a function`)}var A=function e(t,n,r){var i=this;k(this,e),E(this,`dot2`,function(e,t){return i.x*e+i.y*t}),E(this,`dot3`,function(e,t,n){return i.x*e+i.y*t+i.z*n}),this.x=t,this.y=n,this.z=r},le=[new A(1,1,0),new A(-1,1,0),new A(1,-1,0),new A(-1,-1,0),new A(1,0,1),new A(-1,0,1),new A(1,0,-1),new A(-1,0,-1),new A(0,1,1),new A(0,-1,1),new A(0,1,-1),new A(0,-1,-1)],ue=[151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168,68,175,74,165,71,134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,102,143,54,65,25,63,161,1,216,80,73,209,76,132,187,208,89,18,169,200,196,135,130,116,188,159,86,164,100,109,198,173,186,3,64,52,217,226,250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,223,183,170,213,119,248,152,2,44,154,163,70,221,153,101,155,167,43,172,9,129,22,39,253,19,98,108,110,79,113,224,232,178,185,112,104,218,246,97,228,251,34,242,193,238,210,144,12,191,179,162,241,81,51,145,235,249,14,239,107,49,192,214,31,181,199,106,157,184,84,204,176,115,121,50,45,127,4,150,254,138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180],de=Array(512),fe=Array(512);(function(e){e>0&&e<1&&(e*=65536),e=Math.floor(e),e<256&&(e|=e<<8);for(var t=0;t<256;t++){var n=t&1?ue[t]^e&255:ue[t]^e>>8&255;de[t]=de[t+256]=n,fe[t]=fe[t+256]=le[n%12]}})(0),.5*(Math.sqrt(3)-1),(3-Math.sqrt(3))/6,Math.PI*2;function pe(e){if(typeof e==`number`)e=Math.abs(e);else if(typeof e==`string`){var t=e;e=0;for(var n=0;n<t.length;n++)e=(e+(n+1)*(t.charCodeAt(n)%96))%2147483647}return e===0&&(e=311),e}function me(e){var t=pe(e);return function(){var e=t*48271%2147483647;return t=e,e/2147483647}}new function e(t){var n=this;k(this,e),E(this,`seed`,0),E(this,`init`,function(e){n.seed=e,n.value=me(e)}),E(this,`value`,me(this.seed)),this.init(t)}(Math.random());var he=function(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:.01,n=arguments.length>2&&arguments[2]!==void 0?arguments[2]:1,r=arguments.length>3&&arguments[3]!==void 0?arguments[3]:1/(2*Math.PI);return n/Math.atan(1/t)*Math.atan(Math.sin(2*Math.PI*e*r)/t)},ge=function(e){return 1/(1+e+.48*e*e+.235*e*e*e)},_e=function(e){return e},ve={in:function(e){return 1-Math.cos(e*Math.PI/2)},out:function(e){return Math.sin(e*Math.PI/2)},inOut:function(e){return-(Math.cos(Math.PI*e)-1)/2}},ye={in:function(e){return e*e*e},out:function(e){return 1-(1-e)**3},inOut:function(e){return e<.5?4*e*e*e:1-(-2*e+2)**3/2}},be={in:function(e){return e*e*e*e*e},out:function(e){return 1-(1-e)**5},inOut:function(e){return e<.5?16*e*e*e*e*e:1-(-2*e+2)**5/2}},xe={in:function(e){return 1-Math.sqrt(1-e**2)},out:function(e){return Math.sqrt(1-(e-1)**2)},inOut:function(e){return e<.5?(1-Math.sqrt(1-(2*e)**2))/2:(Math.sqrt(1-(-2*e+2)**2)+1)/2}},Se={in:function(e){return e*e*e*e},out:function(e){return 1- --e*e*e*e},inOut:function(e){return e<.5?8*e*e*e*e:1-8*--e*e*e*e}},Ce={in:function(e){return e===0?0:2**(10*e-10)},out:function(e){return e===1?1:1-2**(-10*e)},inOut:function(e){return e===0?0:e===1?1:e<.5?2**(20*e-10)/2:(2-2**(-20*e+10))/2}};function j(e,t,n){var r=arguments.length>3&&arguments[3]!==void 0?arguments[3]:.25,i=arguments.length>4&&arguments[4]!==void 0?arguments[4]:.01,a=arguments.length>5&&arguments[5]!==void 0?arguments[5]:1/0,o=arguments.length>6&&arguments[6]!==void 0?arguments[6]:ge,s=arguments.length>7&&arguments[7]!==void 0?arguments[7]:.001,c=`velocity_`+t;if(e.__damp===void 0&&(e.__damp={}),e.__damp[c]===void 0&&(e.__damp[c]=0),Math.abs(e[t]-n)<=s)return e[t]=n,!1;r=Math.max(1e-4,r);var l=2/r,u=o(l*i),d=e[t]-n,f=n,p=a*r;d=Math.min(Math.max(d,-p),p),n=e[t]-d;var m=(e.__damp[c]+l*d)*i;e.__damp[c]=(e.__damp[c]-l*m)*u;var h=n+(d+m)*u;return f-e[t]>0==h>f&&(h=f,e.__damp[c]=(h-f)/i),e[t]=h,!0}var we=function(e){return e&&e.isCamera},Te=function(e){return e&&e.isLight},M=new x,N=new d,P=new d,F=new S,I=new x;function Ee(e,t,n,r,i,a,o){typeof t==`number`?M.setScalar(t):Array.isArray(t)?M.set(t[0],t[1],t[2]):M.copy(t);var s=e.parent;e.updateWorldMatrix(!0,!1),I.setFromMatrixPosition(e.matrixWorld),we(e)||Te(e)?F.lookAt(I,M,e.up):F.lookAt(M,I,e.up),q(e.quaternion,P.setFromRotationMatrix(F),n,r,i,a,o),s&&(F.extractRotation(s.matrixWorld),N.setFromRotationMatrix(F),q(e.quaternion,P.copy(e.quaternion).premultiply(N.invert()),n,r,i,a,o))}function L(e,t,n,r,i,a,o,s){return j(e,t,e[t]+ce(e[t],n),r,i,a,o,s)}var R=new c,De,Oe;function ke(e,t,n,r,i,a,o){return typeof t==`number`?R.setScalar(t):Array.isArray(t)?R.set(t[0],t[1]):R.copy(t),De=j(e,`x`,R.x,n,r,i,a,o),Oe=j(e,`y`,R.y,n,r,i,a,o),De||Oe}var z=new x,Ae,je,Me;function B(e,t,n,r,i,a,o){return typeof t==`number`?z.setScalar(t):Array.isArray(t)?z.set(t[0],t[1],t[2]):z.copy(t),Ae=j(e,`x`,z.x,n,r,i,a,o),je=j(e,`y`,z.y,n,r,i,a,o),Me=j(e,`z`,z.z,n,r,i,a,o),Ae||je||Me}var V=new p,Ne,Pe,Fe,Ie;function Le(e,t,n,r,i,a,o){return typeof t==`number`?V.setScalar(t):Array.isArray(t)?V.set(t[0],t[1],t[2],t[3]):V.copy(t),Ne=j(e,`x`,V.x,n,r,i,a,o),Pe=j(e,`y`,V.y,n,r,i,a,o),Fe=j(e,`z`,V.z,n,r,i,a,o),Ie=j(e,`w`,V.w,n,r,i,a,o),Ne||Pe||Fe||Ie}var H=new l,Re,ze,Be;function Ve(e,t,n,r,i,a,o){return Array.isArray(t)?H.set(t[0],t[1],t[2],t[3]):H.copy(t),Re=L(e,`x`,H.x,n,r,i,a,o),ze=L(e,`y`,H.y,n,r,i,a,o),Be=L(e,`z`,H.z,n,r,i,a,o),Re||ze||Be}var U=new o,He,Ue,We;function Ge(e,t,n,r,i,a,s){return t instanceof o?U.copy(t):Array.isArray(t)?U.setRGB(t[0],t[1],t[2]):U.set(t),He=j(e,`r`,U.r,n,r,i,a,s),Ue=j(e,`g`,U.g,n,r,i,a,s),We=j(e,`b`,U.b,n,r,i,a,s),He||Ue||We}var W=new d,G=new p,Ke=new p,K=new p,qe,Je,Ye,Xe;function q(e,t,n,r,i,a,o){var s=e;Array.isArray(t)?W.set(t[0],t[1],t[2],t[3]):W.copy(t);var c=e.dot(W)>0?1:-1;return W.x*=c,W.y*=c,W.z*=c,W.w*=c,qe=j(e,`x`,W.x,n,r,i,a,o),Je=j(e,`y`,W.y,n,r,i,a,o),Ye=j(e,`z`,W.z,n,r,i,a,o),Xe=j(e,`w`,W.w,n,r,i,a,o),G.set(e.x,e.y,e.z,e.w).normalize(),Ke.set(s.__damp.velocity_x,s.__damp.velocity_y,s.__damp.velocity_z,s.__damp.velocity_w),K.copy(G).multiplyScalar(Ke.dot(G)/G.dot(G)),s.__damp.velocity_x-=K.x,s.__damp.velocity_y-=K.y,s.__damp.velocity_z-=K.z,s.__damp.velocity_w-=K.w,e.set(G.x,G.y,G.z,G.w),qe||Je||Ye||Xe}var J=new h,Ze,Qe,$e;function et(e,t,n,r,i,a,o){return Array.isArray(t)?J.set(t[0],t[1],t[2]):J.copy(t),Ze=j(e,`radius`,J.radius,n,r,i,a,o),Qe=L(e,`phi`,J.phi,n,r,i,a,o),$e=L(e,`theta`,J.theta,n,r,i,a,o),Ze||Qe||$e}var Y=new S,tt=new x,nt=new d,rt=new x,it,at,ot;function st(e,t,n,r,i,a,o){var s=e;return s.__damp===void 0&&(s.__damp={position:new x,rotation:new d,scale:new x},e.decompose(s.__damp.position,s.__damp.rotation,s.__damp.scale)),Array.isArray(t)?Y.set.apply(Y,ae(t)):Y.copy(t),Y.decompose(tt,nt,rt),it=B(s.__damp.position,tt,n,r,i,a,o),at=q(s.__damp.rotation,nt,n,r,i,a,o),ot=B(s.__damp.scale,rt,n,r,i,a,o),e.compose(s.__damp.position,s.__damp.rotation,s.__damp.scale),it||at||ot}var ct=Object.freeze({__proto__:null,rsqw:he,exp:ge,linear:_e,sine:ve,cubic:ye,quint:be,circ:xe,quart:Se,expo:Ce,damp:j,dampLookAt:Ee,dampAngle:L,damp2:ke,damp3:B,damp4:Le,dampE:Ve,dampC:Ge,dampQ:q,dampS:et,dampM:st});function lt(e,t){if(typeof t!=`function`&&t!==null)throw TypeError(`Super expression must either be null or a function`);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&D(e,t)}function X(e){return X=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},X(e)}function ut(e){if(e===void 0)throw ReferenceError(`this hasn't been initialised - super() hasn't been called`);return e}function dt(e,t){if(t&&(typeof t==`object`||typeof t==`function`))return t;if(t!==void 0)throw TypeError(`Derived constructors may only return object or undefined`);return ut(e)}function ft(e){var t=ee();return function(){var n=X(e),r;if(t){var i=X(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return dt(this,r)}}(function(e){lt(n,e);var t=ft(n);function n(){var e,r=arguments.length>0&&arguments[0]!==void 0?arguments[0]:2,i=arguments.length>1&&arguments[1]!==void 0?arguments[1]:1,a=arguments.length>2&&arguments[2]!==void 0?arguments[2]:.2,o=arguments.length>3&&arguments[3]!==void 0?arguments[3]:16;k(this,n),e=t.call(this),e.parameters={width:r,height:i,radius:a,segments:o};for(var c=r/2-a,l=i/2-a,u=a/r,d=(r-a)/r,f=a/i,p=(i-a)/i,m=[c,l,0,-c,l,0,-c,-l,0,c,-l,0],h=[d,p,u,p,u,f,d,f],g=[3*(o+1)+3,3*(o+1)+4,o+4,o+5,2*(o+1)+4,2,1,2*(o+1)+3,3,4*(o+1)+3,4,0],_=[g[0],g[1],g[2],g[0],g[2],g[3],g[4],g[5],g[6],g[4],g[6],g[7],g[8],g[9],g[10],g[8],g[10],g[11]],v,y,b,x,S,C,w,T,E=0;E<4;E++){x=E<1||E>2?c:-c,S=E<2?l:-l,C=E<1||E>2?d:u,w=E<2?p:f;for(var D=0;D<=o;D++)v=Math.PI/2*(E+D/o),y=Math.cos(v),b=Math.sin(v),m.push(x+a*y,S+a*b,0),h.push(C+u*y,w+f*b),D<o&&(T=(o+1)*E+D+4,_.push(E,T,T+1))}return e.setIndex(new s(new Uint32Array(_),1)),e.setAttribute(`position`,new s(new Float32Array(m),3)),e.setAttribute(`uv`,new s(new Float32Array(h),2)),e}return n})(b);var Z=e(n());e(r());var Q=Z.createContext(null);function pt(){return Z.useContext(Q)}function mt({eps:e=1e-5,enabled:t=!0,infinite:n,horizontal:r,pages:i=1,distance:a=1,damping:o=.25,maxSpeed:s=1/0,prepend:c=!1,style:l={},children:u}){let{get:d,setEvents:f,gl:p,size:h,invalidate:g,events:_}=y(),[v]=Z.useState(()=>document.createElement(`div`)),[b]=Z.useState(()=>document.createElement(`div`)),[x]=Z.useState(()=>document.createElement(`div`)),S=p.domElement.parentNode,C=Z.useRef(0),w=Z.useMemo(()=>({el:v,eps:e,fill:b,fixed:x,horizontal:r,damping:o,offset:0,delta:0,scroll:C,pages:i,range(e,t,n=0){let r=e-n,i=r+t+n*2;return this.offset<r?0:this.offset>i?1:(this.offset-r)/(i-r)},curve(e,t,n=0){return Math.sin(this.range(e,t,n)*Math.PI)},visible(e,t,n=0){let r=e-n,i=r+t+n*2;return this.offset>=r&&this.offset<=i}}),[e,o,r,i]);Z.useEffect(()=>{v.style.position=`absolute`,v.style.width=`100%`,v.style.height=`100%`,v.style[r?`overflowX`:`overflowY`]=`auto`,v.style[r?`overflowY`:`overflowX`]=`hidden`,v.style.top=`0px`,v.style.left=`0px`;for(let e in l)v.style[e]=l[e];x.style.position=`sticky`,x.style.top=`0px`,x.style.left=`0px`,x.style.width=`100%`,x.style.height=`100%`,x.style.overflow=`hidden`,v.appendChild(x),b.style.height=r?`100%`:`${i*a*100}%`,b.style.width=r?`${i*a*100}%`:`100%`,b.style.pointerEvents=`none`,v.appendChild(b),c?S.prepend(v):S.appendChild(v),v[r?`scrollLeft`:`scrollTop`]=1;let e=_.connected||p.domElement;requestAnimationFrame(()=>_.connect==null?void 0:_.connect(v));let t=d().events.compute;return f({compute(e,t){let{left:n,top:r}=S.getBoundingClientRect(),i=e.clientX-n,a=e.clientY-r;t.pointer.set(i/t.size.width*2-1,-(a/t.size.height)*2+1),t.raycaster.setFromCamera(t.pointer,t.camera)}}),()=>{S.removeChild(v),f({compute:t}),_.connect==null||_.connect(e)}},[i,a,r,v,b,x,S]),Z.useEffect(()=>{if(_.connected===v){let e=h[r?`width`:`height`],i=v[r?`scrollWidth`:`scrollHeight`],a=i-e,o=0,s=!0,c=!0,l=()=>{if(!(!t||c)&&(g(),o=v[r?`scrollLeft`:`scrollTop`],C.current=o/a,n)){if(!s){if(o>=a){let e=1-w.offset;v[r?`scrollLeft`:`scrollTop`]=1,C.current=w.offset=-e,s=!0}else if(o<=0){let e=1+w.offset;v[r?`scrollLeft`:`scrollTop`]=i,C.current=w.offset=e,s=!0}}s&&setTimeout(()=>s=!1,40)}};v.addEventListener(`scroll`,l,{passive:!0}),requestAnimationFrame(()=>c=!1);let u=e=>v.scrollLeft+=e.deltaY/2;return r&&v.addEventListener(`wheel`,u,{passive:!0}),()=>{v.removeEventListener(`scroll`,l),r&&v.removeEventListener(`wheel`,u)}}},[v,_,h,n,w,g,r,t]);let T=0;return m((t,n)=>{T=w.offset,ct.damp(w,`offset`,C.current,o,n,s,void 0,e),ct.damp(w,`delta`,Math.abs(T-w.offset),o,n,s,void 0,e),w.delta>e&&g()}),Z.createElement(Q.Provider,{value:w},u)}var ht=C({color:new o(`white`),scale:new c(1,1),imageBounds:new c(1,1),resolution:1024,map:null,zoom:1,radius:0,grayscale:0,opacity:1},`
  varying vec2 vUv;
  varying vec2 vPos;
  void main() {
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.);
    vUv = uv;
    vPos = position.xy;
  }
`,`
  // mostly from https://gist.github.com/statico/df64c5d167362ecf7b34fca0b1459a44
  varying vec2 vUv;
  varying vec2 vPos;
  uniform vec2 scale;
  uniform vec2 imageBounds;
  uniform float resolution;
  uniform vec3 color;
  uniform sampler2D map;
  uniform float radius;
  uniform float zoom;
  uniform float grayscale;
  uniform float opacity;
  const vec3 luma = vec3(.299, 0.587, 0.114);
  vec4 toGrayscale(vec4 color, float intensity) {
    return vec4(mix(color.rgb, vec3(dot(color.rgb, luma)), intensity), color.a);
  }
  vec2 aspect(vec2 size) {
    return size / min(size.x, size.y);
  }
  
  const float PI = 3.14159265;
    
  // from https://iquilezles.org/articles/distfunctions
  float udRoundBox( vec2 p, vec2 b, float r ) {
    return length(max(abs(p)-b+r,0.0))-r;
  }

  void main() {
    vec2 s = aspect(scale);
    vec2 i = aspect(imageBounds);
    float rs = s.x / s.y;
    float ri = i.x / i.y;
    vec2 new = rs < ri ? vec2(i.x * s.y / i.y, s.y) : vec2(s.x, i.y * s.x / i.x);
    vec2 offset = (rs < ri ? vec2((new.x - s.x) / 2.0, 0.0) : vec2(0.0, (new.y - s.y) / 2.0)) / new;
    vec2 uv = vUv * s / new + offset;
    vec2 zUv = (uv - vec2(0.5, 0.5)) / zoom + vec2(0.5, 0.5);

    vec2 res = vec2(scale * resolution);
    vec2 halfRes = 0.5 * res;
    float b = udRoundBox(vUv.xy * res - halfRes, halfRes, resolution * radius);    
	  vec3 a = mix(vec3(1.0,0.0,0.0), vec3(0.0,0.0,0.0), smoothstep(0.0, 1.0, b));
    gl_FragColor = toGrayscale(texture2D(map, zUv) * vec4(color, opacity * a), grayscale);
    
    #include <tonemapping_fragment>
    #include <${w>=154?`colorspace_fragment`:`encodings_fragment`}>
  }
`),gt=Z.forwardRef(({children:e,color:t,segments:n=1,scale:r=1,zoom:i=1,grayscale:a=0,opacity:o=1,radius:s=0,texture:c,toneMapped:l,transparent:u,side:d,...f},p)=>{_({ImageMaterial:ht});let m=Z.useRef(null),h=y(e=>e.size),g=Array.isArray(r)?[r[0],r[1]]:[r,r],b=[c.image.width,c.image.height],x=Math.max(h.width,h.height);return Z.useImperativeHandle(p,()=>m.current,[]),Z.useLayoutEffect(()=>{m.current.geometry.parameters&&m.current.material.scale.set(g[0]*m.current.geometry.parameters.width,g[1]*m.current.geometry.parameters.height)},[g[0],g[1]]),Z.createElement(`mesh`,v({ref:m,scale:Array.isArray(r)?[...r,1]:r},f),Z.createElement(`planeGeometry`,{args:[1,1,n,n]}),Z.createElement(`imageMaterial`,{color:t,map:c,zoom:i,grayscale:a,opacity:o,scale:g,imageBounds:b,resolution:x,radius:s,toneMapped:l,transparent:u,side:d,key:ht.key}),e)}),_t=Z.forwardRef(({url:e,...t},n)=>{let r=T(e);return Z.createElement(gt,v({},t,{texture:r,ref:n}))}),vt=Z.forwardRef(({url:e,...t},n)=>Z.createElement(gt,v({},t,{ref:n}))),yt=Z.forwardRef((e,t)=>{if(e.url)return Z.createElement(_t,v({},e,{ref:t}));if(e.texture)return Z.createElement(vt,v({},e,{ref:t}));throw Error(`<Image /> requires a url or texture`)}),$=t(),bt=_(C({u_time:0,u_resolution:new p,u_aspect:0,u_noiseFreq:0,blur:0,speed:0},` varying vec2 vUv;
    uniform float u_time;
    uniform float u_noiseFreq;

    
vec3 mod289(vec3 x) {
  return x - floor(x * (1.0 / 289.0)) * 289.0;
}

vec4 mod289(vec4 x) {
  return x - floor(x * (1.0 / 289.0)) * 289.0;
}

vec4 permute(vec4 x) {
     return mod289(((x*34.0)+1.0)*x);
}

vec4 taylorInvSqrt(vec4 r)
{
  return 1.79284291400159 - 0.85373472095314 * r;
}


 float snoise(vec3 v) {
  const vec2  C = vec2(1.0/6.0, 1.0/3.0) ;
  const vec4  D = vec4(0.0, 0.5, 1.0, 2.0);
  
  // First corner
  vec3 i  = floor(v + dot(v, C.yyy) );
  vec3 x0 =   v - i + dot(i, C.xxx) ;
  
  // Other corners
  vec3 g = step(x0.yzx, x0.xyz);
  vec3 l = 1.0 - g;
  vec3 i1 = min( g.xyz, l.zxy );
  vec3 i2 = max( g.xyz, l.zxy );

  //   x0 = x0 - 0.0 + 0.0 * C.xxx;
  //   x1 = x0 - i1  + 1.0 * C.xxx;
  //   x2 = x0 - i2  + 2.0 * C.xxx;
  //   x3 = x0 - 1.0 + 3.0 * C.xxx;
  vec3 x1 = x0 - i1 + C.xxx;
  vec3 x2 = x0 - i2 + C.yyy; // 2.0*C.x = 1/3 = C.y
  vec3 x3 = x0 - D.yyy;      // -1.0+3.0*C.x = -0.5 = -D.y
  
  // Permutations
  i = mod289(i);
  vec4 p = permute( permute( permute(
             i.z + vec4(0.0, i1.z, i2.z, 1.0 ))
           + i.y + vec4(0.0, i1.y, i2.y, 1.0 ))
           + i.x + vec4(0.0, i1.x, i2.x, 1.0 ));
           
  // Gradients: 7x7 points over a square, mapped onto an octahedron.
  // The ring size 17*17 = 289 is close to a multiple of 49 (49*6 = 294)
  float n_ = 0.142857142857; // 1.0/7.0
  vec3  ns = n_ * D.wyz - D.xzx;

  vec4 j = p - 49.0 * floor(p * ns.z * ns.z);  //  mod(p,7*7)

  vec4 x_ = floor(j * ns.z);
  vec4 y_ = floor(j - 7.0 * x_ );    // mod(j,N)

  vec4 x = x_ *ns.x + ns.yyyy;
  vec4 y = y_ *ns.x + ns.yyyy;
  vec4 h = 1.0 - abs(x) - abs(y);

  vec4 b0 = vec4( x.xy, y.xy );
  vec4 b1 = vec4( x.zw, y.zw );

  //vec4 s0 = vec4(lessThan(b0,0.0))*2.0 - 1.0;
  //vec4 s1 = vec4(lessThan(b1,0.0))*2.0 - 1.0;
  vec4 s0 = floor(b0)*2.0 + 1.0;
  vec4 s1 = floor(b1)*2.0 + 1.0;
  vec4 sh = -step(h, vec4(0.0));

  vec4 a0 = b0.xzyw + s0.xzyw*sh.xxyy ;
  vec4 a1 = b1.xzyw + s1.xzyw*sh.zzww ;

  vec3 p0 = vec3(a0.xy,h.x);
  vec3 p1 = vec3(a0.zw,h.y);
  vec3 p2 = vec3(a1.xy,h.z);
  vec3 p3 = vec3(a1.zw,h.w);
  
  // Normalise gradients
  vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2, p2), dot(p3,p3)));
  p0 *= norm.x;
  p1 *= norm.y;
  p2 *= norm.z;
  p3 *= norm.w;
  
  // Mix final noise value
  vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
  m = m * m;
  return 42.0 * dot( m*m, vec4( dot(p0,x0), dot(p1,x1),
                                dot(p2,x2), dot(p3,x3) ) );
}

 void main() {
   vUv = uv;

   vec3 pos = position;
   float noiseFreq = 10.5;
   float noiseAmp = 1.5; 
   vec3 noisePos = vec3(pos.x + u_time, pos.y, pos.z);
   pos.z += snoise(noisePos) * u_noiseFreq;

   gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0 );
 }`,`varying vec2 vUv;
    uniform float u_time;
    uniform float u_aspect;


float hue2rgb(float f1, float f2, float hue) {
    if (hue < 0.0)
        hue += 1.0;
    else if (hue > 1.0)
        hue -= 1.0;
    float res;
    if ((6.0 * hue) < 1.0)
        res = f1 + (f2 - f1) * 6.0 * hue;
    else if ((2.0 * hue) < 1.0)
        res = f2;
    else if ((3.0 * hue) < 2.0)
        res = f1 + (f2 - f1) * ((2.0 / 3.0) - hue) * 6.0;
    else
        res = f1;
    return res;
}

vec3 hsl2rgb(vec3 hsl) {
    vec3 rgb;
    
    if (hsl.y == 0.0) {
        rgb = vec3(hsl.z); // Luminance
    } else {
        float f2;
        
        if (hsl.z < 0.5)
            f2 = hsl.z * (1.0 + hsl.y);
        else
            f2 = hsl.z + hsl.y - hsl.y * hsl.z;
            
        float f1 = 2.0 * hsl.z - f2;
        
        rgb.r = hue2rgb(f1, f2, hsl.x + (1.0/3.0));
        rgb.g = hue2rgb(f1, f2, hsl.x);
        rgb.b = hue2rgb(f1, f2, hsl.x - (1.0/3.0));
    }   
    return rgb;
}

vec3 hsl2rgb(float h, float s, float l) {
    return hsl2rgb(vec3(h, s, l));
}

vec3 random3(vec3 c) {
	float j = 4096.0*sin(dot(c,vec3(17.0, 59.4, 15.0)));
	vec3 r;
	r.z = fract(512.0*j);
	j *= .125;
	r.x = fract(512.0*j);
	j *= .125;
	r.y = fract(512.0*j);
	return r-0.5;
}

const float F3 =  0.3333333;
const float G3 =  0.1666667;

float simplex3d(vec3 p) {
	 vec3 s = floor(p + dot(p, vec3(F3)));
	 vec3 x = p - s + dot(s, vec3(G3));
	 
	 vec3 e = step(vec3(0.0), x - x.yzx);
	 vec3 i1 = e*(1.0 - e.zxy);
	 vec3 i2 = 1.0 - e.zxy*(1.0 - e);
	 	
	 vec3 x1 = x - i1 + G3;
	 vec3 x2 = x - i2 + 2.0*G3;
	 vec3 x3 = x - 1.0 + 3.0*G3;
	 
	 vec4 w, d;
	 
	 w.x = dot(x, x);
	 w.y = dot(x1, x1);
	 w.z = dot(x2, x2);
	 w.w = dot(x3, x3);
	 
	 w = max(0.6 - w, 0.0);
	 
	 d.x = dot(random3(s), x);
	 d.y = dot(random3(s + i1), x1);
	 d.z = dot(random3(s + i2), x2);
	 d.w = dot(random3(s + 1.0), x3);
	 
	 w *= w;
	 w *= w;
	 d *= w;
	 
	 return dot(d, vec4(52.0));
}

float hash(vec2 p) { return fract(1e4 * sin(17.0 * p.x + p.y * 0.1) * (0.1 + abs(sin(p.y * 13.0 + p.x)))); }

uniform float blur;
uniform float speed;

    
void main() {

    vec2 center = vUv - 0.5;
	float dist = length(center);
    float alpha = smoothstep(0.5, blur, dist);
    float n = simplex3d(vec3(vUv.xy, u_time * speed));

    vec3 color = hsl2rgb(
        0.6 + n * 0.2,
        0.5,
        0.5
    );

    float val = hash(vUv + u_time);

	gl_FragColor = vec4(color + vec3(val / 20.), alpha);
}`));function xt(){let e=y(),t=(0,Z.useRef)(null);return m(e=>{t.current.uniforms.u_time.value=e.clock.getElapsedTime()}),(0,$.jsx)(`group`,{position:[0,-3,-10],children:(0,$.jsxs)(`mesh`,{children:[(0,$.jsx)(`planeGeometry`,{args:[6,6,16,16]}),(0,$.jsx)(bt,{transparent:!0,ref:t,wireframe:!1,u_aspect:e.viewport.aspect,blur:0,speed:.5,u_noiseFreq:1})]})})}var St=i.div`
  position: relative;
  width: 100vw;
  height: 100vh;
`,Ct=_(class extends u{constructor(e,t,n,r,i){super(t,n,r,i);let a=this.parameters.width*.5,o=new c(-a,0),s=new c(0,e),l=new c(a,0),u=new c().subVectors(o,s),d=new c().subVectors(s,l),f=new c().subVectors(o,l),p=new c(0,e-u.length()*d.length()*f.length()/(2*Math.abs(u.cross(f)))),m=(new c().subVectors(o,p).angle()-Math.PI*.5)*2,h=this.attributes.uv,g=this.attributes.position,_=new c;for(let e=0;e<h.count;e++){let t=h.getX(e),n=g.getY(e);_.copy(l).rotateAround(p,m*t),g.setXYZ(e,_.x,n,-_.y)}g.needsUpdate=!0}}),wt=i.div`
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0.6;
`,Tt=i.circle`
  @keyframes scroll-drop {
    0% {
      transform: translateY(0);
      opacity: 1;
    }
    100% {
      transform: translateY(15px);
      opacity: 0;
    }
  }

  animation: scroll-drop 1.5s ease-in-out infinite;
`;function Et(){return(0,$.jsxs)(St,{children:[(0,$.jsxs)(g,{camera:{position:[0,0,100],fov:15},children:[(0,$.jsx)(`fog`,{attach:`fog`,args:[`#6e6e6e`,8.5,12]}),(0,$.jsx)(mt,{pages:4,infinite:!0,children:(0,$.jsx)(Dt,{rotation:[0,0,.15],children:(0,$.jsx)(Ot,{})})}),(0,$.jsx)(xt,{})]}),(0,$.jsx)(wt,{children:(0,$.jsxs)(`svg`,{width:`20`,height:`32.5`,viewBox:`0 0 40 65`,children:[(0,$.jsx)(`rect`,{x:`2.5`,y:`2.5`,width:`35`,height:`60`,rx:`17.5`,ry:`17.5`,fill:`none`,stroke:`currentColor`,strokeWidth:`3`}),(0,$.jsx)(Tt,{cx:`20`,cy:`15`,r:`3`,fill:`currentColor`})]})})]})}function Dt(e){let t=(0,Z.useRef)(null),n=pt(),r=(0,Z.useRef)(new x(1,1,1));return m((e,i)=>{t.current.rotation.y=-n.offset*(Math.PI*2),e.events.update?.(),r.current.set(-e.pointer.x*2,e.pointer.y+1.5,10),e.camera.position.lerp(r.current,1-Math.exp(-8*i)),e.camera.lookAt(0,0,0)}),(0,$.jsx)(`group`,{ref:t,...e})}function Ot({radius:e=1.4,count:t=8}){let n=a();return Array.from({length:t},(r,i)=>(0,$.jsx)(kt,{url:`/sc-datav/demo_${i%4}.jpg`,position:[Math.sin(i/t*Math.PI*2)*e,0,Math.cos(i/t*Math.PI*2)*e],rotation:[0,Math.PI+i/t*Math.PI*2,0],onClick:e=>{e.stopPropagation(),n([`/demo0`,`/demo1`,`/demo2`,`/demo3`][i%4])}},i))}function kt(e){let t=(0,Z.useRef)(null),n=(0,Z.useRef)(new x(1,1,1)),r=(0,Z.useRef)(.1),i=(0,Z.useRef)(1.5);return m((e,a)=>{t.current.scale.lerp(n.current,1-Math.exp(-10*a)),t.current.material.radius=f.lerp(t.current.material.radius,r.current,1-Math.exp(-8*a)),t.current.material.zoom=f.lerp(t.current.material.zoom,i.current,1-Math.exp(-8*a))}),(0,$.jsx)(yt,{ref:t,transparent:!0,toneMapped:!1,side:2,onPointerOver:e=>{e.stopPropagation(),n.current.setScalar(1.15),r.current=.25,i.current=1,document.body.style.cursor=`pointer`},onPointerOut:()=>{n.current.setScalar(1),r.current=.1,i.current=1.5,document.body.style.cursor=`auto`},...e,children:(0,$.jsx)(Ct,{args:[.1,1,1,20,20]})})}export{Et as default};