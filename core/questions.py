# ─── Categorías (en orden de presentación: de lo más neutro a lo más profundo) ─

CATEGORIAS = [
    {
        "id": "profesiones",
        "nombre": "Profesiones y Vocaciones",
        "icono": "⚒️",
        "preguntas_escala": [5, 6],
        "pregunta_abierta": 103,
        "pausa": "Lo que elegiste hacer con tu vida, ¿lo elegiste tú?",
    },
    {
        "id": "nombres",
        "nombre": "Nombres",
        "icono": "📜",
        "preguntas_escala": [3, 4],
        "pregunta_abierta": 102,
        "pausa": "Llevar el nombre de alguien es también, a veces, cargar su historia.",
    },
    {
        "id": "economico",
        "nombre": "Patrones Económicos",
        "icono": "🌾",
        "preguntas_escala": [13, 14],
        "pregunta_abierta": 107,
        "pausa": "La relación de tu árbol con el dinero vive también en ti.",
    },
    {
        "id": "migraciones",
        "nombre": "Migraciones y Pérdidas",
        "icono": "🌍",
        "preguntas_escala": [15, 16],
        "pregunta_abierta": 108,
        "pausa": "Perder una tierra, un país o una cultura deja una marca que pasa de generación en generación.",
    },
    {
        "id": "fechas_edades",
        "nombre": "Fechas y Edades",
        "icono": "🕰️",
        "preguntas_escala": [1, 2],
        "pregunta_abierta": 101,
        "pausa": "Las fechas que se repiten en un árbol no son coincidencia. Son el árbol hablándote.",
    },
    {
        "id": "enfermedades",
        "nombre": "Enfermedades y Cuerpo",
        "icono": "🫀",
        "preguntas_escala": [9, 10],
        "pregunta_abierta": 105,
        "pausa": "El cuerpo guarda lo que la mente no pudo procesar. Y lo transmite.",
    },
    {
        "id": "secretos",
        "nombre": "Secretos Familiares",
        "icono": "🤫",
        "preguntas_escala": [11, 12],
        "pregunta_abierta": 106,
        "pausa": "Los secretos no desaparecen. Se transmiten como un peso invisible.",
    },
    {
        "id": "relaciones",
        "nombre": "Patrones de Relación",
        "icono": "💞",
        "preguntas_escala": [7, 8],
        "pregunta_abierta": 104,
        "pausa": "Las historias de amor de tus ancestros viven en ti más de lo que crees.",
    },
]

# ─── Textos de preguntas ──────────────────────────────────────────────────────

PREGUNTAS_TEXTO = {
    1:   "¿Hay edades que aparecen como significativas en tu familia? (muertes, crisis, divorcios o enfermedades que ocurrieron a la misma edad en distintas generaciones)",
    2:   "¿Hay fechas del calendario que se repiten como cargadas — aniversarios de pérdidas, accidentes o eventos dolorosos?",
    3:   "¿Llevas el nombre de alguien del árbol, o te pusieron un nombre con una historia detrás?",
    4:   "¿Hay nombres que se repiten en tu familia a través de las generaciones?",
    5:   "¿Hay profesiones o roles que se repiten en tu árbol? (médicos, maestros, militares, comerciantes)",
    6:   "¿Hay una vocación o camino que estuvo 'prohibido' o al que nadie pudo acceder en tu familia?",
    7:   "¿Hay patrones que se repiten en las relaciones de pareja de tu árbol? (abandono, infidelidad, viudez temprana, matrimonios no elegidos)",
    8:   "¿Hay personas en tu árbol que vivieron solas, que nunca formaron pareja, o que la perdieron muy jóvenes?",
    9:   "¿Hay enfermedades o zonas del cuerpo que se repiten como frágiles en tu árbol?",
    10:  "¿Has tenido síntomas o enfermedades que también tuvo alguien de tu familia?",
    11:  "¿Hay algo en tu familia de lo que 'no se habla' — un tema, una persona, un evento?",
    12:  "¿Hay personas del árbol que fueron borradas — de quienes nadie sabe nada o de quienes se habla muy poco?",
    13:  "¿Hay un patrón de abundancia o escasez que se repite en tu árbol?",
    14:  "¿Hubo pérdidas económicas significativas en generaciones anteriores — negocios que quebraron, propiedades perdidas, ruinas?",
    15:  "¿Hubo migraciones, exilios o desplazamientos forzados en tu árbol?",
    16:  "¿Hay pérdidas de tierra, país, cultura o identidad que marcaron a generaciones anteriores?",
    101: "¿A qué edad estás tú ahora? ¿Sabes si algo ocurrió en tu árbol a esa misma edad?",
    102: "¿Hay alguien en tu árbol cuyo nombre se evita — alguien de quien 'no se habla'?",
    103: "¿Tu profesión o vocación fue elegida libremente, o siguió — conscientemente o no — un patrón familiar?",
    104: "¿En qué se parece tu historia de amor a la de alguno de tus ancestros?",
    105: "¿Qué parte de tu cuerpo suele fallar cuando estás bajo presión o en momentos de crisis?",
    106: "¿Qué crees que guarda tu familia en silencio — y cómo crees que ese silencio te ha afectado?",
    107: "¿Tu relación con el dinero se parece a la de algún ancestro? ¿En qué?",
    108: "¿Cómo crees que esas pérdidas o migraciones afectaron la forma en que tu familia se relaciona con el hogar, la seguridad o la pertenencia?",
}

ESCALA_LABELS = [
    "No se reconoce en mi árbol",
    "Quizás, no estoy seguro/a",
    "Algo de esto hay",
    "Sí, claramente",
    "Es un patrón muy evidente",
]

# ─── Intensidades ─────────────────────────────────────────────────────────────

def get_intensidad(score: float) -> tuple:
    if score <= 2.0:
        return "leve", "Este patrón existe en tu árbol de forma suave o poco visible."
    elif score <= 3.0:
        return "moderado", "Este patrón tiene presencia en tu árbol — hay algo ahí para mirar."
    elif score <= 4.0:
        return "intenso", "Este patrón es claramente visible en tu árbol y probablemente lo reconoces en tu propia vida."
    else:
        return "profundo", "Este patrón ha sido una fuerza central en las historias de tu árbol. Hay un trabajo importante aquí."

# ─── Catálogo de actos simbólicos ────────────────────────────────────────────

ACTOS_SIMBOLICOS = {
    "profesiones": {
        "titulo": "El camino elegido",
        "instrucciones": "Dibuja un árbol con las profesiones de tu familia — cada rama representa a un miembro y su camino. Luego dibuja una rama nueva, la tuya, que sale del mismo tronco pero va en su propia dirección. Escribe en esa rama nueva lo que tú has elegido, o lo que quieres elegir. Cuélgalo en un lugar visible durante al menos 7 días.",
        "intencion": "Esta rama es mía. Salgo del mismo árbol pero escribo mi propio camino.",
        "materiales": "Papel, lápiz o colores",
        "duracion": "20-30 minutos",
    },
    "nombres": {
        "titulo": "La carta al que te nombró",
        "instrucciones": "Escríbele una carta a la persona cuyo nombre cargas, o a quien cuya historia sientes que debes continuar. Dile que la ves, que la honras, y que a partir de hoy eliges escribir tu propia historia con tu propio nombre. Lee la carta en voz alta cuando la termines. Luego guárdala o quémala con esa intención.",
        "intencion": "Te veo. Te honro. Y elijo ser yo.",
        "materiales": "Papel y bolígrafo",
        "duracion": "30-45 minutos",
    },
    "economico": {
        "titulo": "El dinero que merezco",
        "instrucciones": "Busca un billete o moneda. Tenlo en tu mano, siente su peso, y di en voz alta: 'El dinero no es peligroso. No tengo que repetir la escasez de mi árbol. Puedo prosperar sin traicionar a nadie.' Repite este gesto cada mañana durante 7 días con la misma moneda. Al final del séptimo día, gasta esa moneda en algo pequeño que te guste.",
        "intencion": "Puedo prosperar sin traicionar a mi árbol.",
        "materiales": "Un billete o moneda cualquiera",
        "duracion": "3 minutos al día durante 7 días",
    },
    "migraciones": {
        "titulo": "Las raíces que elijo",
        "instrucciones": "Consigue un poco de tierra del lugar donde vives — de un jardín, una maceta, o un parque cercano. Sostén esa tierra en tus manos durante unos minutos. Siente su peso y temperatura. Di en voz alta: 'Este es mi hogar. Aquí echo raíces. La pérdida de mis ancestros no tiene que ser la mía.' Guarda esa tierra en un frasco o devuélvela al suelo.",
        "intencion": "Aquí echo raíces. Este es mi hogar.",
        "materiales": "Un puñado de tierra del lugar donde vives",
        "duracion": "10-15 minutos",
    },
    "fechas_edades": {
        "titulo": "El cumpleaños del patrón",
        "instrucciones": "Elige la fecha o edad que reconoces como cargada en tu árbol. En esa fecha — o en el próximo día que puedas dedicarle — escribe en un papel lo que ese momento significó para tu árbol. Luego escribe en otro papel lo que quieres que esa fecha signifique para ti a partir de hoy. Quema el primero. Guarda el segundo.",
        "intencion": "Esta fecha fue del árbol. A partir de hoy, también es mía.",
        "materiales": "Dos papeles, bolígrafo, y un recipiente seguro para quemar",
        "duracion": "20-30 minutos",
    },
    "enfermedades": {
        "titulo": "El cuerpo que no es tuyo",
        "instrucciones": "Pon una mano, con gentileza, sobre la zona del cuerpo que suele fallar. Cierra los ojos. Respira profundo. Di en voz alta: 'Este dolor no empezó conmigo. Lo recibo, lo reconozco, y elijo que termine aquí.' Repite este gesto durante 7 días, cada vez que notes tensión o molestia en esa zona.",
        "intencion": "Reconozco lo heredado. Elijo que termine aquí.",
        "materiales": "Solo tu cuerpo y tu voz",
        "duracion": "3-5 minutos al día durante 7 días",
    },
    "secretos": {
        "titulo": "Nombrar lo innombrable",
        "instrucciones": "Escribe en un papel lo que nunca se dijo en tu familia — el secreto, la persona borrada, el silencio que siempre estuvo ahí. No tienes que saber todo: escribe lo que intuyes o lo que sientes. Luego léelo en voz alta, a solas. Finalmente, quémalo con la intención de que ese silencio no pase a la siguiente generación.",
        "intencion": "Lo que no se nombra no desaparece. Yo lo nombro para que pueda terminar.",
        "materiales": "Papel, bolígrafo, y un recipiente seguro para quemar",
        "duracion": "30-45 minutos",
    },
    "relaciones": {
        "titulo": "El ritual de cierre del ciclo",
        "instrucciones": "Escribe en tres papeles separados las historias de amor del árbol que más resuenan en ti — las que reconoces, las que temes repetir. Lee cada una en voz alta. Luego escribe en un cuarto papel: 'Este ciclo termina conmigo. Puedo amar de otra manera.' Quema los primeros tres papeles. Guarda el cuarto en un lugar especial.",
        "intencion": "Este ciclo termina conmigo.",
        "materiales": "Cuatro papeles, bolígrafo, y un recipiente seguro para quemar",
        "duracion": "45-60 minutos",
    },
}

# ─── Descripciones de categorías para el reporte ─────────────────────────────

CATEGORIAS_DESC = {
    "profesiones": {
        "nombre": "Profesiones y Vocaciones",
        "que_mapea": "Repetición o prohibición de ciertos roles y caminos en el árbol",
        "como_aparece": "Elecciones vocacionales inconscientes, culpa al alejarse del camino familiar, vocaciones reprimidas",
    },
    "nombres": {
        "nombre": "Nombres",
        "que_mapea": "Carga de la historia de un ancestro a través de su nombre",
        "como_aparece": "Confusión de identidad, sentirse 'el continuador' de alguien, peso de una historia que no es propia",
    },
    "economico": {
        "nombre": "Patrones Económicos",
        "que_mapea": "Ciclos de abundancia o escasez, pérdidas de patrimonio, mandatos sobre el dinero",
        "como_aparece": "Autosabotaje económico, creencias limitantes sobre el merecimiento, miedo a prosperar",
    },
    "migraciones": {
        "nombre": "Migraciones y Pérdidas",
        "que_mapea": "Desplazamientos, exilios, pérdidas de tierra, cultura o identidad en el árbol",
        "como_aparece": "Dificultad para echar raíces, nostalgia sin objeto claro, duelos no resueltos transmitidos",
    },
    "fechas_edades": {
        "nombre": "Fechas y Edades",
        "que_mapea": "Repetición de momentos críticos a la misma edad o en las mismas fechas en distintas generaciones",
        "como_aparece": "Hipervigilancia ante ciertas edades, ansiedad en fechas específicas, sensación de estar en peligro a cierta edad",
    },
    "enfermedades": {
        "nombre": "Enfermedades y Cuerpo",
        "que_mapea": "Dolencias o zonas frágiles que se transmiten como metáfora de un dolor emocional no resuelto",
        "como_aparece": "Síntomas físicos recurrentes, zonas del cuerpo que siempre fallan, enfermedades que aparecen en las mismas etapas",
    },
    "secretos": {
        "nombre": "Secretos Familiares",
        "que_mapea": "Lo que no se nombra: personas borradas, eventos ocultos, silencios sostenidos por generaciones",
        "como_aparece": "Ansiedad difusa, sensación de que falta algo, lealtades invisibles a alguien del árbol",
    },
    "relaciones": {
        "nombre": "Patrones de Relación",
        "que_mapea": "Historias de amor que se repiten: abandono, infidelidad, pérdida temprana, vínculos no elegidos",
        "como_aparece": "Repetir el mismo tipo de vínculo, atraer parejas que repiten el patrón ancestral, miedo a la intimidad",
    },
}
