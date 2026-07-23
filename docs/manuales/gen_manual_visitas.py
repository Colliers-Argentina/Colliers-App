#!/usr/bin/env python3
"""Manual de Usuario — Módulo Visitas (Colliers Nexus). Genera DOCX + PDF.

Para ACTUALIZAR tras un cambio en el formulario: editar el contenido de abajo,
sumar una fila en HISTORIAL y volver a ejecutar. No crear un archivo nuevo.
    python3 gen_manual_visitas.py
"""
import os
from manual_base import Manual

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = "1.0"
FECHA = "23/07/2026"

HISTORIAL = [
    ["1.0", "23/07/2026",
     "Versión inicial. Alta del módulo Visitas, botón '+ Nueva Visita' en el Home, "
     "generación automática de Actividad Comercial en la Cuenta y solapa Actividades "
     "en la ficha de Inmueble.", "Equipo Nexus"],
]


def build():
    m = Manual("Módulo Visitas",
               "Registro de visitas comerciales · CRM Comercial", VERSION, FECHA)

    m.h1(2, "Objetivo del formulario")
    m.p("El módulo Visitas permite a los Ejecutivos Comerciales registrar, de forma rápida "
        "y simple, cada visita realizada a un inmueble en el marco de una cuenta. Cada visita "
        "queda guardada como un registro propio del sistema y, automáticamente, genera una "
        "Actividad Comercial dentro de la Cuenta asociada, reactivando su estado a 'Activa'. "
        "Además, la visita queda vinculada al inmueble para poder consultarse desde la ficha "
        "del edificio.")
    m.spacer()

    m.h1(3, "Paso a paso de uso")
    m.h2("Opción A — Desde el Home (acceso rápido)")
    m.steps([
        "Ingresá a Nexus con tu cuenta de Colliers.",
        "En la pantalla de inicio (Home), buscá la sección 'Accesos Rápidos'.",
        "Hacé clic en la tarjeta '📍 Nueva Visita' (botón 'Registrar').",
        "Se abre el formulario 'Nueva Visita'.",
    ])
    m.shot(1, "Home de Nexus con la tarjeta '📍 Nueva Visita' resaltada en Accesos Rápidos.")

    m.h2("Opción B — Desde el módulo Comercial")
    m.steps([
        "En el menú lateral, abrí el grupo 'Comercial'.",
        "Hacé clic en 'Visitas'. Se abre el listado de visitas registradas.",
        "Arriba a la derecha, hacé clic en el botón '+ Nueva Visita'.",
    ])
    m.shot(2, "Solapa 'Visitas' dentro del módulo Comercial, con el listado y el botón '+ Nueva Visita'.")

    m.h2("Completar y guardar el formulario")
    m.steps([
        "Campo 'Cuenta' (obligatorio): escribí el nombre de la cuenta y seleccionala del listado desplegable.",
        "Campo 'Inmueble' (obligatorio): escribí el nombre del inmueble y seleccionalo del listado.",
        "Campo 'Contacto' (opcional): si corresponde, buscá y seleccioná el contacto de la cuenta.",
        "Campo 'Comentarios' (opcional): agregá observaciones de la visita.",
        "Hacé clic en 'Registrar visita'. La visita se guarda y el formulario se cierra.",
    ])
    m.shot(3, "Formulario 'Nueva Visita' con los campos Cuenta e Inmueble completados.")
    m.shot(4, "Ficha de la Cuenta > solapa 'Actividades', mostrando la Actividad Comercial 'Visita Comercial' generada automáticamente.")
    m.shot(5, "Ficha del Inmueble > solapa 'Actividades', mostrando la visita registrada.")
    m.spacer()

    m.h1(4, "Capturas de pantalla del flujo")
    m.p("Las capturas numeradas (Figuras 1 a 5) están intercaladas en el paso a paso de la "
        "sección 3, en el punto exacto del flujo al que corresponden:")
    m.bullets([
        "Figura 1 — Acceso rápido desde el Home.",
        "Figura 2 — Listado de Visitas en el módulo Comercial.",
        "Figura 3 — Formulario 'Nueva Visita' completo.",
        "Figura 4 — Actividad automática generada en la Cuenta.",
        "Figura 5 — Visita visible en la ficha del Inmueble.",
    ])
    m.spacer()

    m.h1(5, "Explicación de todos los campos")
    m.table(
        ["Campo", "Tipo", "Obligatorio", "Descripción"],
        [
            ["Cuenta", "Buscador", "Sí", "Empresa/cuenta sobre la que se realiza la visita. Se elige de las cuentas existentes."],
            ["Inmueble", "Buscador", "Sí", "Edificio/inmueble visitado. Se elige del inventario de edificios."],
            ["Contacto", "Buscador", "No", "Persona de contacto de la cuenta. El listado se filtra por la cuenta elegida."],
            ["Comentarios", "Texto libre", "No", "Observaciones de la visita (temas tratados, superficie de interés, etc.)."],
            ["Usuario", "Automático", "—", "Usuario logueado que registra la visita. No se completa a mano."],
            ["Ejecutivo Comercial", "Automático", "—", "Se determina solo: ejecutivo del inmueble, o de la cuenta, o el usuario que registra."],
            ["Fecha y hora", "Automático", "—", "Momento exacto del registro. No se completa a mano."],
        ],
        widths=[1.4, 1.1, 1.0, 3.2],
    )
    m.spacer()

    m.h1(6, "Validaciones y reglas de negocio")
    m.bullets([
        "No se puede registrar una visita sin Cuenta: el campo se marca en rojo y no guarda.",
        "No se puede registrar una visita sin Inmueble: el campo se marca en rojo y no guarda.",
        "Al guardar, se crea automáticamente una Actividad Comercial del tipo 'Visita Comercial' dentro de la Cuenta.",
        "Esa actividad reactiva el estado de la Cuenta a 'Activa' (actualiza la fecha de última actividad comercial).",
        "La visita queda vinculada al Inmueble y se muestra en la solapa 'Actividades' de su ficha.",
        "El Contacto ofrecido en el buscador corresponde a la cuenta seleccionada.",
        "Los campos automáticos (usuario, ejecutivo, fecha y hora) no son editables por el usuario.",
    ])
    m.spacer()

    m.h1(7, "Buenas prácticas")
    m.bullets([
        "Registrá la visita el mismo día en que ocurre, para que la fecha refleje la realidad.",
        "Elegí siempre la cuenta y el inmueble desde el buscador (evitá homónimos o duplicados).",
        "Usá el campo Contacto cuando la visita se hizo con una persona concreta: mejora la trazabilidad.",
        "Escribí comentarios claros y accionables (qué se habló, próximos pasos).",
        "Si la cuenta o el inmueble no aparecen, verificá que estén cargados en sus módulos antes de registrar la visita.",
    ])
    m.spacer()

    m.h1(8, "Resultado esperado al guardar")
    m.bullets([
        "Se crea un registro de Visita en el sistema (colección 'visitas').",
        "Aparece una nueva Actividad Comercial 'Visita Comercial' en la ficha de la Cuenta (solapa Actividades).",
        "La Cuenta pasa (o se mantiene) en estado 'Activa'.",
        "La visita se lista en el módulo Comercial > Visitas.",
        "La visita se muestra en la ficha del Inmueble, solapa 'Actividades'.",
    ])
    m.spacer()

    m.h1(9, "Preguntas frecuentes")
    m.faq([
        ("¿Puedo registrar una visita sin elegir un contacto?",
         "Sí. El contacto es opcional; solo Cuenta e Inmueble son obligatorios."),
        ("¿Por qué no encuentro una cuenta o un inmueble en el buscador?",
         "Porque todavía no está cargado en su módulo. Primero creá la cuenta (Comercial > Cuentas) "
         "o el inmueble (Inmuebles), y luego registrá la visita."),
        ("¿Dónde veo las visitas que registré?",
         "En Comercial > Visitas (listado general), en la ficha de la Cuenta (solapa Actividades) "
         "y en la ficha del Inmueble (solapa Actividades)."),
        ("¿La visita cambia el estado de la cuenta?",
         "Sí. Al generarse la Actividad Comercial automática, la cuenta queda en estado 'Activa'."),
        ("¿Puedo editar o borrar una visita?",
         "En esta versión la visita se registra y se consulta. La gestión/edición de visitas "
         "se evaluará en futuras versiones."),
        ("¿Quién queda registrado como responsable?",
         "El sistema guarda automáticamente el usuario logueado que registró la visita y el "
         "Ejecutivo Comercial asociado (del inmueble, de la cuenta, o el propio usuario)."),
    ])
    m.spacer()

    m.h1(10, "Historial de cambios")
    m.table(["Versión", "Fecha", "Cambios", "Autor"], HISTORIAL, widths=[0.8, 1.0, 4.0, 1.0])

    docx, pdf = m.build(HERE, "Manual_Visitas")
    print("Generado:", docx, "|", pdf)


if __name__ == "__main__":
    build()
