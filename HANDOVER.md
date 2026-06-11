# HANDOVER TÉCNICO — COLLIERS NEXUS
**Fecha:** Junio 2026 · Para nuevo Claude Code · Sin acceso a conversaciones anteriores

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
- **CRM:** Cuentas + Contactos funcionales; Leads en construcción (placeholder)
- **Generador PPT:** Funcional, usa Google Sheets como fuente de datos
- **Analytics:** Funcional, acceso restringido por whitelist de emails
- **Transacciones:** Funcional

### Nivel de avance estimado: ~75%

**Pendiente relevante:** flujo completo de Leads, fichas automáticas por edificio, integración email (EmailJS vacío), módulo de documentos (Storage), mejoras al generador PPT.

---

## 2. ARQUITECTURA GENERAL

### Stack técnico
```
Frontend:    HTML5 + CSS3 + Vanilla JS (ES6+) — UN SOLO ARCHIVO: index.html (~6.200+ líneas)
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
  └─ Rankings

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
| CRM - Leads | 🚧 Placeholder | Pantalla "Próximamente", colección leads existe |
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
**Propósito:** Cuentas/empresas del CRM (también referenciada como "cuentas" en UI)

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
**Propósito:** Pipeline comercial (módulo en construcción)

**Campos conocidos:**
```javascript
origen, nombre, email, estado,
fechaCreacion, ultimaActividad,
contactoId, cuentaId
```

**Colección relacionada:** `leadTimeline` — historial de actividad por lead (field: leadId → leads)

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

---

### `timeline`
**Propósito:** Eventos CRM generales por cliente

---

### `history`
**Propósito:** Historial de cambios de edificios (audit trail)

---

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
- `home-bg.jpg` (8.3 MB) — fondo del dashboard
- `login-bg.jpg` (721 KB) — fondo del login
- `colliers-logo-white.png` — logo en sidebar
- Imágenes PPT en CDN externo: `https://raw.githubusercontent.com/mazaretto-wq/colliers-fotos/main/`

---

## 6. MÓDULO INVENTARIO — ARQUITECTURA

### Un solo panel HTML, tres modos
**Panel:** `#buildings-panel` — es el mismo para Oficinas, Industrial y Retail.

**Variable de control:** `let _bldAssetType = 'office'` — cambia según módulo seleccionado.

### Cómo funciona la diferenciación
```javascript
// Al navegar a un módulo de inventario:
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
Cambia dinámicamente:
- Título de la sección
- Texto del botón "Nuevo activo"
- Filtros del filter bar (completamente distintos por tipo)
- Columnas de la tabla lista
- Cards de KPIs
- Labels del editor

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
2. **General** (nombre, dirección, localidad, provincia, corredor, etapa, categoría)
3. **Superficies** (terreno, cubiertos, semicubiertos, oficinas)
4. **Características** (altura libre, docks, potencia eléctrica, playa maniobras, sprinklers, certificación)
5. **Comercial** (precio alquiler, precio venta, disponible)

```javascript
let _indWizSubtipo = '';  // valor seleccionado en paso 1
const IND_WIZ_STEPS = 5;
const IND_WIZ_LABELS = ['Tipo','General','Superficies','Características','Comercial'];
```

**Retail** — 3 pasos:
1. General
2. Características
3. Comercial

```javascript
const RET_WIZ_STEPS = 3;
const RET_WIZ_LABELS = ['General','Características','Comercial'];
```

### Vistas disponibles
- `'grid'` — cards con foto
- `'list'` — tabla
- `'map'` — Leaflet con clustering

---

## 7. DASHBOARD HOME

### Estructura del nuevo dashboard (full-width, max 1440px)

**1. Hero** — Saludo personalizado (`¡Buenos días, Nombre!`), badge de alertas, hora de actualización, total de registros activos

**2. Accesos Rápidos** — 8 cards en una fila (8 columnas, responsive → 4 cols → 2 cols → 1 col):
Oficinas / Industrial / Retail / Leads / Cuentas / Contactos / PPTs / Analytics (admin only)

Cada card muestra: ícono, título, contadores live desde Firestore, CTA button.

**3. Resumen del Mercado** — 3 columnas (Oficinas azul / Industrial amber / Retail purple):
- Stats primarios: activos, disponibles, m² disponibles
- Stats secundarios: vacancia %, precio promedio USD/m², mayor oferta (zona), categoría top
- Insights inline: zona demandada, rango m² buscado

**4. Insights Comerciales** — 4 cards horizontales:
🔥 Zona Caliente / 🏢 Edificio más enviado / 👤 Broker Líder / 📐 Demanda m²
(calculados desde colección `descargas`)

**5. Actividad Reciente + Radar Comercial** — 2 columnas:
- Actividad: timeline de últimas 10 acciones (cuentas, contactos, edificios, PPTs)
- Radar: texto contextual generado dinámicamente con zona demandada + m² range

**6. KPIs Operacionales** — 6 mini-cards:
Edificios activos / Disponibilidades / m² disponibles / Cuentas CRM / Tx abiertas / Tx cerradas mes

**7. Alertas** (SOLO si hay alertas > 0, oculto si todas son 0):
Leads sin contactar (rojo) / Sin actividad +14d (naranja) / Tx cerradas mes (verde) / Nuevos inmuebles (azul) / PPTs 7d (violeta)

### Funciones principales del dashboard
```javascript
renderHubCards()           // Renderiza accesos rápidos y dispara carga de datos
_loadHubDashboardData()    // Un solo fetch paralelo de TODOS los datos del dashboard
_renderHubMarket()         // Sección Resumen del Mercado
_renderHubInsights()       // Insights comerciales (4 cards)
_renderHubAlerts()         // Alertas condicionales
_renderHubKPIs()           // KPIs compactos
_renderHubRadar()          // Radar comercial
_renderHubActivity()       // Timeline de actividad
_updateHubGreeting()       // Saludo personalizado
```

### Datos del Dashboard (todo calculado, nada hardcodeado)
```javascript
// Un solo fetch paralelo en _loadHubDashboardData():
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
**CRÍTICO:** Solo para emails en `ANALYTICS_ALLOWED`. Si el usuario no está en la lista, el panel no existe en la UI — no griseado, no disabled: **directamente invisible**.

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
  rankings:   'an-leads-section'
};
```

**Inteligencia Comercial (`intel`):** KPIs de descargas, insights automáticos
**Heatmaps:** Visualización de demanda por zona geográfica
**Dashboard Brokers:** Rankings y performance por ejecutivo
**Tendencias:** Evolución temporal de métricas
**Rankings:** Top edificios, zonas, clientes por actividad

### Filtros de Analytics
```javascript
let _anFilters = {
  periodo: 0,         // días: 0=todos, 7, 30, 90, 365
  zonas: new Set(),   // Set de zonas seleccionadas
  ejecutivo: '',      // email del broker
  edificio: '',       // nombre del edificio
  m2min: 0,
  m2max: 0
};
```

### Fuente de datos: colección `descargas`
Cada PPT generado agrega un documento a `descargas`. Analytics procesa estos documentos.

### Funciones principales
```javascript
loadAnalytics()              // Carga descargas, popula filtros, renderiza
renderAnalytics(docs)        // Render principal de todos los submodulos
generateInsights(docs)       // Genera insights automáticos de texto
renderAnHeatmap(docs)        // Heatmap de demanda
renderTendencias(docs, dias) // Tendencia temporal
exportAnPDF(), exportAnPPT() // Exportación
_anGoTo(submod)              // Navegar entre submodulos
```

---

## 9. GENERADOR PPT

### Panel: `#as`
La aplicación de presentaciones (`as` = "alternativas") es el módulo original del sistema.

### Fuente de datos: `masterBuildings[]`
**ES LA ÚNICA FUENTE DE VERDAD** para el generador y el módulo de inventario de Oficinas.

```javascript
let masterBuildings = [];  // Cargado por loadData()
```

**Prioridad de carga:**
1. Google Sheets CSV (3 CORS proxies en orden)
2. Firestore `buildings` (fallback si Sheet falla)

**URL del Sheet:**
```
https://docs.google.com/spreadsheets/d/e/2PACX-1vRLUmjoaea_htH898sLsLIzQsk_JJdNNk7mwou9Wc9LvDUtBwYKGd4E_kEpiaS4Fw/pub?gid=1012730079&single=true&output=csv
```

### Campos del schema `masterBuildings`
```javascript
{
  nombre, direccion, submercado, cat,
  anio, pisos, cocheras,
  supDisp, pisosDisp, supPlanta, supMinima,
  rent, comentarios, foto,
  lat, lng, gMapsAddr    // geocodificación
}
```

### Geocodificación (prioridad)
1. Sheet `Latitud` / `Longitud` columns
2. Sheet `Google Maps Address` column
3. campo `direccion` del edificio

### Wizard de generación (chat-based)
- Usuario responde preguntas secuenciales (zona, m², categoría, etc.)
- Respuestas → filtros sobre `masterBuildings`
- Tabla de resultados → selección de edificios
- Exporta PPT con PptxGenJS

### Logging a Firestore
Cada PPT generado → `db.collection('descargas').add({...})` (alimenta Analytics)

### Integración con edificios
```javascript
// Al navegar a Generator, recarga desde Sheet:
loadData().then(() => {
  console.log('[masterBuildings] Generator opened — '+masterBuildings.length+' buildings loaded');
});
```

---

## 10. CRM

### Estructura de tabs
```javascript
function switchCRMTab(tab) {  // 'cuentas' | 'contactos' | 'leads'
  _crmActiveTab = tab;
  // Muestra sección correspondiente, carga datos
}
```

### Tab: Cuentas (`#crm-cuentas-section`)
**Carga:** `loadCRM()` → `db.collection('clientes').orderBy('ultimaActividad','desc')`

**Ficha de cuenta (`openClientDetail(docId)`):** 9 tabs:
Información / Resumen / Búsquedas / PPTs generados / Alternativas enviadas / Notas / Contactos / Timeline / Inventario

**Contactos de la cuenta:** `loadCuentaContactos(cuentaId)` → `db.collection('contactos').where('cuentaId','==',...)`

**Drawer "Nueva Cuenta":** `#cdr-drawer`
```javascript
cdrVal(id)          // leer input del drawer por ID
cdrToggleVal(field) // leer toggle activo
window.cdrToggle(btn) // toggle exclusivo (data-field)
```

### Tab: Contactos (`#crm-contactos-section`)
**Carga:** `loadContactos()` → `db.collection('contactos').orderBy('ultimaActividad','desc')`

**Drawer "Nuevo Contacto":** `#ctdr-drawer`
```javascript
window.ctdrTogglePref(btn)  // toggle NO exclusivo (preferencias de inversión)
```

### Tab: Leads (`#crm-leads-section`)
**Estado actual:** Placeholder "Próximamente". La colección `leads` existe en Firestore y tiene funciones básicas (`loadLeads`, `renderLeadsTable`) pero la UI completa está pendiente.

### Email al broker
Funcionalidad de envío de email al broker por lead. EmailJS integrado pero **keys vacías** (`EMAILJS_TEMPLATE_ID = ""`, `EMAILJS_PUBLIC_KEY = ""`). No funciona hasta completar credenciales.

---

## 11. TIMELINE

### Colecciones relacionadas
| Colección | Propósito | Campo de vínculo |
|-----------|-----------|-----------------|
| `timeline` | Eventos CRM por cliente | clienteId |
| `leadTimeline` | Actividad de leads | leadId |
| `contactoTimeline` | Actividad de contactos | contactoId |
| `buildings/{id}/timeline` | Eventos por edificio | (subcolección) |

### Función de registro
```javascript
// Ejemplo de registro en timeline de edificio:
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
let _crmActiveTab = 'cuentas';
let _cdrEditId = null;        // ID de cuenta en edición
let _ctdrEditId = null;       // ID de contacto en edición

// Buildings
let _bldDocs = [];            // edificios cargados
let _bldFiltered = [];        // edificios filtrados
let _bldAssetType = 'office'; // tipo activo (office|industrial|retail)
let _bldListView = 'grid';    // vista (grid|list|map)
let _bldEditId = null;
let _bldMap = null;           // instancia Leaflet
let _bldClusterGroup = null;  // MarkerClusterGroup
let _indWizStep = 1;          // paso actual wizard industrial
let _indWizSubtipo = '';      // sub-tipo seleccionado en paso 1
let _retWizStep = 1;          // paso actual wizard retail

// Analytics
let _anDocs = [];             // descargas cargadas
let _anActiveSubmod = 'intel';
let _anFilters = {...};

// Transacciones
let _txDocs = [], _txFiltered = [], _txEditId = null;
```

---

## 13. HELPERS JS CRÍTICOS

```javascript
// Timestamps Firestore
function _tsToDate(ts){
  if(!ts) return null;
  if(ts.toDate) return ts.toDate();
  if(ts.seconds) return new Date(ts.seconds*1000);
  return new Date(ts);
}

function fmtDate(ts) { /* formatea a "dd MMM yyyy" */ }

// Helpers CRM
function cdrVal(id)           // leer input drawer cuenta
function cdrToggleVal(field)  // leer toggle activo
window.cdrToggle(btn)         // toggle exclusivo
window.ctdrTogglePref(btn)    // toggle NO exclusivo

// Utilidades
function show(id)             // document.getElementById(id).style.display=''
function gv(id)               // document.getElementById(id)?.value?.trim()||''
function esc(v)               // escapeHTML
```

---

## 14. SEGURIDAD CRÍTICA — NO ROMPER

```javascript
// NUNCA modificar esto sin aprobación explícita:
const ANALYTICS_ALLOWED = ['mazaretto@gmail.com', 'matias.azaretto@colliers.com', 'colliers.arg@gmail.com'];
```

**Regla de seguridad:**
- Usuarios NO en `ANALYTICS_ALLOWED` → Analytics y Admin **no existen en la UI**
- No griseados, no deshabilitados: **directamente no renderizados**
- Se verifica en: `showModule()`, renderizado del sidebar, `renderHubCards()`

---

## 15. CONVENCIONES DE CÓDIGO

1. **Sin build system** — editar `index.html` directamente
2. **Sin comentarios** — salvo cuando el WHY es no obvio (constraint oculto, workaround de bug)
3. **Sin abstracciones prematuras** — 3 líneas similares son mejores que una abstracción prematura
4. **Sin manejo de errores** para escenarios imposibles
5. **CSS inline en JS** para elementos generados dinámicamente (template literals)
6. **Timestamps:** siempre `_tsToDate(ts)` para leer, `firebase.firestore.Timestamp.now()` para escribir
7. **IDs consistentes:** panel IDs con prefijo del módulo (`bld-`, `crm-`, `an-`, `tx-`, etc.)

---

## 16. VERIFICACIÓN DE SINTAXIS JS

Comando para verificar antes de commitear:
```bash
SCRIPT_START=$(grep -n "^<script>$" index.html | head -1 | cut -d: -f1)
SCRIPT_END=$(grep -n "^</script>" index.html | tail -1 | cut -d: -f1)
sed -n "$((SCRIPT_START+1)),$((SCRIPT_END-1))p" index.html > /tmp/check.mjs
node --check /tmp/check.mjs && echo "SYNTAX OK"
```

---

## 17. GIT — FLUJO DE TRABAJO

```bash
# Branch activo de desarrollo:
claude/update-dom-constant-8eiPY

# Push a producción (Vercel):
git push --force-with-lease origin claude/update-dom-constant-8eiPY:main
git push -u origin claude/update-dom-constant-8eiPY

# Si hay error de "Unverified commits" (stop hook):
git config user.email noreply@anthropic.com
git config user.name Claude
git rebase --exec "git commit --amend --no-edit --reset-author" origin/claude/update-dom-constant-8eiPY
git push --force-with-lease origin claude/update-dom-constant-8eiPY:main
```

**Historial reciente:**
```
fadd5e3  Dashboard: mejorar tipografía y contraste en cards de Resumen del Mercado
f12c6ab  Dashboard full-width completo — Resumen del Mercado + Insights + Alertas condicionales
ff435ac  Dashboard: inicio rediseño full-width — CSS market summary + nuevo layout HTML
0d75399  Dashboard: eliminar reloj, cards más grandes y mejor tipografía
cbe19d6  Rediseño completo Dashboard Home — Centro de Operaciones Comerciales
aa78a43  FASE 1-5: Industrial wizard tipo picker + dashboard 8 cards
cf5c576  feat(inventario): formularios, filtros y vistas específicas por tipo de activo
d6e775b  Refactor buildings module: Oficinas/Industrial/Retail as independent sidebar modules
```

---

## 18. PROBLEMAS CONOCIDOS / LIMITACIONES ACTUALES

| Problema | Impacto | Estado |
|----------|---------|--------|
| EmailJS keys vacías | Envío de emails al broker no funciona | Pendiente — requiere configurar credenciales |
| Leads tab = placeholder | El módulo de Leads no tiene UI completa | En construcción |
| Oportunidades = disabled | No implementado | Roadmap |
| ZONAS_DEFAULT hardcodeadas | Zonas fijas, no editables desde UI | Aceptado por ahora |
| BROKERS hardcodeados | Lista estática de brokers | Candidato a migrar a Firestore |
| Google Maps API key vacía | Geocodificación falla, usa fallback | Pendiente |
| Sheet CSV depende de CORS proxies | Si proxies fallan, usa Firestore | Riesgo de disponibilidad |
| Firestore Security Rules | No auditadas en código | Verificar en consola Firebase |

---

## 19. ROADMAP RECOMENDADO

### Corto plazo (próximas sesiones)
1. **Completar módulo Leads** — UI completa con CRUD, estados, kanban board
2. **Configurar EmailJS** — Template para notificación al broker de nuevo lead
3. **Google Maps API key** — Para geocodificación de edificios

### Mediano plazo
4. **Fichas automáticas por edificio** — PDF/PPT de ficha individual de activo
5. **Módulo Oportunidades** — Pipeline inmobiliario (distintos a leads)
6. **Migrar BROKERS a Firestore** — Lista dinámica desde colección `usuarios`
7. **Mejoras Analytics** — Más dimensiones de análisis (cliente, tipo activo)

### Largo plazo
8. **Migración Firebase corporativo** — Nuevo proyecto bajo cuenta Colliers Argentina
9. **Migración GitHub corporativo** — Repo bajo organización Colliers
10. **Portal de búsqueda para clientes** — Vista pública/limitada del inventario
11. **Módulo de documentos** — Gestión de Storage más robusta (fichas, planos, brochures)
12. **SSO corporativo** — SAML/OIDC con Azure AD de Colliers en lugar de Google genérico
13. **Notificaciones push** — Alertas de nuevos leads, cambios de precio

---

## 20. DECISIONES DE NEGOCIO TOMADAS

| Decisión | Justificación | Impacto técnico |
|----------|---------------|-----------------|
| Separación Oficinas/Industrial/Retail como módulos independientes | UX más clara, datos distintos por tipo | Un panel HTML, `_bldAssetType` controla todo |
| Dashboard ejecutivo full-width | "Centro de Operaciones" en < 10 segundos | Nuevo layout 1440px, 7 secciones |
| Analytics solo whitelist | Datos sensibles de negocio | ANALYTICS_ALLOWED, panel completamente oculto |
| Industrial con picker de sub-tipo | Distintas características por tipo de activo | IND_WIZ_STEPS=5, `tipoActivo` en Firestore |
| Google Sheets como fuente de datos del generador | Brokers editan el inventario en Sheets sin acceso a la app | masterBuildings[] cargado via CSV con fallback Firestore |
| CRM en la misma app (no Salesforce) | Costo, simplicidad, datos integrados con inventario | 3 colecciones Firestore + tabs en un panel |
| Single-file SaaS | Sin build, sin npm, deploy instantáneo | Riesgo de tamaño de archivo a largo plazo |
| Nomenclatura `clientes` para "cuentas" | Colección histórica, UI dice "Cuentas" | Mantener `db.collection('clientes')` — NO renombrar |

---

## 21. CHECKLIST DE CONTINUIDAD

### Revisar primero
- [ ] Leer este documento completo
- [ ] Ejecutar syntax check: `node --check /tmp/check.mjs && echo "SYNTAX OK"`
- [ ] Verificar que `ANALYTICS_ALLOWED` no fue modificado
- [ ] Revisar últimos 5 commits con `git log --oneline`

### Archivos críticos
- `index.html` — **El único archivo a modificar**
- `vercel.json` — Config de deploy (no modificar sin razón)
- `CLAUDE.md` — Instrucciones para Claude Code
- `home-bg.jpg` — Fondo del dashboard (no reemplazar)

### Funciones críticas (NO modificar sin auditoría)
```
ANALYTICS_ALLOWED     ← seguridad
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

## 22. RESUMEN EJECUTIVO (2 páginas)

### ¿Qué es?
Colliers Nexus es una plataforma SaaS inmobiliaria para Colliers Argentina, construida como **un único archivo HTML** (`index.html`, ~6.200+ líneas) sin build system ni framework. Contiene CSS, HTML y JavaScript inline. Se despliega en Vercel con Firebase Firestore como base de datos.

### ¿Cómo navegar el código?
La aplicación entera vive en `index.html`. La estructura es:
1. `<head>` — CDN scripts, CSS inline en `<style>`
2. `<body>` — HTML de todos los paneles (ocultos por defecto con `display:none`)
3. `<script>` — Todo el JavaScript de la aplicación

El módulo activo se controla con `showModule(mod)` que muestra/oculta paneles.

### ¿Cuáles son los módulos principales?
| Módulo | Panel HTML | Función de carga |
|--------|-----------|-----------------|
| Dashboard | `#home-hub` | `renderHubCards()` |
| Inventario | `#buildings-panel` | `loadBuildings()` |
| CRM | `#crm-panel` | `loadCRM()` |
| Generador PPT | `#as` | `loadData()` |
| Analytics | `#analytics-panel` | `loadAnalytics()` |
| Transacciones | `#transacciones-panel` | `loadTransacciones()` |

### ¿Cuál es el dato más importante?
`masterBuildings[]` es la fuente de verdad del generador de PPTs. Se carga desde Google Sheets CSV (con 3 proxies CORS) y usa Firestore como fallback.

### ¿Qué seguridad tiene?
Auth: Google OAuth2. Analytics y Admin solo para 3 emails en `ANALYTICS_ALLOWED`. Sin esos emails, los módulos no existen en la UI.

### ¿Qué está completo?
Dashboard (100%), Inventario Oficinas/Industrial/Retail (100%), CRM Cuentas+Contactos (100%), Generador PPT (90%), Analytics (85%), Transacciones (100%).

### ¿Qué está pendiente?
Leads module UI (30%), EmailJS config, fichas automáticas, módulo Oportunidades, migración Firebase/GitHub corporativo.

### ¿Cómo deployar?
```bash
git add index.html
git commit -m "descripción del cambio"
git push origin claude/update-dom-constant-8eiPY:main
# Vercel despliega automáticamente en ~30 segundos
```

### ¿Qué verificar antes de commitear?
```bash
SCRIPT_START=$(grep -n "^<script>$" index.html | head -1 | cut -d: -f1)
SCRIPT_END=$(grep -n "^</script>" index.html | tail -1 | cut -d: -f1)
sed -n "$((SCRIPT_START+1)),$((SCRIPT_END-1))p" index.html > /tmp/check.mjs
node --check /tmp/check.mjs && echo "SYNTAX OK"
```

---

*Documento generado en Junio 2026 por auditoría completa del código. Actualizar este documento con cada sprint importante.*
