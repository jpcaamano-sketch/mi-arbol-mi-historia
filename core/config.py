import os


def _get(key: str, default: str = "") -> str:
    try:
        import streamlit as st
        return st.secrets[key]
    except Exception:
        return os.environ.get(key, default)


SUPABASE_URL   = _get("SUPABASE_URL")
SUPABASE_KEY   = _get("SUPABASE_KEY")
RESEND_API_KEY = _get("RESEND_API_KEY")
GOOGLE_API_KEY = _get("GOOGLE_API_KEY")
BASE_URL       = _get("BASE_URL", "http://localhost:8545")

FROM_EMAIL     = "Mi Árbol, Mi Historia <noreply@escuelayocreo.cl>"
AGENDA_URL     = _get("AGENDA_URL", "https://jpecoachdevida.cl/agendar-sesion")
