import streamlit as st
import datetime
import os
import urllib.parse 
import pandas as pd

# --- CONFIGURACIÓN ---
NOMBRE_TIENDA = "JESSY STORE 🛍️" 
COSTO_ENVIO = 4.00
WHATSAPP_NEGOCIO = "50376813561" 
ARCHIVO_PEDIDOS = "pedidos_base.csv"

st.set_page_config(page_title=NOMBRE_TIENDA, page_icon="🛍️", layout="wide")

# --- MOTOR DE DATOS ---
def guardar_pedido(datos):
    df_nuevo = pd.DataFrame([datos])
    if not os.path.isfile(ARCHIVO_PEDIDOS):
        df_nuevo.to_csv(ARCHIVO_PEDIDOS, index=False, encoding="utf-8")
    else:
        df_nuevo.to_csv(ARCHIVO_PEDIDOS, mode='a', header=False, index=False, encoding="utf-8")

# --- LISTA DE PRODUCTOS ---
productos = [
    {"id": 1, "nombre": "Paraguas Reforzado", "precio": 10.00, "desc": "Protección contra lluvia y sol.", "imagen": "paraguas.png.jpg"},
    {"id": 2, "nombre": "Bicicleta Montañera", "precio": 20.00, "desc": "Resistente para todo terreno.", "imagen": "catalogo/bicicleta.jpg"},
    {"id": 3, "nombre": "Paila de Plástico", "precio": 25.00, "desc": "Paila de plástico reforzado.", "imagen": "catalogo/paila.jpg"},
    {"id": 4, "nombre": "Cocina de Gas", "precio": 30.00, "desc": "Eficiente para el hogar.", "imagen": "catalogo/cocina.jpg"}
]

st.title(f"🌸 {NOMBRE_TIENDA}")

# --- PANEL DE CONTROL (ARRIBA) ---
with st.expander("🛠️ PANEL DE CONTROL (PEDIDOS CONFIRMADOS)"):
    if os.path.exists(ARCHIVO_PEDIDOS):
        try:
            df_p = pd.read_csv(ARCHIVO_PEDIDOS)
            if 'Celular' in df_p.columns:
                st.dataframe(df_p, use_container_width=True)
                for i, row in df_p.iterrows():
                    st.checkbox(f"Hecho: {row['Cliente']} ({row['Producto']})", key=f"e_{i}")
            else:
                st.warning("⚠️ Borra 'pedidos_base.csv' para actualizar el sistema.")
        except:
            st.error("Error al leer datos.")
    else:
        st.info("No hay pedidos registrados.")

st.write("---")

# --- CATÁLOGO ---
for p in productos:
    with st.container():
        col_img, col_txt = st.columns([1, 2])
        with col_img:
            if os.path.exists(p['imagen']): st.image(p['imagen'], width=200)
            else: st.warning("Sin foto")
        with col_txt:
            st.header(p['nombre'])
            st.subheader(f"${p['precio']:.2f}")
            st.write(p['desc'])
            
            c1, c2 = st.columns(2)
            with c1:
                url_i = f"https://wa.me/{WHATSAPP_NEGOCIO}?text=Info%20de%20{p['nombre']}"
                st.link_button("💬 Consultar WhatsApp", url=url_i, use_container_width=True)
            with c2:
                if st.button(f"🛒 Pedir {p['nombre']}", key=f"btn_{p['id']}", use_container_width=True):
                    st.session_state.id_comprando = p['id']
                    st.session_state.pedido_exitoso = False # Reiniciamos estado al pedir nuevo
                    st.rerun()

    # --- LÓGICA DE FORMULARIO O BOTÓN DE WHATSAPP ---
    if st.session_state.get('id_comprando') == p['id']:
        
        # SI EL PEDIDO YA SE REGISTRÓ, MOSTRAMOS EL BOTÓN DE WHATSAPP JUSTO AQUÍ
        if st.session_state.get('pedido_exitoso'):
            st.balloons()
            st.success("✅ ¡Datos registrados en nuestra lista!")
            st.link_button("📲 ENVIAR PEDIDO POR WHATSAPP", url=st.session_state.url_final, type="primary", use_container_width=True)
            if st.button("Finalizar y cerrar"):
                st.session_state.id_comprando = None
                st.session_state.pedido_exitoso = False
                st.rerun()
        
        # SI NO SE HA REGISTRADO, MOSTRAMOS EL FORMULARIO
        else:
            st.info(f"📍 Datos de entrega para: {p['nombre']}")
            with st.form(key=f"form_{p['id']}"):
                f1, f2 = st.columns(2)
                with f1:
                    nombre = st.text_input("Nombre y Apellido*")
                    celular = st.text_input("Número de Celular*")
                with f2:
                    depto = st.selectbox("Departamento*", ["Ahuachapán", "Cabañas", "Chalatenango", "Cuscatlán", "La Libertad", "La Paz", "La Unión", "Morazán", "San Miguel", "San Salvador", "San Vicente", "Santa Ana", "Sonsonate", "Usulután"])
                    distrito = st.text_input("Distrito*")
                
                direccion = st.text_input("Dirección Exacta*")
                total = p['precio'] + COSTO_ENVIO
                
                b_env, b_can = st.columns(2)
                with b_env:
                    if st.form_submit_button("🚀 REGISTRAR PEDIDO"):
                        if nombre and celular and distrito and direccion:
                            fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                            # GUARDAR EN CSV
                            guardar_pedido({
                                "Fecha": fecha, "Producto": p['nombre'], "Precio": p['precio'],
                                "Total": total, "Cliente": nombre, "Celular": celular,
                                "Depto": depto, "Distrito": distrito, "Direccion": direccion
                            })
                            # PREPARAR WHATSAPP
                            texto_wa = f"✅ *NUEVO PEDIDO*\n📦 *Producto:* {p['nombre']}\n👤 *Cliente:* {nombre}\n📱 *Cel:* {celular}\n🏠 *Dirección:* {direccion}, {distrito}\n💰 *TOTAL:* ${total:.2f}"
                            st.session_state.url_final = f"https://wa.me/{WHATSAPP_NEGOCIO}?text={urllib.parse.quote(texto_wa)}"
                            st.session_state.pedido_exitoso = True # Cambiamos a estado exitoso
                            st.rerun()
                        else:
                            st.error("⚠️ Llena todos los campos.")
                with b_can:
                    if st.form_submit_button("❌ CANCELAR"):
                        st.session_state.id_comprando = None
                        st.rerun()
    st.write("---")