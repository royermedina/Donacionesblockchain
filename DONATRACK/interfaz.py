import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from sistema import (
    obtener_donaciones,
    obtener_donacion,
    crear_donacion,
    registrar_llegada,
    verificar_donacion,
    verificar_blockchain,
    alterar_bloque
)


# ============================================================
# VENTANA
# ============================================================

ventana = tk.Tk()

ventana.title(
    "DONATRACK - Rastreo de Donaciones"
)

ventana.geometry(
    "1200x720"
)

ventana.configure(
    bg="#eef3f8"
)


# ============================================================
# COLORES
# ============================================================

AZUL = "#1f4e79"
AZUL_OSCURO = "#173b5f"
VERDE = "#198754"
ROJO = "#dc3545"
FONDO = "#eef3f8"
BLANCO = "#ffffff"


# ============================================================
# ENCABEZADO
# ============================================================

header = tk.Frame(
    ventana,
    bg=AZUL,
    height=70
)

header.pack(
    fill="x"
)

tk.Label(
    header,
    text="DONATRACK",
    font=("Arial", 22, "bold"),
    fg="white",
    bg=AZUL
).pack(
    side="left",
    padx=25,
    pady=18
)

tk.Label(
    header,
    text="Sistema de rastreo de donaciones mediante Blockchain",
    font=("Arial", 10),
    fg="white",
    bg=AZUL
).pack(
    side="left"
)


# ============================================================
# ESTRUCTURA PRINCIPAL
# ============================================================

menu = tk.Frame(
    ventana,
    bg=AZUL_OSCURO,
    width=210
)

menu.pack(
    side="left",
    fill="y"
)

menu.pack_propagate(False)


contenido = tk.Frame(
    ventana,
    bg=FONDO
)

contenido.pack(
    side="right",
    fill="both",
    expand=True
)


# ============================================================
# FUNCIONES GENERALES
# ============================================================

def limpiar():

    for widget in contenido.winfo_children():
        widget.destroy()


def titulo(texto, descripcion):

    tk.Label(
        contenido,
        text=texto,
        font=("Arial", 20, "bold"),
        fg="#172b4d",
        bg=FONDO
    ).pack(
        anchor="w",
        padx=30,
        pady=(25, 3)
    )

    tk.Label(
        contenido,
        text=descripcion,
        font=("Arial", 10),
        fg="#667085",
        bg=FONDO
    ).pack(
        anchor="w",
        padx=30,
        pady=(0, 15)
    )


def campo(parent, texto, fila, columna):

    tk.Label(
        parent,
        text=texto,
        font=("Arial", 10, "bold"),
        bg=BLANCO
    ).grid(
        row=fila,
        column=columna,
        sticky="w",
        padx=15,
        pady=(10, 3)
    )

    entrada = tk.Entry(
        parent,
        width=30,
        font=("Arial", 10)
    )

    entrada.grid(
        row=fila + 1,
        column=columna,
        padx=15,
        pady=(0, 10)
    )

    return entrada


# ============================================================
# 1. REGISTRAR DONACIÓN
# ============================================================

def registrar_donacion():

    limpiar()

    titulo(
        "Registrar donación",
        "Registra la información inicial de la donación."
    )

    donaciones = obtener_donaciones()

    tarjeta = tk.Frame(
        contenido,
        bg=BLANCO,
        bd=1,
        relief="solid"
    )

    tarjeta.pack(
        padx=30,
        fill="x"
    )

    siguiente = len(donaciones) + 1

    id_donacion = f"DON-{siguiente:04d}"

    tk.Label(
        tarjeta,
        text=f"ID automático: {id_donacion}",
        font=("Arial", 12, "bold"),
        fg=AZUL,
        bg=BLANCO
    ).grid(
        row=0,
        column=0,
        columnspan=2,
        sticky="w",
        padx=15,
        pady=15
    )

    donante = campo(
        tarjeta,
        "Donante",
        1,
        0
    )

    descripcion = campo(
        tarjeta,
        "Descripción",
        1,
        1
    )

    cantidad = campo(
        tarjeta,
        "Cantidad",
        3,
        0
    )

    unidad = campo(
        tarjeta,
        "Unidad",
        3,
        1
    )

    origen = campo(
        tarjeta,
        "Origen",
        5,
        0
    )

    destino = campo(
        tarjeta,
        "Destino final",
        5,
        1
    )

    def guardar():

        try:

            cant = float(
                cantidad.get()
            )

            if cant <= 0:
                raise ValueError

        except:

            messagebox.showwarning(
                "DONATRACK",
                "La cantidad debe ser un número mayor que cero."
            )

            return

        if not all([
            donante.get().strip(),
            descripcion.get().strip(),
            unidad.get().strip(),
            origen.get().strip(),
            destino.get().strip()
        ]):

            messagebox.showwarning(
                "DONATRACK",
                "Complete todos los campos."
            )

            return

        id_creado = crear_donacion(
            donante.get().strip(),
            descripcion.get().strip(),
            cant,
            unidad.get().strip(),
            origen.get().strip(),
            destino.get().strip()
        )

        messagebox.showinfo(
            "DONATRACK",
            f"{id_creado} registrada correctamente."
        )

        registrar_donacion()

    tk.Button(
        tarjeta,
        text="Registrar donación",
        command=guardar,
        bg=AZUL,
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=20,
        pady=8
    ).grid(
        row=7,
        column=0,
        columnspan=2,
        pady=20
    )


# ============================================================
# 2. RECORRIDO
# ============================================================

def recorrido():

    limpiar()

    titulo(
        "Recorrido / distribución",
        "Registra cada lugar donde llega la donación."
    )

    donaciones = obtener_donaciones()

    tarjeta = tk.Frame(
        contenido,
        bg=BLANCO,
        bd=1,
        relief="solid"
    )

    tarjeta.pack(
        padx=30,
        fill="x"
    )

    tk.Label(
        tarjeta,
        text="Donación",
        font=("Arial", 10, "bold"),
        bg=BLANCO
    ).grid(
        row=0,
        column=0,
        sticky="w",
        padx=15,
        pady=(15, 3)
    )

    combo = ttk.Combobox(
        tarjeta,
        values=list(donaciones.keys()),
        state="readonly",
        width=28
    )

    combo.grid(
        row=1,
        column=0,
        padx=15,
        pady=(0, 10)
    )

    ciudad = campo(
        tarjeta,
        "Ciudad / lugar donde llega",
        0,
        1
    )

    cantidad = campo(
        tarjeta,
        "Cantidad recibida",
        2,
        0
    )

    receptor = campo(
        tarjeta,
        "Persona que recibe",
        2,
        1
    )

    tk.Label(
        tarjeta,
        text="Estado físico",
        font=("Arial", 10, "bold"),
        bg=BLANCO
    ).grid(
        row=4,
        column=0,
        sticky="w",
        padx=15
    )

    estado = ttk.Combobox(
        tarjeta,
        values=[
            "Bueno",
            "Regular",
            "Dañado"
        ],
        state="readonly",
        width=28
    )

    estado.grid(
        row=5,
        column=0,
        padx=15,
        pady=5
    )

    info = tk.Label(
        tarjeta,
        text="",
        bg=BLANCO,
        fg=AZUL
    )

    info.grid(
        row=6,
        column=0,
        columnspan=2,
        sticky="w",
        padx=15,
        pady=10
    )

    def mostrar_info(event=None):

        if combo.get() in donaciones:

            datos = donaciones[
                combo.get()
            ]["datos"]

            info.config(
                text=(
                    f"Original: "
                    f"{datos['cantidad']:g} "
                    f"{datos['unidad']} | "
                    f"Destino: "
                    f"{datos['destino']}"
                )
            )

    combo.bind(
        "<<ComboboxSelected>>",
        mostrar_info
    )

    def guardar():

        if combo.get() not in donaciones:

            messagebox.showwarning(
                "DONATRACK",
                "Seleccione una donación."
            )

            return

        try:

            cant = float(
                cantidad.get()
            )

            if cant < 0:
                raise ValueError

        except:

            messagebox.showwarning(
                "DONATRACK",
                "Ingrese una cantidad válida."
            )

            return

        datos = donaciones[
            combo.get()
        ]["datos"]

        original = datos["cantidad"]

        if cant > original:

            messagebox.showerror(
                "Cantidad inválida",
                f"No puede superar "
                f"{original:g} "
                f"{datos['unidad']}."
            )

            return

        if not ciudad.get().strip():

            messagebox.showwarning(
                "DONATRACK",
                "Ingrese el lugar de llegada."
            )

            return

        if not receptor.get().strip():

            messagebox.showwarning(
                "DONATRACK",
                "Ingrese la persona que recibe."
            )

            return

        if not estado.get():

            messagebox.showwarning(
                "DONATRACK",
                "Seleccione el estado físico."
            )

            return

        correcto, resultado = registrar_llegada(
            combo.get(),
            ciudad.get().strip(),
            cant,
            receptor.get().strip(),
            estado.get()
        )

        if not correcto:

            messagebox.showerror(
                "DONATRACK",
                resultado
            )

            return

        messagebox.showinfo(
            "DONATRACK",
            f"Llegada registrada: {resultado}"
        )

        ciudad.delete(
            0,
            tk.END
        )

        cantidad.delete(
            0,
            tk.END
        )

        receptor.delete(
            0,
            tk.END
        )

        estado.set("")

    tk.Button(
        tarjeta,
        text="Registrar llegada",
        command=guardar,
        bg=AZUL,
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=20,
        pady=8
    ).grid(
        row=7,
        column=0,
        columnspan=2,
        pady=20
    )


# ============================================================
# 3. VERIFICACIÓN FINAL
# ============================================================

def verificacion():

    limpiar()

    titulo(
        "Verificación final",
        "Comprueba la llegada de la donación a su destino."
    )

    donaciones = obtener_donaciones()

    tarjeta = tk.Frame(
        contenido,
        bg=BLANCO,
        bd=1,
        relief="solid"
    )

    tarjeta.pack(
        padx=30,
        fill="x"
    )

    tk.Label(
        tarjeta,
        text="Donación",
        font=("Arial", 10, "bold"),
        bg=BLANCO
    ).grid(
        row=0,
        column=0,
        sticky="w",
        padx=15,
        pady=(15, 3)
    )

    combo = ttk.Combobox(
        tarjeta,
        values=list(donaciones.keys()),
        state="readonly",
        width=28
    )

    combo.grid(
        row=1,
        column=0,
        padx=15
    )

    tk.Label(
        tarjeta,
        text="Destino final",
        font=("Arial", 10, "bold"),
        bg=BLANCO
    ).grid(
        row=0,
        column=1,
        sticky="w",
        padx=15,
        pady=(15, 3)
    )

    destino = tk.Label(
        tarjeta,
        text="Seleccione una donación",
        font=("Arial", 11, "bold"),
        fg=AZUL,
        bg="#eaf2f8",
        width=30,
        anchor="w"
    )

    destino.grid(
        row=1,
        column=1,
        padx=15
    )

    cantidad = campo(
        tarjeta,
        "Cantidad recibida en destino",
        2,
        0
    )

    persona = campo(
        tarjeta,
        "Persona que verifica",
        2,
        1
    )

    def mostrar(event=None):

        if combo.get() in donaciones:

            destino.config(
                text=donaciones[
                    combo.get()
                ]["datos"]["destino"]
            )

    combo.bind(
        "<<ComboboxSelected>>",
        mostrar
    )

    def verificar():

        if combo.get() not in donaciones:

            messagebox.showwarning(
                "DONATRACK",
                "Seleccione una donación."
            )

            return

        try:

            cant = float(
                cantidad.get()
            )

        except:

            messagebox.showwarning(
                "DONATRACK",
                "Cantidad inválida."
            )

            return

        datos = donaciones[
            combo.get()
        ]["datos"]

        if cant > datos["cantidad"]:

            messagebox.showerror(
                "DONATRACK",
                "La cantidad supera la cantidad original."
            )

            return

        if not persona.get().strip():

            messagebox.showwarning(
                "DONATRACK",
                "Ingrese la persona que verifica."
            )

            return

        correcto, resultado = verificar_donacion(
            combo.get(),
            cant,
            persona.get().strip()
        )

        if not correcto:

            messagebox.showerror(
                "DONATRACK",
                resultado
            )

            return

        messagebox.showinfo(
            "DONATRACK",
            f"{datos['destino']}\n\n"
            f"{resultado}"
        )

    tk.Button(
        tarjeta,
        text="Realizar verificación",
        command=verificar,
        bg=VERDE,
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=20,
        pady=8
    ).grid(
        row=5,
        column=0,
        columnspan=2,
        pady=20
    )

def cadena():

    limpiar()

    titulo(
        "Revisión de cadena Blockchain",
        "Consulta los bloques y comprueba si fueron alterados."
    )

    donaciones = obtener_donaciones()

    arriba = tk.Frame(
        contenido,
        bg=FONDO
    )

    arriba.pack(
        fill="x",
        padx=30
    )

    combo = ttk.Combobox(
        arriba,
        values=list(donaciones.keys()),
        state="readonly",
        width=25
    )

    combo.pack(
        side="left"
    )

    estado = tk.Label(
        arriba,
        text="",
        font=("Arial", 11, "bold"),
        bg=FONDO
    )

    estado.pack(
        side="left",
        padx=15
    )


    marco = tk.Frame(
        contenido,
        bg=FONDO
    )

    marco.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=10
    )

    canvas = tk.Canvas(
        marco,
        bg=FONDO,
        highlightthickness=0
    )

    scroll = ttk.Scrollbar(
        marco,
        orient="vertical",
        command=canvas.yview
    )

    lista = tk.Frame(
        canvas,
        bg=FONDO
    )

    canvas.create_window(
        (0, 0),
        window=lista,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scroll.set
    )

    lista.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scroll.pack(
        side="right",
        fill="y"
    )

    def mostrar():

        for widget in lista.winfo_children():
            widget.destroy()

        if combo.get() not in donaciones:
            return

        bc = donaciones[
            combo.get()
        ]["blockchain"]

        valido, roto, motivo = verificar_blockchain(
            combo.get()
        )

        if valido:

            estado.config(
                text="✓ CADENA ÍNTEGRA",
                fg=VERDE
            )

        else:

            estado.config(
                text=f"✗ ALTERADA EN BLOQUE #{roto}",
                fg=ROJO
            )

        for b in bc.chain:

            roto_bloque = (
                not valido and b.index == roto
            )

            color = (
                "#fdecec"
                if roto_bloque
                else BLANCO
            )

            tarjeta = tk.Frame(
                lista,
                bg=color,
                bd=2,
                relief="solid"
            )

            tarjeta.pack(
                fill="x",
                pady=8
            )

            encabezado = (
                f"BLOQUE #{b.index}"
                + (
                    " - GÉNESIS"
                    if b.index == 0
                    else ""
                )
                + (
                    "   ⚠ ALTERADO"
                    if roto_bloque
                    else ""
                )
            )

            tk.Label(
                tarjeta,
                text=encabezado,
                font=("Arial", 12, "bold"),
                fg=ROJO if roto_bloque else AZUL,
                bg=color
            ).pack(
                anchor="w",
                padx=15,
                pady=8
            )

            informacion = (
                f"Fecha:\n{b.date}\n\n"
                f"Datos:\n{b.data}\n\n"
                f"Hash anterior:\n"
                f"{b.previous_hash or 'SIN HASH ANTERIOR'}\n\n"
                f"Nonce: {b.nonce}\n\n"
                f"Hash:\n{b.hash}"
            )

            tk.Label(
                tarjeta,
                text=informacion,
                font=("Courier New", 9),
                bg=color,
                fg="#172b4d",
                justify="left",
                wraplength=850,
                anchor="w"
            ).pack(
                fill="x",
                padx=15,
                pady=(0, 12)
            )

    combo.bind(
        "<<ComboboxSelected>>",
        lambda e: mostrar()
    )


    def alterar():

        if combo.get() not in donaciones:

            messagebox.showwarning(
                "DONATRACK",
                "Seleccione una donación."
            )

            return

        bc = donaciones[
            combo.get()
        ]["blockchain"]

        bloques = [
            str(b.index)
            for b in bc.chain
            if b.index != 0
        ]

        if not bloques:

            messagebox.showinfo(
                "DONATRACK",
                "No existen bloques para alterar."
            )

            return

        ventana_alterar = tk.Toplevel(
            ventana
        )

        ventana_alterar.title(
            "Prueba de alteración"
        )

        ventana_alterar.geometry(
            "400x220"
        )

        ventana_alterar.configure(
            bg=FONDO
        )

        tk.Label(
            ventana_alterar,
            text="Prueba de alteración",
            font=("Arial", 15, "bold"),
            bg=FONDO,
            fg=AZUL
        ).pack(
            pady=15
        )

        tk.Label(
            ventana_alterar,
            text="Seleccione el bloque:",
            bg=FONDO
        ).pack()

        bloque = ttk.Combobox(
            ventana_alterar,
            values=bloques,
            state="readonly"
        )

        bloque.pack(
            pady=5
        )

        nuevo = tk.Entry(
            ventana_alterar,
            width=40
        )

        nuevo.insert(
            0,
            "INFORMACIÓN ALTERADA"
        )

        nuevo.pack(
            pady=8
        )

        def aplicar():

            if not bloque.get():
                return

            alterar_bloque(
                combo.get(),
                int(bloque.get()),
                nuevo.get()
            )

            ventana_alterar.destroy()

            mostrar()

            messagebox.showwarning(
                "PRUEBA",
                "Bloque alterado sin recalcular su hash.\n\n"
                "Ahora verifica la integridad de la cadena."
            )

        tk.Button(
            ventana_alterar,
            text="Alterar bloque",
            command=aplicar,
            bg=ROJO,
            fg="white",
            relief="flat",
            padx=15,
            pady=7
        ).pack()

    

    def verificar():

        if combo.get() not in donaciones:
            return

        valido, roto, motivo = verificar_blockchain(
            combo.get()
        )

        mostrar()

        if valido:

            messagebox.showinfo(
                "Blockchain",
                "✓ CADENA ÍNTEGRA\n\n"
                "No se detectaron alteraciones."
            )

        else:

            messagebox.showerror(
                "Blockchain",
                f"✗ CADENA ALTERADA\n\n"
                f"Bloque: #{roto}\n"
                f"Motivo: {motivo}"
            )

    botones = tk.Frame(
        contenido,
        bg=FONDO
    )

    botones.pack(
        padx=30,
        pady=10
    )

    tk.Button(
        botones,
        text="Alterar bloque (prueba)",
        command=alterar,
        bg=ROJO,
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=15,
        pady=8
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        botones,
        text="Verificar integridad",
        command=verificar,
        bg=VERDE,
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=15,
        pady=8
    ).pack(
        side="left",
        padx=5
    )


def boton(texto, funcion):

    tk.Button(
        menu,
        text=texto,
        command=funcion,
        bg=AZUL_OSCURO,
        fg="white",
        activebackground="#2f75b5",
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        anchor="w",
        padx=20,
        pady=12
    ).pack(
        fill="x"
    )


tk.Label(
    menu,
    text="MÓDULOS",
    font=("Arial", 10, "bold"),
    fg="#b8cbe0",
    bg=AZUL_OSCURO
).pack(
    pady=(25, 15)
)

boton(
    "Registrar donación",
    registrar_donacion
)

boton(
    "Recorrido / distribución",
    recorrido
)

boton(
    "Verificación final",
    verificacion
)

boton(
    "Revisión de cadena",
    cadena
)

tk.Label(
    menu,
    text="DONATRACK\nBlockchain",
    font=("Arial", 9),
    fg="#9fb6cc",
    bg=AZUL_OSCURO
).pack(
    side="bottom",
    pady=25
)


# ============================================================
# INICIO
# ============================================================

registrar_donacion()

ventana.mainloop()