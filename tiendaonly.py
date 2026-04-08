import streamlit as st
import datetime

# --- CONFIGURACIÓN DEL NEGOCIO ---
COSTO_ENVIO = 4.00
WHATSAPP_NEGOCIO = "50370000000" # Tu número real aquí

# Configuración de la página (Título en la pestaña del navegador)
st.set_page_config(page_title="Tienda Online | Pedidos", layout="wide")

# --- BASE DE DATOS DE PRODUCTOS ---
# Si quieres agregar más, solo copia una línea y cambia los datos
productos = [
    {"id": 1, "nombre": "Reloj Inteligente Z", "precio": 45.0, "desc": "Pantalla AMOLED, ideal para deportes."},
    {"id": 2, "nombre": "Audífonos Bluetooth G", "precio": 25.0, "desc": "Sonido HD con cancelación de ruido."},
    {"id": 3, "nombre": "Cargador Carga Rápida", "precio": 15.0, "desc": "Carga tu celular al 100% en minutos."}
]

# --- INTERFAZ DEL CLIENTE ---
st.title("🛍️ BIENVENIDO A NUESTRA TIENDA")
st.write("Selecciona tus productos favoritos y te los enviamos a la puerta de tu casa.")
st.divider()

# Mostramos los productos en columnas
cols = st.columns(len(productos))

for i, p in enumerate(productos):
    with cols[i]:
        st.subheader(p['nombre'])
        st.write(f"### ${p['precio']}")
        st.write(p['desc'])
        
        # Botón de consulta rápida
        url_wa = f"https://wa.me/{WHATSAPP_NEGOCIO}?text=Hola, quiero info de {p['nombre']}"
        st.markdown(f"[💬 Info por WhatsApp]({url_wa})")
        
        if st.button(f"Comprar {p['nombre']}", key=f"btn_{p['id']}"):
            st.session_state.producto_elegido = p

# --- PROCESO DE PEDIDO ---
if 'producto_elegido' in st.session_state:
    p_compra = st.session_state.producto_elegido
    st.divider()
    st.header(f"📦 Datos de Envío para: {p_compra['nombre']}")
    
    with st.form("datos_cliente"):
        nombre = st.text_input("Nombre y Apellido*")
        
        c1, c2 = st.columns(2)
        with c1:
            depto = st.text_input("Departamento*")
            distrito = st.text_input("Distrito / Municipio*")
        with c2:
            colonia = st.text_input("Colonia / Caserío / Cantón*")
            casa = st.text_input("Número de casa / Lote")
            
        referencia = st.text_area("Punto de referencia detallado (ej: frente al árbol de ceiba)*")
        celular = st.text_input("Número de celular (Te llamaremos para confirmar)*")
        
        total = p_compra['precio'] + COSTO_ENVIO
        st.info(f"**Total a pagar al recibir:** ${total} (Incluye ${COSTO_ENVIO} de envío)")
        
        if st.form_submit_button("🚀 CONFIRMAR PEDIDO"):
            if nombre and depto and distrito and colonia and referencia and celular:
                # GUARDAR VENTA
                fecha_hora = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                registro = f"[{fecha_hora}] {p_compra['nombre']} | CLIENTE: {nombre} | CEL: {celular} | DIR: {colonia}, {distrito}, {depto} | REF: {referencia}\n"
                
                with open("pedidos.txt", "a", encoding="utf-8") as f:
                    f.write(registro)
                
                st.success(f"¡Pedido de {p_compra['nombre']} recibido! Prepárate, te llamaremos pronto.")
                st.balloons()
                del st.session_state.producto_elegido
            else:
                st.error("Por favor llena todos los campos marcados con *")