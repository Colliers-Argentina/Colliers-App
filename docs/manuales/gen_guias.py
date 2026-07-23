#!/usr/bin/env python3
"""Guías Rápidas de Usuario — Colliers Nexus (todos los formularios).

Genera DOCX + PDF de cada formulario en docs/manuales/.
Para ACTUALIZAR una guía tras un cambio en su formulario: editar su bloque abajo,
subir la versión/fecha y volver a ejecutar. No crear archivos nuevos.
    python3 gen_guias.py
"""
import os
from guia_base import Guia

HERE = os.path.dirname(os.path.abspath(__file__))
FECHA = "23/07/2026"

GUIAS = {}

# ─────────────────────────── CUENTAS ───────────────────────────
GUIAS["Guia_Cuentas"] = Guia(
    "Cuentas", "1.2", FECHA,
    "Permite dar de alta y mantener las cuentas (empresas) con las que trabaja Colliers. "
    "Es la base del CRM: sobre las cuentas se cargan contactos, visitas y actividad comercial. "
    "Los usuarios comerciales ven un formulario reducido (Nombre comercial, Cliente Colliers, "
    "Unidades de negocio y Tipo de cuenta) para un alta rápida; los administradores ven el "
    "formulario completo. Es el mismo formulario que aparece al crear una cuenta desde otros módulos.",
    [
        ("Nombre comercial", "Nombre de la empresa."),
        ("Categoría", "Clasificación interna de la cuenta (Top, A, B, C o No aplica). Disponible solo para administradores."),
        ("Cliente Colliers", "Seleccionar \"Sí\" si la empresa alguna vez recibió un servicio de Colliers o firmó una exclusividad. Seleccionar \"No\" en caso contrario."),
        ("Rubro", "Seleccionar la actividad principal de la empresa. Disponible solo para administradores."),
        ("Sub rubro", "Seleccionar la actividad específica dentro del rubro. Disponible solo para administradores."),
        ("Unidades de negocio de interés", "Marcar los tipos de inmueble que le interesan a la empresa: Oficinas, Retail, Industria y/o Logística. Se puede elegir más de una."),
        ("Tipo de cuenta", "Indicar el tipo de empresa: Inmobiliaria, Desarrollador o Ninguno."),
        ("Creado por", "Se completa solo con el usuario que da de alta la cuenta. No hace falta escribir nada."),
    ],
    [
        "Se crea la Cuenta.",
        "Queda disponible para todos los usuarios autorizados.",
        "Puede editarse posteriormente según permisos.",
        "La ficha de la cuenta incluye una solapa Comentarios con historial cronológico.",
    ],
)

# ─────────────────────────── CONTACTOS ───────────────────────────
GUIAS["Guia_Contactos"] = Guia(
    "Contactos", "2.0", FECHA,
    "Permite registrar personas (contactos) y vincularlas a una cuenta. La ficha del contacto "
    "usa el mismo estilo que Cuentas, con solapas de Información General, Comentarios, "
    "Actividades, Inventario y Timeline.",
    [
        ("Cuenta asociada", "Buscar y seleccionar la empresa a la que pertenece el contacto. Si la empresa no existe todavía, al final de la lista aparece la opción \"➕ Crear nueva cuenta\": se crea en el momento, sin salir del formulario, y queda seleccionada."),
        ("Nombre", "Nombre de pila de la persona."),
        ("Apellidos", "Apellido de la persona."),
        ("Cargo segmentado", "Seleccionar el tipo de cargo: CEO, CFO, Compras, Real Estate u Otro."),
        ("Puesto", "Escribir el puesto tal cual figura (por ejemplo: Director Comercial). Campo libre."),
        ("Especificar cargo", "Solo si en Cargo se eligió \"Otro\": escribir el cargo concreto."),
        ("Inversor", "Indicar si la persona es inversor (Sí/No). Disponible solo para administradores."),
        ("Correo electrónico", "Email de la persona."),
        ("Estado del correo", "Indica si el correo es Funcional, Rebotado o Sin comprobar. Los ejecutivos comerciales no lo editan: se actualiza mediante importaciones masivas y los administradores pueden ajustarlo."),
        ("Teléfono", "Número de celular, sin el 11 y sin espacios (por ejemplo: 1551234567). Por privacidad, el teléfono solo lo ven el creador del contacto, los ejecutivos asignados y los administradores."),
        ("LinkedIn", "Dirección del perfil de LinkedIn. Disponible solo para administradores."),
        ("Ejecutivo(s) Comercial(es)", "Asignar hasta 3 ejecutivos responsables del contacto. Disponible solo para administradores."),
        ("Comentarios", "Observaciones sobre el contacto. La ficha tiene además una solapa Comentarios con historial cronológico, donde cualquier usuario puede sumar comentarios."),
    ],
    [
        "Se crea el Contacto y queda vinculado a la cuenta elegida.",
        "Aparece en la ficha de la cuenta, dentro de la solapa Contactos.",
        "Los ejecutivos comerciales pueden crear contactos, ver todos, registrar actividades y agregar comentarios; la edición y la administración quedan a cargo de los administradores.",
    ],
)

# ─────────────────────────── LEADS ───────────────────────────
GUIAS["Guia_Leads"] = Guia(
    "Leads", "2.1", FECHA,
    "Permite registrar oportunidades entrantes (consultas de posibles interesados) y seguir su "
    "ciclo comercial: desde su creación hasta la conversión en Contacto o su cierre. El lead "
    "maneja tres conceptos independientes: Clasificación (calidad al ingresar), Resultado "
    "(Pendiente/Próspero/No Próspero) y Estado (Activo/Inactivo).",
    [
        ("Nombre", "Nombre de la persona que hizo la consulta."),
        ("Apellido", "Apellido de la persona."),
        ("Email", "Correo electrónico de contacto (opcional). Si se completa, debe tener formato válido."),
        ("Teléfono móvil", "Número de celular de la persona (opcional). Se puede completar más adelante."),
        ("Empresa", "Empresa del interesado. Se puede buscar entre las cuentas existentes. Si no existe, aparece la opción \"➕ Crear nueva cuenta\" para crearla en el momento sin perder los datos del lead."),
        ("Puesto", "Puesto o rol de la persona (opcional)."),
        ("Tipo de inmueble", "Tipo de propiedad que busca (oficina, local, depósito, etc.)."),
        ("Clasificación", "Obligatorio. Indicar la calidad del lead al ingresar: Estándar o Calificado. No tiene valor por defecto."),
        ("Origen", "Cómo llegó la consulta: Zonaprop, Argenprop, Mercado Libre, Referido, LinkedIn, Web, Llamado, Email u Otro."),
        ("Ejecutivo Comercial asignado", "Ejecutivo que se hará cargo del seguimiento del lead."),
        ("Inmueble de interés", "Buscar y seleccionar el edificio/inmueble por el que consulta (opcional)."),
        ("Link de origen", "Pegar el enlace del aviso o publicación de donde surgió la consulta (opcional). Si se completa, debe ser una URL válida."),
        ("Comentarios", "Observaciones: superficie buscada, urgencia, detalles de la consulta."),
        ("Resultado (en la ficha)", "Se crea como Pendiente. Luego se actualiza a Próspero o No Próspero. Cuando es Próspero aparece la acción \"Convertir a Contacto\"; No Próspero conserva el lead como registro histórico."),
    ],
    [
        "Se crea el Lead con Resultado Pendiente y Estado Activo, asignado al ejecutivo indicado.",
        "Si pasa 14 días en Pendiente sin resolución, el lead pasa automáticamente a Inactivo (con recordatorios previos en los días 10 y 13). No se elimina.",
        "Al actualizar el Resultado (u otra acción comercial), un lead Inactivo vuelve a Activo.",
        "Con Resultado Próspero se puede convertir en Contacto reutilizando la cuenta asociada, sin duplicar información; el lead queda como registro histórico.",
    ],
)

# ─────────────────────────── VISITAS ───────────────────────────
GUIAS["Guia_Visitas"] = Guia(
    "Visitas", "1.1", FECHA,
    "Permite registrar de forma rápida las visitas comerciales realizadas a un inmueble en "
    "el marco de una cuenta. Cada visita queda asociada a la cuenta y al inmueble.",
    [
        ("Cuenta", "Buscar y seleccionar la empresa sobre la que se hizo la visita. Si no existe, aparece la opción \"➕ Crear nueva cuenta\" para crearla en el momento sin salir del formulario."),
        ("Inmueble", "Buscar y seleccionar el inmueble visitado."),
        ("Contacto", "Buscar y seleccionar la persona con la que se realizó la visita (opcional)."),
        ("Comentarios", "Observaciones de la visita: qué se habló, próximos pasos (opcional)."),
    ],
    [
        "Se registra la Visita.",
        "Se genera automáticamente una actividad \"Visita Comercial\" en la cuenta.",
        "La cuenta queda en estado Activa.",
        "La visita se puede ver en la cuenta y en la ficha del inmueble.",
    ],
)

# ─────────────────────────── OFICINAS ───────────────────────────
GUIAS["Guia_Oficinas"] = Guia(
    "Oficinas", "1.0", FECHA,
    "Permite dar de alta un edificio de oficinas en el inventario, con sus datos generales, "
    "superficies y enlaces a documentación.",
    [
        ("Nombre", "Nombre del edificio (por ejemplo: Torre Catalinas Norte)."),
        ("Etapa", "Estado del edificio: Proyecto, En Construcción o Existente."),
        ("Categoría", "Categoría del edificio: A+, A, B+, B o C."),
        ("Corredor", "Zona/submercado donde está ubicado el edificio."),
        ("Tipología", "Tipo constructivo (Perímetro Libre, Entre Medianeras, En Esquina, etc.)."),
        ("Dirección", "Domicilio del edificio."),
        ("Año", "Año de construcción o de finalización."),
        ("Pisos", "Cantidad de pisos del edificio."),
        ("Cocheras", "Cantidad total de cocheras."),
        ("Certificación", "Certificación ambiental o de calidad, si tiene (por ejemplo: LEED Gold)."),
        ("Ejecutivo Comercial responsable", "Ejecutivo a cargo del edificio."),
        ("Superficie total", "Metros cuadrados rentables totales."),
        ("Superficie propia", "Metros cuadrados de propiedad exclusiva."),
        ("Superficie promedio por piso", "Se calcula solo a partir de los datos cargados. No hace falta completarlo."),
        ("Superficie mínima", "Metros cuadrados mínimos alquilables."),
        ("Ficha / Brochure / Planos / Fotos", "Pegar los enlaces a la documentación del edificio, si están disponibles."),
    ],
    [
        "Se crea el edificio en el inventario de Oficinas.",
        "Queda disponible para asociarle componentes (unidades) y para usarlo en informes.",
        "Puede editarse posteriormente según permisos.",
    ],
)

# ─────────────────────── INDUSTRIA & LOGÍSTICA ───────────────────────
GUIAS["Guia_Industria_Logistica"] = Guia(
    "Industria & Logística", "1.0", FECHA,
    "Permite dar de alta un activo industrial o logístico en el inventario, con sus "
    "características técnicas y comerciales.",
    [
        ("Tipo de activo", "Seleccionar el tipo: Centro Logístico, Nave Industrial, Parque Industrial, Depósito, Terreno Industrial, Planta Productiva u Otro."),
        ("Nombre", "Nombre del activo industrial."),
        ("Dirección", "Domicilio del inmueble."),
        ("Localidad", "Localidad donde se ubica."),
        ("Provincia", "Provincia donde se ubica."),
        ("Corredor", "Zona logística/industrial (por ejemplo: GBA Norte, GBA Sur, Rosario)."),
        ("Etapa", "Estado del inmueble: Existente, En Construcción o Proyecto."),
        ("Categoría", "Categoría del activo: A, B o C."),
        ("Superficie de terreno", "Metros cuadrados del terreno."),
        ("Superficie cubierta", "Metros cuadrados cubiertos."),
        ("Superficie semicubierta", "Metros cuadrados semicubiertos."),
        ("Superficie de oficinas", "Metros cuadrados destinados a oficinas."),
        ("Altura libre", "Altura libre en metros."),
        ("Cantidad de docks", "Cantidad de dársenas/docks de carga."),
        ("Potencia eléctrica", "Potencia disponible en kVA."),
        ("Playa de maniobras", "Metros cuadrados de playa de maniobras."),
        ("Sprinklers", "Indicar si cuenta con sistema de sprinklers (Sí/No)."),
        ("Certificación", "Certificación ambiental o de calidad, si tiene."),
        ("Precio alquiler", "Precio de alquiler en USD por m²."),
        ("Precio venta", "Precio de venta en USD por m²."),
        ("Disponible", "Indicar si el inmueble está disponible (Sí/No)."),
    ],
    [
        "Se crea el activo en el inventario de Industria & Logística.",
        "Queda disponible para asociarle componentes y para usarlo en informes.",
        "Puede editarse posteriormente según permisos.",
    ],
)

# ─────────────────────────── RETAIL ───────────────────────────
GUIAS["Guia_Retail"] = Guia(
    "Retail", "1.0", FECHA,
    "Permite dar de alta un local comercial (retail) en el inventario, con sus medidas, "
    "superficies y condiciones comerciales.",
    [
        ("Nombre", "Nombre del local. Si se deja vacío, se usa la dirección."),
        ("Dirección", "Domicilio del local."),
        ("Corredor Retail", "Zona comercial donde se ubica (por ejemplo: Florida, Av. Santa Fe, Palermo Soho)."),
        ("Ciudad", "Ciudad donde se ubica el local."),
        ("Frente", "Metros de frente del local."),
        ("Fondo", "Metros de fondo del local."),
        ("Metros de vidriera", "Metros lineales de vidriera."),
        ("Superficie PB", "Metros cuadrados en planta baja."),
        ("Superficie SS", "Metros cuadrados en subsuelo."),
        ("Superficie PA", "Metros cuadrados en planta alta."),
        ("Alquiler", "Precio de alquiler en USD por mes."),
        ("Venta", "Precio de venta en USD."),
        ("Expensas", "Monto de expensas en USD por mes."),
        ("Disponible", "Indicar si el local está disponible (Sí/No)."),
    ],
    [
        "Se crea el local en el inventario de Retail.",
        "Queda disponible para asociarle componentes y para usarlo en informes.",
        "Puede editarse posteriormente según permisos.",
    ],
)

# ─────────────────────────── COMPONENTES ───────────────────────────
GUIAS["Guia_Componentes"] = Guia(
    "Componentes", "1.0", FECHA,
    "Los componentes son las unidades dentro de un inmueble (por ejemplo: los pisos o "
    "locales de un edificio). Se cargan desde la ficha del inmueble, en la solapa Componentes, "
    "completando una fila por cada unidad.",
    [
        ("Piso", "Piso en el que está la unidad."),
        ("Unidad", "Identificación de la unidad (por ejemplo: A, B, 101)."),
        ("Estado", "Situación de la unidad: Disponible, Ocupada, etc."),
        ("Ocupante", "Empresa o persona que ocupa la unidad. Se puede vincular a una cuenta existente."),
        ("Propietario", "Empresa o persona dueña de la unidad. Se puede vincular a una cuenta existente."),
        ("m²", "Metros cuadrados de la unidad."),
        ("Tipo de oferta", "Indicar si la unidad se ofrece en alquiler, venta o ambos."),
        ("Alquiler", "Precio de alquiler pedido."),
        ("Precio venta", "Precio de venta pedido."),
        ("Expensas", "Monto de expensas de la unidad."),
        ("Cocheras", "Cantidad de cocheras de la unidad."),
        ("Vencimiento de contrato", "Fecha de vencimiento del contrato, si la unidad está ocupada."),
        ("Observaciones", "Comentarios sobre la unidad."),
        ("Ejecutivo", "Ejecutivo comercial asignado a la unidad."),
    ],
    [
        "La unidad queda cargada dentro del inmueble.",
        "Se actualizan los totales y la disponibilidad del inmueble.",
        "Puede editarse o eliminarse posteriormente según permisos.",
    ],
)


def build_all():
    for basename, guia in GUIAS.items():
        d, p = guia.build(HERE, basename)
        print("OK:", os.path.basename(d), "|", os.path.basename(p))


if __name__ == "__main__":
    build_all()
