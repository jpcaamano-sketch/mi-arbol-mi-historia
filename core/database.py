import json
from datetime import datetime, timezone

_client = None


def _db():
    global _client
    if _client is None:
        from core.config import SUPABASE_URL, SUPABASE_KEY
        from supabase import create_client
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


# ─── Procesos ─────────────────────────────────────────────────────────────────

def create_proceso(nombre: str, correo: str) -> dict:
    r = _db().table("arbol_procesos").insert({
        "nombre": nombre, "correo": correo
    }).execute()
    return r.data[0]


def get_proceso(proceso_id: str) -> dict | None:
    r = _db().table("arbol_procesos").select("*").eq("id", proceso_id).execute()
    return r.data[0] if r.data else None


def update_proceso(proceso_id: str, **kwargs):
    _db().table("arbol_procesos").update(kwargs).eq("id", proceso_id).execute()


def completar_proceso(proceso_id: str, patron_dom: str, patron_sec: str,
                      patron_ter: str | None, intensidad: str, puntajes: dict,
                      carta: str, acto: str, mensaje: str, practicas: str):
    now = datetime.now(timezone.utc).isoformat()
    update_proceso(
        proceso_id,
        estado="completado",
        patron_dominante=patron_dom,
        patron_secundario=patron_sec,
        patron_terciario=patron_ter,
        intensidad_dominante=intensidad,
        puntajes=json.dumps(puntajes),
        carta_generada=carta,
        acto_generado=acto,
        mensaje_liberacion=mensaje,
        practicas_generadas=practicas,
        fecha_completado=now,
    )


def get_all_procesos() -> list:
    r = _db().table("arbol_procesos").select("*").order("fecha_creacion", desc=True).execute()
    return r.data


# ─── Respuestas ───────────────────────────────────────────────────────────────

def save_respuesta(proceso_id: str, pregunta_id: int, valor_escala=None, texto=None):
    row = {"proceso_id": proceso_id, "pregunta_id": pregunta_id}
    if valor_escala is not None:
        row["valor_escala"] = int(valor_escala)
    if texto:
        row["texto_respuesta"] = str(texto)
    _db().table("arbol_respuestas").upsert(
        row, on_conflict="proceso_id,pregunta_id"
    ).execute()


def get_respuestas(proceso_id: str) -> dict:
    r = _db().table("arbol_respuestas").select("*").eq("proceso_id", proceso_id).execute()
    result = {}
    for row in r.data:
        pid = row["pregunta_id"]
        result[pid] = row["valor_escala"] if row["valor_escala"] is not None else row["texto_respuesta"]
    return result


# ─── Contexto familiar ────────────────────────────────────────────────────────

def save_familia(proceso_id: str, familia: list):
    rows = [{"proceso_id": proceso_id, **f} for f in familia if f.get("nombre_referencia") or f.get("pais_origen")]
    if rows:
        _db().table("arbol_familia").upsert(
            rows, on_conflict="proceso_id,generacion"
        ).execute()


def get_familia(proceso_id: str) -> list:
    r = _db().table("arbol_familia").select("*").eq("proceso_id", proceso_id).execute()
    return r.data
