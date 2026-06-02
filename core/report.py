import io
import re
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                 Table, TableStyle, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from core.questions import CATEGORIAS, CATEGORIAS_DESC, ACTOS_SIMBOLICOS, get_intensidad

_gemini = None


def _get_gemini():
    global _gemini
    if _gemini is None:
        from google import genai
        from core.config import GOOGLE_API_KEY
        _gemini = genai.Client(api_key=GOOGLE_API_KEY)
    return _gemini


# ─── Scoring ──────────────────────────────────────────────────────────────────

def calcular_puntajes(respuestas: dict) -> dict:
    scores = {}
    for cat in CATEGORIAS:
        vals = [respuestas[q] for q in cat["preguntas_escala"] if respuestas.get(q)]
        scores[cat["id"]] = round(sum(vals) / len(vals), 2) if vals else 0.0
    return scores


def determinar_patrones(scores: dict) -> tuple:
    sorted_cats = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    dom_id, dom_score = sorted_cats[0]
    sec_id, sec_score = sorted_cats[1]
    ter_id, ter_score = sorted_cats[2]

    intensidad_nombre, _ = get_intensidad(dom_score)
    patron_terciario = ter_id if ter_score >= 3.0 else None

    return dom_id, sec_id, patron_terciario, intensidad_nombre, scores


# ─── Sanitize JSON ────────────────────────────────────────────────────────────

def _sanitize_json(text: str) -> str:
    result = []
    in_string = False
    escape_next = False
    for ch in text:
        if escape_next:
            result.append(ch); escape_next = False
        elif ch == '\\' and in_string:
            result.append(ch); escape_next = True
        elif ch == '"':
            in_string = not in_string; result.append(ch)
        elif in_string and ord(ch) < 0x20:
            if ch == '\n': result.append('\\n')
            elif ch == '\r': result.append('\\r')
            elif ch == '\t': result.append('\\t')
        else:
            result.append(ch)
    return ''.join(result)


# ─── Análisis Gemini ──────────────────────────────────────────────────────────

def generar_analisis(nombre: str, scores: dict, patron_dom: str,
                     patron_sec: str, patron_ter: str | None,
                     intensidad: str, respuestas: dict, familia: list) -> dict:

    dom_info = CATEGORIAS_DESC.get(patron_dom, {})
    sec_info = CATEGORIAS_DESC.get(patron_sec, {})

    # Respuestas abiertas no vacías
    respuestas_abiertas = []
    for cat in CATEGORIAS:
        pid = cat["pregunta_abierta"]
        texto = respuestas.get(pid)
        if texto and str(texto).strip():
            from core.questions import PREGUNTAS_TEXTO
            respuestas_abiertas.append(f"- {PREGUNTAS_TEXTO[pid]}\n  Respuesta: {texto}")

    # Contexto familiar
    familia_texto = ""
    if familia:
        lineas = []
        for f in familia:
            gen = f.get("generacion", "")
            nom = f.get("nombre_referencia", "")
            pais = f.get("pais_origen", "")
            lineas.append(f"  {gen}: {nom} ({pais})" if nom or pais else "")
        familia_texto = "\n".join(l for l in lineas if l)

    prompt = f"""Eres un guía experto en metagenealogía, siguiendo la metodología de Alejandro Jodorowsky y Marianne Costa.
Genera el reporte personalizado de {nombre} basándote en los patrones detectados en su árbol genealógico.

PATRONES DETECTADOS (escala 1-5):
- Patrón dominante: {dom_info.get('nombre', patron_dom)} (puntaje: {scores[patron_dom]:.1f}/5, intensidad: {intensidad})
- Patrón secundario: {sec_info.get('nombre', patron_sec)} (puntaje: {scores[patron_sec]:.1f}/5)
{"- Patrón terciario: " + CATEGORIAS_DESC.get(patron_ter, {}).get('nombre', patron_ter) + " (puntaje: " + str(scores.get(patron_ter, 0)) + "/5)" if patron_ter else ""}

TODOS LOS PUNTAJES:
{chr(10).join(f"- {CATEGORIAS_DESC[cat['id']]['nombre']}: {scores[cat['id']]:.1f}" for cat in CATEGORIAS)}

REFLEXIONES DE {nombre}:
{chr(10).join(respuestas_abiertas) if respuestas_abiertas else "No compartió reflexiones abiertas."}

CONTEXTO FAMILIAR:
{familia_texto if familia_texto else "No proporcionó contexto familiar."}

Genera el reporte en JSON con este formato exacto:
{{
  "mensaje_liberacion": {{
    "reconocimiento": "Párrafo que nombra el patrón dominante sin juicio. Lo hace visible. Dirige a {nombre} directamente.",
    "origen": "Párrafo que sitúa el patrón en el árbol — en qué generaciones estuvo más presente.",
    "umbral": "Párrafo que declara que {nombre} es la primera generación que puede verlo — y que verlo es el primer acto de liberación."
  }},
  "carta_ancestros": {{
    "encuentro": "Párrafo en primera persona: {nombre} ve a sus ancestros, los nombra, los sitúa, los reconoce.",
    "comprension": "Párrafo: valida el contexto en que vivieron sin justificar el daño, reconociendo sus limitaciones.",
    "verdad": "Párrafo: les dice lo que necesitaban escuchar y nunca escucharon — el mensaje que el patrón buscaba comunicar.",
    "liberacion": "Párrafo: declara que ese ciclo termina. Agradece lo que transmitieron y anuncia lo que cambia."
  }},
  "practicas": [
    {{
      "nombre": "Nombre corto de la práctica",
      "instrucciones": "Instrucciones claras en 3-5 líneas. Accesible sin guía profesional.",
      "materiales": "Lo que se necesita — siempre simple y accesible",
      "frecuencia": "Cada cuánto y por cuánto tiempo"
    }},
    {{
      "nombre": "Segunda práctica",
      "instrucciones": "...",
      "materiales": "...",
      "frecuencia": "..."
    }},
    {{
      "nombre": "Tercera práctica",
      "instrucciones": "...",
      "materiales": "...",
      "frecuencia": "..."
    }}
  ]
}}

Reglas:
- Solo texto plano, sin markdown, sin asteriscos, sin guiones al inicio
- Lenguaje poético pero concreto — no clínico, no autoayuda genérica
- Primera persona para la carta (como si {nombre} escribiera)
- El mensaje de liberación habla a {nombre} directamente (segunda persona)
- Las prácticas son específicas para el patrón dominante: {dom_info.get('nombre', patron_dom)}
- Nunca uses lenguaje determinista — siempre de apertura
- Responde SOLO el JSON, sin texto adicional"""

    response = _get_gemini().models.generate_content(model="gemini-2.5-flash", contents=prompt)
    texto = response.text.strip()
    texto = re.sub(r"^```json\s*", "", texto)
    texto = re.sub(r"\s*```$", "", texto)
    texto = _sanitize_json(texto)
    return json.loads(texto)


# ─── Gráfico de barras ────────────────────────────────────────────────────────

def generar_grafico(scores: dict, patron_dom: str, patron_sec: str,
                    patron_ter: str | None) -> bytes:
    dominantes = {patron_dom, patron_sec}
    if patron_ter:
        dominantes.add(patron_ter)

    cats_sorted = sorted(CATEGORIAS, key=lambda c: scores.get(c["id"], 0), reverse=True)
    nombres = [c["nombre"].replace(" y ", "\ny ").replace(" de ", "\nde ") for c in cats_sorted]
    valores = [scores.get(c["id"], 0) for c in cats_sorted]
    colores = ["#c9a040" if c["id"] in dominantes else "#3d3020" for c in cats_sorted]

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#0f1710")
    ax.set_facecolor("#0f1710")

    bars = ax.barh(nombres, valores, color=colores, height=0.6, zorder=3)

    for bar, val in zip(bars, valores):
        if val > 0:
            ax.text(val + 0.08, bar.get_y() + bar.get_height() / 2,
                    f"{val:.1f}", va="center", ha="left",
                    color="#f0ead6", fontsize=9, fontweight="bold")

    ax.set_xlim(0, 5.5)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels(["1", "2", "3", "4", "5"], color="#7a6a50", fontsize=9)
    ax.tick_params(axis="y", colors="#f0ead6", labelsize=8)
    ax.spines[:].set_visible(False)
    ax.grid(axis="x", color="#2a2010", linewidth=0.8, zorder=0)
    ax.set_title("Mapa de Patrones de tu Árbol", color="#c9a040", fontsize=12,
                 fontweight="bold", pad=14)

    gold_patch = mpatches.Patch(color="#c9a040", label="Patrones dominantes")
    dark_patch = mpatches.Patch(color="#3d3020", label="Otros patrones")
    ax.legend(handles=[gold_patch, dark_patch], loc="lower right",
              framealpha=0, labelcolor="#f0ead6", fontsize=8)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor="#0f1710")
    buf.seek(0)
    img_bytes = buf.read()
    plt.close()
    return img_bytes


# ─── PDF ─────────────────────────────────────────────────────────────────────

def generar_pdf(nombre: str, scores: dict, patron_dom: str, patron_sec: str,
                patron_ter: str | None, intensidad: str, analisis: dict,
                grafico_bytes: bytes, respuestas: dict) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    dorado   = colors.HexColor("#c9a040")
    crema    = colors.HexColor("#f0ead6")
    oscuro   = colors.HexColor("#0f1710")
    tierra   = colors.HexColor("#3d2b1a")
    muted    = colors.HexColor("#7a6a50")

    estilo_titulo = ParagraphStyle("titulo", parent=styles["Heading1"],
                                   textColor=dorado, fontSize=22, spaceAfter=4,
                                   alignment=TA_CENTER, fontName="Helvetica-Bold")
    estilo_sub    = ParagraphStyle("sub", parent=styles["Normal"],
                                   textColor=muted, fontSize=11, spaceAfter=16,
                                   alignment=TA_CENTER)
    estilo_h2     = ParagraphStyle("h2", parent=styles["Heading2"],
                                   textColor=dorado, fontSize=13,
                                   spaceBefore=18, spaceAfter=8,
                                   fontName="Helvetica-Bold")
    estilo_body   = ParagraphStyle("body", parent=styles["Normal"],
                                   fontSize=10, leading=16, spaceAfter=10,
                                   textColor=colors.HexColor("#2d2010"),
                                   alignment=TA_JUSTIFY)
    estilo_cita   = ParagraphStyle("cita", parent=styles["Normal"],
                                   fontSize=10, leading=16, spaceAfter=10,
                                   textColor=colors.HexColor("#2d2010"),
                                   leftIndent=20, rightIndent=20,
                                   borderPad=8, alignment=TA_JUSTIFY)
    estilo_carta  = ParagraphStyle("carta", parent=styles["Normal"],
                                   fontSize=10, leading=17, spaceAfter=12,
                                   textColor=colors.HexColor("#1a1005"),
                                   leftIndent=10, rightIndent=10,
                                   fontName="Helvetica", alignment=TA_JUSTIFY)
    estilo_frase  = ParagraphStyle("frase", parent=styles["Normal"],
                                   fontSize=11, leading=17, spaceAfter=8,
                                   textColor=dorado, alignment=TA_CENTER,
                                   fontName="Helvetica-Oblique")

    story = []
    from datetime import date

    story.append(Paragraph("Mi Árbol, Mi Historia", estilo_titulo))
    story.append(Paragraph(f"Reporte de {nombre}  ·  {date.today().strftime('%d/%m/%Y')}", estilo_sub))
    story.append(Paragraph("<i>Lo que ves hoy no es tu destino. Es el origen de donde vienes.</i>", estilo_frase))
    story.append(Spacer(1, 0.4*cm))

    graf_buf = io.BytesIO(grafico_bytes)
    img = Image(graf_buf, width=16*cm, height=8*cm)
    img.hAlign = "CENTER"
    story.append(img)
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("Tus patrones dominantes", estilo_h2))
    _, intensidad_desc = get_intensidad(scores.get(patron_dom, 0))
    dom_info = CATEGORIAS_DESC.get(patron_dom, {})
    sec_info = CATEGORIAS_DESC.get(patron_sec, {})

    story.append(Paragraph(
        f"<b>1. {dom_info.get('nombre', patron_dom)}</b> — {intensidad.upper()} ({scores.get(patron_dom, 0):.1f}/5)",
        estilo_body))
    story.append(Paragraph(intensidad_desc, estilo_cita))
    story.append(Paragraph(
        f"<b>Qué mapea:</b> {dom_info.get('que_mapea', '')}", estilo_body))
    story.append(Paragraph(
        f"<b>Cómo aparece:</b> {dom_info.get('como_aparece', '')}", estilo_body))

    story.append(Spacer(1, 0.2*cm))
    _, sec_intensidad_nombre = get_intensidad(scores.get(patron_sec, 0))
    story.append(Paragraph(
        f"<b>2. {sec_info.get('nombre', patron_sec)}</b> ({scores.get(patron_sec, 0):.1f}/5)",
        estilo_body))
    story.append(Paragraph(
        f"<b>Qué mapea:</b> {sec_info.get('que_mapea', '')}", estilo_body))

    if patron_ter:
        ter_info = CATEGORIAS_DESC.get(patron_ter, {})
        story.append(Spacer(1, 0.1*cm))
        story.append(Paragraph(
            f"<b>3. {ter_info.get('nombre', patron_ter)}</b> ({scores.get(patron_ter, 0):.1f}/5)",
            estilo_body))

    story.append(HRFlowable(width="100%", thickness=0.5, color=dorado, spaceAfter=10))

    ml = analisis.get("mensaje_liberacion", {})
    story.append(Paragraph("Mensaje de Liberación", estilo_h2))
    for parrafo in [ml.get("reconocimiento",""), ml.get("origen",""), ml.get("umbral","")]:
        if parrafo:
            story.append(Paragraph(parrafo, estilo_body))

    story.append(HRFlowable(width="100%", thickness=0.5, color=dorado, spaceAfter=10))

    carta = analisis.get("carta_ancestros", {})
    story.append(Paragraph("Carta a mis Ancestros", estilo_h2))
    story.append(Paragraph("<i>Queridos ancestros,</i>", estilo_carta))
    for parrafo in [carta.get("encuentro",""), carta.get("comprension",""),
                    carta.get("verdad",""), carta.get("liberacion","")]:
        if parrafo:
            story.append(Paragraph(parrafo, estilo_carta))

    story.append(HRFlowable(width="100%", thickness=0.5, color=dorado, spaceAfter=10))

    story.append(Paragraph("Prácticas de Sanación", estilo_h2))
    for i, p in enumerate(analisis.get("practicas", []), 1):
        story.append(Paragraph(f"<b>{i}. {p.get('nombre','')}</b>", estilo_body))
        story.append(Paragraph(p.get("instrucciones", ""), estilo_cita))
        story.append(Paragraph(
            f"<b>Materiales:</b> {p.get('materiales','')}  ·  <b>Frecuencia:</b> {p.get('frecuencia','')}",
            estilo_body))

    story.append(HRFlowable(width="100%", thickness=0.5, color=dorado, spaceAfter=10))

    acto = ACTOS_SIMBOLICOS.get(patron_dom, {})
    story.append(Paragraph("El Acto Simbólico", estilo_h2))
    story.append(Paragraph(f"<b>{acto.get('titulo','')}</b>", estilo_body))
    story.append(Paragraph(acto.get("instrucciones", ""), estilo_cita))
    story.append(Paragraph(f"<i>Intención: {acto.get('intencion','')}</i>", estilo_frase))
    story.append(Paragraph(
        f"<b>Materiales:</b> {acto.get('materiales','')}  ·  {acto.get('duracion','')}",
        estilo_body))

    # Reflexiones del usuario
    from core.questions import CATEGORIAS as CATS, PREGUNTAS_TEXTO
    abiertas = []
    for cat in CATS:
        pid = cat["pregunta_abierta"]
        texto = respuestas.get(pid)
        if texto and str(texto).strip():
            abiertas.append((PREGUNTAS_TEXTO[pid], str(texto)))

    if abiertas:
        story.append(HRFlowable(width="100%", thickness=0.5, color=dorado, spaceAfter=10))
        story.append(Paragraph("Lo que ya sabías", estilo_h2))
        for pregunta, respuesta in abiertas:
            story.append(Paragraph(f"<i>{pregunta}</i>", estilo_body))
            story.append(Paragraph(f"<b>{respuesta}</b>", estilo_cita))

    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "<i>Conocer de dónde vienes no te condena a repetirlo. Te da la libertad de elegir a dónde vas.</i>",
        estilo_frase))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "Tu árbol es el mapa. El camino de vuelta a ti mismo es tuyo. "
        "Si quieres caminarlo acompañado, estoy aquí. — Juan Pablo",
        estilo_sub))

    doc.build(story)
    buf.seek(0)
    return buf.read()


# ─── Punto de entrada ─────────────────────────────────────────────────────────

def generar_reporte_completo(nombre: str, respuestas: dict, familia: list) -> dict:
    scores = calcular_puntajes(respuestas)
    patron_dom, patron_sec, patron_ter, intensidad, _ = determinar_patrones(scores)
    analisis = generar_analisis(nombre, scores, patron_dom, patron_sec, patron_ter,
                                intensidad, respuestas, familia)
    grafico = generar_grafico(scores, patron_dom, patron_sec, patron_ter)
    pdf = generar_pdf(nombre, scores, patron_dom, patron_sec, patron_ter,
                      intensidad, analisis, grafico, respuestas)
    acto = ACTOS_SIMBOLICOS.get(patron_dom, {})
    return {
        "scores": scores,
        "patron_dom": patron_dom,
        "patron_sec": patron_sec,
        "patron_ter": patron_ter,
        "intensidad": intensidad,
        "analisis": analisis,
        "grafico": grafico,
        "pdf": pdf,
        "acto": acto,
    }
