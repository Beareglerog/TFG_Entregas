import streamlit as st
from main import *


st.set_page_config(
    layout="wide",
    page_title="TFG – Simulador Energético (EES → Python)"
)

# ============================================================
# LISTAS DE ENTRADA
# ============================================================
PROVINCIAS = ["Albacete", "Alicante/Alacant", "Almería", "Ávila", "Badajoz", "Barcelona", "Bizkaia",
            "Burgos", "Cáceres", "Cádiz", "Castellón/Castelló", "Ceuta", "Ciudad Real", "Córdoba", 
            "Coruña, A", "Cuenca", "Gipuzkoa", "Girona", "Granada", "Guadalajara", "Huelva", "Huesca", 
            "Jaén", "León", "Lleida", "Rioja, La", "Lugo", "Madrid", "Málaga", "Melilla", "Murcia", "Ourense", 
            "Asturias", "Palencia", "Baleares, Illes", "Palmas, Las", "Navarra", "Pontevedra", "Salamanca", 
            "Santa Cruz de Tenerife", "Cantabria", "Segovia", "Sevilla", "Soria", "Tarragona", "Teruel", "Toledo",
              "Valencia/València", "Valladolid", "Araba/Álava", "Zamora", "Zaragoza"]
ANOS_CONSTRUCCION_CALIFE = ["Anterior a 1981", "1981 a 2007", "Posterior a 2007","A", "B", "C", "D Alta", "D Baja", "E Alta", "E Media", "E Baja" "F", "G"]
TIPOS_VIVIENDA = ["Bloque", "Unifamiliar"]
SISTEMAS_ACS = [ "glp", "Biomasa", "Carbón", "Gas Natural", "Electricidad"]
SISTEMAS_CALEFACCION = [ "glp", "Gasóleo","Biomasa", "Carbón", "Gas Natural", "Electricidad (radiadores)", "Electricidad (acumuladores)", "Bomba de calor"]
TIPOS_INSTALACION_ACS = ["Individual", "Central"]
TIPOS_INSTALACION_CAL = ["Individual", "Central", "Aparatos"]




# ============================================================
# CSS
# ============================================================
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* ---------------------------
       Base tipografía
    --------------------------- */
    html, body, [class*="st-emotion-"] {
        font-family: 'Merriweather', serif !important;
        font-size: 1.0em;
        color: #212529;
    }

    h1,h2,h3 {
        font-family: 'Merriweather', serif !important;
        font-weight: 800;
        color: #0B3A66;
        letter-spacing: -0.2px;
    }

    /* Fondo */
    .stApp {
        background: radial-gradient(1200px 500px at 10% 0%, rgba(0,123,255,0.08), transparent 60%),
                    radial-gradient(900px 450px at 90% 0%, rgba(40,167,69,0.06), transparent 55%),
                    #fbfcfe;
    }

    /* ---------------------------
       Inputs
    --------------------------- */
    div[data-testid="stSelectbox"],
    div[data-testid="stNumberInput"],
    div[data-testid="stTextInput"],
    div[data-testid="stSlider"] {
        max-width: 200 !important;
    }

    /* Labels */
    .stForm label, label {
    /* Esto controla el tamaño de los titulos de los dropdowns etc */
        font-size: 1.3em !important;
        font-weight: 700 !important;
        color: #3f5b75;
    }
#####################################################################################################
    /* Checkboxes*/
    div[data-testid="stCheckbox"] * {
        font-size: 1.2em !important;
    }

    /* Selectbox*/
    div[data-testid="stSelectbox"] input,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        font-size: 1.1em !important;
        font-weight: 400 !important;
    }

    /* Number input*/
    div[data-testid="stNumberInput"] input {
        font-size: 1.1em !important;
        font-weight: 400 !important;
    }

    /* Opciones del dropdown cuando se despliega */
    div[role="listbox"] li {
        font-size: 1.1em !important;
    }
###################################################################################################################

    /* ---------------------------
       Tabs
    --------------------------- */
    div[data-baseweb="tab-list"] {
        gap: 15px;
        padding-bottom: 6px;
        padding-top: 6px; 
    }
    
    div[data-baseweb="tab-list"] button {
        background: #ffffff;
        border: 1px solid rgba(13, 59, 102, 0.15);
        border-radius: 12px; /*esquinas redondeadas */
        padding: 12px 12px;
        font-weight: 700;
        font-size: 1.25em;
        color: #0B3A66;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
    }

    /* Cuando paso el botón por encima: */
    div[data-baseweb="tab-list"] button:hover {
        box-shadow: 0 2px 10px #3b4045;
        transform: translateY(-1px);
        outline: none;
        transition: 0.15s ease-in-out;
    }

    /* Cuando esta seleccionada la pestaña: */
    div[data-baseweb="tab-list"] button[aria-selected="true"] {
        background: linear-gradient(180deg, rgba(0,123,255,0.14), rgba(0,123,255,0.06));
        border: 1px solid rgba(0,123,255,0.45);
        color: #0B3A66;
    }

    /* ---------------------------
       Paneles
    --------------------------- */
    .panel {
        background: rgba(255,255,255,0.92);
        border: 1px solid rgba(15, 23, 42, 0.10);
        border-radius: 16px;
        width: fit-content;      
        margin-left: auto;           
        margin-right: auto;
        padding: 10px 15px 7px 15px;
        margin-bottom: 20px;  
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
        backdrop-filter: blur(6px);
    }

    .panel-title {
        
        display: block;                
        width: fit-content;           
        margin: 0 auto 5px auto;             
        padding: 5px 8px;
        border-radius: 12px;
        font-weight: 900;
        letter-spacing: 0.1px;
        font-size: 1.5em;
        border: 1px solid rgba(15, 23, 42, 0.10);
    }
   
    .tag-blue { background: rgba(0,123,255,0.10); color: #0B3A66; }
    .tag-green { background: rgba(40,167,69,0.10); color: #145a2b; }
    .tag-orange { background: rgba(253,126,20,0.12); color: #7a3d05; }
    .tag-purple { background: rgba(111,66,193,0.10); color: #3f1e7a; }
    .tag-indigo { background: #e0f7fa; color: #006064;}


    /* ---------------------------
       Cajas resultados
    --------------------------- */
    .caja-demand {
    padding: 14px 18px;
    border-radius: 14px;
    background: rgba(255, 248, 225, 0.85);
    border: 1px solid rgba(255, 236, 179, 0.9);
    box-shadow: 0 10px 22px rgba(15, 23, 42, 0.06);
    }

    .caja-cost {
    padding: 14px 18px;
    border-radius: 14px;
    background: rgba(252, 228, 228, 0.75);
    border: 1px solid rgba(249, 189, 189, 0.9);
    box-shadow: 0 10px 22px rgba(15, 23, 42, 0.06);
    }

    .caja-consumo {
    padding: 14px 18px;
    border-radius: 14px;
    background: rgba(232, 245, 233, 0.78);
    border: 1px solid rgba(200, 230, 201, 0.95);
    box-shadow: 0 10px 22px rgba(15, 23, 42, 0.06);
    }

    .caja-demand h4, .caja-cost h4, .caja-consumo h4 {
    margin: 6px 0;
    font-weight: 700;
    color: #374151;
    font-size: 1.05em;
    }

    .num-right {
    float: right;
    font-weight: 700;
    color: #1f2937;
    }

    /* Botón principal */
    div.stButton > button {
        background-color: #c4e6ff;
        font-weight: 900;
        font-size: 1.25em;
        border-radius: 12px;
        padding: 12px 18px;
        border: 1px solid #4b7ea6;
        box-shadow: 0 10px 14px #4b7ea6;
        transition: 0.15s ease-in-out;
    }
    div.stButton > button:hover {
        background-color: #f5c0ba;
        box-shadow: 0 14px 20px #9fafbf;
        transform: translateY(-1px);

    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================
def panel_open(title: str, color_class: str):
    st.markdown(
        f"""
        <div class="panel">
          <div class="panel-title {color_class}">{title}</div>
        """,
        unsafe_allow_html=True
    )

def panel_close():
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# APP PRINCIPAL
# ============================================================
def main():
    st.title("Simulador de Demanda Energética")
    st.markdown("---")

    # PESTAÑAS AGRUPADAS
    tab_ppal, tab_activa, tab_elec = st.tabs([
        "Pág. ppal",
        "Parte activa",
        "Instalaciones eléctricas",
    ])

    # ---------------------------------------------------------
    # PÁG. PPAL: (Datos generales) + (Horarios y Dimension)
    # ---------------------------------------------------------
    with tab_ppal:
        c1, c_space, c2 = st.columns([1.2, 0.05, 1.2])

        with c1:
            panel_open("DATOS GENERALES Y DEFINICIÓN DE EDIFICIO", "tag-blue")

            st.selectbox("Provincia", PROVINCIAS, key="prov")
            st.number_input("Localidad (altitud) (m)", min_value=0, value=8000, step=50, key="alt")
            st.selectbox("Antigüedad/calificación energética", ANOS_CONSTRUCCION_CALIFE, key="ano")
            st.selectbox("Tipo de vivienda", TIPOS_VIVIENDA, key="tipo_viv")

        with c2:
            panel_open("OCUPACIÓN Y TAMAÑO", "tag-green")

            st.number_input("Número de habitantes (ocupación)", min_value=1, value=3, key="habitantes")
            st.number_input("Espacio (m^2)", min_value=0, value=100, step=10, key="dim")
            st.number_input("Área climatizada en verano (%)", min_value=0, max_value=100, value=100, step=1, key="area_clim")

        panel_close()

    # ---------------------------------------------------------
    # PARTE ACTIVA: ACS + calefacción + refrigeración
    # ---------------------------------------------------------
    with tab_activa:

        st.markdown(
            """
            <div class="section-badge" style="margin-bottom: 20px;">
                <div class="panel-title tag-purple">
                    SISTEMAS TÉRMICOS
                </div>
            </div>
            """,
            unsafe_allow_html=True)
    
        act1, act_space, act2 = st.columns([1.2, 0.05, 1.2])
        
        with act1:
            panel_open("CALEFACCIÓN", "tag-indigo")

            cal1, cal_sapce, cal2 = st.columns([1.2, 0.05, 1.2])

            with cal1:
                st.selectbox("Equipo calefacción", SISTEMAS_CALEFACCION, key="sistema_cal")
            with cal2:
                st.selectbox("Tipo instalación calefacción", TIPOS_INSTALACION_CAL, key="inst_cal")
        with act2:
            panel_open("ACS", "tag-orange")
            ac1, ac_space, ac2 = st.columns([1.2, 0.05, 1.2])
                
            with ac1:
                st.selectbox("Equipo ACS", SISTEMAS_ACS, key="sistema_acs")
            with ac2:
                st.selectbox("Tipo instalación ACS", TIPOS_INSTALACION_ACS, key="inst_acs")
        panel_close()

    # ---------------------------------------------------------
    # INSTALACIONES ELÉCTRICAS
    # ---------------------------------------------------------
    with tab_elec:
        panel_open("INSTALACIONES ELÉCTRICAS", "tag-indigo")

        e1, e2, e3 = st.columns(3)

        with e1:
            st.checkbox("Cocina", key="e_cocina")
            st.checkbox("Horno", key="e_horno")
            st.checkbox("Microondas", key="e_micro")
            st.checkbox("Lavavajillas", key="e_lavavaj")

        with e2:
            st.checkbox("Frigorífico", key="e_frigo")
            st.checkbox("Congelador", key="e_cong")
            st.checkbox("Lavadora", key="e_lav")
            st.checkbox("Secadora", key="e_sec")

        with e3:
            st.checkbox("Televisión", key="e_tv")
            st.checkbox("Ordenador", key="e_pc")
            st.checkbox("Móvil", key="e_mov")
            st.checkbox("Tablet", key="e_tab")

        panel_close()

    # ============================================================
    # RESULTADOS DEMO
    # ============================================================
    st.markdown("---")
    if st.button("EJECUTAR SIMULACIÓN", use_container_width=True):

        # RECOJO INPUTS

        inputs = {

         # De tab_ppal
        'provincia': st.session_state.prov,
        'altitud': st.session_state.alt,
        'calificacion': st.session_state.ano,
        'tipo_vivienda': st.session_state.tipo_viv,
        'habitantes': st.session_state.habitantes,
        'superficie': st.session_state.dim,
        'area_climatizada': st.session_state.area_clim,
        
        # De tab_activa
        'sistema_calefaccion': st.session_state.sistema_cal,
        'inst_calefaccion': st.session_state.inst_cal,
        'sistema_acs': st.session_state.sistema_acs,
        'inst_acs': st.session_state.inst_acs,
        
        # De tab_elec
        'e_cocina': st.session_state.e_cocina,
        'e_horno': st.session_state.e_horno,
        'e_micro': st.session_state.e_micro,
        'e_lavavaj': st.session_state.e_lavavaj,
        'e_frigo': st.session_state.e_frigo,
        'e_cong': st.session_state.e_cong,
        'e_lav': st.session_state.e_lav,
        'e_sec': st.session_state.e_sec,
        'e_tv': st.session_state.e_tv,
        'e_pc': st.session_state.e_pc,
        'e_mov': st.session_state.e_mov,
        'e_tab': st.session_state.e_tab,
        }

        print("Imprimiendo inputs recogidos:")
        for key, value in inputs.items():
            print(f"{key}: {value}")

        resultados = run_demo(inputs)
        print("imprimiendo resultados calculados:")
        for key, value in resultados.items():
            print(f"{key}: {value}")

        # MOSTRAR RESULTADOS
        st.header("Resultados Anuales de Demanda y Gasto")
        st.markdown("---")

        col_out1, col_out2, col_out3 = st.columns([1, 1, 1])

        with col_out1:
            st.subheader("DEMANDA ENERGÉTICA ANUAL (kWh)")
            st.markdown(
                f"""
                <div class="caja-demand">
                    <h4>CALEFACCIÓN <span class="num-right">{resultados['demanda_CorregidaCal']:.0f} kWh</span></h4>
                    <h4>REFRIGERACIÓN <span class="num-right">{resultados['demanda_CorregidaRef']:.0f} kWh</span></h4>
                    <h4>ACS <span class="num-right">{resultados['demanda_ACS']:.0f} kWh</span></h4>
                    <h4>ELECTRICIDAD (NO TÉRMICA) <span class="num-right">{resultados['energia_electrica']:.0f} kWh</span></h4>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_out2:
            st.subheader("GASTO ANUAL (€)")
            st.markdown(
                f"""
                <div class="caja-cost">
                    <h4>GASTO EN CALEFACCIÓN <span class="num-right">€ {resultados['gasto_CAL']:.2f}</span></h4>
                    <h4>GASTO EN ACS <span class="num-right">€ {resultados['gasto_ACS']:.2f}</span></h4>
                    <h4>GASTO EN REFRIGERACIÓN <span class="num-right">€ {resultados['gasto_REFRIGERACION']:.2f}</span></h4>
                    <h4>GASTO EN COMBUSTIBLES <span class="num-right">€ {resultados['gasto_COMBUSTIBLE']:.2f}</span></h4>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_out3:
            st.subheader("CONSUMO ANUAL (kWh)")
            st.markdown(
                f"""
                <div class="caja-consumo">
                    <h4>CONSUMO DE CALEFACCIÓN <span class="num-right">{resultados['consumo_calefaccion']:.0f} kWh</span></h4>
                    <h4>CONSUMO DE ACS <span class="num-right">{resultados['consumo_ACS']:.0f} kWh</span></h4>
                    <h4>CONSUMO DE REFRIGERACIÓN <span class="num-right">{resultados['consumo_refrigeracion']:.0f} kWh</span></h4>
                    <h4>ELECTRICIDAD (NO TÉRMICA) <span class="num-right">{resultados['energia_electrica']:.0f} kWh</span></h4>
                </div>
                """,
                unsafe_allow_html=True
            )

        

        st.toast("Simulación completada.")

if __name__ == "__main__":
    main()
