import sys,json
# usage: rep.py file.json  ; json = [[path, old, new], ...]
for path,old,new in json.load(open(sys.argv[1],encoding='utf-8')):
    s=open(path,encoding='utf-8').read()
    n=s.count(old)
    assert n==1,(path,old[:60],n)
    open(path,'w',encoding='utf-8').write(s.replace(old,new))
    print('ok',path,old[:40])
