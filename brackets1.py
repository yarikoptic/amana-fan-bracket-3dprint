# specifics of the wheel

outdia=215  # mm, outer diam
# it is actually a radius in the code... uff
outdia=outdia/2
rimthck=2   # mm. actually varies 1.85-2.1 or so
rimheight=6.25 # mm (where not eatten)
nspikes=44
spikethck=2.35 # mm at a distance of about 3mm from rim. th varies
spikeangle=45  # deg, approx visually -- from the rim

# our params for the bracket
topthck=1.5  # mm thickness on top
inthck=2
outthck=1.5
# lip?

import cadquery as cq
from math import cos, sin, pi

rout = cq.Workplane('front')\
    .circle(outdia + outthck)\
    .circle(outdia).extrude(rimheight+topthck)

rin = cq.Workplane('front')\
    .circle(outdia - rimthck)\
    .circle(outdia - rimthck - inthck).extrude(rimheight+topthck)

# cut outs for spikes/fins
rfincut = cq.Workplane('front')\
    .rect(inthck*4, spikethck*1.2)\
    .extrude(rimheight)\
    .translate((0, 0, topthck))

finoffset = outdia - (inthck + rimthck)*0.9
for fin in range(nspikes):
    angl = 360*fin/nspikes
    angl_rad = pi * angl/180
    # since I don't know cq, will do all trigonom silly way
    # since will be rotating etc, 0.9
    rfincut1 = rfincut\
        .rotate((0,0,0), (0,0,1), -spikeangle + angl)\
        .translate((finoffset * cos(angl_rad), finoffset * sin(angl_rad), 0))
    rin = rin.cut(rfincut1)

rtop = cq.Workplane('front')\
    .circle(outdia + outthck)\
    .circle(outdia - rimthck - inthck).extrude(topthck)

# join them all
r = rtop.union(rout).union(rin)

del rfincut1
del rfincut
del rout
del rin
del rtop

#r = rfincut # .union(rfincut)

# split!

# TEMP-- to get one short to try -- well -- 4th part
rcut = r.faces('>Z').workplane()\
    .transformed(offset=cq.Vector(0, 0, 0), rotate=cq.Vector(0, 90, 0))\
    .split(keepTop=True, keepBottom=False)
# that would be for the quarter!
rcut2 = rcut.faces('>Z').workplane()\
    .transformed(offset=cq.Vector(0, 0, 0), rotate=cq.Vector(0, 90, 0))\
    .transformed(offset=cq.Vector(0, 0, 0), rotate=cq.Vector(90, 0, 0))\
    .split(keepBottom=True)
del r, rcut
# and for trial -- 8th
rcut3 = rcut2.faces('>Z').workplane()\
    .transformed(offset=cq.Vector(0, 0, 0), rotate=cq.Vector(0, 90, 0))\
    .transformed(offset=cq.Vector(0, 0, 0), rotate=cq.Vector(45, 0, 0))\
    .split(keepTop=True)
del rcut2
# now we need to make cut outs for the spike/fins

#    .circle(outdia - rimthck)\
#    .circle(outdia - rimthck - inthck)\
#    .extrude(rimheight + topthck)
#r = r.circle(outdia).extrude(-rimheight)
#r = r.faces(">Z").workplane()\
#    .hole(outdia)\
#    .extrude(rimheight)