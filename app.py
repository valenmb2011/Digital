import streamlit as st
st.set_page_config(page_title="App Gimnasio", page_icon="🏋️‍♂️")

# --- 1. CONFIGURACIÓN INICIAL DEL ESTADO (st.session_state) ---
if 'clientes' not in st.session_state:
    # Inicializamos los 3 clientes base vacíos para que pida la info la primera vez
    st.session_state.clientes = {
        "Cliente 1": {},
        "Cliente 2": {},
        "Cliente 3": {}
    }

if 'rutinas' not in st.session_state:
    # Diccionario separado para las rutinas de los clientes
    st.session_state.rutinas = {
        "Cliente 1": [],
        "Cliente 2": [],
        "Cliente 3": []
    }

if 'pantalla' not in st.session_state:
    st.session_state.pantalla = "inicio"

if 'cliente_actual' not in st.session_state:
    st.session_state.cliente_actual = None

if 'modo_edicion' not in st.session_state:
    st.session_state.modo_edicion = False

# --- FUNCIONES DE NAVEGACIÓN ---
def cambiar_pantalla(nueva_pantalla, cliente=None):
    st.session_state.pantalla = nueva_pantalla
    if cliente is not None:
        st.session_state.cliente_actual = cliente
    st.session_state.modo_edicion = False
    st.rerun()

def volver_inicio():
    cambiar_pantalla("inicio")

# --- PANTALLAS DE LA APP ---

def pantalla_inicio():
    st.title("Bienvenido")
    
   # Buscador de clientes
    st.subheader("Buscar cliente ...")
    buscar = st.text_input("Ingrese el nombre del cliente que busca:", key="input_buscar")
    
    if st.button("Buscar"):
        encontrado = None
        for key, data in st.session_state.clientes.items():
            if buscar.lower() in key.lower() or (data and buscar.lower() in data.get('Nombre', '').lower()):
                encontrado = key
                break
        
        # Guardamos el resultado en la memoria temporal
        st.session_state.cliente_buscado = encontrado if encontrado else "NO_EXISTE"

    # Mostramos el segundo botón de forma independiente
    if st.session_state.get("cliente_buscado"):
        if st.session_state.cliente_buscado == "NO_EXISTE":
            st.error("Cliente no encontrado")
        else:
            cliente_hallado = st.session_state.cliente_buscado
            st.success(f"Cliente encontrado: {cliente_hallado}")
            if st.button(f"Ir al perfil de {cliente_hallado}"):
                st.session_state.cliente_buscado = None # Limpiamos la búsqueda
                cambiar_pantalla("perfil", cliente_hallado)
                
    st.write("---")
    
    # Lista de usuarios (basado en el boceto 1)
    st.subheader("Lista de Usuarios")
    for cliente in st.session_state.clientes.keys():
        nombre_mostrar = st.session_state.clientes[cliente].get('Nombre', 'Sin datos')
        if st.button(f"• {cliente} ({nombre_mostrar})", use_container_width=True):
            cambiar_pantalla("perfil", cliente)

    st.write("---")
    
    # Botones de agregar y eliminar
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Agregar usuario", use_container_width=True):
            cambiar_pantalla("agregar")
    with col2:
        if st.button("➖ Eliminar usuario", use_container_width=True):
            cambiar_pantalla("eliminar")


def pantalla_agregar():
    st.title("Agregar nuevo usuario")
    
    with st.form("form_agregar"):
        nombre = st.text_input("Nombre y apellido")
        edad = st.text_input("Edad")
        telefono = st.text_input("Teléfono")
        objetivo = st.text_input("Objetivo")
        dias_entrena = st.text_input("Días que entrena")
        lesiones = st.text_input("Lesiones (si tiene)")
        peso_altura = st.text_input("Peso y altura")
        rutina = st.text_input("Nombre de rutina")
        estado_pago = st.text_input("Estado del pago")
        
        guardar = st.form_submit_button("Guardar usuario")
        
        if guardar:
            if nombre:
                nuevo_id = f"Cliente {len(st.session_state.clientes) + 1}"
                st.session_state.clientes[nuevo_id] = {
                    "Nombre": nombre,
                    "Edad": edad,
                    "Teléfono": telefono,
                    "Objetivo": objetivo,
                    "Días que entrena": dias_entrena,
                    "Lesiones": lesiones,
                    "Peso y altura": peso_altura,
                    "Rutina": rutina,
                    "Estado del pago": estado_pago
                }
                st.session_state.rutinas[nuevo_id] = []
                st.success(f"{nuevo_id} ({nombre}) agregado correctamente.")
                volver_inicio()
            else:
                st.warning("El nombre es obligatorio.")

    if st.button("Volver al inicio"):
        volver_inicio()


def pantalla_eliminar():
    st.title("Eliminar usuario")
    
    opciones = list(st.session_state.clientes.keys())
    if not opciones:
        st.info("No hay clientes para eliminar.")
    else:
        eliminar = st.selectbox("Seleccione el cliente a eliminar:", opciones)
        if st.button("Eliminar"):
            del st.session_state.clientes[eliminar]
            if eliminar in st.session_state.rutinas:
                del st.session_state.rutinas[eliminar]
            st.success(f"{eliminar} eliminado.")
            st.rerun() # Recarga automática para actualizar la lista

    if st.button("Volver al inicio"):
        volver_inicio()


def pantalla_perfil():
    cliente = st.session_state.cliente_actual
    datos = st.session_state.clientes.get(cliente, {})
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(f"{cliente}")
    with col2:
        if st.button("Editar" if not st.session_state.modo_edicion else "Cancelar edición"):
            st.session_state.modo_edicion = not st.session_state.modo_edicion
            st.rerun()

    # Si no tiene datos, o si presionó editar, mostramos el formulario
    if not datos or st.session_state.modo_edicion:
        st.info("Por favor, ingrese o actualice la información del cliente.")
        with st.form("form_perfil"):
            nombre = st.text_input("Nombre y apellido", value=datos.get("Nombre", ""))
            edad = st.text_input("Edad", value=datos.get("Edad", ""))
            telefono = st.text_input("Teléfono", value=datos.get("Teléfono", ""))
            objetivo = st.text_input("Objetivo", value=datos.get("Objetivo", ""))
            dias_entrena = st.text_input("Días que entrena", value=datos.get("Días que entrena", ""))
            lesiones = st.text_input("Lesiones", value=datos.get("Lesiones", ""))
            peso_altura = st.text_input("Peso y altura", value=datos.get("Peso y altura", ""))
            rutina = st.text_input("Rutina y ejercicios", value=datos.get("Rutina", ""))
            estado_pago = st.text_input("Estado del pago", value=datos.get("Estado del pago", ""))
            
            if st.form_submit_button("Guardar"):
                st.session_state.clientes[cliente] = {
                    "Nombre": nombre,
                    "Edad": edad,
                    "Teléfono": telefono,
                    "Objetivo": objetivo,
                    "Días que entrena": dias_entrena,
                    "Lesiones": lesiones,
                    "Peso y altura": peso_altura,
                    "Rutina": rutina,
                    "Estado del pago": estado_pago
                }
                st.session_state.modo_edicion = False
                st.rerun()
    else:
        # Si ya tiene datos, los mostramos como en el boceto 2
        st.subheader(f"{datos.get('Nombre', '')}")
        
        # Convertimos el diccionario a una lista de diccionarios para st.table
        datos_tabla = [{"Campo": k, "Valor": v} for k, v in datos.items()]
        st.table(datos_tabla)
        
        st.write("---")
        col_rutina, col_volver = st.columns(2)
        with col_rutina:
            if st.button("Ver rutina", use_container_width=True):
                cambiar_pantalla("rutina", cliente)
        with col_volver:
            if st.button("Volver al inicio", use_container_width=True):
                volver_inicio()


def pantalla_rutina():
    cliente = st.session_state.cliente_actual
    rutina_guardada = st.session_state.rutinas.get(cliente, [])
    
    col1, col2 = st.columns([3, 1])
    with col1:
        nombre_rutina = st.session_state.clientes.get(cliente, {}).get("Rutina", "Tren superior")
        st.title(f"Rutina de {cliente}")
        st.subheader(f"{nombre_rutina}")
    with col2:
        if st.button("Editar rutina" if not st.session_state.modo_edicion else "Cancelar edición"):
            st.session_state.modo_edicion = not st.session_state.modo_edicion
            st.rerun()

    # Originalmente se pedían 9 ejercicios. Los mostramos en 3 series como en el código base.
    if len(rutina_guardada) < 9 or st.session_state.modo_edicion:
        st.info("Configure los 9 ejercicios de la rutina.")
        with st.form("form_ejercicios"):
            ejercicios = []
            for i in range(1, 10):
                val_actual = rutina_guardada[i-1] if len(rutina_guardada) >= i else ""
                ejercicios.append(st.text_input(f"Ejercicio {i}", value=val_actual))
            
            if st.form_submit_button("Guardar Rutina"):
                st.session_state.rutinas[cliente] = ejercicios
                st.session_state.modo_edicion = False
                st.rerun()
    else:
        # Mostrar las series como en el código original pero con estilo Streamlit (boceto 3)
        st.markdown("### Serie 1")
        st.write(f"• Ejercicio 1: {rutina_guardada[0]}")
        st.write(f"• Ejercicio 2: {rutina_guardada[1]}")
        st.write(f"• Ejercicio 3: {rutina_guardada[2]}")
        
        st.markdown("### Serie 2")
        st.write(f"• Ejercicio 4: {rutina_guardada[3]}")
        st.write(f"• Ejercicio 5: {rutina_guardada[4]}")
        st.write(f"• Ejercicio 6: {rutina_guardada[5]}")
        
        st.markdown("### Serie 3")
        st.write(f"• Ejercicio 7: {rutina_guardada[6]}")
        st.write(f"• Ejercicio 8: {rutina_guardada[7]}")
        st.write(f"• Ejercicio 9: {rutina_guardada[8]}")
        
    st.write("---")
    col_perfil, col_inicio = st.columns(2)
    with col_perfil:
        if st.button("Volver al perfil", use_container_width=True):
            cambiar_pantalla("perfil", cliente)
    with col_inicio:
        if st.button("Volver al inicio", use_container_width=True):
            volver_inicio()

# --- ENRUTADOR PRINCIPAL ---
if st.session_state.pantalla == "inicio":
    pantalla_inicio()
elif st.session_state.pantalla == "agregar":
    pantalla_agregar()
elif st.session_state.pantalla == "eliminar":
    pantalla_eliminar()
elif st.session_state.pantalla == "perfil":
    pantalla_perfil()
elif st.session_state.pantalla == "rutina":
    pantalla_rutina()
