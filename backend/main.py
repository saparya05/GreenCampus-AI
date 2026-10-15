"""Optional FastAPI + SQLite persistence API for GreenCampus AI.
The frontend local demo runs independently; this API is an optional backend starter.
"""
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import json, os, sqlite3
from pathlib import Path
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
DB_PATH = Path(os.getenv('GREEN_CAMPUS_DB', Path(__file__).with_name('greencampus.db')))
def connect():
    con=sqlite3.connect(DB_PATH); con.row_factory=sqlite3.Row; return con
@asynccontextmanager
async def lifespan(app: FastAPI):
    with connect() as db:
        db.execute('CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY, kind TEXT NOT NULL, payload TEXT NOT NULL, updated_at TEXT NOT NULL)')
    yield
app=FastAPI(title='GreenCampus AI API',version='1.0.0',lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=os.getenv('CORS_ORIGINS','http://localhost:5173').split(','),allow_methods=['GET','POST','PUT','DELETE'],allow_headers=['*'])
class Record(BaseModel):
    id: str = Field(min_length=1,max_length=200)
    kind: str = Field(min_length=1,max_length=60)
    payload: dict[str,Any]
@app.get('/health')
def health(): return {'status':'ok','mode':'local-demo','database':str(DB_PATH.name)}
@app.get('/api/records')
def list_records(kind: str|None=None):
    with connect() as db:
        rows=db.execute('SELECT id,kind,payload,updated_at FROM records WHERE kind=? ORDER BY updated_at DESC',(kind,)).fetchall() if kind else db.execute('SELECT id,kind,payload,updated_at FROM records ORDER BY updated_at DESC').fetchall()
    return [{'id':r['id'],'kind':r['kind'],'payload':json.loads(r['payload']),'updated_at':r['updated_at']} for r in rows]
@app.put('/api/records/{record_id}')
def upsert_record(record_id: str, record: Record):
    if record_id != record.id: raise HTTPException(400,'Path ID must match record ID')
    now=datetime.now(timezone.utc).isoformat()
    try:
        with connect() as db: db.execute('INSERT INTO records(id,kind,payload,updated_at) VALUES(?,?,?,?) ON CONFLICT(id) DO UPDATE SET kind=excluded.kind,payload=excluded.payload,updated_at=excluded.updated_at',(record.id,record.kind,json.dumps(record.payload,allow_nan=False),now))
    except (ValueError,sqlite3.Error) as exc: raise HTTPException(400,f'Invalid record: {exc}')
    return {'id':record.id,'kind':record.kind,'updated_at':now}
@app.delete('/api/records/{record_id}')
def delete_record(record_id: str):
    with connect() as db: cur=db.execute('DELETE FROM records WHERE id=?',(record_id,))
    if cur.rowcount==0: raise HTTPException(404,'Record not found')
    return {'deleted':record_id}
