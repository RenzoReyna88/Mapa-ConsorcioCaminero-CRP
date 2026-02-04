import streamlit as st
import geopandas as gpd
from streamlit_folium import st_folium
import folium

def plot_map(caminos=None, municipio=None):
    """Genera un mapa folium con hasta 3 capas fijas"""
    m = folium.Map(location=[-30.7777517, -64.3105173], zoom_start=10, tiles="CartoDB positron")


    color_dict = {
    "Primaria": "red",
    "Secundaria": "yellow",
    "Terciaria": "orange"
    }


    if caminos is not None:
        folium.GeoJson(
            caminos,
            name="Red Vial Consorcio",
            style_function=lambda x: {
                "color": color_dict.get(x["properties"].get("red"), "black"),
                "weight": 2
            },
            tooltip=folium.GeoJsonTooltip(fields=caminos.columns[:5].tolist())
        ).add_to(m)

    if municipio is not None:
        folium.GeoJson(
            municipio,
            name="Jurisdicción Sarmiento",
            style_function=lambda x: {"color": "Blue", "weight": 2, "fillOpacity": 0.1}
        ).add_to(m)

    folium.LayerControl().add_to(m)
    return m

def main():
    st.set_page_config(
    page_title="Mapa vial del Consorcio Caminero C.C. 033 – Cañada de Río Pinto",
    page_icon="🗺️",
    layout="wide",
)

    # Cargar capas
    caminos = gpd.read_file("assets/archivos-vectorial/gdf_consorcio_crp.json")
    municipio = gpd.read_file("assets/archivos-vectorial/radio_municipio_sarmiento.geojson")
    # Asegurar que los datos estén en el CRS correcto (WGS84 - EPSG:4326)
    if caminos.crs is None:
        caminos = caminos.set_crs("EPSG:22174")  # CRS original de los datos
        caminos = caminos.to_crs("EPSG:4326")
    if municipio.crs is None:
        municipio = municipio.set_crs("EPSG:22174")  # CRS original de los datos
        municipio = municipio.to_crs("EPSG:4326")

    # Opciones de visualización
    st.sidebar.header("Capas disponibles")
    mostrar_caminos = st.sidebar.checkbox("Mostrar Red Vial", True)
    mostrar_municipio = st.sidebar.checkbox("Mostrar Jurisdicción de Sarmiento", True)
    

    # Generar mapa con capas seleccionadas
    m = plot_map(
        caminos if mostrar_caminos else None,
        municipio if mostrar_municipio else None,

    )

   
    st.header("Referencias del mapa vial")
     # Línea roja: Red primaria 
    st.markdown("""
    <span style="display:inline-block; width: 20px; height: 3px; background-color:red; margin-right:5px;"></span>
    Red primaria
    """, unsafe_allow_html=True)
    # Línea amarilla: Red secundaria
    st.markdown("""
    <span style="display:inline-block; width: 20px; height: 3px; background-color:yellow; margin-right:5px;"></span>
    Red secundaria
    """, unsafe_allow_html=True)
    # Línea naranja: Red terciaria
    st.markdown("""
    <span style="display:inline-block; width: 20px; height: 3px; background-color:orange; margin-right:5px;"></span>
    Red terciaria
    """, unsafe_allow_html=True)

    # Línea azul: Radio Municipal
    st.markdown("""
    <span style="display:inline-block; width: 20px; height: 3px; background-color:blue; margin-right:5px;"></span>
    Municipio de Sarmiento
    """, unsafe_allow_html=True)

    # Asegurarse de que la columna lzn sea numérica
    caminos["lzn"] = caminos["lzn"].astype(float)

    # Calcular total de la red
    total_red = caminos["lzn"].sum()

    # Mostrar tarjeta estilo Power BI
    st.metric(label="LONGITUD TOTAL DE LA RED (Km)", value=f"{total_red:.2f}")

    
    # Contenedor con borde redondeado
    st.markdown("""
    <div style="
        border-radius: 20px;      /* Redondea bordes */
        overflow: hidden;         /* Evita que el contenido se salga del contenedor */
        border: 2px solid #ccc;   /* Opcional: borde visible */
    ">
    """, unsafe_allow_html=True)

    st_folium(m, width="100%", height=600)

    st.markdown("</div>", unsafe_allow_html=True)


    st.header("Gestión vial rural y planificación territorial con mapas interactivos personalizables")
    st.markdown("""
    Esta herramienta interactiva permite visualizar la **red vial del Consorcio Caminero C.C. 033 - Cañada de Río Pinto**, 
    la **jurisdicción del municipio de Sarmiento**, y potencialmente las **Zonas productivas**.  

    La aplicación puede personalizarse y adaptase de acuerdo a las necesidades y requerimientos para que las autoridades del Consorcio puedan:
    - Identificar tramos críticos de la red que requieren mejoras o mantenimiento.
    - Analizar la accesibilidad a áreas productivas.
    - Planificar obras de infraestructura de manera estratégica basándose en la geografía y la logística de transporte de productos agropecuarios.
    """)

    st.markdown("---")
    st.markdown("""
    **Autor:** Renzo Gerardo Reyna  
    **Especialidad:** Análisis de datos, SIG y desarrollo de aplicaciones en Python  
    """)

    st.markdown("### Contacto")
    st.markdown("Teléfono: +54 3252 62-0842")
    st.markdown("Email: reynarenzo.88@gmail.com")
    st.markdown("Domicilio: INDEPENDENCIA 0, SARMIENTO, CÓRDOBA, ARGENTINA")

    st.markdown("""
                <div style='text-align: center;'>
                    © 2025 Renzo Gerardo Reyna - Análisis de datos / Desarrollo en Python
                </div>""",
                unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()

