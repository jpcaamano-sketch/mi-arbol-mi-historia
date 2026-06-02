import streamlit as st
import time
import json
from core.questions import (CATEGORIAS, PREGUNTAS_TEXTO, ESCALA_LABELS,
                              ACTOS_SIMBOLICOS, CATEGORIAS_DESC, get_intensidad)

st.set_page_config(
    page_title="Mi Árbol, Mi Historia",
    page_icon="🌳",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbarActions"], [data-testid="stDeployButton"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

html, body, [data-testid="stAppViewContainer"] {
  background: #0f1710 !important;
}
[data-testid="stMain"], [data-testid="stVerticalBlock"] {
  background: #0f1710 !important;
}
section[data-testid="stSidebar"] { display: none !important; }

/* Tipografía base */
* { font-family: Georgia, 'Times New Roman', serif; }
h1, h2, h3 { color: #c9a040 !important; }
p, li { color: #f0ead6; }

/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
  background: #1a1205 !important;
  border: 1px solid #3d2b1a !important;
  color: #f0ead6 !important;
  border-radius: 6px !important;
  font-family: Georgia, serif !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: #c9a040 !important;
  box-shadow: 0 0 0 2px rgba(201,160,64,0.15) !important;
}

/* Radio buttons */
[data-testid="stRadio"] label {
  color: #f0ead6 !important;
  font-family: Georgia, serif !important;
}
[data-testid="stRadio"] [data-baseweb="radio"] {
  background: transparent !important;
}

/* Buttons */
[data-testid="stButton"] > button {
  background: #c9a040 !important;
  color: #0f1710 !important;
  border: none !important;
  border-radius: 6px !important;
  font-family: Georgia, serif !important;
  font-weight: 700 !important;
  font-size: 15px !important;
  padding: 12px 32px !important;
  width: 100% !important;
  cursor: pointer !important;
  transition: all 0.2s !important;
}
[data-testid="stButton"] > button:hover {
  background: #d4b050 !important;
  transform: translateY(-1px) !important;
}

/* Download button */
[data-testid="stDownloadButton"] > button {
  background: transparent !important;
  color: #c9a040 !important;
  border: 1px solid #c9a040 !important;
  border-radius: 6px !important;
  font-family: Georgia, serif !important;
  font-weight: 600 !important;
}

/* Divider */
hr { border-color: #2d2010 !important; }

/* Progress bar */
[data-testid="stProgress"] > div > div {
  background: #c9a040 !important;
}
[data-testid="stProgress"] > div {
  background: #1a1205 !important;
}

/* Selectbox */
[data-testid="stSelectbox"] select {
  background: #1a1205 !important;
  color: #f0ead6 !important;
  border: 1px solid #3d2b1a !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Helpers de estado ────────────────────────────────────────────────────────

def init_state():
    defaults = {
        "etapa": "inicio",
        "proceso_id": None,
        "nombre": "",
        "correo": "",
        "bloque_actual": 1,
        "pregunta_actual": 1,
        "respuestas": {},
        "familia": [],
        "reporte": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def ir_a(etapa, **kwargs):
    st.session_state.etapa = etapa
    for k, v in kwargs.items():
        st.session_state[k] = v
    st.rerun()


def box(content_html: str, color_border: str = "#2d2010"):
    st.markdown(
        f'<div style="background:#1a1205;border:1px solid {color_border};'
        f'border-radius:10px;padding:20px 24px;margin-bottom:16px;">'
        f'{content_html}</div>',
        unsafe_allow_html=True)


def header_bloque(num_bloque: int):
    cat = CATEGORIAS[num_bloque - 1]
    progreso = (num_bloque - 1) / 8
    st.progress(progreso)
    st.markdown(
        f'<p style="color:#7a6a50;font-size:12px;text-align:center;margin:4px 0 20px;">'
        f'Bloque {num_bloque} de 8</p>',
        unsafe_allow_html=True)
    st.markdown(
        f'<h2 style="text-align:center;font-size:22px;">'
        f'{cat["icono"]} {cat["nombre"]}</h2>',
        unsafe_allow_html=True)


# ─── Página: Inicio ───────────────────────────────────────────────────────────

def page_inicio():
    st.markdown("""
<div style="text-align:center;padding:40px 0 20px;">
  <div style="font-size:56px;margin-bottom:16px;">🌳</div>
  <h1 style="font-size:32px;margin-bottom:8px;">Mi Árbol, Mi Historia</h1>
  <p style="color:#c9a040;font-size:16px;font-style:italic;margin-bottom:24px;">
    Descubre qué patrones de tus ancestros viven todavía en ti
  </p>
  <p style="color:#b09870;font-size:14px;max-width:520px;margin:0 auto 32px;line-height:1.8;">
    Una herramienta de metagenealogía inspirada en la metodología de Alejandro Jodorowsky.
    No evalúa quién eres — explora los patrones que tu árbol ha transmitido de generación en generación.
  </p>
  <p style="color:#7a6a50;font-size:13px;">⏱️ Tiempo estimado: 15 a 20 minutos</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align:center;font-size:16px;margin-bottom:16px;'>Ingresa tus datos para comenzar</h3>",
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        nombre = st.text_input("Tu nombre", placeholder="¿Cómo te llamas?",
                               key="inp_nombre")
        correo = st.text_input("Tu correo", placeholder="Para recibir tu reporte",
                               key="inp_correo")

        st.markdown("""
<div style="background:#1a1205;border:1px solid #2d2010;border-radius:8px;
            padding:12px 16px;margin:16px 0;font-size:12px;color:#7a6a50;line-height:1.7;">
<strong style="color:#c9a040;">Aviso importante:</strong><br>
Esta herramienta es una experiencia de autoconocimiento basada en metagenealogía y psicomagia.
No es un diagnóstico clínico, no reemplaza la psicoterapia ni la atención de un profesional de salud mental.
Si durante o después de la experiencia sientes una angustia intensa, te recomendamos buscar apoyo profesional.
</div>
""", unsafe_allow_html=True)

        if st.button("🌱 Comenzar el recorrido"):
            if not nombre.strip():
                st.error("Por favor ingresa tu nombre.")
                return
            if not correo.strip() or "@" not in correo:
                st.error("Por favor ingresa un correo válido.")
                return
            from core.database import create_proceso
            proceso = create_proceso(nombre.strip(), correo.strip().lower())
            ir_a("contexto",
                 proceso_id=proceso["id"],
                 nombre=nombre.strip(),
                 correo=correo.strip().lower())


# ─── Página: Contexto ─────────────────────────────────────────────────────────

def page_contexto():
    st.markdown("""
<div style="text-align:center;padding:20px 0 32px;">
  <h2 style="font-size:24px;margin-bottom:24px;">Antes de comenzar</h2>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        box("""
<p style="color:#c9a040;font-size:15px;line-height:1.8;margin-bottom:14px;">
  Tu árbol familiar no es solo historia.
  Es un programa que se transmite de generación en generación.
  Hoy vas a comenzar a verlo.
</p>
<p style="color:#b09870;font-size:14px;line-height:1.8;margin-bottom:14px;">
  Vas a recorrer <strong style="color:#c9a040;">8 categorías de patrones</strong>
  — desde las más concretas hasta las más profundas emocionalmente.
  En cada bloque, responderás 2 preguntas de escala y una pregunta de reflexión
  (que es completamente opcional).
</p>
<p style="color:#b09870;font-size:14px;line-height:1.8;">
  <strong style="color:#c9a040;">Lo que necesitas:</strong>
  tiempo, honestidad y apertura.
  No necesitas saber todo sobre tu familia —
  <em>lo que no sabes también es información.</em>
</p>
""", "#3d2b1a")

        st.markdown("""
<div style="background:#1a1005;border-left:3px solid #c9a040;padding:14px 18px;
            border-radius:0 6px 6px 0;margin:8px 0 24px;">
  <p style="color:#7a6a50;font-size:13px;margin:0;line-height:1.7;">
    <strong style="color:#b09870;">Escala de respuestas:</strong><br>
    1 = No se reconoce en mi árbol<br>
    2 = Quizás, no estoy seguro/a<br>
    3 = Algo de esto hay<br>
    4 = Sí, claramente<br>
    5 = Es un patrón muy evidente
  </p>
</div>
""", unsafe_allow_html=True)

        if st.button("Entendido, comenzar →"):
            ir_a("familia")


# ─── Página: Contexto familiar (opcional) ────────────────────────────────────

def page_familia():
    st.markdown("""
<div style="text-align:center;padding:16px 0 24px;">
  <h2 style="font-size:22px;">Cuéntame sobre tu árbol</h2>
  <p style="color:#7a6a50;font-size:13px;font-style:italic;">
    Este paso es completamente opcional — no afecta el diagnóstico
  </p>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown("""
<p style="color:#b09870;font-size:14px;line-height:1.7;margin-bottom:20px;">
  Si quieres, puedes ingresar algunos datos básicos de las generaciones anteriores.
  Solo escribe lo que sabes — los campos que dejes en blanco también tienen significado.
</p>
""", unsafe_allow_html=True)

        generaciones = [
            ("bisabuelos", "👴👵 Bisabuelos"),
            ("abuelos",    "👨‍🦳👩‍🦳 Abuelos"),
            ("padres",     "👨👩 Padres"),
        ]

        familia_data = []
        for gen_id, gen_label in generaciones:
            st.markdown(f"<p style='color:#c9a040;font-size:14px;margin:12px 0 6px;'>{gen_label}</p>",
                        unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                nombre_ref = st.text_input("Nombre o apodo", key=f"fam_{gen_id}_nombre",
                                           placeholder="Opcional")
            with c2:
                pais = st.text_input("País de origen", key=f"fam_{gen_id}_pais",
                                     placeholder="Opcional")
            notas = st.text_input("Algo que quieras destacar", key=f"fam_{gen_id}_notas",
                                  placeholder="Opcional — cualquier dato que sientas importante")
            familia_data.append({
                "generacion": gen_id,
                "nombre_referencia": nombre_ref.strip() or None,
                "pais_origen": pais.strip() or None,
                "notas_libres": notas.strip() or None,
            })

        st.markdown("<br>", unsafe_allow_html=True)

        c_skip, c_cont = st.columns(2)
        with c_skip:
            if st.button("Prefiero continuar sin esto"):
                ir_a("bloque", bloque_actual=1, pregunta_actual=1)
        with c_cont:
            if st.button("Ya ingresé lo que sé →"):
                from core.database import save_familia
                save_familia(st.session_state.proceso_id, familia_data)
                st.session_state.familia = [f for f in familia_data
                                            if f.get("nombre_referencia") or f.get("pais_origen")]
                ir_a("bloque", bloque_actual=1, pregunta_actual=1)


# ─── Página: Pregunta de bloque ───────────────────────────────────────────────

def page_bloque():
    num = st.session_state.bloque_actual
    q_num = st.session_state.pregunta_actual
    cat = CATEGORIAS[num - 1]

    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        header_bloque(num)

        if q_num in (1, 2):
            pid = cat["preguntas_escala"][q_num - 1]
            st.markdown(
                f'<p style="color:#f0ead6;font-size:16px;line-height:1.7;'
                f'text-align:center;margin:20px 0 28px;">'
                f'{PREGUNTAS_TEXTO[pid]}</p>',
                unsafe_allow_html=True)

            # Get previous answer if exists
            prev = st.session_state.respuestas.get(pid)
            prev_idx = (prev - 1) if prev else None

            seleccion = st.radio(
                "Tu respuesta:",
                options=list(range(1, 6)),
                format_func=lambda x: f"{x} — {ESCALA_LABELS[x-1]}",
                index=prev_idx,
                key=f"radio_b{num}_q{q_num}",
                label_visibility="collapsed",
            )

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Continuar →"):
                if seleccion is None:
                    st.error("Por favor selecciona una respuesta.")
                    return
                st.session_state.respuestas[pid] = seleccion
                from core.database import save_respuesta
                save_respuesta(st.session_state.proceso_id, pid, valor_escala=seleccion)
                ir_a("bloque", bloque_actual=num, pregunta_actual=q_num + 1)

        else:
            pid = cat["pregunta_abierta"]
            st.markdown(
                f'<p style="color:#c9a040;font-size:15px;line-height:1.7;'
                f'text-align:center;font-style:italic;margin:20px 0 16px;">'
                f'Una pregunta para reflexionar (opcional)</p>',
                unsafe_allow_html=True)
            st.markdown(
                f'<p style="color:#f0ead6;font-size:15px;line-height:1.7;'
                f'text-align:center;margin:0 0 24px;">'
                f'{PREGUNTAS_TEXTO[pid]}</p>',
                unsafe_allow_html=True)

            prev_texto = st.session_state.respuestas.get(pid, "")
            respuesta = st.text_area(
                "Tu reflexión (puedes dejarla en blanco):",
                value=str(prev_texto) if prev_texto else "",
                key=f"open_b{num}",
                height=100,
                placeholder="Escribe lo que venga — sin filtro, sin juicio...",
                label_visibility="collapsed",
            )

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Continuar →"):
                if respuesta.strip():
                    st.session_state.respuestas[pid] = respuesta.strip()
                    from core.database import save_respuesta
                    save_respuesta(st.session_state.proceso_id, pid, texto=respuesta.strip())
                # After last question of block → pausa
                ir_a("pausa", bloque_actual=num)


# ─── Página: Pausa entre bloques ─────────────────────────────────────────────

def page_pausa():
    num = st.session_state.bloque_actual
    cat = CATEGORIAS[num - 1]

    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown(f"""
<div style="text-align:center;padding:60px 20px;">
  <div style="font-size:40px;margin-bottom:24px;">{cat['icono']}</div>
  <p style="color:#c9a040;font-size:20px;font-style:italic;line-height:1.7;
             max-width:480px;margin:0 auto 40px;">
    "{cat['pausa']}"
  </p>
  <p style="color:#3d3020;font-size:13px;">— Tómate un momento —</p>
</div>
""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if num < 8:
            sig_cat = CATEGORIAS[num]
            if st.button(f"Continuar → {sig_cat['icono']} {sig_cat['nombre']}"):
                ir_a("bloque", bloque_actual=num + 1, pregunta_actual=1)
        else:
            if st.button("Ver lo que tu árbol tiene para mostrarte →"):
                ir_a("transicion")


# ─── Página: Transición ───────────────────────────────────────────────────────

def page_transicion():
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        placeholder = st.empty()

        mensajes = [
            ("🌳", "Tu árbol tiene algo que mostrarte..."),
            ("🍃", "Reuniendo los patrones de tu historia..."),
            ("✨", "Preparando tu reporte..."),
        ]

        for icono, msg in mensajes:
            placeholder.markdown(f"""
<div style="text-align:center;padding:80px 20px;">
  <div style="font-size:52px;margin-bottom:24px;animation:pulse 1.5s infinite;">{icono}</div>
  <p style="color:#c9a040;font-size:18px;font-style:italic;">{msg}</p>
</div>
<style>
@keyframes pulse {{
  0%, 100% {{ opacity: 1; transform: scale(1); }}
  50% {{ opacity: 0.6; transform: scale(0.95); }}
}}
</style>
""", unsafe_allow_html=True)
            time.sleep(1.2)

        placeholder.empty()

        # Generar reporte
        with st.spinner("Generando tu análisis personalizado..."):
            from core.report import generar_reporte_completo
            from core.database import completar_proceso, get_familia
            respuestas = st.session_state.respuestas
            familia = get_familia(st.session_state.proceso_id)
            reporte = generar_reporte_completo(
                st.session_state.nombre, respuestas, familia
            )
            completar_proceso(
                proceso_id=st.session_state.proceso_id,
                patron_dom=reporte["patron_dom"],
                patron_sec=reporte["patron_sec"],
                patron_ter=reporte["patron_ter"],
                intensidad=reporte["intensidad"],
                puntajes=reporte["scores"],
                carta=json.dumps(reporte["analisis"].get("carta_ancestros", {})),
                acto=json.dumps(reporte["acto"]),
                mensaje=json.dumps(reporte["analisis"].get("mensaje_liberacion", {})),
                practicas=json.dumps(reporte["analisis"].get("practicas", [])),
            )
            st.session_state.reporte = reporte

        ir_a("resultado")


# ─── Página: Resultado ────────────────────────────────────────────────────────

def page_resultado(reporte=None, proceso=None):
    if reporte is None:
        reporte = st.session_state.get("reporte")
    if proceso is None:
        from core.database import get_proceso
        proceso = get_proceso(st.session_state.proceso_id)

    nombre = proceso["nombre"] if proceso else st.session_state.nombre

    if not reporte:
        st.error("No se encontró el reporte.")
        return

    scores = reporte["scores"]
    patron_dom = reporte["patron_dom"]
    patron_sec = reporte["patron_sec"]
    patron_ter = reporte.get("patron_ter")
    intensidad  = reporte["intensidad"]
    analisis    = reporte["analisis"]
    acto        = reporte["acto"]
    grafico     = reporte["grafico"]
    pdf         = reporte["pdf"]

    dom_info = CATEGORIAS_DESC.get(patron_dom, {})
    _, intensidad_desc = get_intensidad(scores.get(patron_dom, 0))

    # Encabezado
    st.markdown(f"""
<div style="text-align:center;padding:24px 0 16px;">
  <div style="font-size:44px;margin-bottom:12px;">🌳</div>
  <h1 style="font-size:26px;margin-bottom:8px;">Mi Árbol, Mi Historia</h1>
  <p style="color:#7a6a50;font-size:14px;">Reporte de {nombre}</p>
  <p style="color:#c9a040;font-size:13px;font-style:italic;margin:8px 0 0;">
    "Lo que ves hoy no es tu destino. Es el origen de donde vienes."
  </p>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # Mapa de patrones
    st.markdown("<h2 style='font-size:18px;'>🗺️ Mapa de Patrones</h2>", unsafe_allow_html=True)
    st.image(grafico, use_container_width=True)

    st.divider()

    # Patrones dominantes
    st.markdown("<h2 style='font-size:18px;'>⭐ Tus Patrones Dominantes</h2>", unsafe_allow_html=True)

    dom_nom = dom_info.get("nombre", patron_dom)
    box(f"""
<p style="color:#c9a040;font-size:15px;font-weight:bold;margin:0 0 6px;">
  1. {dom_nom} — {intensidad.upper()} ({scores.get(patron_dom, 0):.1f}/5)
</p>
<p style="color:#b09870;font-size:13px;font-style:italic;margin:0 0 10px;">{intensidad_desc}</p>
<p style="color:#b09870;font-size:13px;margin:0 0 4px;"><strong style="color:#f0ead6;">Qué mapea:</strong> {dom_info.get('que_mapea','')}</p>
<p style="color:#b09870;font-size:13px;margin:0;"><strong style="color:#f0ead6;">Cómo aparece:</strong> {dom_info.get('como_aparece','')}</p>
""", "#c9a040")

    sec_info = CATEGORIAS_DESC.get(patron_sec, {})
    box(f"""
<p style="color:#f0ead6;font-size:15px;font-weight:bold;margin:0 0 6px;">
  2. {sec_info.get('nombre', patron_sec)} ({scores.get(patron_sec, 0):.1f}/5)
</p>
<p style="color:#b09870;font-size:13px;margin:0;"><strong style="color:#f0ead6;">Qué mapea:</strong> {sec_info.get('que_mapea','')}</p>
""")

    if patron_ter:
        ter_info = CATEGORIAS_DESC.get(patron_ter, {})
        box(f"""
<p style="color:#f0ead6;font-size:15px;font-weight:bold;margin:0 0 6px;">
  3. {ter_info.get('nombre', patron_ter)} ({scores.get(patron_ter, 0):.1f}/5)
</p>
<p style="color:#b09870;font-size:13px;margin:0;"><strong style="color:#f0ead6;">Qué mapea:</strong> {ter_info.get('que_mapea','')}</p>
""")

    st.divider()

    # Mensaje de liberación
    ml = analisis.get("mensaje_liberacion", {})
    st.markdown("<h2 style='font-size:18px;'>💫 Mensaje de Liberación</h2>", unsafe_allow_html=True)
    for parrafo in [ml.get("reconocimiento",""), ml.get("origen",""), ml.get("umbral","")]:
        if parrafo:
            st.markdown(
                f'<p style="color:#f0ead6;font-size:14px;line-height:1.8;margin-bottom:14px;">{parrafo}</p>',
                unsafe_allow_html=True)

    st.divider()

    # Carta a los ancestros
    carta = analisis.get("carta_ancestros", {})
    st.markdown("<h2 style='font-size:18px;'>✉️ Carta a mis Ancestros</h2>", unsafe_allow_html=True)

    carta_html = '<div style="background:#1a1005;border:1px solid #3d2b1a;border-radius:8px;padding:24px 28px;">'
    carta_html += '<p style="color:#c9a040;font-size:13px;font-style:italic;margin-bottom:16px;">Queridos ancestros,</p>'
    for parrafo in [carta.get("encuentro",""), carta.get("comprension",""),
                    carta.get("verdad",""), carta.get("liberacion","")]:
        if parrafo:
            carta_html += f'<p style="color:#f0ead6;font-size:14px;line-height:1.8;margin-bottom:14px;">{parrafo}</p>'
    carta_html += '</div>'
    st.markdown(carta_html, unsafe_allow_html=True)

    st.divider()

    # Prácticas de sanación
    st.markdown("<h2 style='font-size:18px;'>🌿 Prácticas de Sanación</h2>", unsafe_allow_html=True)
    for i, p in enumerate(analisis.get("practicas", []), 1):
        box(f"""
<p style="color:#c9a040;font-size:14px;font-weight:bold;margin:0 0 8px;">{i}. {p.get('nombre','')}</p>
<p style="color:#f0ead6;font-size:13px;line-height:1.7;margin:0 0 10px;">{p.get('instrucciones','')}</p>
<p style="color:#7a6a50;font-size:12px;margin:0;">
  <strong style="color:#b09870;">Materiales:</strong> {p.get('materiales','')} &nbsp;·&nbsp;
  <strong style="color:#b09870;">Frecuencia:</strong> {p.get('frecuencia','')}
</p>
""")

    st.divider()

    # Acto simbólico
    st.markdown("<h2 style='font-size:18px;'>🔥 El Acto Simbólico</h2>", unsafe_allow_html=True)
    box(f"""
<p style="color:#c9a040;font-size:15px;font-weight:bold;margin:0 0 10px;">{acto.get('titulo','')}</p>
<p style="color:#f0ead6;font-size:14px;line-height:1.8;margin:0 0 14px;">{acto.get('instrucciones','')}</p>
<p style="color:#c9a040;font-size:13px;font-style:italic;margin:0 0 10px;">
  Intención: "{acto.get('intencion','')}"
</p>
<p style="color:#7a6a50;font-size:12px;margin:0;">
  <strong style="color:#b09870;">Materiales:</strong> {acto.get('materiales','')} &nbsp;·&nbsp; {acto.get('duracion','')}
</p>
""", "#c9a040")

    # Reflexiones del usuario
    from core.questions import PREGUNTAS_TEXTO
    abiertas = []
    for cat in CATEGORIAS:
        pid = cat["pregunta_abierta"]
        texto = st.session_state.respuestas.get(pid) or (
            reporte.get("respuestas", {}).get(pid) if reporte.get("respuestas") else None
        )
        if texto and str(texto).strip():
            abiertas.append((PREGUNTAS_TEXTO[pid], str(texto)))

    if abiertas:
        st.divider()
        st.markdown("<h2 style='font-size:18px;'>🪞 Lo que ya sabías</h2>", unsafe_allow_html=True)
        for pregunta, respuesta in abiertas:
            st.markdown(
                f'<p style="color:#7a6a50;font-size:13px;font-style:italic;margin-bottom:4px;">{pregunta}</p>'
                f'<p style="color:#f0ead6;font-size:14px;margin-bottom:18px;padding-left:16px;'
                f'border-left:2px solid #3d2b1a;">{respuesta}</p>',
                unsafe_allow_html=True)

    st.divider()

    # Cierre
    st.markdown("""
<div style="text-align:center;padding:20px 0 10px;">
  <p style="color:#c9a040;font-size:15px;font-style:italic;margin-bottom:16px;">
    "Conocer de dónde vienes no te condena a repetirlo.<br>Te da la libertad de elegir a dónde vas."
  </p>
  <p style="color:#7a6a50;font-size:13px;line-height:1.7;">
    Tu árbol es el mapa. El camino de vuelta a ti mismo es tuyo.<br>
    Si quieres caminarlo acompañado, estoy aquí.
    <strong style="color:#b09870;">— Juan Pablo</strong>
  </p>
</div>
""", unsafe_allow_html=True)

    from core.config import AGENDA_URL
    st.link_button("Agendar una conversación con Juan Pablo", AGENDA_URL)

    st.divider()

    # Acciones
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="⬇️ Descargar reporte PDF",
            data=pdf,
            file_name=f"mi_arbol_mi_historia_{nombre.lower().replace(' ','_')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    with col2:
        if st.button("📧 Recibir por correo", use_container_width=True):
            with st.spinner("Enviando tu reporte..."):
                from core.email_service import enviar_reporte
                from core.config import BASE_URL
                link = f"{BASE_URL}/?resultado={st.session_state.proceso_id}"
                try:
                    enviar_reporte(nombre, proceso["correo"] if proceso else st.session_state.correo,
                                   link, pdf)
                    st.success("✅ Reporte enviado a tu correo.")
                except Exception as e:
                    st.error(f"Error al enviar: {e}")


# ─── Resultado desde URL ──────────────────────────────────────────────────────

def page_resultado_from_db(proceso_id: str):
    import re
    if not re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", proceso_id.lower()):
        st.error("Enlace inválido.")
        return

    from core.database import get_proceso, get_respuestas, get_familia
    from core.report import (calcular_puntajes, determinar_patrones,
                              generar_analisis, generar_grafico, generar_pdf)

    proceso = get_proceso(proceso_id)
    if not proceso or proceso["estado"] != "completado":
        st.error("Reporte no disponible.")
        return

    respuestas = get_respuestas(proceso_id)
    familia = get_familia(proceso_id)
    scores = calcular_puntajes(respuestas)
    patron_dom, patron_sec, patron_ter, intensidad, _ = determinar_patrones(scores)

    analisis_raw = {
        "mensaje_liberacion": json.loads(proceso.get("mensaje_liberacion") or "{}"),
        "carta_ancestros": json.loads(proceso.get("carta_generada") or "{}"),
        "practicas": json.loads(proceso.get("practicas_generadas") or "[]"),
    }
    acto = json.loads(proceso.get("acto_generado") or "{}")
    grafico = generar_grafico(scores, patron_dom, patron_sec, patron_ter)
    pdf = generar_pdf(proceso["nombre"], scores, patron_dom, patron_sec, patron_ter,
                      intensidad, analisis_raw, grafico, respuestas)

    reporte = {
        "scores": scores,
        "patron_dom": patron_dom,
        "patron_sec": patron_sec,
        "patron_ter": patron_ter,
        "intensidad": intensidad,
        "analisis": analisis_raw,
        "acto": acto,
        "grafico": grafico,
        "pdf": pdf,
        "respuestas": respuestas,
    }
    st.session_state.proceso_id = proceso_id
    st.session_state.respuestas = respuestas
    page_resultado(reporte=reporte, proceso=proceso)


# ─── Router principal ─────────────────────────────────────────────────────────

def main():
    init_state()

    resultado_id = st.query_params.get("resultado")
    if resultado_id:
        page_resultado_from_db(resultado_id)
        return

    etapa = st.session_state.etapa

    if etapa == "inicio":
        page_inicio()
    elif etapa == "contexto":
        page_contexto()
    elif etapa == "familia":
        page_familia()
    elif etapa == "bloque":
        page_bloque()
    elif etapa == "pausa":
        page_pausa()
    elif etapa == "transicion":
        page_transicion()
    elif etapa == "resultado":
        reporte = st.session_state.get("reporte")
        from core.database import get_proceso
        proceso = get_proceso(st.session_state.proceso_id)
        page_resultado(reporte=reporte, proceso=proceso)
    else:
        ir_a("inicio")


if __name__ == "__main__":
    main()
