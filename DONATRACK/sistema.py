from blockchain import BlockChain


donaciones = {}

contador = 1
 


def crear_donacion(
    donante,
    descripcion,
    cantidad,
    unidad,
    origen,
    destino
):

    global contador

    id_donacion = f"DON-{contador:04d}"

    datos = {
        "donante": donante,
        "descripcion": descripcion,
        "cantidad": cantidad,
        "unidad": unidad,
        "origen": origen,
        "destino": destino
    }

    texto = (
        f"REGISTRO | {id_donacion} | "
        f"{descripcion} | "
        f"{cantidad:g} {unidad} | "
        f"{origen} -> {destino}"
    )

    donaciones[id_donacion] = {
        "datos": datos,
        "blockchain": BlockChain(texto)
    }

    contador += 1

    return id_donacion


# ============================================================
# OBTENER DONACIONES
# ============================================================

def obtener_donaciones():

    return donaciones


# ============================================================
# OBTENER UNA DONACIÓN
# ============================================================

def obtener_donacion(id_donacion):

    return donaciones.get(
        id_donacion
    )


# ============================================================
# REGISTRAR LLEGADA
# ============================================================

def registrar_llegada(
    id_donacion,
    ciudad,
    cantidad,
    receptor,
    estado
):

    if id_donacion not in donaciones:

        return False, "La donación no existe."

    donacion = donaciones[
        id_donacion
    ]

    datos = donacion["datos"]

    original = datos["cantidad"]

    # La cantidad nunca puede aumentar
    if cantidad > original:

        return (
            False,
            f"No puede superar "
            f"{original:g} {datos['unidad']}."
        )

    estado_cantidad = (
        "COMPLETA"
        if cantidad == original
        else "INCOMPLETA"
    )

    texto = (
        f"DISTRIBUCIÓN | {id_donacion} | "
        f"Lugar: {ciudad} | "
        f"Cantidad: {cantidad:g} {datos['unidad']} | "
        f"{estado_cantidad} | "
        f"Recibe: {receptor} | "
        f"Estado: {estado}"
    )

    donacion["blockchain"].add_block(
        texto
    )

    return True, estado_cantidad


# ============================================================
# VERIFICACIÓN FINAL
# ============================================================

def verificar_donacion(
    id_donacion,
    cantidad,
    persona
):

    if id_donacion not in donaciones:

        return False, "La donación no existe."

    donacion = donaciones[
        id_donacion
    ]

    datos = donacion["datos"]

    original = datos["cantidad"]

    if cantidad > original:

        return (
            False,
            "La cantidad supera la cantidad original."
        )

    resultado = (
        "VERIFICACIÓN COMPLETA"
        if cantidad == original
        else "VERIFICACIÓN INCOMPLETA"
    )

    texto = (
        f"VERIFICACIÓN | {id_donacion} | "
        f"Destino: {datos['destino']} | "
        f"Cantidad: {cantidad:g} {datos['unidad']} | "
        f"{resultado} | "
        f"Verificó: {persona}"
    )

    donacion["blockchain"].add_block(
        texto
    )

    return True, resultado


# ============================================================
# VERIFICAR BLOCKCHAIN
# ============================================================

def verificar_blockchain(id_donacion):

    if id_donacion not in donaciones:

        return False, None, "La donación no existe."

    return donaciones[
        id_donacion
    ]["blockchain"].is_valid()




def alterar_bloque(
    id_donacion,
    numero_bloque,
    nuevo_dato
):

    if id_donacion not in donaciones:
        return False

    donaciones[
        id_donacion
    ]["blockchain"].update_block(
        numero_bloque,
        nuevo_dato
    )

    return True