from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, hashlib, threading, time
from send2trash import send2trash

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global scan state
state = {
    'root': os.path.abspath('.'),
    'scanning': False,
    'progress': 0.0,
    'total_files': 0,
    'scanned_files': 0,
    'groups': {},  # hash -> [paths]
}

IMAGE_VIDEO_EXTS = {'.jpg','.jpeg','.png','.gif','.bmp','.tiff','.mp4','.mov','.avi','.mkv','.webm','.heic','.heif','.mpg','.mpeg'}

def md5_file(path, chunk_size=4*1024*1024):
    h = hashlib.md5()
    try:
        with open(path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                h.update(chunk)
    except Exception:
        return None
    return h.hexdigest()

def scan_folder(root):
    state['scanning'] = True
    state['progress'] = 0.0
    state['groups'] = {}
    paths = []
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in IMAGE_VIDEO_EXTS:
                paths.append(os.path.join(dirpath, fn))
    state['total_files'] = len(paths)
    state['scanned_files'] = 0
    for i, p in enumerate(paths, start=1):
        h = md5_file(p)
        if h:
            state['groups'].setdefault(h, []).append(p)
        state['scanned_files'] = i
        state['progress'] = i / max(1, state['total_files'])
    state['scanning'] = False
    state['progress'] = 1.0

class ChangeFolder(BaseModel):
    path: str

@app.post('/api/change-folder')
def change_folder(payload: ChangeFolder, background_tasks: BackgroundTasks):
    p = payload.path.strip()
    if not p or not os.path.isdir(p):
        raise HTTPException(status_code=400, detail='Invalid path')
    state['root'] = os.path.abspath(p)
    # start background scan
    t = threading.Thread(target=scan_folder, args=(state['root'],), daemon=True)
    t.start()
    return {'status': 'scanning', 'root': state['root']}

@app.get('/api/progress')
def progress():
    return {'scanning': state['scanning'], 'progress': state['progress'], 'scanned': state['scanned_files'], 'total': state['total_files']}

@app.get('/api/summary')
def summary():
    space = 0
    groups = {h: v for h,v in state['groups'].items() if len(v) > 1}
    for h, paths in groups.items():
        try:
            sz = sum(os.path.getsize(p) for p in paths[1:])
            space += sz
        except Exception:
            pass
    return {'files': state['total_files'], 'groups': len(groups), 'space': space}

@app.get('/api/duplicates')
def duplicates():
    out = []
    for h, paths in state['groups'].items():
        if len(paths) > 1:
            try:
                size = os.path.getsize(paths[0])
            except Exception:
                size = 0
            out.append({'hash': h, 'size': size, 'paths': paths, 'keeper': paths[0]})
    return out
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, hashlib, threading
from send2trash import send2trash

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global scan state
state = {
    'root': os.path.abspath('.'),
    'scanning': False,
    'progress': 0.0,
    'total_files': 0,
    'scanned_files': 0,
    'groups': {},  # hash -> [paths]
}

IMAGE_VIDEO_EXTS = {'.jpg','.jpeg','.png','.gif','.bmp','.tiff','.mp4','.mov','.avi','.mkv','.webm','.heic','.heif','.mpg','.mpeg'}

def md5_file(path, chunk_size=4*1024*1024):
    h = hashlib.md5()
    try:
        with open(path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                h.update(chunk)
    except Exception:
        return None
    return h.hexdigest()

def scan_folder(root):
    state['scanning'] = True
    state['progress'] = 0.0
    state['groups'] = {}
    paths = []
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in IMAGE_VIDEO_EXTS:
                paths.append(os.path.join(dirpath, fn))
    state['total_files'] = len(paths)
    state['scanned_files'] = 0
    for i, p in enumerate(paths, start=1):
        h = md5_file(p)
        if h:
            state['groups'].setdefault(h, []).append(p)
        state['scanned_files'] = i
        state['progress'] = i / max(1, state['total_files'])
    state['scanning'] = False
    state['progress'] = 1.0

class ChangeFolder(BaseModel):
    path: str

@app.post('/api/change-folder')
def change_folder(payload: ChangeFolder):
    p = payload.path.strip()
    if not p or not os.path.isdir(p):
        raise HTTPException(status_code=400, detail='Invalid path')
    state['root'] = os.path.abspath(p)
    # start background scan
    t = threading.Thread(target=scan_folder, args=(state['root'],), daemon=True)
    t.start()
    return {'status': 'scanning', 'root': state['root']}

@app.get('/api/progress')
def progress():
    return {'scanning': state['scanning'], 'progress': state['progress'], 'scanned': state['scanned_files'], 'total': state['total_files']}

@app.get('/api/summary')
def summary():
    space = 0
    groups = {h: v for h,v in state['groups'].items() if len(v) > 1}
    for h, paths in groups.items():
        try:
            sz = sum(os.path.getsize(p) for p in paths[1:])
            space += sz
        except Exception:
            pass
    return {'files': state['total_files'], 'groups': len(groups), 'space': space}

@app.get('/api/duplicates')
def duplicates():
    out = []
    for h, paths in state['groups'].items():
        if len(paths) > 1:
            try:
                size = os.path.getsize(paths[0])
            except Exception:
                size = 0
            out.append({'hash': h, 'size': size, 'paths': paths, 'keeper': paths[0]})
    return out

@app.get('/file')
def get_file(path: str):
    real = os.path.abspath(path)
    try:
        if os.path.commonpath([state['root'], real]) != state['root']:
            raise HTTPException(status_code=403)
    except Exception:
        raise HTTPException(status_code=403)
    if not os.path.exists(real):
        raise HTTPException(status_code=404)
    return FileResponse(real)

class DeletePaths(BaseModel):
    paths: list
    method: str = 'recycle'

@app.post('/api/delete-paths')
def delete_paths(payload: DeletePaths):
    deleted = 0
    failed = []
    for p in payload.paths:
        real = os.path.abspath(p)
        try:
            if os.path.commonpath([state['root'], real]) != state['root']:
                failed.append({'path': p, 'error': 'outside root'})
                continue
        except Exception:
            failed.append({'path': p, 'error': 'invalid path'})
            continue
        if not os.path.exists(real):
            failed.append({'path': p, 'error': 'missing'})
            continue
        try:
            if payload.method == 'recycle':
                send2trash(real)
            else:
                os.remove(real)
            deleted += 1
            # mark deleted locally
            for g in state['groups'].values():
                for f in list(g):
                    if f == real:
                        try:
                            g.remove(f)
                        except Exception:
                            pass
        except Exception as e:
            failed.append({'path': p, 'error': str(e)})
    return {'deleted': deleted, 'failed': failed}

@app.post('/api/delete-all')
def delete_all(payload: dict = None):
    # delete all duplicates, keep first in each group
    deleted = 0
    freed = 0
    for h, paths in list(state['groups'].items()):
        if len(paths) <= 1:
            continue
        keeper = paths[0]
        for p in paths[1:]:
            try:
                sz = os.path.getsize(p)
            except Exception:
                sz = 0
            try:
                send2trash(p)
                deleted += 1
                freed += sz
            except Exception:
                try:
                    os.remove(p)
                    deleted += 1
                    freed += sz
                except Exception:
                    pass
        # keep only keeper
        state['groups'][h] = [keeper]
    return {'deleted': deleted, 'freed': freed}


if __name__ == '__main__':
    try:
        import uvicorn
        uvicorn.run('server.app:app', host='127.0.0.1', port=8888, log_level='info')
    except Exception as e:
        print('Unable to start uvicorn:', e)
        print('Make sure dependencies are installed (uvicorn).')
