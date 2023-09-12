import os
from os import system
import time
import CONEXION_DB as conn
db = conn.DB()
from tabulate import tabulate
def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def crear_cliente():
    limpiar_consola()
    cliente_nuevo = {}

    while True:
        cedula = input("Digite el numero de cedula del cliente: ")
        if cedula.isdigit():
            cliente_nuevo["cedula"] = int(cedula)
            break
        else:
            print("La cédula debe contener solo números. Inténtelo de nuevo.")

    while True:
        nombre = input("Digite el nombre: ")
        if nombre.isalpha():
            cliente_nuevo["nombre"] = nombre
            break
        else:
            print("El nombre no debe contener números. Inténtelo de nuevo.")

    while True:
        apellido1 = input("Digite el primer apellido: ")
        if apellido1.isalpha():
            cliente_nuevo["apellido1"] = apellido1
            break
        else:
            print("El apellido no debe contener números. Inténtelo de nuevo.")

    while True:
        apellido2 = input("Digite el segundo apellido: ")
        if apellido2.isalpha():
            cliente_nuevo["apellido2"] = apellido2
            break
        else:
            print("El apellido no debe contener números. Inténtelo de nuevo.")

    consulta = "INSERT INTO CLIENTE (cedula, nombre, apellido1, apellido2) VALUES (?, ?, ?, ?)"
    parametros = (cliente_nuevo["cedula"], cliente_nuevo["nombre"], cliente_nuevo["apellido1"], cliente_nuevo["apellido2"])

    db.ejecutar_consulta(consulta, parametros)
    print("Cliente registrado exitosamente.")
    input("Presione ENTER para continuar...")

def consultar_cliente():
    limpiar_consola()
    sql = "SELECT cedula, nombre, apellido1, apellido2 FROM CLIENTE"
    result = db.ejecutar_consulta(sql)
    
    data = []
    for row in result:
        data.append([row[0], row[1], row[2], row[3]])
    
    print("Listado de Clientes:")
    headers = ["Cedula", "Nombre", "Apellido 1", "Apellido 2"]
    print(tabulate(data, headers=headers, tablefmt="grid"))
    
    input("\nPresione ENTER para continuar...")

def actualizar_cliente():
    consultar_cliente()
    id_cliente = int(input("Seleccione el ID del cliente a actualizar: "))
    
    if id_cliente != 0:
        nuevo_nombre = str(input("Ingrese el nuevo nombre: "))
        nuevo_apellido1 = str(input("Ingrese el nuevo primer apellido: "))
        nuevo_apellido2 = str(input("Ingrese el nuevo segundo apellido: "))
        
        if len(nuevo_nombre) > 0 and len(nuevo_apellido1) > 0 and len(nuevo_apellido2) > 0:
            sql = "UPDATE CLIENTE SET nombre=?, apellido1=?, apellido2=? WHERE cedula=?"
            parametros = (nuevo_nombre, nuevo_apellido1, nuevo_apellido2, id_cliente)
            db.ejecutar_consulta(sql, parametros)
            print("************************************************")
            print("Cliente actualizado con éxito.")
            input("\nPresione ENTER para continuar...")
        else:
            print("Por favor, ingrese valores válidos.")
    else:
        print("Seleccione un ID válido.")
    
def menu_actualizar_cliente():
    consultar_cliente()
    id_cliente = int(input("Ingrese la cedula del cliente que desea actualizar: "))
    actualizar_cliente(id_cliente)

def eliminar_cliente():
    consultar_cliente()
    id_cliente = int(input("Ingrese la cédula del cliente que desea eliminar: "))
    
    if id_cliente != 0:
        sql = "DELETE FROM CLIENTE WHERE cedula=?"
        parametros = (id_cliente,)
        db.ejecutar_consulta(sql, parametros)
        print("************************************************")
        print("Cliente eliminado exitosamente.")
        input("\nPresione ENTER para continuar...")

    else:
        print("Seleccione una cédula válida.")

def buscar_cliente():
    nombre = str(input("Digite el nombre a consultar: "))
    
    if len(nombre) > 0:
        nombre_buscado = nombre.capitalize() 
        sql = "SELECT * FROM CLIENTE WHERE nombre LIKE ? OR apellido1 LIKE ? OR apellido2 LIKE ?"
        parametros = ('%{}%'.format(nombre_buscado), '%' + nombre_buscado + '%', '%' + nombre_buscado + '%')
        result = db.ejecutar_consulta(sql, parametros)
        
        if result:
            print("Resultados de la búsqueda:")
            for data in result:
                print("""
                Cedula:        {}
                Nombre:        {}
                Apellido 1:    {}
                Apellido 2:    {}
                """.format(data[1], data[2], data[3], data[4]))
                input("\nPresione ENTER para continuar...")
        else:
            print("No se encontraron resultados.")
            input("\nPresione ENTER para continuar...")
    else:
        print("Por favor, ingrese un nombre válido.")
        input("\nPresione ENTER para continuar...")

def menu_clientes():
    while True:
        limpiar_consola() 
        print("************************ MENU DE CLIENTES ************************")
        print("\t[1] Registrar Cliente Nuevo.")
        print("\t[2] Consultar Clientes")
        print("\t[3] Actualizar un registro.")
        print("\t[4] Eliminar un registro.")
        print("\t[5] Buscar un registro.")
        print("\t[6] Volver al menu anterior.")
        print("*****************************************************************")
        try:
            opcion = int(input("Seleccione una opción: "))
            if opcion == 1:
                crear_cliente()
            elif opcion == 2:
                consultar_cliente()
            elif opcion == 3:
                actualizar_cliente()
            elif opcion == 4:
                eliminar_cliente()
            elif opcion == 5:
                buscar_cliente()
            elif opcion == 6:
                break
            else:
                print("Opción no válida. Por favor, elija una opción del menú.")
        except ValueError:
            print("Error: Por favor, ingrese un número válido.")

def crear_cuentas():
    limpiar_consola()
    
    try:
        cantidad = int(input("Ingrese la cantidad de cuentas a crear: "))
        
        if cantidad <= 0:
            print("La cantidad debe ser un número positivo mayor que cero.")
            return
        
        cuentas_creadas = []

        # Obtener el último CUENTA_ID existente
        consulta = "SELECT MAX(CUENTA_ID) FROM CUENTA"
        resultado = db.ejecutar_consulta(consulta)
        ultimo_cuenta_id = resultado.fetchone()[0]

        if ultimo_cuenta_id is None:
            nuevo_cuenta_id = 1
        else:
            nuevo_cuenta_id = ultimo_cuenta_id + 1

        for _ in range(cantidad):
            nuevo_numero_cuenta = f"CTA{str(nuevo_cuenta_id).zfill(4)}"
            
            # Crear la cuenta
            consulta = "INSERT INTO CUENTA (NUM_CUENTA, SALDO, ESTADO, USUARIO_CEDULA) VALUES (?, ?, ?, ?)"
            parametros = (nuevo_numero_cuenta, 0, "INACTIVA", "")
            db.ejecutar_consulta(consulta, parametros)
            
            cuentas_creadas.append(nuevo_numero_cuenta)
            nuevo_cuenta_id += 1

        print(f"{cantidad} cuentas fueron creadas satisfactoriamente:")
        for cuenta in cuentas_creadas:
            print("Número de cuenta:", cuenta)
        
        input("\nPresione ENTER para continuar...")
        
    except ValueError:
        print("Por favor, ingrese un número válido.")

def asignar_cuenta_a_usuario():
    limpiar_consola()
    
    try:
        consultar_cliente()  # Llamar a la función para consultar clientes
        
        cedula = input("Ingrese la cédula del cliente: ")
        
        consulta_cliente = "SELECT * FROM CLIENTE WHERE cedula = ?"
        parametros_cliente = (cedula,)
        resultado_cliente = db.ejecutar_consulta(consulta_cliente, parametros_cliente)
        cliente = resultado_cliente.fetchone()
        
        if cliente is None:
            print("No se encontró ningún cliente con esa cédula.")
            return
        
        consulta_cuenta_disponible = "SELECT * FROM CUENTA WHERE USUARIO_CEDULA = '' LIMIT 1"
        resultado_cuenta_disponible = db.ejecutar_consulta(consulta_cuenta_disponible)
        cuenta_disponible = resultado_cuenta_disponible.fetchone()
        
        if cuenta_disponible is None:
            print("No hay cuentas disponibles. Por favor, crear más cuentas.")
            return
        
        num_cuenta = cuenta_disponible[1]
        
        consulta_asignar_cuenta = "UPDATE CUENTA SET USUARIO_CEDULA = ?, ESTADO = 'ACTIVA' WHERE NUM_CUENTA = ?"
        parametros_asignar_cuenta = (cedula, num_cuenta)
        db.ejecutar_consulta(consulta_asignar_cuenta, parametros_asignar_cuenta)
        
        print(f"La cuenta {num_cuenta} fue asignada correctamente al usuario con cédula {cedula}.")
        input("\nPresione ENTER para continuar...")
        
    except Exception as e:
        print("Ocurrió un error:", e)

def consultar_cuentas():
    limpiar_consola()
    sql = "SELECT CUENTA_ID, NUM_CUENTA, SALDO, ESTADO, USUARIO_CEDULA FROM CUENTA"
    result = db.ejecutar_consulta(sql)
    
    data = []
    for row in result:
        data.append([row[0], row[1], row[2], row[3], row[4]])
    
    print("Listado de Cuentas:")
    headers = ["ID", "Número de Cuenta", "Saldo", "Estado", "Cédula del Usuario"]
    print(tabulate(data, headers=headers, tablefmt="grid"))
    
    input("\nPresione ENTER para continuar...")

def obtener_transacciones_por_cuenta(numero_cuenta):
    sql = "SELECT * FROM TRANSACCION WHERE NUM_CUENTA = ?"
    parametros = (numero_cuenta,)
    result = db.ejecutar_consulta(sql, parametros)
    
    transacciones_data = []
    for data in result:
        transacciones_data.append([data[0], data[1], data[2], data[3]])
    
    return transacciones_data

def buscar_cuenta_por_cedula(cedula):
    sql = "SELECT * FROM CUENTA WHERE USUARIO_CEDULA = ?"
    parametros = (cedula,)
    result = db.ejecutar_consulta(sql, parametros)
    
    if result:
        cuentas_data = []
        for data in result:
            cuentas_data.append([data[0], data[1], data[2], data[3]])
        
        headers = ["ID de Cuenta", "Número de Cuenta", "Saldo", "Estado"]
        print("Cuentas del cliente:")
        print(tabulate(cuentas_data, headers=headers, tablefmt="grid"))
        
        for cuenta in cuentas_data:
            num_cuenta = cuenta[1]
            transacciones_data = obtener_transacciones_por_cuenta(num_cuenta)
            
            if transacciones_data:
                transacciones_headers = ["ID de Transacción", "Tipo", "Monto", "Número de Cuenta"]
                print(f"\nTransacciones de la cuenta {num_cuenta}:")
                print(tabulate(transacciones_data, headers=transacciones_headers, tablefmt="grid"))
            else:
                print(f"\nNo hay registros para la cuenta {num_cuenta}.")
    else:
        print("No se encontraron cuentas para el cliente.")
    input("\nPresione ENTER para continuar...")

def buscar_cuenta_por_numero(numero_cuenta):
    sql = "SELECT * FROM CUENTA WHERE NUM_CUENTA = ?"
    parametros = (numero_cuenta,)
    result = db.ejecutar_consulta(sql, parametros)
    
    row = result.fetchone()  # Obtener la primera fila de resultados como tupla
    
    if row:
        cuenta_data = [[row[0], row[1], row[2], row[3], row[4]]]
        headers = ["ID de Cuenta", "Número de Cuenta", "Saldo", "Estado", "Usuario"]
        print("Información de la cuenta:")
        print(tabulate(cuenta_data, headers=headers, tablefmt="grid"))
        
        transacciones_data = obtener_transacciones_por_cuenta(numero_cuenta)
        if transacciones_data:
            transacciones_headers = ["ID de Transacción", "Tipo", "Monto", "Número de Cuenta"]
            print("\nTransacciones de la cuenta:")
            print(tabulate(transacciones_data, headers=transacciones_headers, tablefmt="grid"))
        else:
            print("\nNo hay registros para esta cuenta.")
    else:
        print("No se encontró la cuenta.")
    input("\nPresione ENTER para continuar...")

def actualizar_cuenta():
    print("Seleccione una opción:")
    print("1. Buscar por cédula del cliente")
    print("2. Buscar por número de cuenta")
    
    opcion = int(input("Ingrese el número de opción: "))
    
    if opcion == 1:
        cedula = str(input("Ingrese la cédula del cliente: "))
        buscar_cuenta_por_cedula(cedula)
    elif opcion == 2:
        numero_cuenta = str(input("Ingrese el número de cuenta: "))
        buscar_cuenta_por_numero(numero_cuenta)
    else:
        print("Opción no válida.")
        return
    
    numero_cuenta = input("Ingrese el número de cuenta a actualizar: ")
    nuevo_estado = input("Ingrese el nuevo estado (INACTIVA o ACTIVA): ")
    nuevo_estado = nuevo_estado.upper()

    if nuevo_estado == "":
        print("No se actualizará el estado.")
        nuevo_cedula = input("Ingrese el nuevo número de cédula del usuario (presione ENTER para mantener el valor actual): ")
        if nuevo_cedula == "":
            print("No se actualizará el estado ni el número de cédula.")
            input("\nPresione ENTER para continuar...")
            return
    else:
        nuevo_cedula = input("Ingrese el nuevo número de cédula del usuario (presione ENTER para mantener el valor actual): ")
    
    sql = "SELECT * FROM CUENTA WHERE NUM_CUENTA = ?"
    parametros = (numero_cuenta,)
    result = db.ejecutar_consulta(sql, parametros)
    
    if result:
        cuenta_data = result[0]
        cedula_actual = cuenta_data[4]
        
        if nuevo_cedula == "":
            nuevo_cedula = cedula_actual
        
        sql_actualizacion = "UPDATE CUENTA SET ESTADO=?, USUARIO_CEDULA=? WHERE NUM_CUENTA=?"
        parametros_actualizacion = (nuevo_estado, nuevo_cedula, numero_cuenta)
        db.ejecutar_consulta(sql_actualizacion, parametros_actualizacion)
        
        print("************************************************")
        print("Cuenta actualizada con éxito.")
    else:
        print("No se encontró la cuenta.")
    input("\nPresione ENTER para continuar...")

def obtener_info_cuenta(numero_cuenta):
    sql = "SELECT * FROM CUENTA WHERE NUM_CUENTA = ?"
    parametros = (numero_cuenta,)
    result = db.ejecutar_consulta(sql, parametros)
    return result.fetchone()

def eliminar_cuenta():
    consultar_cuentas()
    numero_cuenta = input("Ingrese el número de cuenta que desea eliminar: ")
    cuenta_info = obtener_info_cuenta(numero_cuenta)
    
    if cuenta_info is None:
        print("La cuenta no existe.")
        input("\nPresione ENTER para continuar...")
        return
    
    saldo = cuenta_info[2]
    
    if saldo == 0:
        sql = "DELETE FROM CUENTA WHERE NUM_CUENTA=?"
        parametros = (numero_cuenta,)
        db.ejecutar_consulta(sql, parametros)
        print("Cuenta eliminada exitosamente.")
        input("\nPresione ENTER para continuar...")
    else:
        print("La cuenta no se puede eliminar ya que tiene saldo.")
        input("\nPresione ENTER para continuar...")

def menu_mantenimiento_cuentas():
    while True: 
        limpiar_consola()
        print("************************ MANTENIMIENTO DE CUENTAS ************************")
        print("\t[1] Asignar cuenta a un cliente.")
        print("\t[2] Consultar las cuentas")
        print("\t[3] Actualizar un registro.")
        print("\t[4] Eliminar un registro.")
        print("\t[5] Buscar una cuenta.")
        print("\t[6] Crear cuentas (inventario de cuentas).")
        print("\t[7] Volver al menu anterior.")
        print("*****************************************************************")
        try:
            opcion = int(input("Seleccione una opción: "))
            if opcion == 1:
                asignar_cuenta_a_usuario()
            elif opcion == 2:
                consultar_cuentas()
            elif opcion == 3:
                actualizar_cuenta()
            elif opcion == 4:
                eliminar_cuenta()
            elif opcion == 5:
                print("\nSeleccione una opción:")
                print("1. Buscar por cédula del cliente")
                print("2. Buscar por número de cuenta")
    
                opcion = int(input("Ingrese el número de opción: "))
    
                if opcion == 1:
                    cedula = str(input("Ingrese la cédula del cliente: "))
                    buscar_cuenta_por_cedula(cedula)
                elif opcion == 2:
                    numero_cuenta = str(input("Ingrese el número de cuenta: "))
                    buscar_cuenta_por_numero(numero_cuenta)
                else:
                    print("Opción no válida.")
                    return
            elif opcion == 6:
                crear_cuentas()
            elif opcion == 7:
                break
            else:
                print("Opción no válida. Por favor, elija una opción del menú.")
        except ValueError:
            print("Error: Por favor, ingrese un número válido.")

def registro_deposito():
    limpiar_consola()
    print("\nSeleccione una opción:")
    print("1. Buscar por cédula del cliente")
    print("2. Buscar por número de cuenta")
    
    opcion = int(input("Ingrese el número de opción: "))
    
    if opcion == 1:
        cedula = str(input("Ingrese la cédula del cliente: "))
        buscar_cuenta_por_cedula(cedula)
    elif opcion == 2:
        numero_cuenta = str(input("Ingrese el número de cuenta: "))
        buscar_cuenta_por_numero(numero_cuenta)
    else:
        print("Opción no válida.")
        return
    
    numero_cuenta = input("Ingrese el número de cuenta seleccionada: ")
    sql_estado = "SELECT ESTADO FROM CUENTA WHERE NUM_CUENTA = ?"
    estado_result = db.ejecutar_consulta(sql_estado, (numero_cuenta,))
    
    estado_row = estado_result.fetchone()
    
    if estado_row:
        estado_cuenta = estado_row[0]
        
        if estado_cuenta != "ACTIVA":
            print("La cuenta seleccionada no está activa.")
            return
        
        monto = float(input("Ingrese el monto a depositar: "))
        if monto <= 0:
            print("El monto debe ser mayor que cero.")
            return
        
        sql_actualizar_saldo = "UPDATE CUENTA SET SALDO = SALDO + ? WHERE NUM_CUENTA = ?"
        parametros_actualizacion = (monto, numero_cuenta)
        db.ejecutar_consulta(sql_actualizar_saldo, parametros_actualizacion)
            
        sql_registro_transaccion = "INSERT INTO TRANSACCION (TIPO, MONTO_TRANS, NUM_CUENTA) VALUES (?, ?, ?)"
        parametros_transaccion = ("DEPOSITO", monto, numero_cuenta)
        db.ejecutar_consulta(sql_registro_transaccion, parametros_transaccion)
        
        print("Depósito registrado con éxito.")
    else:
        print("No se encontró la cuenta.")
    input("\nPresione ENTER para continuar...")

def registro_retiro():
    limpiar_consola()
    print("\nSeleccione una opción:")
    print("1. Buscar por cédula del cliente")
    print("2. Buscar por número de cuenta")
    
    opcion = int(input("Ingrese el número de opción: "))
    
    if opcion == 1:
        cedula = str(input("Ingrese la cédula del cliente: "))
        buscar_cuenta_por_cedula(cedula)
    elif opcion == 2:
        numero_cuenta = str(input("Ingrese el número de cuenta: "))
        buscar_cuenta_por_numero(numero_cuenta)
    else:
        print("Opción no válida.")
        return
    
    numero_cuenta = input("Ingrese el número de cuenta seleccionada: ")
    sql_estado = "SELECT ESTADO FROM CUENTA WHERE NUM_CUENTA = ?"
    estado_result = db.ejecutar_consulta(sql_estado, (numero_cuenta,))
    
    estado_row = estado_result.fetchone()
    
    if estado_row:
        estado_cuenta = estado_row[0]
        
        if estado_cuenta != "ACTIVA":
            print("La cuenta seleccionada no está activa.")
            return
        
        sql_saldo_actual = "SELECT SALDO FROM CUENTA WHERE NUM_CUENTA = ?"
        saldo_result = db.ejecutar_consulta(sql_saldo_actual, (numero_cuenta,))
        
        saldo_row = saldo_result.fetchone()
        
        if saldo_row:
            saldo_actual = saldo_row[0]
            if saldo_actual <= 0:
                print("La cuenta no tiene fondos disponibles para un retiro.")
                return
                
            monto = float(input("Ingrese el monto a retirar: "))
            if monto <= 0 or monto > saldo_actual:
                print("Monto inválido para retiro.")
                return
                
            sql_actualizar_saldo = "UPDATE CUENTA SET SALDO = SALDO - ? WHERE NUM_CUENTA = ?"
            parametros_actualizacion = (monto, numero_cuenta)
            db.ejecutar_consulta(sql_actualizar_saldo, parametros_actualizacion)
            
            sql_registro_transaccion = "INSERT INTO TRANSACCION (TIPO, MONTO_TRANS, NUM_CUENTA) VALUES (?, ?, ?)"
            parametros_transaccion = ("RETIRO", monto, numero_cuenta)
            db.ejecutar_consulta(sql_registro_transaccion, parametros_transaccion)
        
            print("Retiro registrado con éxito.")
    else:
        print("No se encontró la cuenta.")
    input("\nPresione ENTER para continuar...")

def menu_registro_transacciones():
    limpiar_consola()
    while True: 
        print("************************ REGISTRO DE TRANSACCIONES ************************")
        print("\t[1] Registrar un deposito.")
        print("\t[2] Registrar un retiro.")
        print("\t[3] Consultar las cuentas")
        print("\t[4] Volver al menu anterior.")
        print("*****************************************************************")
        try:
            opcion = int(input("Seleccione una opción: "))
            if opcion == 1:
                registro_deposito()
                pass
            elif opcion == 2:
                registro_retiro()
                pass
            elif opcion == 3:
                consultar_cuentas()
                pass
            elif opcion == 4:
                break  
            else:
                print("Opción no válida. Por favor, elija una opción del menú.")
        except ValueError:
            print("Error: Por favor, ingrese un número válido.")

while True: 
    limpiar_consola()
    print("************************ MENU DE SISTEMA ************************")
    print("\t[1] Menu de Clientes.")
    print("\t[2] Mantenimiento de Cuentas.")
    print("\t[3] Registro de transacciones.")
    print("\t[4] Salir del sistema.")
    print("*****************************************************************")
    try:
        opcion = int(input("Seleccione una opción: "))
        if opcion == 1:
            menu_clientes()
        elif opcion == 2:
            menu_mantenimiento_cuentas()
        elif opcion == 3:
            menu_registro_transacciones()
        elif opcion == 4:
            break
        else:
            print("Opción no válida. Por favor, elija una opción del menú.")
    except ValueError:
        print("Error: Por favor, ingrese un número válido.")


    