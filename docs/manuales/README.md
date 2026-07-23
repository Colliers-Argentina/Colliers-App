# Manuales de Usuario — Colliers Nexus

Carpeta compartida con los manuales de usuario de Nexus. Cada manual se entrega
en **DOCX** y **PDF**, listos para guardar y enviar a los usuarios finales.

## Regla del proyecto

Cada vez que se implementa **un formulario nuevo** o **una modificación relevante**
en Nexus, además del desarrollo se genera/actualiza su Manual de Usuario. Si el
manual ya existe, se **actualiza** (nueva fila en el Historial de cambios y nueva
versión) — nunca se duplica. La documentación se mantiene sincronizada con la
versión actual de Nexus.

## Estructura de cada manual (10 secciones)

1. Portada (logo, módulo, versión y fecha)
2. Objetivo del formulario
3. Paso a paso de uso
4. Capturas de pantalla numeradas del flujo
5. Explicación de todos los campos
6. Validaciones y reglas de negocio
7. Buenas prácticas
8. Resultado esperado al guardar
9. Preguntas frecuentes
10. Historial de cambios

## Cómo se generan

Los manuales se generan por código para que DOCX y PDF salgan siempre del mismo
contenido y no se desincronicen:

- `manual_base.py` — motor común (estilo Colliers + render DOCX y PDF).
- `gen_manual_<modulo>.py` — contenido de cada manual.

```bash
cd docs/manuales
pip install python-docx reportlab   # dependencias
python3 gen_manual_visitas.py       # genera Manual_Visitas.docx + .pdf
```

### Nota sobre las capturas (sección 4)

Las capturas se insertan como **marcadores numerados** (`[ CAPTURA n ]`) con la
descripción de qué debe mostrar cada una, porque no se pueden tomar screenshots
automáticos de la app en vivo (requiere login Google + Firebase). Para la versión
final, reemplazar cada marcador por la imagen real del flujo.

## Manuales disponibles

| Módulo | Archivos | Versión |
|--------|----------|---------|
| Visitas | `Manual_Visitas.docx` / `.pdf` | 1.0 |
