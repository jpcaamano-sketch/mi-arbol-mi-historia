import resend
from core.config import RESEND_API_KEY, FROM_EMAIL


def _send(to: str, subject: str, html: str, attachments: list = None):
    resend.api_key = RESEND_API_KEY
    params = {"from": FROM_EMAIL, "to": [to], "subject": subject, "html": html}
    if attachments:
        params["attachments"] = attachments
    resend.Emails.send(params)


def enviar_reporte(nombre: str, correo: str, link: str, pdf_bytes: bytes):
    import base64
    html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#0f1710;font-family:Georgia,serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="padding:30px 0;">
<tr><td align="center">
<table width="580" cellpadding="0" cellspacing="0"
       style="background:#1a1205;border-radius:12px;overflow:hidden;border:1px solid #3d2b1a;">
  <tr>
    <td style="background:linear-gradient(135deg,#1a1005,#2d1f08);padding:40px;text-align:center;border-bottom:1px solid #3d2b1a;">
      <div style="font-size:36px;margin-bottom:12px;">🌳</div>
      <h1 style="margin:0;color:#c9a040;font-size:24px;font-family:Georgia,serif;">
        Mi Árbol, Mi Historia
      </h1>
      <p style="margin:12px 0 0;color:#7a6a50;font-size:13px;font-style:italic;">
        Tu reporte de metagenealogía está listo
      </p>
    </td>
  </tr>
  <tr>
    <td style="padding:36px 40px;">
      <p style="margin:0 0 16px;color:#c9a040;font-size:16px;font-family:Georgia,serif;">
        Querido/a <strong>{nombre}</strong>,
      </p>
      <p style="margin:0 0 16px;color:#b09870;font-size:14px;line-height:1.8;font-family:Georgia,serif;">
        Has completado tu recorrido por los patrones de tu árbol genealógico.
        Tu reporte personal está adjunto a este correo en PDF.
      </p>
      <p style="margin:0 0 16px;color:#b09870;font-size:14px;line-height:1.8;font-style:italic;font-family:Georgia,serif;">
        "Lo que ves hoy no es tu destino. Es el origen de donde vienes."
      </p>
      <p style="margin:0 0 24px;color:#b09870;font-size:14px;line-height:1.8;font-family:Georgia,serif;">
        También puedes ver tu reporte completo en línea en cualquier momento:
      </p>
      <div style="text-align:center;margin:24px 0;">
        <a href="{link}"
           style="display:inline-block;background:#c9a040;color:#0f1710;
                  text-decoration:none;padding:14px 36px;border-radius:6px;
                  font-weight:700;font-size:15px;font-family:Georgia,serif;">
          Ver mi reporte →
        </a>
      </div>
      <p style="margin:24px 0 0;color:#7a6a50;font-size:13px;text-align:center;font-style:italic;font-family:Georgia,serif;">
        Tu árbol es el mapa. El camino de vuelta a ti mismo es tuyo.<br>
        — Juan Pablo Caamaño
      </p>
    </td>
  </tr>
  <tr>
    <td style="background:#0f1005;padding:16px;text-align:center;border-top:1px solid #2d2010;">
      <p style="margin:0;color:#3d3020;font-size:11px;font-family:Georgia,serif;">
        Mi Árbol, Mi Historia · jpecoachdevida.cl
      </p>
    </td>
  </tr>
</table>
</td></tr>
</table>
</body></html>"""

    attachment = {
        "filename": f"mi_arbol_mi_historia_{nombre.lower().replace(' ','_')}.pdf",
        "content": base64.b64encode(pdf_bytes).decode(),
    }
    _send(correo, f"Tu árbol te habla, {nombre} — Reporte Mi Árbol, Mi Historia 🌳",
          html, attachments=[attachment])
