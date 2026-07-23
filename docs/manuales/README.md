# Documentación de Usuario — Colliers Nexus

Carpeta compartida con la documentación de usuario de Nexus. Los documentos se
entregan en **DOCX** y **PDF**, listos para guardar y enviar a los usuarios finales.

## Política del proyecto

**Todos los formularios del sistema** tienen su guía rápida de uso, no solo los que
se desarrollan o modifican. Cuando un formulario cambia, se **actualiza** su documento
(se sube la versión/fecha), no se crea uno nuevo. La documentación se mantiene siempre
sincronizada con la versión actual de Nexus.

## Formato: Guía Rápida (vigente)

Guía breve y sencilla para el usuario final. Cada guía contiene:

- **Título**: `Manual de Usuario - <Formulario>`
- **Versión** y **Fecha**
- **Objetivo** (2-3 líneas)
- **Campos**: cada campo con "Qué ingresar:" explicado en lenguaje de usuario
- **Al finalizar**: qué sucede al presionar Guardar / Crear

No incluye capturas, diagramas, arquitectura, código ni reglas técnicas.

### Guías disponibles

| Formulario | Archivos |
|------------|----------|
| Cuentas | `Guia_Cuentas.docx` / `.pdf` |
| Contactos | `Guia_Contactos.docx` / `.pdf` |
| Leads | `Guia_Leads.docx` / `.pdf` |
| Visitas | `Guia_Visitas.docx` / `.pdf` |
| Oficinas | `Guia_Oficinas.docx` / `.pdf` |
| Retail | `Guia_Retail.docx` / `.pdf` |
| Industria & Logística | `Guia_Industria_Logistica.docx` / `.pdf` |
| Componentes | `Guia_Componentes.docx` / `.pdf` |
| Oportunidades | *Pendiente — el formulario aún no está implementado ("Pronto").* |

## Cómo se generan

```bash
cd docs/manuales
pip install python-docx reportlab
python3 gen_guias.py     # regenera todas las guías (DOCX + PDF)
```

- `guia_base.py` — motor común (estilo Colliers + render DOCX y PDF).
- `gen_guias.py` — contenido de todas las guías (un bloque `Guia(...)` por formulario).

**Para actualizar** una guía tras un cambio en su formulario: editar su bloque en
`gen_guias.py`, subir la versión/fecha y volver a ejecutar.
**Para un formulario nuevo**: agregar su bloque `Guia(...)` y regenerar.

## Formato extendido (opcional)

Si en algún caso se necesita un manual más completo (10 secciones, con marcadores de
captura), están `manual_base.py` + `gen_manual_<modulo>.py`. Ejemplo: `Manual_Visitas`.
El formato por defecto es la Guía Rápida.
