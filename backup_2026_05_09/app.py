import streamlit as st
import sqlite3
import datetime
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="MARY'S GYM | Premium", layout="wide", initial_sidebar_state="collapsed")

# Estilos CSS Avanzados (Mejorados)
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
    * { font-family: 'Outfit', sans-serif; }
    
    /* Animaciones */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 255, 135, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(0, 255, 135, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 135, 0); }
    }
    
    .stApp {
        background: linear-gradient(135deg, #0A0E17 0%, #121824 50%, #1A1C29 100%);
        color: #FFFFFF;
    }
    
    .header-container {
        text-align: center;
        padding: 30px 0;
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        animation: fadeIn 0.6s ease-out;
    }
    
    .header-title {
        font-weight: 800;
        font-size: 3rem;
        background: linear-gradient(90deg, #00FF87 0%, #60EFFF 50%, #00D2FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }
    
    .header-subtitle {
        font-weight: 400;
        color: #8A99AD;
        font-size: 1.1rem;
        letter-spacing: 1px;
    }
    
    .metric-card {
        background: rgba(21, 28, 44, 0.6);
        backdrop-filter: blur(20px);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        max-width: 400px;
        margin: 0 auto 20px auto;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeIn 0.8s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 255, 135, 0.3);
        box-shadow: 0 15px 35px rgba(0, 255, 135, 0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #00FF87;
        text-shadow: 0 0 20px rgba(0, 255, 135, 0.2);
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #8A99AD;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 8px;
        font-weight: 600;
    }
    
    /* Tabs Principales Estilizados */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(21, 28, 44, 0.5);
        border-radius: 16px;
        padding: 8px;
        display: flex;
        justify-content: center;
        gap: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #8A99AD !important;
        font-weight: 600;
        font-size: 1rem;
        padding: 12px 25px;
        border-radius: 12px;
        transition: all 0.3s ease;
        border: none !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #0A0E17 !important;
        background: linear-gradient(90deg, #00FF87 0%, #00D2FF 100%) !important;
        box-shadow: 0 8px 20px rgba(0, 255, 135, 0.3);
        transform: translateY(-2px);
    }
    
    .stForm {
        background: rgba(21, 28, 44, 0.4) !important;
        backdrop-filter: blur(20px);
        border-radius: 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 25px !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.7s ease-out;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #00FF87 0%, #00D2FF 100%) !important;
        color: #0A0E17 !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 14px 20px !important;
        width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 5px 15px rgba(0, 255, 135, 0.2) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 255, 135, 0.4) !important;
        filter: brightness(1.1);
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    .client-card {
        background: rgba(21, 28, 44, 0.5);
        border-radius: 16px;
        padding: 18px 25px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.03);
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    .client-card:hover {
        background: rgba(21, 28, 44, 0.8);
        border-color: rgba(255, 255, 255, 0.08);
        transform: translateX(5px);
    }
    
    .client-name { font-weight: 600; font-size: 1.15rem; color: #FFFFFF; }
    .client-info { font-size: 0.9rem; color: #8A99AD; margin-top: 3px; }
    
    .badge {
        padding: 8px 16px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .badge-active { background: rgba(0, 255, 135, 0.1); color: #00FF87; border: 1px solid rgba(0, 255, 135, 0.2); }
    .badge-warning { background: rgba(255, 170, 0, 0.1); color: #FFAA00; border: 1px solid rgba(255, 170, 0, 0.2); }
    .badge-expired { background: rgba(255, 0, 85, 0.1); color: #FF0055; border: 1px solid rgba(255, 0, 85, 0.2); }
    
    .badge-plan {
        background: rgba(0, 210, 255, 0.1);
        color: #00D2FF;
        border: 1px solid rgba(0, 210, 255, 0.2);
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
        margin-top: 5px;
        margin-bottom: 5px;
    }
    
    .wa-link { 
        color: #00FF87; 
        text-decoration: none; 
        font-weight: 600; 
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 5px;
        transition: color 0.2s;
    }
    
    .wa-link:hover { color: #60EFFF; }
    
    /* Tablas Personalizadas */
    .custom-table-container {
        background: rgba(21, 28, 44, 0.3);
        border-radius: 16px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 15px;
        overflow-x: auto;
    }
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        color: white;
        text-align: left;
    }
    .custom-table th, .custom-table td {
        padding: 14px 18px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .custom-table th {
        background: rgba(10, 14, 23, 0.5);
        font-weight: 600;
        color: #8A99AD;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 1px;
    }
    .custom-table tr:hover td {
        background: rgba(255, 255, 255, 0.02);
        color: #00FF87;
        transition: all 0.2s ease;
    }
    .custom-table td {
        font-size: 0.95rem;
    }
    
    /* Inputs estilizados */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: rgba(10, 14, 23, 0.8) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #00FF87 !important;
        box-shadow: 0 0 10px rgba(0, 255, 135, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# Inicialización de la Base de Datos
def init_db():
    conn = sqlite3.connect('gym.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            fecha_ultimo_pago DATE,
            fecha_vencimiento DATE
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS pagos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            monto REAL,
            fecha DATE,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id)
        )
    ''')
    try:
        c.execute("ALTER TABLE pagos ADD COLUMN notas TEXT")
    except:
        pass
        
    # Nuevas columnas para clientes
    try:
        c.execute("ALTER TABLE clientes ADD COLUMN fecha_inscripcion DATE")
    except: pass
    try:
        c.execute("ALTER TABLE clientes ADD COLUMN plan_actual TEXT")
    except: pass
    try:
        c.execute("ALTER TABLE clientes ADD COLUMN con_entrenadora BOOLEAN DEFAULT 0")
    except: pass

    # Nuevas columnas para pagos
    try:
        c.execute("ALTER TABLE pagos ADD COLUMN metodo_pago TEXT")
    except: pass
    try:
        c.execute("ALTER TABLE pagos ADD COLUMN plan_tipo TEXT")
    except: pass
    try:
        c.execute("ALTER TABLE pagos ADD COLUMN con_entrenadora BOOLEAN DEFAULT 0")
    except: pass

    # Nueva tabla de asistencia
    c.execute('''
        CREATE TABLE IF NOT EXISTS asistencia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            fecha DATE,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id)
        )
    ''')
        
    c.execute("SELECT id FROM clientes WHERE nombre = 'CLIENTE CASUAL'")
    if not c.fetchone():
        c.execute("INSERT INTO clientes (nombre, telefono, fecha_ultimo_pago, fecha_vencimiento) VALUES ('CLIENTE CASUAL', '', '2000-01-01', '2000-01-01')")
        
    conn.commit()
    conn.close()

init_db()

# Funciones de base de datos
def get_clientes():
    conn = sqlite3.connect('gym.db')
    df = pd.read_sql_query("SELECT * FROM clientes WHERE nombre != 'CLIENTE CASUAL'", conn)
    conn.close()
    return df

TARIFAS = {
    "Normal": {
        "Rutina": 5000,
        "Semana": 20000,
        "Quincena": 40000,
        "Mensual": 60000
    },
    "Con Entrenadora": {
        "Rutina": 10000,
        "Semana": 30000,
        "Quincena": 60000,
        "Mensual": 100000
    }
}

def calcular_vencimiento(fecha_inicio, plan_tipo):
    if plan_tipo == "Rutina":
        return fecha_inicio
    elif plan_tipo == "Semana":
        return fecha_inicio + datetime.timedelta(days=6)
    elif plan_tipo == "Quincena":
        return fecha_inicio + datetime.timedelta(days=14)
    elif plan_tipo == "Mensual":
        vencimiento = pd.to_datetime(fecha_inicio) + pd.DateOffset(months=1) - pd.Timedelta(days=1)
        return vencimiento.date()
    return fecha_inicio

def registrar_pago(nombre, telefono, plan_tipo, con_entrenadora, metodo_pago):
    conn = sqlite3.connect('gym.db')
    c = conn.cursor()
    hoy = datetime.date.today()
    
    categoria = "Con Entrenadora" if con_entrenadora else "Normal"
    monto = TARIFAS[categoria][plan_tipo]
    
    vencimiento = calcular_vencimiento(hoy, plan_tipo)
    
    c.execute("SELECT id FROM clientes WHERE nombre = ?", (nombre,))
    cliente = c.fetchone()
    
    if cliente:
        cliente_id = cliente[0]
        c.execute("UPDATE clientes SET fecha_ultimo_pago = ?, fecha_vencimiento = ?, telefono = ?, plan_actual = ?, con_entrenadora = ? WHERE id = ?", (hoy, vencimiento, telefono, plan_tipo, con_entrenadora, cliente_id))
    else:
        c.execute("INSERT INTO clientes (nombre, telefono, fecha_ultimo_pago, fecha_vencimiento, fecha_inscripcion, plan_actual, con_entrenadora) VALUES (?, ?, ?, ?, ?, ?, ?)", (nombre, telefono, hoy, vencimiento, hoy, plan_tipo, con_entrenadora))
        cliente_id = c.lastrowid
        
    c.execute("INSERT INTO pagos (cliente_id, monto, fecha, metodo_pago, plan_tipo, con_entrenadora) VALUES (?, ?, ?, ?, ?, ?)", (cliente_id, monto, hoy, metodo_pago, plan_tipo, con_entrenadora))
    
    conn.commit()
    conn.close()

def registrar_pago_casual(monto, notas):
    conn = sqlite3.connect('gym.db')
    c = conn.cursor()
    hoy = datetime.date.today()
    
    c.execute("SELECT id FROM clientes WHERE nombre = 'CLIENTE CASUAL'")
    cliente_id = c.fetchone()[0]
    
    c.execute("INSERT INTO pagos (cliente_id, monto, fecha, notas) VALUES (?, ?, ?, ?)", 
              (cliente_id, monto, hoy, notas))
    conn.commit()
    conn.close()

def get_ingresos_hoy():
    conn = sqlite3.connect('gym.db')
    c = conn.cursor()
    hoy = datetime.date.today()
    c.execute("SELECT SUM(monto) FROM pagos WHERE fecha = ?", (str(hoy),))
    total = c.fetchone()[0]
    conn.close()
    return total if total else 0.0

def get_casuales_hoy():
    conn = sqlite3.connect('gym.db')
    hoy = datetime.date.today()
    df = pd.read_sql_query("SELECT p.monto, p.notas FROM pagos p JOIN clientes c ON p.cliente_id = c.id WHERE c.nombre = 'CLIENTE CASUAL' AND p.fecha = ?", conn, params=(str(hoy),))
    conn.close()
    return df

def registrar_asistencia(cliente_id):
    conn = sqlite3.connect('gym.db')
    c = conn.cursor()
    cliente_id = int(cliente_id) # Forzar entero de Python para evitar BLOBs
    
    c.execute("SELECT id FROM asistencia WHERE cliente_id = ? AND date(fecha) = date('now', 'localtime')", (cliente_id,))
    
    if not c.fetchone():
        # Guardar datetime completo (fecha y hora)
        c.execute("INSERT INTO asistencia (cliente_id, fecha) VALUES (?, datetime('now', 'localtime'))", (cliente_id,))
        conn.commit()
    conn.close()

def get_ingresos_semana():
    conn = sqlite3.connect('gym.db')
    c = conn.cursor()
    hoy = datetime.date.today()
    inicio_semana = hoy - datetime.timedelta(days=hoy.weekday()) # Lunes
    c.execute("SELECT SUM(monto) FROM pagos WHERE fecha >= ? AND fecha <= ?", (str(inicio_semana), str(hoy)))
    total = c.fetchone()[0]
    conn.close()
    return total if total else 0.0

def get_ingresos_mes():
    conn = sqlite3.connect('gym.db')
    c = conn.cursor()
    hoy = datetime.date.today()
    inicio_mes = hoy.replace(day=1)
    c.execute("SELECT SUM(monto) FROM pagos WHERE fecha >= ? AND fecha <= ?", (str(inicio_mes), str(hoy)))
    total = c.fetchone()[0]
    conn.close()
    return total if total else 0.0

def get_asistencia_hoy():
    conn = sqlite3.connect('gym.db')
    df = pd.read_sql_query("SELECT c.nombre, strftime('%d/%m/%Y', a.fecha) as dia, strftime('%H:%M:%S', a.fecha) as hora FROM asistencia a JOIN clientes c ON a.cliente_id = c.id WHERE date(a.fecha) = date('now', 'localtime')", conn)
    conn.close()
    return df

# --- INTERFAZ ---

# Header
st.markdown('''
<div class="header-container">
    <div class="header-title">MARY'S GYM</div>
    <div class="header-subtitle">Panel de Control Inteligente</div>
</div>
''', unsafe_allow_html=True)

# KPIs
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown(f'<div class="metric-card"><div class="metric-value">${get_ingresos_hoy():,.0f}</div><div class="metric-label">Ingresos Hoy</div></div>', unsafe_allow_html=True)
with col_m2:
    st.markdown(f'<div class="metric-card"><div class="metric-value">${get_ingresos_semana():,.0f}</div><div class="metric-label">Esta Semana</div></div>', unsafe_allow_html=True)
with col_m3:
    st.markdown(f'<div class="metric-card"><div class="metric-value">${get_ingresos_mes():,.0f}</div><div class="metric-label">Este Mes</div></div>', unsafe_allow_html=True)

# Tabs
tab_dash, tab_reg, tab_asist, tab_hist, tab_asist_hist = st.tabs(["📊 DASHBOARD", "💰 REGISTRAR PAGO", "📝 ASISTENCIA", "📜 HISTORIAL", "📅 HIST. ASISTENCIA"])

with tab_dash:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Estado de Clientes")
    df_clientes = get_clientes()
    
    if not df_clientes.empty:
        df_clientes['fecha_vencimiento'] = pd.to_datetime(df_clientes['fecha_vencimiento']).dt.date
        hoy = datetime.date.today()
        df_clientes['Dias_Restantes'] = df_clientes['fecha_vencimiento'].apply(lambda x: (x - hoy).days)
        df_clientes = df_clientes.sort_values('Dias_Restantes')
        
        # Filtrar clientes con planes largos (Semana, Quincena, Mensual) para las columnas
        df_planes_largos = df_clientes[df_clientes['plan_actual'].isin(['Semana', 'Quincena', 'Mensual'])]
        
        # Filtrar clientes de rutina pagados HOY
        df_rutinas_hoy = df_clientes[(df_clientes['plan_actual'] == 'Rutina') & (df_clientes['fecha_ultimo_pago'] == str(hoy))]
        
        col_act, col_por, col_ven = st.columns(3)
        
        with col_act:
            st.markdown("### Activos")
            for index, row in df_planes_largos[df_planes_largos['Dias_Restantes'] > 3].iterrows():
                st.markdown(f'<div class="client-card"><div><div class="client-name">{row["nombre"]}</div><div class="badge-plan">{row["plan_actual"]}</div><div class="client-info">Vence: {row["fecha_vencimiento"]} ({row["Dias_Restantes"]} días)</div></div><div><span class="badge badge-active">Activo</span></div></div>', unsafe_allow_html=True)
                
        with col_por:
            st.markdown("### Por Vencer")
            for index, row in df_planes_largos[(df_planes_largos['Dias_Restantes'] <= 3) & (df_planes_largos['Dias_Restantes'] >= 0)].iterrows():
                st.markdown(f'<div class="client-card"><div><div class="client-name">{row["nombre"]}</div><div class="badge-plan">{row["plan_actual"]}</div><div class="client-info">Vence: {row["fecha_vencimiento"]} ({row["Dias_Restantes"]} días)</div></div><div><span class="badge badge-warning">Alerta</span></div></div>', unsafe_allow_html=True)
                
                if row['telefono']:
                    tel_limpio = "".join(filter(str.isdigit, row['telefono']))
                    msg = f"Hola {row['nombre']}, te recordamos que tu plan en MARY'S GYM está por vencer. ¡Te esperamos!"
                    link = f"https://wa.me/{tel_limpio}?text={msg.replace(' ', '%20')}"
                    st.markdown(f'<div style="text-align: right; margin-top: -10px;"><a href="{link}" target="_blank" class="wa-link">💬 WhatsApp</a></div>', unsafe_allow_html=True)

        with col_ven:
            st.markdown("### Vencidos")
            for index, row in df_planes_largos[df_planes_largos['Dias_Restantes'] < 0].iterrows():
                st.markdown(f'<div class="client-card"><div><div class="client-name">{row["nombre"]}</div><div class="badge-plan">{row["plan_actual"]}</div><div class="client-info">Venció: {row["fecha_vencimiento"]} ({abs(row["Dias_Restantes"])} días)</div></div><div><span class="badge badge-expired">Vencido</span></div></div>', unsafe_allow_html=True)
                
                if row['telefono']:
                    tel_limpio = "".join(filter(str.isdigit, row['telefono']))
                    msg = f"Hola {row['nombre']}, tu plan en MARY'S GYM ya venció. Te invitamos a renovarlo. ¡Gracias!"
                    link = f"https://wa.me/{tel_limpio}?text={msg.replace(' ', '%20')}"
                    st.markdown(f'<div style="text-align: right; margin-top: -10px;"><a href="{link}" target="_blank" class="wa-link">💬 WhatsApp</a></div>', unsafe_allow_html=True)
                    
        # Sección para Rutinas de Hoy
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Rutinas de Hoy")
        if not df_rutinas_hoy.empty:
            for index, row in df_rutinas_hoy.iterrows():
                st.markdown(f'<div class="client-card"><div><div class="client-name">{row["nombre"]}</div><div class="badge-plan">RUTINA</div></div><div><span class="badge badge-active">Hoy</span></div></div>', unsafe_allow_html=True)
        else:
            st.info("No hay clientes con plan de Rutina registrados hoy.")
    else:
        st.info("No hay clientes registrados.")

with tab_reg:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Registrar Pago")
    
    if 'success_pago' in st.session_state:
        st.success(st.session_state.success_pago)
        del st.session_state.success_pago
        
    st.markdown('''**Tarifas Normales:** Rutina: $5,000 | Semana: $20,000 | Quincena: $40,000 | Mensual: $60,000\n**Con Entrenadora:** Rutina: $10,000 | Semana: $30,000 | Quincena: $60,000 | Mensual: $100,000''')
    
    with st.form("registro_pago_form", clear_on_submit=True):
        nombre = st.text_input("Nombre del Cliente")
        telefono = st.text_input("Teléfono (ej: 573001234567)")
        plan = st.selectbox("Tipo de Plan", ["Rutina", "Semana", "Quincena", "Mensual"])
        entrenadora = st.checkbox("Con Entrenadora")
        metodo = st.selectbox("Método de Pago", ["Efectivo", "Nequi", "Transferencia", "Otro"])
        
        submit_btn = st.form_submit_button("REGISTRAR PAGO")
        
        if submit_btn:
            if nombre:
                registrar_pago(nombre, telefono, plan, entrenadora, metodo)
                st.session_state.success_pago = f"¡Pago registrado para {nombre}!"
                st.rerun()
            else:
                st.error("Por favor completa el nombre.")

with tab_asist:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Control de Asistencia")
    
    if 'success_asist' in st.session_state:
        st.success(st.session_state.success_asist)
        del st.session_state.success_asist
        
    df_clientes = get_clientes()
    if not df_clientes.empty:
        # Filtrar solo clientes con plan Semana, Quincena o Mensual
        df_clientes_filtrados = df_clientes[df_clientes['plan_actual'].isin(['Semana', 'Quincena', 'Mensual'])]
        
        # Obtener los que ya asistieron hoy
        df_asist_hoy = get_asistencia_hoy()
        asistidos_hoy = df_asist_hoy['nombre'].tolist() if not df_asist_hoy.empty else []
        
        # Filtrar los que NO han asistido hoy
        df_clientes_por_asistir = df_clientes_filtrados[~df_clientes_filtrados['nombre'].isin(asistidos_hoy)]
        
        if not df_clientes_por_asistir.empty:
            nombres_clientes = df_clientes_por_asistir['nombre'].tolist()
            
            with st.form("asistencia_form", clear_on_submit=False):
                cliente_sel = st.selectbox("Seleccionar Cliente para Asistencia", nombres_clientes)
                submit_asist = st.form_submit_button("REGISTRAR ENTRADA")
                
                if submit_asist:
                    cliente_id = df_clientes_por_asistir[df_clientes_por_asistir['nombre'] == cliente_sel]['id'].values[0]
                    registrar_asistencia(cliente_id)
                    st.session_state.success_asist = f"¡Asistencia registrada para {cliente_sel}!"
                    st.rerun()
        else:
            if df_clientes_filtrados.empty:
                st.info("No hay clientes con planes de Semana, Quincena o Mensual para registrar asistencia.")
            else:
                st.success("¡Todos los clientes aptos ya registraron su asistencia el día de hoy! 🏋️‍♂️")
            
    st.subheader("Asistentes de Hoy")
    df_asist = get_asistencia_hoy()
    if not df_asist.empty:
        html = '''<div class="custom-table-container">
<table class="custom-table">
<thead>
<tr>
<th>Nombre</th>
<th>Día</th>
<th>Hora</th>
</tr>
</thead>
<tbody>'''
        for index, row in df_asist.iterrows():
            html += f'''<tr>
<td>{row['nombre']}</td>
<td>{row['dia']}</td>
<td>{row['hora']}</td>
</tr>'''
        html += '''</tbody>
</table>
</div>'''
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("No hay asistencia registrada hoy.")

with tab_hist:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Historial de Pagos")
    
    conn = sqlite3.connect('gym.db')
    df_pagos = pd.read_sql_query("SELECT p.fecha, c.nombre, p.monto, p.plan_tipo, p.metodo_pago, p.con_entrenadora FROM pagos p JOIN clientes c ON p.cliente_id = c.id ORDER BY p.fecha DESC", conn)
    conn.close()
    
    if not df_pagos.empty:
        df_pagos['con_entrenadora'] = df_pagos['con_entrenadora'].apply(lambda x: "Sí" if x else "No")
        
        html = '''<div class="custom-table-container">
<table class="custom-table">
<thead>
<tr>
<th>Fecha</th>
<th>Cliente</th>
<th>Monto</th>
<th>Plan</th>
<th>Método</th>
<th>Entrenadora</th>
</tr>
</thead>
<tbody>'''
        for index, row in df_pagos.iterrows():
            html += f'''<tr>
<td>{row['fecha']}</td>
<td>{row['nombre']}</td>
<td>${row['monto']:,.0f}</td>
<td>{row['plan_tipo']}</td>
<td>{row['metodo_pago']}</td>
<td>{row['con_entrenadora']}</td>
</tr>'''
        html += '''</tbody>
</table>
</div>'''
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("No hay historial de pagos.")

with tab_asist_hist:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Historial de Asistencia")
    
    conn = sqlite3.connect('gym.db')
    df_asist_full = pd.read_sql_query("SELECT c.nombre, strftime('%d/%m/%Y', a.fecha) as dia, strftime('%H:%M:%S', a.fecha) as hora FROM asistencia a JOIN clientes c ON a.cliente_id = c.id ORDER BY a.fecha DESC", conn)
    conn.close()
    
    if not df_asist_full.empty:
        html = '''<div class="custom-table-container">
<table class="custom-table">
<thead>
<tr>
<th>Nombre</th>
<th>Día</th>
<th>Hora</th>
</tr>
</thead>
<tbody>'''
        for index, row in df_asist_full.iterrows():
            html += f'''<tr>
<td>{row['nombre']}</td>
<td>{row['dia']}</td>
<td>{row['hora']}</td>
</tr>'''
        html += '''</tbody>
</table>
</div>'''
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("No hay historial de asistencia.")
