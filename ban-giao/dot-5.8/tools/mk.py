import json,sys,runpy,os
# usage: mk.py spec.py  ; spec defines PAGE, ROWS=[(old,new)], MAP=[(unit,ci,[rows],applied,why)]
g=runpy.run_path(sys.argv[1])
page=g['PAGE']; path='docs/'+page
src=open('/Users/mitu/Desktop/work/projects/logos/'+path,encoding='utf-8').read()
rows=g['ROWS']
# sort by position in original
pos=[src.find(o) for o,n in rows]
assert all(p>=0 for p in pos), [o for (o,n),p in zip(rows,pos) if p<0]
order=sorted(range(len(rows)),key=lambda i:pos[i])
remap={old:new for new,old in enumerate(order)}
out=[[path,rows[i][0],rows[i][1]] for i in order]
name=os.path.basename(page)[:-3]
json.dump(out,open(name+'.json','w'),ensure_ascii=False,indent=1)
m=[{"unit":u,"claim_index":ci,"rows":sorted(remap[r] for r in rs),"applied":ap,"why":why} for u,ci,rs,ap,why in g['MAP']]
json.dump(m,open(name+'.map.json','w'),ensure_ascii=False,indent=1)
print(name, len(out),'rows')
