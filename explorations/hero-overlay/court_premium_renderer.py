#!/usr/bin/env python3
"""Premium render of the geometrically-exact padel court (from padel_court
geometry) + neural-net + smash tracking. World frame: origin at net centre,
X=length (net at 0, +/-10), Y=width (+/-5), Z up. Metres."""
import numpy as np, math

HL, HW, SL = 10.0, 5.0, 6.95
NET_C, NET_P, POST_OUT = 0.88, 0.92, 0.5
GLASS = 3.0

EYE = np.array([-15.5, -1.6, 9.2]); TGT = np.array([1.2, 0.0, 0.4]); UP = np.array([0.,0.,1.])
F, SCALE, CX, CY = 1.55, 43.0, 50.0, 40.0
fwd = TGT-EYE; fwd/=np.linalg.norm(fwd)
right = np.cross(fwd,UP); right/=np.linalg.norm(right); tup = np.cross(right,fwd)
def proj(p):
    d=np.asarray(p,float)-EYE; xc,yc,zc=d@right,d@tup,d@fwd
    zc=max(zc,0.05); return (CX+F*xc/zc*SCALE, CY-F*yc/zc*SCALE)
def P(*pts): return [proj(p) for p in pts]
def ptsstr(pl): return " ".join(f"{x:.2f},{y:.2f}" for x,y in pl)
def poly(pl,**k): return f'<polygon points="{ptsstr(pl)}" '+" ".join(f'{a.replace("_","-")}="{v}"' for a,v in k.items())+'/>'
def line(a,b,**k):
    (x1,y1),(x2,y2)=proj(a),proj(b); return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '+" ".join(f'{p.replace("_","-")}="{v}"' for p,v in k.items())+'/>'

L=[]  # layers
# ---- floodlight glows (soft) ----
for fx in (-7,-2.5,2,6,9):
    px,py=proj((fx,0,7.5))
    L.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7" fill="url(#flood)"/>')

# ---- glass side + back walls (gradient + bright edges + reflection streak) ----
def wall(a,b,h,op):
    (ax,ay),(bx,by)=proj((*a,0)),proj((*b,0)); (cx2,cy2),(dx,dy)=proj((*b,h)),proj((*a,h))
    p=[(ax,ay),(bx,by),(cx2,cy2),(dx,dy)]
    s=poly(p,fill="url(#glass)",fill_opacity=f"{op}",stroke="#5B7FB0",stroke_width="0.28",stroke_opacity="0.7")
    # reflection streak
    mx1=ax+(bx-ax)*0.15; my1=ay+(by-ay)*0.15
    return s
for sy in (HW,-HW): L.append(wall((-HL,sy),(HL,sy),GLASS,0.10))
for sx in (HL,-HL): L.append(wall((sx,-HW),(sx,HW),GLASS,0.14))
# bright top rail of glass
for sy in (HW,-HW): L.append(line((-HL,sy,GLASS),(HL,sy,GLASS),stroke="#7FA8DC",stroke_width="0.3",stroke_opacity="0.55"))
for sx in (HL,-HL): L.append(line((sx,-HW,GLASS),(sx,HW,GLASS),stroke="#7FA8DC",stroke_width="0.35",stroke_opacity="0.6"))

# ---- court floor: gradient + sheen ----
floor=P((-HL,-HW,0),(HL,-HW,0),(HL,HW,0),(-HL,HW,0))
L.append(poly(floor,fill="url(#court)"))
# elliptical light sheen on the court
sx0,sy0=proj((-3,0,0)); L.append(f'<ellipse cx="{sx0:.1f}" cy="{sy0:.1f}" rx="34" ry="12" fill="url(#sheen)" opacity="0.5"/>')
# subtle vignette
L.append(poly(floor,fill="url(#vign)"))

# ---- floor reflection of the net (premium wet look), drawn faint UNDER lines ----
refl=[]
refl.append(line((0,-HW,-NET_C),(0,HW,-NET_C),stroke="#FFFFFF",stroke_width="0.5",stroke_opacity="0.10"))
for i in range(1,10):
    y=-HW+i*(2*HW/10); refl.append(line((0,y,0),(0,y,-NET_C),stroke="#9FC0E8",stroke_width="0.13",stroke_opacity="0.08"))
L+=refl

# ---- court lines (glow + crisp) ----
def cline(a,b,w=0.5):
    return (line(a,b,stroke="#BFE0FF",stroke_width=f"{w*3}",stroke_opacity="0.18")
            + line(a,b,stroke="#FFFFFF",stroke_width=f"{w}",stroke_opacity="0.95"))
segs=[((-HL,-HW,0),(HL,-HW,0)),((HL,-HW,0),(HL,HW,0)),((HL,HW,0),(-HL,HW,0)),((-HL,HW,0),(-HL,-HW,0)),
      ((SL,-HW,0),(SL,HW,0)),((-SL,-HW,0),(-SL,HW,0)),((-SL,0,0),(SL,0,0))]
for a,b in segs: L.append(cline(a,b))

# ---- net: mesh + white band + posts (with glow) ----
L.append(poly(P((0,-HW,0),(0,HW,0),(0,HW,NET_C),(0,-HW,NET_C)),fill="#0B1426",fill_opacity="0.28"))
for i in range(1,20):
    y=-HW+i*(2*HW/20); L.append(line((0,y,0),(0,y,NET_C),stroke="#8FB2DC",stroke_width="0.1",stroke_opacity="0.3"))
for zf in (0.33,0.66):
    L.append(line((0,-HW,NET_C*zf),(0,HW,NET_C*zf),stroke="#8FB2DC",stroke_width="0.1",stroke_opacity="0.25"))
L.append(line((0,-HW,NET_C),(0,HW,NET_C),stroke="#DBEBFF",stroke_width="1.6",stroke_opacity="0.22"))
L.append(line((0,-HW,NET_C),(0,HW,NET_C),stroke="#FFFFFF",stroke_width="0.65",stroke_opacity="0.95"))
for sy in (HW+POST_OUT,-(HW+POST_OUT)): L.append(line((0,sy,0),(0,sy,NET_P),stroke="#22304A",stroke_width="0.7",stroke_opacity="0.9"))

# =================== AI OVERLAY ===================
CY_,YEL,INK="#42A5F5","#FDD835","#0B1320"; O=[]
mesh_world=[(-HL,HW,0),(-HL,-HW,0),(HL,-HW,0),(HL,HW,0),(0,HW,0),(0,-HW,0),(0,0,0),
            (-SL,HW,0),(-SL,-HW,0),(SL,-HW,0),(SL,HW,0),(-SL,0,0),(SL,0,0),(-5,0,0),(5,0,0)]
mp=[proj(p) for p in mesh_world]; E=set()
for i,a in enumerate(mp):
    for j in sorted(range(len(mp)),key=lambda k:(mp[k][0]-a[0])**2+(mp[k][1]-a[1])**2)[1:4]: E.add(tuple(sorted((i,j))))
for i,j in E: O.append(f'<line x1="{mp[i][0]:.2f}" y1="{mp[i][1]:.2f}" x2="{mp[j][0]:.2f}" y2="{mp[j][1]:.2f}" stroke="{CY_}" stroke-width="0.2" opacity="0.4"/>')
for x,y in mp: O.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="1.6" fill="{CY_}" opacity="0.22" filter="url(#soft)"/><circle cx="{x:.2f}" cy="{y:.2f}" r="0.6" fill="#BFE6FF"/>')
# smash: contact high near net -> bounce side B -> up over far mesh
A=np.array([-1.,1.,2.6]);B=np.array([4.,1.5,0.05]);C=np.array([10.7,2.,4.5])
def seg(p,q,n,z=0.):
    o=[]
    for k in range(n+1):
        t=k/n; pt=p+(q-p)*t; pt=pt.copy(); pt[2]+=z*math.sin(math.pi*t); o.append(proj(pt))
    return o
for x,y in seg(A,B,7,0.6)+seg(B,C,7): O.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="0.8" fill="{YEL}" filter="url(#softy)"/>')
bx,by=proj(B); O.append(f'<circle cx="{bx:.2f}" cy="{by:.2f}" r="2.0" fill="none" stroke="{YEL}" stroke-width="0.4"/><circle cx="{bx:.2f}" cy="{by:.2f}" r="0.85" fill="{YEL}"/><text x="{bx+2.6:.2f}" y="{by+0.8:.2f}" fill="{YEL}" font-family="Roboto Mono,monospace" font-size="1.9" font-weight="700">BOUNCE</text>')
cx3,cy3=proj(C); O.append(f'<circle cx="{cx3:.2f}" cy="{cy3:.2f}" r="1.6" fill="{YEL}" stroke="{INK}" stroke-width="0.3" filter="url(#softy)"/>')
for dx,dy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
    O.append(f'<path d="M {cx3+dx*4.2:.2f} {cy3+dy*2.8:.2f} v {dy*1.5:.2f} h {dx*1.5:.2f}" stroke="{CY_}" stroke-width="0.6" fill="none"/>')
O.append(f'<g transform="translate(6,10)"><rect x="0" y="-3" width="27" height="4.4" rx="1" fill="{INK}" opacity="0.92"/><circle cx="2.4" cy="-0.8" r="0.9" fill="{YEL}"/><text x="4.6" y="0.2" fill="#fff" font-family="Roboto Mono,monospace" font-size="2.2" font-weight="700">SMASH · 200 km/h</text></g>')

defs=('<defs>'
 '<radialGradient id="bg" cx="50%" cy="18%" r="90%"><stop offset="0" stop-color="#12203A"/><stop offset="0.55" stop-color="#0A1327"/><stop offset="1" stop-color="#050A16"/></radialGradient>'
 '<radialGradient id="flood"><stop offset="0" stop-color="#CFE0F5" stop-opacity="0.15"/><stop offset="1" stop-color="#DCEBFF" stop-opacity="0"/></radialGradient>'
 '<linearGradient id="court" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#1E88E5"/><stop offset="0.55" stop-color="#1565C0"/><stop offset="1" stop-color="#0D3E86"/></linearGradient>'
 '<linearGradient id="glass" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#0F1F3A" stop-opacity="0.55"/><stop offset="1" stop-color="#6FA0DC" stop-opacity="0.16"/></linearGradient>'
 '<radialGradient id="sheen"><stop offset="0" stop-color="#BFE0FF" stop-opacity="0.55"/><stop offset="1" stop-color="#BFE0FF" stop-opacity="0"/></radialGradient>'
 '<radialGradient id="vign" cx="50%" cy="55%" r="75%"><stop offset="0.55" stop-color="#000000" stop-opacity="0"/><stop offset="1" stop-color="#04070F" stop-opacity="0.5"/></radialGradient>'
 '<filter id="soft" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="0.9"/></filter>'
 '<filter id="softy" x="-120%" y="-120%" width="340%" height="340%"><feGaussianBlur stdDeviation="0.7"/></filter>'
 '</defs>')
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="1200" height="1200">{defs}'
     '<rect width="100" height="100" fill="url(#bg)"/>'+ "".join(L)+ "".join(O) +'</svg>')
open("court.svg","w").write(svg); print("wrote premium court.svg")
