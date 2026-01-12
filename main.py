import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel

app = FastAPI()

# Dočasná paměť přímo v RAM serveru
memory_db = {}
measure_trigger = False 

# Definice našich Rigů
RIGS = {
    "jakub-103-243": {"specs": "RTX 3060 12GB", "price": 40},
    "apponfly-gaming-2": {"specs": "RTX 4080 16GB", "price": 80},
}

class LatencyData(BaseModel):
    rig_id: str
    ms: int
    p2p: str

# CSS styly bokem, aby nezpůsobovaly SyntaxError v f-stringu
CSS_STYLES = """
<style>
    body { font-family: sans-serif; margin: 40px; background: #f4f7f6; }
    table { border-collapse: collapse; width: 100%; background: white; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
    th { background-color: #2c3e50; color: white; }
    .btn { padding: 15px 25px; background: #e67e22; color: white; border: none; 
             border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: bold; }
    .btn:hover { background: #d35400; }
</style>
"""

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    rows = ""
    for r_id, info in RIGS.items():
        data = memory_db.get(r_id, {})
        latency = data.get("ms", "--")
        conn_type = data.get("p2p", "Unknown")
        
        # Barva pro typ spojení
        color = "#4CAF50" if conn_type == "P2P" else "#FF9800" if "Relay" in conn_type else "#757575"
        
        rows += f"""
        <tr>
            <td><strong>{r_id}</strong></td>
            <td>{info['specs']}</td>
            <td style="text-align
