"""Load a commit-pinned, password-protected public release. No remote commands."""
import hashlib,io,json,re,shutil,stat,sys,urllib.request,zipfile
from pathlib import Path
REPO='jmsstore/cutsapay'
MAX_ARCHIVE=16*1024*1024
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):return None

def get(url,limit):
    req=urllib.request.Request(url,headers={'User-Agent':'CUTSAPAY-Package/1','Cache-Control':'no-cache'})
    with urllib.request.build_opener(NoRedirect()).open(req,timeout=45) as res:data=res.read(limit+1)
    if len(data)>limit:raise ValueError('Paket terlalu besar')
    return data

def metadata(raw):
    r=json.loads(raw)
    if not isinstance(r,dict) or r.get('schema')!=1:raise ValueError('Format release salah')
    if not re.fullmatch(r'\d+\.\d+\.\d+',r.get('version','')):raise ValueError('Versi paket salah')
    if r.get('archive')!='payload/cutsapay-vpn-'+r['version']+'.zip':raise ValueError('Jalur paket salah')
    if not re.fullmatch('[a-f0-9]{64}',r.get('sha256','')) or not re.fullmatch('[a-f0-9]{64}',r.get('key_hex','')):raise ValueError('Metadata paket salah')
    if type(r.get('bytes')) is not int or not 1<=r['bytes']<=MAX_ARCHIVE:raise ValueError('Ukuran paket salah')
    return r

def fetch(commit):
    if not re.fullmatch('[a-f0-9]{40}',commit):raise ValueError('Commit salah')
    base='https://raw.githubusercontent.com/'+REPO+'/'+commit+'/'
    r=metadata(get(base+'release.json',8192))
    data=get(base+r['archive'],MAX_ARCHIVE)
    verify(data,r)
    return {'archive':data,'release':r}

def verify(data,r):
    r=metadata(json.dumps(r))
    if len(data)!=r['bytes'] or hashlib.sha256(data).hexdigest()!=r['sha256']:raise ValueError('Hash paket tidak sesuai')

def extract(bundle,root):
    data,r=bundle['archive'],bundle['release'];verify(data,r)
    root=Path(root).resolve();root.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        items=z.infolist()
        if len(items)>4096 or sum(i.file_size for i in items)>32*1024*1024:raise ValueError('Paket terlalu besar')
        seen=set()
        for i in items:
            rel=Path(i.filename)
            p=(root/rel).resolve();kind=stat.S_IFMT(i.external_attr>>16)
            if rel.is_absolute() or '..' in rel.parts or not i.filename.startswith('cutsapay-vpn/') or '\\' in i.filename or root not in p.parents or p in seen or kind not in (0,stat.S_IFREG,stat.S_IFDIR):raise ValueError('Jalur arsip tidak aman')
            seen.add(p)
            if not i.is_dir() and not (i.flag_bits&1):raise ValueError('Paket memuat file tanpa password')
        password=bytes.fromhex(r['key_hex'])
        for i in items:
            p=root/i.filename
            if i.is_dir():p.mkdir(parents=True,exist_ok=True)
            else:
                p.parent.mkdir(parents=True,exist_ok=True)
                with z.open(i,pwd=password) as src,p.open('wb') as out:shutil.copyfileobj(src,out)
                p.chmod(0o644)
    result=root/'cutsapay-vpn'
    if not (result/'src/install.sh').is_file():raise ValueError('Paket installer tidak lengkap')
    return result

if __name__=='__main__':
    try:extract(fetch(sys.argv[1]),Path(sys.argv[2]))
    except Exception:raise SystemExit('Paket belum bisa dibuka; periksa release GitHub dan jaringan.')
