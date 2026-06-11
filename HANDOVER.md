# HANDOVER TÉCNICO — COLLIERS NEXUS
**Última actualización:** Junio 2026 · Para nuevo Claude Code · Sin acceso a conversaciones anteriores

> **Nota de versión:** Este documento fue actualizado para reflejar el estado REAL del código. La versión anterior describía el módulo Leads como "placeholder / Próximamente (30%)" — eso quedó **obsoleto**: el módulo Leads ya está **completo y funcional** (ver sección 10). Ante cualquier discrepancia, **el código es la fuente de verdad**.

---

## 1. RESUMEN EJECUTIVO

### ¿Qué es Colliers Nexus?
SaaS inmobiliario propietario de Colliers Argentina. Plataforma de gestión comercial 360° para el equipo de brokers. Centraliza inventario inmobiliario (Oficinas, Industrial, Retail), CRM, generación de presentaciones PPT y analytics.

### Objetivo del sistema
Permitir que los brokers de Colliers Argentina gestionen desde un solo lugar:
- Inventario de activos inmobiliarios disponibles
- Pipeline comercial (leads, cuentas, contactos)
- Generación automática de propuestas PPT para clientes
- Análisis de demanda y comportamiento del mercado

### Estado actual del proyecto
- **Frontend:** 100% funcional y en producción
- **Backend (Firebase):** 100% operativo
- **Dashboard Home:** Rediseñado completamente como "Centro de Operaciones Comerciales" — funcional
- **Módulo Inventario:** Oficinas/Industrial/Retail como módulos independientes — funcional
- **CRM:** Cuentas + Contactos + **Leads** funcionales
- **Generador PPT:** Funcional, usa Google Sheets como fuente de datos
- **Analytics:** Funcional, acceso restringido por whitelist de emails
- **Transacciones:** Funcional

### Nivel de avance estimado: ~90%

**Pendiente relevante:** integración email (EmailJS con keys vacías), Google Maps API key para geocodificación, fichas automáticas por edificio, módulo Oportunidades, módulo de documentos (Storage).

---

## 2. ARQUITECTURA GENERAL

### Stack técnico
```
Frontend:    HTML5 + CSS3 + Vanilla JS (ES6+) — UN SOLO ARCHIVO: index.html (~12.200 líneas)
Backend:     Firebase Firestore (compat SDK v10.7.1) — modo: db.collection(...)
Auth:        Google Identity Services (GSI) — OAuth2 con cuentas Google
Mapas:       Leaflet.js 1.9.4 + Leaflet.markercluster 1.5.3, tiles CartoDB Voyager
PPT:         PptxGenJS 3.12.0
Charts:      Chart.js 4.4.0
Storage:     Firebase Storage (compat v10.7.1)
Deploy:      Vercel — push a main = autodeploy (no build step, no npm)
```

### Regla más importante
**NO hay build system. NO hay npm. NO hay framework.** Todo el CSS, HTML y JavaScript está inline en un único archivo `index.html`. Cualquier modificación va directamente en ese archivo.

### Interacción entre componentes
```
Usuario navega → showModule(mod) → muestra panel HTML correspondiente
                                 → dispara función de carga (loadBuildings, loadCRM, etc.)
                                 → función fetch Firestore con db.collection()
                                 → renderiza HTML con innerHTML
```

### CDN dependencies (orden en <head>)
1. Leaflet 1.9.4 — mapas
2. Leaflet.markercluster 1.5.3 — clustering de marcadores
3. PptxGenJS 3.12.0 — generación de PPTs
4. Chart.js 4.4.0 — gráficos de analytics
5. Google Identity Services (async) — autenticación
6. EmailJS browser@3 — email (integración incompleta, keys vacías)
7. Firebase App compat 10.7.1
8. Firebase Firestore compat 10.7.1
9. Firebase Storage compat 10.7.1
10. Google Fonts Open Sans (CSS)
11. Leaflet CSS + MarkerCluster CSS

### Firebase config (hardcodeada en index.html ~línea 4330)
```javascript
const FIREBASE_CONFIG = {
  apiKey:            "AIzaSyDmV3KCBD0euDgtbw2nQ-ynw2aB_CDGq-A",
  authDomain:        "colliers-alternativas-1db71.firebaseapp.com",
  projectId:         "colliers-alternativas-1db71",
  storageBucket:     "colliers-alternativas-1db71.firebasestorage.app",
  messagingSenderId: "272619762449",
  appId:             "1:272619762449:web:ce885bddd1aa1fb9b892b0"
};
```

### Vercel config (`vercel.json`)
- Rewrite: todas las rutas → `/index.html` (SPA routing)
- Cache: `no-cache, no-store` en todos los assets (forzar actualización)
- Deploy automático en push a `main`

---

## 2-BIS. AUTENTICACIÓN Y DOMINIOS PERMITIDOS

### Control de acceso por dominio (~línea 4323)
```javascript
const ALLOWED_DOMAINS = ["gmail.com","colliers.com.ar","colliers.com"];
```

El login con Google solo permite cuentas cuyo email termine en alguno de esos dominios. La verificación está en `handlePayload(payload)`:
```javascript
if(!payload.email||!ALLOWED_DOMAINS.some(d=>payload.email.endsWith('@'+d))){
  // muestra pantalla "Acceso denegado" (#ds)
  return;
}
```

> **Histórico:** Antes era una sola constante `const DOM = "gmail.com"` que solo permitía `@gmail.com`. Se migró a `ALLOWED_DOMAINS` (array) para habilitar las cuentas corporativas `@colliers.com.ar` y `@colliers.com`.

> **Importante:** habilitar un dominio acá NO basta si el **CLIENT_ID de Google OAuth** (Google Cloud Console) no tiene permitido ese dominio de Google Workspace. Si un usuario corporativo no puede entrar pese a estar en `ALLOWED_DOMAINS`, revisar la configuración del OAuth Consent Screen / orígenes autorizados en Google Cloud.

---

## 3. ESTRUCTURA DE MÓDULOS

### Navegación principal — `showModule(mod)`
```javascript
// Valores válidos de mod:
'home'          → #home-hub
'office'        → #buildings-panel, _bldAssetType='office'
'industrial'    → #buildings-panel, _bldAssetType='industrial'
'retail'        → #buildings-panel, _bldAssetType='retail'
'crm'           → #crm-panel, tab cuentas
'crm-cuentas'   → #crm-panel, tab cuentas
'crm-contactos' → #crm-panel, tab contactos
'crm-leads'     → #crm-panel, tab leads
'generator'     → #as (panel generador PPT)
'analytics'     → #analytics-panel (GUARDED)
'admin'         → #admin-panel (GUARDED)
'transacciones' → #transacciones-panel
```

### Sidebar — grupos y ítems
```
Home
  └─ Dashboard

Comercial
  ├─ Leads (crm-leads)
  ├─ Contactos (crm-contactos)
  ├─ Cuentas (crm-cuentas)
  ├─ Oportunidades [DESHABILITADO - Coming Soon]
  └─ Transacciones

Inmuebles
  ├─ Oficinas (office)
  ├─ Industrial (industrial)
  └─ Retail (retail)

Presentaciones
  └─ Generador de Alternativas (generator)

Analytics [SOLO ANALYTICS_ALLOWED]
  ├─ Inteligencia Comercial
  ├─ Heatmaps
  ├─ Dashboard Brokers
  ├─ Tendencias
  └─ Rankings (incluye Funnel de Leads)

Administración [SOLO ANALYTICS_ALLOWED]
  ├─ Usuarios
  ├─ Configuración [DESHABILITADO]
  ├─ Base de Datos [DESHABILITADO]
  └─ Logs [DESHABILITADO]
```

### Estado detallado por módulo

| Módulo | Estado | Notas |
|--------|--------|-------|
| Home/Dashboard | ✅ Completo | Rediseñado full-width, 7 secciones, datos live Firestore |
| Inventario - Oficinas | ✅ Completo | Wizard 4 pasos, grid/lista/mapa, editor completo |
| Inventario - Industrial | ✅ Completo | Wizard 5 pasos (tipo picker incluido), tipoActivo en Firestore |
| Inventario - Retail | ✅ Completo | Wizard 3 pasos |
| CRM - Cuentas | ✅ Completo | CRUD, detalle con 9 tabs, contactos vinculados |
| CRM - Contactos | ✅ Completo | CRUD, vinculación a cuenta, timeline |
| CRM - Leads | ✅ Completo | CRUD, drawer crear/editar, detalle con timeline, estados, motivos de descarte, convertir a contacto, notificaciones, analytics funnel |
| Generador PPT | ✅ Funcional | Wizard chat, Sheet CSV como fuente, exporta PPT |
| Analytics | ✅ Funcional | 5 submodulos, filtros avanzados, solo whitelist |
| Transacciones | ✅ Funcional | CRUD, estados, cálculo de totales |
| Admin | ✅ Básico | Lista registros de descargas |

---

## 4. FIRESTORE — COLECCIONES

### `buildings`
**Propósito:** Inventario de activos inmobiliarios (Oficinas + Industrial + Retail)

**Campos principales:**
```javascript
// Comunes a todos los tipos
nombre, direccion, localidad, provincia,
assetType,          // 'office' | 'industrial' | 'retail'  ← CLAVE para clasificación
_tipo,              // legacy: 'industrial' | 'retail' (office = ausente)
activo,             // boolean — false = eliminado lógico
estado,             // 'Disponible' | 'Ocupado' | 'En construcción'
disponible,         // boolean
zona, corredor, submercado,  // aliases entre sí según módulo
categoria, cat,     // 'A+', 'A', 'B+', 'B', etc.
foto, imageUrl,     // URL de imagen
lat, lng,           // coordenadas para mapa
superficieTotal, superficieCubierta,
askingRent, precioAlquilerM2,
createdAt, updatedAt,  // Timestamps
_source,            // 'manual' | 'sheets'

// Solo Oficinas
pisos, cantPisos, cocheras, certificacion,
superficieMinima, superficieMaxima,

// Solo Industrial
tipoActivo,        // 'Centro Logístico' | 'Nave Industrial' | etc.
alturaLibre, cantidadDocks, potenciaElectrica,
playaManiobras, sprinklers, superficieTerreno,
superficieSemicubierta, superficieOficinas,

// Solo Retail
corredor,          // corredor comercial
formatoLocal,      // 'Local', 'Esquina', etc.
```

**Subcolecciones por documento:**
- `buildings/{id}/units` — pisos/unidades individuales (fields: estado, piso, supunitaria, rent, etc.)
- `buildings/{id}/history` — historial de cambios
- `buildings/{id}/timeline` — eventos
- `buildings/{id}/documentos` — archivos adjuntos (Storage refs)

**Clasificación legacy (backward compat):**
```javascript
const classify = d => d.assetType || (d._tipo==='industrial' ? 'industrial' : d._tipo==='retail' ? 'retail' : 'office');
```

---

### `clientes`
**Propósito:** Cuentas/empresas del CRM (también referenciada como "cuentas" en UI). **NO renombrar** — la colección se llama `clientes` aunque la UI diga "Cuentas".

**Campos principales:**
```javascript
nombre, razonSocial, categoria,
ubicacionPrincipal, clienteColliers,
propietarioOcupante, contactoPrincipal, cargo,
emailContacto, telefono, sitioWeb,
rubro, subRubro, bu,
esBroker, cuentaCorporativa, esDesarrollador, esAdministradora,
brokerCreador,
pptsGenerados, cantidadPPTs,
fechaCreacion, ultimaActividad  // Timestamps
```

---

### `contactos`
**Propósito:** Personas vinculadas a cuentas

**Campos principales:**
```javascript
cuentaId,          // → clientes.id
cuentaNombre,
nombre, apellidos,
cargo, puesto, propietario,
email, estadoCorreo,   // 'funcional' | 'sin_comprobar' | 'rebotado'
telefono, interno, linkedin,
inversor, prefsInversion[], volumenInversion,
comentarios,
brokerResponsable,
fechaCreacion, ultimoContacto, ultimaActividad
```

---

### `leads`
**Propósito:** Pipeline comercial. **Módulo COMPLETO y funcional** (ver sección 10).

**Campos principales (escritos por `saveLeadDrawer`):**
```javascript
nombre, apellido, email, telefono,
empresa, puesto,
origen,            // 'Zonaprop'|'Argenprop'|'Referido'|'LinkedIn'|'Web'|'Llamado'|'Email'|'Otro'
tipoInmueble,      // tipo de inmueble consultado
buildingId, buildingName,  // inmueble consultado (vinculado a buildings)
brokerAsignado,    // 'Matienzo'|'Bartra'|'Farola'|'Troncoso'|'Giancontieri'|'Zuliani'
linkOrigen,        // link al aviso/origen
comentarios,
estado,            // ver LEAD_ESTADOS abajo
estadoRegistro,    // 'activo' | 'archivado'
motivoDescarte,    // si estado='Descartado'
creadoPor, usuarioUltimaModificacion,
fechaCreacion, ultimaActividad, ultimaModificacion  // Timestamps
```

**Estados del lead (`LEAD_ESTADOS`):**
```javascript
['Nuevo','Intento de contacto','Contactado','Calificado',
 'Visita coordinada','Visita realizada','Propuesta enviada',
 'Descartado','Convertido']
```

**Motivos de descarte (`LEAD_DESCARTE`):**
```javascript
['No responde','No interesado','Ya cerró operación',
 'Fuera de presupuesto','Datos inválidos','Otro']
```

**Subcolección:** `leads/{id}/timeline` — historial de actividad del lead (escrito por `addLeadTimeline`).

---

### `contactoTimeline`
**Propósito:** Historial de actividad de contactos
```javascript
contactoId,   // → contactos.id
tipo, descripcion, fecha, usuario
```

---

### `descargas`
**Propósito:** Registro de PPTs generados (fuente de datos de Analytics)

**Campos principales:**
```javascript
tipo,           // 'ficha_comercial' | etc.
edificio, buildingId, edificioNombre,
usuario, email, broker, brokerEmail, userEmail,
clienteNombre, cliente,
corredor, zona, submercado,
supMin, supMax, supReq,
categoria, cat,
fecha,          // Timestamp
```

---

### `transacciones`
**Propósito:** Transacciones inmobiliarias cerradas o en curso

**Campos principales:**
```javascript
estado,    // 'abierta' | 'cerrada' | 'Cerrada'
fecha,     // Timestamp
// + campos de operación (monto, tipo, partes, etc.)
```

---

### `feedback`
**Propósito:** Feedback de usuarios — standalone, no tiene relaciones

### `timeline`
**Propósito:** Eventos CRM generales por cliente

### `history`
**Propósito:** Historial de cambios de edificios (audit trail)

### `sheets`
**Propósito:** Datos sincronizados desde Google Sheets (flag `_source:'sheets'`)

---

## 5. FIREBASE STORAGE

**Bucket:** `colliers-alternativas-1db71.firebasestorage.app`

**Estructura de carpetas:**
```
buildings/
  └── {buildingId}/
        └── docs/
              └── {filename}     ← PDFs, planos, brochures, fichas
```

**Operaciones en código:**
```javascript
// Upload
const ref = storage.ref(`buildings/${buildingId}/docs/${safeName}`);
await ref.put(file);
const url = await ref.getDownloadURL();

// Delete
await storage.ref(storageRef).delete();
```

**Assets estáticos (NO en Firebase Storage):**
- `home-bg.jpg` — fondo del dashboard
- `login-bg.jpg` — fondo del login
- `colliers-logo-white.png` — logo en sidebar
- Imágenes PPT en CDN externo: `https://raw.githubusercontent.com/mazaretto-wq/colliers-fotos/main/`

---

## 6. MÓDULO INVENTARIO — ARQUITECTURA

### Un solo panel HTML, tres modos
**Panel:** `#buildings-panel` — es el mismo para Oficinas, Industrial y Retail.

**Variable de control:** `let _bldAssetType = 'office'` — cambia según módulo seleccionado.

### Cómo funciona la diferenciación
```javascript
showModule('industrial')
→ _bldAssetType = 'industrial'
→ show('buildings-panel')
→ loadBuildings()           // filtra Firestore por assetType
→ _bldAdaptUI()             // adapta títulos, botones, filtros

// Clasificación de documentos (backward compat):
const classify = d =>
  d.assetType ||
  (d._tipo==='industrial' ? 'industrial' :
   d._tipo==='retail'     ? 'retail'     : 'office');
```

### UI Adaptation (`_bldAdaptUI()`)
Cambia dinámicamente: título de sección, texto del botón "Nuevo activo", filtros del filter bar (distintos por tipo), columnas de la tabla lista, cards de KPIs, labels del editor.

### Filtros por tipo
| Tipo | Filtros disponibles |
|------|-------------------|
| Oficinas | Categoría, Tipo de Oferta (pills) |
| Industrial | Localidad, Provincia, m² min/max, Disponible |
| Retail | Corredor, Ciudad, m² rango, Disponible |

### Wizards de creación
**Oficinas** — 4 pasos: General / Pisos / Características / Comercial

**Industrial** — 5 pasos:
1. **Tipo** (picker: Centro Logístico, Nave Industrial, Parque Industrial, Depósito, Terreno Industrial, Planta Productiva, Otro)
2. **General**, 3. **Superficies**, 4. **Características**, 5. **Comercial**
```javascript
let _indWizSubtipo = '';
const IND_WIZ_STEPS = 5;
const IND_WIZ_LABELS = ['Tipo','General','Superficies','Características','Comercial'];
```

**Retail** — 3 pasos: General / Características / Comercial
```javascript
const RET_WIZ_STEPS = 3;
const RET_WIZ_LABELS = ['General','Características','Comercial'];
```

### Vistas disponibles
- `'grid'` — cards con foto · `'list'` — tabla · `'map'` — Leaflet con clustering

---

## 7. DASHBOARD HOME

### Estructura (full-width, max 1440px)
1. **Hero** — Saludo personalizado, badge de alertas, hora de actualización, total de registros activos
2. **Accesos Rápidos** — 8 cards: Oficinas / Industrial / Retail / Leads / Cuentas / Contactos / PPTs / Analytics (admin only)
3. **Resumen del Mercado** — 3 columnas (Oficinas / Industrial / Retail) con stats, vacancia, precio promedio, insights
4. **Insights Comerciales** — 4 cards: Zona Caliente / Edificio más enviado / Broker Líder / Demanda m² (de `descargas`)
5. **Actividad Reciente + Radar Comercial** — timeline de últimas 10 acciones + texto contextual
6. **KPIs Operacionales** — 6 mini-cards
7. **Alertas** (SOLO si hay alertas > 0): Leads sin contactar / Sin actividad +14d / Tx cerradas mes / Nuevos inmuebles / PPTs 7d

### Funciones principales
```javascript
renderHubCards()           // accesos rápidos + dispara carga
_loadHubDashboardData()    // un solo fetch paralelo de TODO
_renderHubMarket()         // Resumen del Mercado
_renderHubInsights()       // Insights (4 cards)
_renderHubAlerts()         // Alertas condicionales
_renderHubKPIs()           // KPIs compactos
_renderHubRadar()          // Radar comercial
_renderHubActivity()       // Timeline de actividad
_updateHubGreeting()       // Saludo personalizado
```

### Datos del Dashboard (un solo fetch paralelo)
```javascript
const [bldSnap, ctoSnap, ctaSnap, descSnap, txSnap] = await Promise.all([
  db.collection('buildings').where('activo','==',true).get(),
  db.collection('contactos').get(),
  db.collection('clientes').get(),
  db.collection('descargas').orderBy('fecha','desc').limit(200).get(),
  db.collection('transacciones').get(),
]);
```

---

## 8. ANALYTICS

### Acceso
**CRÍTICO:** Solo para emails en `ANALYTICS_ALLOWED`. Si el usuario no está en la lista, el panel **no existe** en la UI — no griseado, no disabled: **directamente invisible**.

```javascript
const ANALYTICS_ALLOWED = [
  'mazaretto@gmail.com',
  'matias.azaretto@colliers.com',
  'colliers.arg@gmail.com'
];
```

### Submodulos
```javascript
const _AN_SCROLL = {
  intel:      'an-kpis',
  heatmaps:   'an-demand-heatmap-card',
  brokers:    'an-brokers-dash-card',
  tendencias: 'an-tend-card',
  rankings:   'an-leads-section'   // incluye el Funnel de Leads
};
```

### Funnel de Leads (dentro de Analytics)
`loadLeadsAnalytics()` / `renderLeadsAnalytics(leads)` renderizan: KPIs del funnel, distribución por origen, ranking de ejecutivos comerciales, motivos de descarte. IDs: `an-lead-kpis`, `an-leads-funnel`, `an-leads-origen`, `an-leads-brokers`, `an-leads-descarte`.

### Filtros de Analytics
```javascript
let _anFilters = { periodo:0, zonas:new Set(), ejecutivo:'', edificio:'', m2min:0, m2max:0 };
```

### Funciones principales
```javascript
loadAnalytics(), renderAnalytics(docs), generateInsights(docs),
renderAnHeatmap(docs), renderTendencias(docs, dias),
exportAnPDF(), exportAnPPT(), _anGoTo(submod)
```

---

## 9. GENERADOR PPT

### Panel: `#as`
La aplicación de presentaciones (`as` = "alternativas") es el módulo original del sistema.

### Fuente de datos: `masterBuildings[]`
**ES LA ÚNICA FUENTE DE VERDAD** para el generador y el inventario de Oficinas.
```javascript
let masterBuildings = [];  // Cargado por loadData()
```
**Prioridad de carga:** 1) Google Sheets CSV (3 CORS proxies en orden) → 2) Firestore `buildings` (fallback).

**URL del Sheet:**
```
https://docs.google.com/spreadsheets/d/e/2PACX-1vRLUmjoaea_htH898sLsLIzQsk_JJdNNk7mwou9Wc9LvDUtBwYKGd4E_kEpiaS4Fw/pub?gid=1012730079&single=true&output=csv
```

### Schema `masterBuildings`
```javascript
{ nombre, direccion, submercado, cat, anio, pisos, cocheras,
  supDisp, pisosDisp, supPlanta, supMinima, rent, comentarios, foto,
  lat, lng, gMapsAddr }
```

### Geocodificación (prioridad)
1. Sheet `Latitud`/`Longitud` → 2. Sheet `Google Maps Address` → 3. campo `direccion`

### Wizard (chat-based)
Usuario responde preguntas → filtros sobre `masterBuildings` → tabla de resultados → selección → exporta PPT con PptxGenJS. Cada PPT generado → `db.collection('descargas').add({...})` (alimenta Analytics).

---

## 10. CRM

### Estructura de tabs
```javascript
function switchCRMTab(tab) {  // 'cuentas' | 'contactos' | 'leads'
  _crmActiveTab = tab;
}
```

### Tab: Cuentas (`#crm-cuentas-section`)
**Carga:** `loadCRM()` → `db.collection('clientes').orderBy('ultimaActividad','desc')`
**Ficha (`openClientDetail(docId)`):** 9 tabs: Información / Resumen / Búsquedas / PPTs generados / Alternativas enviadas / Notas / Contactos / Timeline / Inventario
**Contactos de la cuenta:** `loadCuentaContactos(cuentaId)` → `contactos where cuentaId==`
**Drawer "Nueva Cuenta":** `#cdr-drawer` — `cdrVal(id)`, `cdrToggleVal(field)`, `window.cdrToggle(btn)`

### Tab: Contactos (`#crm-contactos-section`)
**Carga:** `loadContactos()` → `contactos orderBy ultimaActividad desc`
**Drawer "Nuevo Contacto":** `#ctdr-drawer` — `window.ctdrTogglePref(btn)` (toggle no exclusivo, prefs de inversión)

### Tab: Leads (`#crm-leads-section`) — ✅ COMPLETO
La colección `leads` y la UI completa están implementadas. Estructura:

**Vistas:**
- **Lista** (`#lead-list-view`): subtítulo con conteo, buscador (`filterLeads`), filtros por estado y origen, fila de KPIs (`lead-kpi-row`), tabla (`lead-table-wrap`), botón "+ Nuevo lead".
- **Detalle** (`#lead-detail-view`): timeline, tabs, cambio de estado inline, botones "Convertir a contacto", "Enviar al Broker", "Copiar Resumen".

**Constantes (~línea 6610):**
```javascript
const LEAD_ESTADOS   = ['Nuevo','Intento de contacto','Contactado','Calificado',
                        'Visita coordinada','Visita realizada','Propuesta enviada',
                        'Descartado','Convertido'];
const LEAD_ESTADO_CLS= { ... };   // mapea estado → clase CSS del badge
const LEAD_DESCARTE  = ['No responde','No interesado','Ya cerró operación',
                        'Fuera de presupuesto','Datos inválidos','Otro'];
```

**Funciones principales:**
```javascript
loadLeads()                 // fetch leads orderBy fechaCreacion desc
filterLeads()               // aplica buscador + filtros + oculta archivados
renderLeadsKPIs(docs)       // KPIs de la lista
renderLeadsTable(docs)      // tabla de leads
openLeadDetail(docId)       // abre ficha de detalle
leadDetTab(el, tabId)       // navegación de tabs del detalle
updateLeadEstado(id, est)   // cambia estado + registra en timeline
updateLeadMotivo(id, mot)   // setea motivo de descarte
addLeadTimeline(id, evento) // escribe en leads/{id}/timeline
loadLeadTimeline(docId)     // carga el timeline del lead

// Drawer crear/editar:
window.openLeadDrawer(prefillBuildingId, prefillBuildingName, prefillBroker)
window.openLeadDrawer_edit(docId)
window.closeLeadDrawer()
window.saveLeadDrawer()     // crea o actualiza; valida campos requeridos
window.ldrBldSearch(q)      // autocompletado de inmueble consultado
window.ldrSelectBld(id, nombre)
window.archiveLead(docId)   // baja lógica (estadoRegistro='archivado')

// Convertir a contacto:
openConvertModal()          // modal de conversión lead → contacto
_ldrConvertOpt              // 'existente' | 'nueva' (vincular a cuenta)

// Notificaciones / utilidades:
showLeadNotification(d)     // toast al crear lead
_leadResumenText(d), _leadCopyResumen(id), _leadSendToBroker(id)

// Analytics:
loadLeadsAnalytics(), renderLeadsAnalytics(leads)
```

**Campos requeridos en el drawer:** nombre, apellido, email, origen, brokerAsignado (Ejecutivo Comercial), linkOrigen.

**Brokers válidos (hardcodeados):** `Matienzo, Bartra, Farola, Troncoso, Giancontieri, Zuliani`.

### Email al broker
`_leadSendToBroker(id)` arma un email comercial. EmailJS integrado pero **keys vacías** (`EMAILJS_TEMPLATE_ID=""`, `EMAILJS_PUBLIC_KEY=""`, `EMAILJS_SERVICE_ID=""`). No envía hasta completar credenciales. `_leadCopyResumen(id)` es el fallback (copia el resumen al portapapeles).

---

## 11. TIMELINE

| Colección | Propósito | Campo de vínculo |
|-----------|-----------|-----------------|
| `timeline` | Eventos CRM por cliente | clienteId |
| `leads/{id}/timeline` | Actividad de leads | (subcolección) |
| `contactoTimeline` | Actividad de contactos | contactoId |
| `buildings/{id}/timeline` | Eventos por edificio | (subcolección) |

```javascript
function addBldTimelineEvent(buildingId, tipo, descripcion, nombre) {
  db.collection('buildings').doc(buildingId).collection('timeline').add({
    tipo, descripcion, nombre,
    fecha: firebase.firestore.Timestamp.now(),
    usuario: user?.displayName || user?.email || ''
  });
}
```

---

## 12. VARIABLES GLOBALES CRÍTICAS

```javascript
// Firebase
let db = null, storage = null;

// Auth
let user = null;              // usuario logueado (GSI)

// Generator
let masterBuildings = [];     // FUENTE DE VERDAD — edificios del Sheet
let filt = [];                // edificios filtrados
let sel = new Set();          // edificios seleccionados para PPT

// CRM
let _crmDocs = [];            // cuentas cargadas
let _ctoDocs = [];            // contactos cargados
let _leadDocs = [];           // leads cargados
let _currentLeadId = null;    // lead abierto en detalle
let _ldrConvertOpt = 'existente';
let _ldrEditId = null;        // lead en edición (drawer)
let _crmActiveTab = 'cuentas';
let _cdrEditId = null;        // cuenta en edición
let _ctdrEditId = null;       // contacto en edición

// Buildings
let _bldDocs = [];            // edificios cargados
let _bldFiltered = [];        // edificios filtrados
let _bldAssetType = 'office'; // tipo activo (office|industrial|retail)
let _bldListView = 'grid';    // vista (grid|list|map)
let _bldEditId = null;
let _bldMap = null;           // instancia Leaflet
let _bldClusterGroup = null;  // MarkerClusterGroup
let _indWizStep = 1; let _indWizSubtipo = '';
let _retWizStep = 1;

// Analytics
let _anDocs = [];
let _anActiveSubmod = 'intel';
let _anFilters = {...};

// Transacciones
let _txDocs = [], _txFiltered = [], _txEditId = null;
```

---

## 13. HELPERS JS CRÍTICOS

```javascript
function _tsToDate(ts){
  if(!ts) return null;
  if(ts.toDate) return ts.toDate();
  if(ts.seconds) return new Date(ts.seconds*1000);
  return new Date(ts);
}
function fmtDate(ts) { /* "dd MMM yyyy" */ }

// CRM
function cdrVal(id); function cdrToggleVal(field);
window.cdrToggle(btn); window.ctdrTogglePref(btn);

// Diff de campos (usado en edición de leads/cuentas para timeline)
function _diffFields(oldObj, newObj, labels)  // → [{field, before, after}]

// Utilidades
function show(id); function gv(id); function esc(v);
```

---

## 14. SEGURIDAD CRÍTICA — NO ROMPER

```javascript
// NUNCA modificar sin aprobación explícita:
const ANALYTICS_ALLOWED = ['mazaretto@gmail.com', 'matias.azaretto@colliers.com', 'colliers.arg@gmail.com'];
```

**Regla de seguridad:**
- Usuarios NO en `ANALYTICS_ALLOWED` → Analytics y Admin **no existen en la UI**
- No griseados, no deshabilitados: **directamente no renderizados**
- Se verifica en: `showModule()`, renderizado del sidebar, `renderHubCards()`

---

## 15. CONVENCIONES DE CÓDIGO

1. **Sin build system** — editar `index.html` directamente
2. **Sin comentarios** — salvo cuando el WHY es no obvio
3. **Sin abstracciones prematuras**
4. **Sin manejo de errores** para escenarios imposibles
5. **CSS inline en JS** para elementos generados dinámicamente
6. **Timestamps:** `_tsToDate(ts)` para leer, `firebase.firestore.Timestamp.now()` para escribir
7. **IDs consistentes:** prefijo del módulo (`bld-`, `crm-`, `ldr-`, `an-`, `tx-`, etc.)

---

## 16. VERIFICACIÓN DE SINTAXIS JS

```bash
SCRIPT_START=$(grep -n "^<script>$" index.html | head -1 | cut -d: -f1)
SCRIPT_END=$(grep -n "^</script>" index.html | tail -1 | cut -d: -f1)
sed -n "$((SCRIPT_START+1)),$((SCRIPT_END-1))p" index.html > /tmp/check.mjs
node --check /tmp/check.mjs && echo "SYNTAX OK"
```

---

## 17. GIT — FLUJO DE TRABAJO

```bash
# Branch de desarrollo activo (cambia según sesión):
claude/dreamy-hawking-45kt4d

# Push a producción (Vercel):
git push origin <branch>:main
git push -u origin <branch>

# Si hay error de "Unverified commits" (stop hook):
git config user.email noreply@anthropic.com
git config user.name Claude
git rebase --exec "git commit --amend --no-edit --reset-author" origin/main
git push -f origin <branch>:main
```

> **Nota:** El nombre del branch de desarrollo cambia por sesión. La constante es: **push a `main` = deploy en Vercel (~30 s)**. Verificar siempre en qué branch estás con `git branch`.

---

## 18. PROBLEMAS CONOCIDOS / LIMITACIONES ACTUALES

| Problema | Impacto | Estado |
|----------|---------|--------|
| EmailJS keys vacías | Envío de emails al broker no funciona (fallback: copiar resumen) | Pendiente — requiere credenciales |
| Google Maps API key vacía | Geocodificación falla, usa fallback | Pendiente |
| OAuth corporativo | Dominios en `ALLOWED_DOMAINS` deben estar habilitados también en Google Cloud Console | Verificar en consola |
| Oportunidades = disabled | No implementado | Roadmap |
| ZONAS_DEFAULT hardcodeadas | Zonas fijas, no editables desde UI | Aceptado por ahora |
| BROKERS hardcodeados | Lista estática (Matienzo, Bartra, Farola, Troncoso, Giancontieri, Zuliani) | Candidato a migrar a Firestore |
| Sheet CSV depende de CORS proxies | Si proxies fallan, usa Firestore | Riesgo de disponibilidad |
| Firestore Security Rules | No auditadas en código | Verificar en consola Firebase |

---

## 19. ROADMAP RECOMENDADO

### Corto plazo
1. **Configurar EmailJS** — notificación al broker de nuevo lead (keys: Service/Template/Public)
2. **Google Maps API key** — geocodificación de edificios
3. **Verificar OAuth corporativo** — que `@colliers.com.ar` entre sin fricción

### Mediano plazo
4. **Fichas automáticas por edificio** — PDF/PPT de ficha individual
5. **Módulo Oportunidades** — pipeline inmobiliario (distinto a leads)
6. **Migrar BROKERS a Firestore** — lista dinámica desde colección `usuarios`
7. **Vista kanban de Leads** — board por estado (drag & drop)
8. **Mejoras Analytics** — más dimensiones (cliente, tipo activo)

### Largo plazo
9. **Migración Firebase corporativo** — proyecto bajo cuenta Colliers Argentina
10. **Migración GitHub corporativo** — repo bajo organización Colliers
11. **Portal de búsqueda para clientes** — vista pública/limitada del inventario
12. **Módulo de documentos** — gestión de Storage robusta
13. **SSO corporativo** — SAML/OIDC con Azure AD de Colliers
14. **Notificaciones push** — nuevos leads, cambios de precio

---

## 20. DECISIONES DE NEGOCIO TOMADAS

| Decisión | Justificación | Impacto técnico |
|----------|---------------|-----------------|
| Separación Oficinas/Industrial/Retail | UX más clara, datos distintos | Un panel HTML, `_bldAssetType` controla todo |
| Dashboard ejecutivo full-width | "Centro de Operaciones" en < 10 s | Layout 1440px, 7 secciones |
| Analytics solo whitelist | Datos sensibles de negocio | `ANALYTICS_ALLOWED`, panel oculto |
| Industrial con picker de sub-tipo | Distintas características por tipo | `IND_WIZ_STEPS=5`, `tipoActivo` en Firestore |
| Google Sheets como fuente del generador | Brokers editan inventario sin acceso a la app | `masterBuildings[]` via CSV con fallback Firestore |
| CRM propio (no Salesforce) | Costo, simplicidad, datos integrados | colecciones Firestore + tabs |
| Single-file SaaS | Sin build, deploy instantáneo | Riesgo de tamaño de archivo a largo plazo |
| Nomenclatura `clientes` para "cuentas" | Colección histórica | Mantener `db.collection('clientes')` — NO renombrar |
| `ALLOWED_DOMAINS` multi-dominio | Habilitar cuentas corporativas Colliers | array en vez de la vieja constante `DOM` |

---

## 21. CHECKLIST DE CONTINUIDAD

### Revisar primero
- [ ] Leer este documento completo
- [ ] `git branch` — confirmar branch de desarrollo
- [ ] Ejecutar syntax check: `node --check /tmp/check.mjs && echo "SYNTAX OK"`
- [ ] Verificar que `ANALYTICS_ALLOWED` no fue modificado
- [ ] Revisar últimos 5 commits con `git log --oneline`

### Archivos críticos
- `index.html` — **El único archivo a modificar**
- `vercel.json` — Config de deploy (no modificar sin razón)
- `CLAUDE.md` — Instrucciones para Claude Code
- `HANDOVER.md` — Este documento (actualizar con cada sprint importante)

### Funciones críticas (NO modificar sin auditoría)
```
ANALYTICS_ALLOWED     ← seguridad
ALLOWED_DOMAINS       ← control de acceso por dominio
showModule()          ← navegación principal
loadBuildings()       ← carga inventario
_bldAdaptUI()         ← diferenciación por tipo
classify()            ← backward compat legacy data
loadData()            ← fuente de verdad generador
_tsToDate()           ← helper timestamps Firestore
renderHubCards()      ← dashboard home
```

### NO tocar sin auditoría previa
- El array `ANALYTICS_ALLOWED` — requiere aprobación del usuario
- La colección `clientes` — no renombrar aunque la UI diga "Cuentas"
- La variable `masterBuildings` — fuente de verdad del generador
- Los IDs de paneles HTML (`#crm-panel`, `#buildings-panel`, etc.)
- La lógica de `classify()` para backward compat

---

## 22. RESUMEN EJECUTIVO

### ¿Qué es?
Colliers Nexus es una plataforma SaaS inmobiliaria para Colliers Argentina, construida como **un único archivo HTML** (`index.html`) sin build system ni framework. CSS, HTML y JS inline. Deploy en Vercel con Firebase Firestore.

### ¿Cómo navegar el código?
1. `<head>` — CDN scripts, CSS inline en `<style>`
2. `<body>` — HTML de todos los paneles (ocultos por defecto con `display:none`)
3. `<script>` — Todo el JavaScript de la aplicación

El módulo activo se controla con `showModule(mod)`.

### Módulos principales
| Módulo | Panel HTML | Función de carga |
|--------|-----------|-----------------|
| Dashboard | `#home-hub` | `renderHubCards()` |
| Inventario | `#buildings-panel` | `loadBuildings()` |
| CRM | `#crm-panel` | `loadCRM()` / `loadContactos()` / `loadLeads()` |
| Generador PPT | `#as` | `loadData()` |
| Analytics | `#analytics-panel` | `loadAnalytics()` |
| Transacciones | `#transacciones-panel` | `loadTransacciones()` |

### Dato más importante
`masterBuildings[]` es la fuente de verdad del generador de PPTs (Google Sheets CSV con fallback Firestore).

### Seguridad
Auth: Google OAuth2 + `ALLOWED_DOMAINS`. Analytics y Admin solo para los 3 emails en `ANALYTICS_ALLOWED`.

### ¿Qué está completo?
Dashboard (100%), Inventario Oficinas/Industrial/Retail (100%), CRM Cuentas+Contactos+**Leads** (100%), Generador PPT (90%), Analytics (90%), Transacciones (100%).

### ¿Qué está pendiente?
EmailJS config, Google Maps API key, fichas automáticas, módulo Oportunidades, migración Firebase/GitHub corporativo, vista kanban de Leads.

### ¿Cómo deployar?
```bash
git add index.html
git commit -m "descripción del cambio"
git push origin <branch>:main   # Vercel despliega en ~30 s
```

---

*Documento actualizado en Junio 2026. Refleja el estado real del código (módulo Leads completo, auth multi-dominio). Actualizar con cada sprint importante.*
