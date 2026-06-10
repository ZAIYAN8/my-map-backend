import json,sys
p=r"F:\qgis\knight-l.github.iosc-datav\sc-datav\src\assets\sc_outline.json"
try:
    with open(p,encoding='utf-8') as f:
        j=json.load(f)
except Exception as e:
    print('LOAD_ERROR',e)
    sys.exit(2)
feats=j.get('features',[])
print('FEATURE_COUNT',len(feats))

invalid_features=[]
for i,f in enumerate(feats):
    name=f.get('properties',{}).get('name')
    geom=f.get('geometry')
    if not geom:
        invalid_features.append((i,name,'NO_GEOM'))
        continue
    gt=geom.get('type')
    coords=geom.get('coordinates')
    if coords is None:
        invalid_features.append((i,name,'NO_COORDS'))
        continue
    # normalize polygons
    polys=[]
    try:
        if gt=='Polygon':
            polys=[coords]
        elif gt=='MultiPolygon':
            # flatten one level of nesting to get rings lists
            for part in coords:
                if isinstance(part,list):
                    if part and isinstance(part[0],list) and isinstance(part[0][0],list):
                        polys.extend(part)
                    else:
                        polys.append(part)
        elif isinstance(coords,list) and isinstance(coords[0],list):
            polys=coords
        else:
            invalid_features.append((i,name,'UNHANDLED_GEOM',type(coords).__name__))
            continue
    except Exception as e:
        invalid_features.append((i,name,'NORM_ERROR',str(e)))
        continue
    # check rings
    bad=False
    for ring in polys:
        if not isinstance(ring,list) or len(ring)==0:
            bad=True
            break
        for coord in ring:
            if not isinstance(coord,list) or len(coord)<2:
                bad=True
                break
            if coord[0] is None or coord[1] is None:
                bad=True
                break
    if bad:
        invalid_features.append((i,name,'BAD_COORDS'))

print('INVALID_FEATURES',len(invalid_features))
for it in invalid_features[:50]:
    print(it)

# print sample of first features
print('SAMPLE_FIRST_10')
for i,f in enumerate(feats[:10]):
    name=f.get('properties',{}).get('name')
    geom=f.get('geometry')
    gt=geom.get('type') if geom else None
    print(i,name,gt)
print('DONE')
