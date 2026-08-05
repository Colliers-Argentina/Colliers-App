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
    "Contactos", "2.2", FECHA,
    "Permite registrar personas (contactos) y vincularlas a una cuenta. La ficha del contacto "
    "usa el mismo estilo que Cuentas, con solapas de Información General, Comentarios, "
    "Actividades, Inventario y Timeline.",
    [
        ("Cuenta asociada", "Buscar y seleccionar la empresa a la que pertenece el contacto. Si la empresa no existe todavía, al final de la lista aparece la opción \"➕ Crear nueva cuenta\": se crea en el momento, sin salir del formulario, y queda seleccionada."),
        ("Nombre", "Nombre de pila de la persona."),
        ("Apellidos", "Apellido de la persona."),
        ("Cargo", "Seleccionar el tipo de cargo: CEO, CFO, Compras, Real Estate u Otro."),
        ("Puesto", "Escribir el puesto tal cual figura (por ejemplo: Director Comercial). Campo libre."),
        ("Especificar cargo", "Solo si en Cargo se eligió \"Otro\": escribir el cargo concreto."),
        ("¿Es inversor?", "En la tarjeta 'Perfil Comercial': indicar Sí o No. Es obligatorio elegir una opción (no viene seleccionada por defecto)."),
        ("Unidad de negocio de interés", "Aparece solo si '¿Es inversor?' = Sí: seleccionar las unidades que le interesan (Oficinas, Retail, Industria & Logística)."),
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
    "Leads", "2.7", FECHA,
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
        ("Cargo", "Seleccionar el tipo de cargo (CEO, CFO, Compras, Real Estate u Otro), igual que en Contactos. Si se elige \"Otro\", especificar el cargo en el campo Puesto."),
        ("Puesto", "Aparece solo cuando en Cargo se elige \"Otro\": campo de texto para especificar el cargo (igual que en Contactos)."),
        ("Tipo de consulta", "Tipo de consulta realizada: Oficina, Industria, Depósito, Terreno, Retail, SPS, Valuaciones u Otros. Si se elige \"Otros\", aparece un campo para especificar la consulta."),
        ("Clasificación", "Obligatorio. Indicar la calidad del lead al ingresar: Estándar o Calificado. No tiene valor por defecto."),
        ("Requerimiento", "Caja de texto libre (entre Datos del Lead y Origen) para registrar el requerimiento inicial del cliente: qué busca, superficie, zona, presupuesto, plazos. En la ficha, si tiene contenido, se muestra arriba de todo; si está vacío, no se muestra."),
        ("Origen", "Cómo llegó la consulta: Zonaprop, Argenprop, Mercado Libre, Referido, LinkedIn, Web, Llamado, Email u Otro."),
        ("Ejecutivo(s) Comercial(es) asignado(s)", "Obligatorio. Se pueden asignar hasta 3 ejecutivos con el buscador predictivo (selección múltiple). Cada ejecutivo ve únicamente los leads que tiene asignados; los administradores ven toda la base."),
        ("Fecha de vencimiento y Countdown", "Cada lead tiene una fecha de vencimiento (30 días) y un contador de días restantes con semáforo: rojo 1–10, amarillo 11–20, verde 21–30. Se muestra en la lista y en el panel del lead."),
        ("Inmueble de interés", "Buscar y seleccionar el edificio/inmueble por el que consulta (opcional)."),
        ("Link de origen", "Pegar el enlace del aviso o publicación de donde surgió la consulta (opcional). Si se completa, debe ser una URL válida."),
        ("Comentarios", "Observaciones: superficie buscada, urgencia, detalles de la consulta."),
        ("Resultado (en la ficha)", "Se crea como Pendiente. Luego se actualiza a Próspero o No Próspero. Cuando es Próspero aparece la acción \"Convertir a Contacto\"; No Próspero conserva el lead como registro histórico."),
    ],
    [
        "Se crea el Lead con Resultado Pendiente y Estado Activo, asignado al ejecutivo indicado.",
        "Si pasa 14 días en Pendiente sin resolución, el lead pasa automáticamente a Inactivo (con recordatorios previos en los días 10 y 13). No se elimina.",
        "Al actualizar el Resultado (u otra acción comercial), un lead Inactivo vuelve a Activo.",
        "Con Resultado Próspero, 'Convertir a Contacto' abre el formulario completo de Contacto precargado con los datos del Lead; se completa lo que falte y recién al presionar 'Crear Contacto' se genera. Dentro del formulario se elige la cuenta: existente, nueva o vacío (Particular). Si se crea una cuenta nueva durante la conversión, queda vinculada al lead y su Empresa se actualiza en toda la interfaz. Antes de crear, avisa si ya existe un contacto con el mismo nombre y apellido. El lead queda como registro histórico y desaparece de la lista principal (accesible desde la vista 'Convertidos').",
        "El perfil Ejecutivo Comercial sólo puede cambiar el Estado, agregar/editar Comentarios y Convertir a Contacto; el resto de los datos los edita un administrador.",
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

# ─────────────────────────── OPORTUNIDADES ───────────────────────────
GUIAS["Guia_Oportunidades"] = Guia(
    "Oportunidades", "2.1", FECHA,
    "Centro de seguimiento de la gestión comercial. Cada oportunidad es una gestión entre una "
    "Cuenta y Colliers. Al ingresar se ven las Cuentas ordenadas por la actividad más reciente; "
    "los widgets superiores filtran la grilla. Crear o cambiar una oportunidad registra "
    "automáticamente una actividad en la Cuenta (y en el Contacto asociado).",
    [
        ("Cuenta", "Buscar y seleccionar la empresa de la oportunidad (obligatorio)."),
        ("Contacto principal", "Buscar y seleccionar el contacto de la cuenta (opcional). Si no hay, se continúa solo con la Cuenta."),
        ("Inmueble(s) asociado(s)", "Buscar y agregar uno o varios inmuebles relacionados (opcional)."),
        ("Estado", "Etapa de la gestión con cuatro estados: En gestión, En negociación, Ganada o Perdida."),
        ("Prioridad", "Atributo independiente del estado, con tres niveles: 🟢 Alta, 🟡 Media o ⚪ Baja. Reemplaza a los porcentajes de probabilidad (ya no se usan). Se elige del desplegable y se puede cambiar desde la grilla; se muestra como etiqueta en la lista y en Analytics."),
        ("Ejecutivo Comercial", "Ejecutivo responsable de la oportunidad (obligatorio)."),
        ("Actividad Comercial", "Acción comercial más relevante en curso: Visita comercial, Informe de alternativas o Propuesta de servicios. Al elegirla o cambiarla se registra automáticamente esa actividad en la Cuenta y el Contacto. Convive con el Estado (no lo reemplaza)."),
        ("Unidad de negocio", "Oficinas, Retail o Industria & Logística (opcional)."),
        ("Título / Nota", "Breve descripción de la oportunidad (opcional)."),
    ],
    [
        "Se crea la Oportunidad asociada a la Cuenta.",
        "Se registra automáticamente una actividad en la Cuenta y, si hay contacto, también en el Contacto.",
        "La Cuenta aparece en la grilla de Oportunidades, ordenada por la actividad más reciente.",
        "Desde la grilla se puede cambiar el Estado (la Probabilidad se ajusta sola) y esos cambios quedan registrados.",
        "Al pasar el estado a 'Ganada', la oportunidad aún no está finalizada: aparece un aviso destacado y el botón 'Completar cierre', que abre el formulario de Cierre de Transacción precargado. La Transacción queda vinculada a la Oportunidad (trazabilidad completa): Lead → Cuenta/Contacto → Oportunidad → Ganada → Cierre → Transacción.",
        "También se puede crear una oportunidad desde la ficha de la Cuenta (botón '+ Nueva oportunidad').",
    ],
)


# ─────────────────────────── CENTRO DE SOLICITUDES ───────────────────────────
GUIAS["Guia_Solicitudes"] = Guia(
    "Centro de Solicitudes", "1.7", FECHA,
    "Centraliza las solicitudes internas de todas las áreas de Colliers. Cada servicio tiene su "
    "propio formulario; el primero disponible es 'Ficha y Publicaciones – Oficinas'. Al enviar se "
    "genera un Ticket, se puede descargar un PDF corporativo y se notifica al responsable.",
    [
        ("Nueva Solicitud", "El alta se hace en dos pasos: 1) elegir el Servicio (por ahora 'Ficha y Publicaciones'); 2) elegir el Tipo de inmueble (Oficinas, Retail o Industria y Logística). En esta etapa solo está disponible Oficinas; el resto figura como 'Próximamente'. Según la opción elegida se abre el formulario correspondiente."),
        ("Carga guiada (wizard)", "El formulario de 'Ficha y Publicaciones – Oficinas' se completa en pasos, con la misma experiencia que el alta de Oficinas: 1) Información General, 2) Información Comercial, 3) Características, 4) Marketing, 5) Revisión y 6) Confirmación. Arriba se ve una barra de progreso; se avanza con 'Siguiente' y se puede volver con 'Atrás' sin perder datos. Cada paso valida solo sus campos obligatorios; no deja avanzar si faltan. En Revisión se ve el resumen y se puede volver a cualquier paso para corregir; al 'Finalizar' se genera la solicitud, el PDF, el historial y el aviso al responsable, y aparece la pantalla de confirmación con el número de solicitud."),
        ("Datos automáticos", "Solicitante, Broker y Fecha se toman solos del usuario logueado; no hay que cargarlos."),
        ("Cuenta", "Buscar la cuenta con el buscador inteligente. Si no existe, se puede crear en el momento (mismo flujo que en el resto de Nexus)."),
        ("Propietario", "Obligatorio y siempre asociado a un Contacto de Nexus (no se admite texto libre). Buscar el contacto; si no existe, usar '+ Crear nuevo contacto' (pide datos mínimos) y queda vinculado como propietario. Al enviar, el sistema ofrece completar luego la ficha del contacto."),
        ("Prioridad", "Definir la urgencia de la solicitud: Baja, Media, Alta o Urgente."),
        ("Inmueble asociado", "Buscar el inmueble con el buscador inteligente. Si no existe, usar '+ Crear nuevo inmueble' (solo pide Dirección y Tipo). Al enviar la solicitud, el sistema ofrece continuar completando la ficha del inmueble."),
        ("Tipo de transacción", "Alquiler, Venta o Ambas. Según lo elegido, en Condiciones Comerciales aparecen solo los precios que correspondan (alquiler y/o venta)."),
        ("Equipamiento y Servicios", "Para cada servicio (aire acondicionado, ascensor, seguridad, etc.) marcar Sí o No, indicando si el edificio cuenta con él."),
        ("Especificaciones de los equipos", "Campo de texto libre y opcional, debajo de Equipamiento y Servicios. Detallar características técnicas que no se representan con Sí/No (tipo de aire, capacidad del grupo electrógeno, cantidad de ascensores, certificaciones, etc.). Admite varias líneas y se incluye en el PDF."),
        ("Ejecutivo(s) Comercial(es) a cargo", "El usuario que crea la solicitud queda asignado automáticamente como primer ejecutivo. Se pueden agregar hasta 2 ejecutivos adicionales con el selector predictivo."),
        ("Superficies", "La Superficie Total debe ser mayor o igual a la Superficie Cubierta (pueden ser iguales). No se permiten valores negativos ni una superficie total en cero. Si no se cumple, el sistema resalta los campos y no deja enviar."),
        ("Fecha de requerimiento / entrega", "La fecha comprometida que se ingresa en el formulario se muestra luego como 'Fecha de entrega' en el panel lateral de la solicitud."),
        ("Descripción general", "Describir el edificio y el entorno. Este texto se usa para la publicación y la ficha."),
        ("Documentación", "Agregar todos los elementos necesarios indicando el tipo: Fotografías, Planos, Brochure, Video, Tour Virtual, Render u Otro. Se pueden sumar varios."),
        ("Acciones de Marketing", "Selección múltiple: Ficha técnica, Portales, Campaña Email, Redes Sociales, Cartelería, Video, Tour Virtual, Otro."),
        ("Estado", "Cada ticket tiene un estado: Pendiente, En proceso o Finalizada. Se puede cambiar desde la ficha del ticket."),
    ],
    [
        "Se crea el Ticket (por ejemplo, Solicitud #000001) con estado Pendiente.",
        "Se puede descargar un PDF corporativo con el formulario completo (botón PDF en la ficha del ticket).",
        "Se notifica automáticamente al responsable del servicio (cuando el correo está configurado).",
        "La solicitud queda en el historial; con 'Mis Solicitudes' cada usuario ve las suyas. El Timeline registra creación, cambios de estado y comentarios.",
    ],
)


def build_all():
    for basename, guia in GUIAS.items():
        d, p = guia.build(HERE, basename)
        print("OK:", os.path.basename(d), "|", os.path.basename(p))


if __name__ == "__main__":
    build_all()
