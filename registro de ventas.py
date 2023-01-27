import json
import math

def recibir_caracteres(mensaje, maximo=math.inf):
    while True:
        valor = str(input(mensaje))
        if len(valor) > maximo:
            print('Error: No puede tener más de 20 caracteres')
        else:
            break

    return valor

def recibir_entero(mensaje, minimo=1000000, maximo=math.inf, error='Error'):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo < valor <= maximo:
                break
            else:
                print(error)
        except ValueError:
            print('Error: solo números enteros')

    return valor

def recibir_flotante(mensaje, minimo=0.0, error='Error'):
    while True:
        try:
            valor = float(input(mensaje))
            if minimo <= valor:
                break
            else:
                print(error)
        except ValueError:
            print('Error: solo números')

    return valor

def ordenar_lista_dicc(lista_ordenar, clave, tipo='desc'):
    desordenado = True
    while desordenado:
        desordenado = False
        for posicion in range(len(lista_ordenar)-1):
            if lista_ordenar[posicion][clave] < lista_ordenar[posicion+1][clave] and tipo == 'desc':
                desordenado = True
                lista_ordenar[posicion], lista_ordenar[posicion+1] = lista_ordenar[posicion+1], lista_ordenar[posicion]
            elif lista_ordenar[posicion][clave] > lista_ordenar[posicion+1][clave] and tipo == 'asc':
                desordenado = True
                lista_ordenar[posicion], lista_ordenar[posicion+1] = lista_ordenar[posicion+1], lista_ordenar[posicion]
    return lista_ordenar

def encontrar_mayor(lista_mayor):
    mayor = 0, lista_mayor[0]
    for i in range(1, len(lista_mayor)):
        if mayor[1] < lista_mayor[i]:
            mayor = i, lista_mayor[i]

    return mayor[0]

listaNombres = []
listaDocumentos = []
listaProductos = []
listaCantidades = []
listaDescuentos = []
listaTotal = []
listaSubTotal = []
listaClientes = []

ventas = {}

express = [10000, 20000, 40000]
normal = [5000, 10000, 20000]

while True:
    print('REGISTRO DE VENTA')

    while True:
        print("\n1. Agregar un nuevo producto\n"
              "2. Registrar una nueva compra\n"
              "3. Ver resumen de compras\n"
              "4. Salir\n")

        opcion = recibir_entero("Elija una opción: ", 0, 4)

        if opcion == 4:
            exit()

        elif opcion == 1:
            with open("productos.txt", encoding="utf-8") as archivo:
                listaProductosVender = json.load(archivo)

            nombreAgregar = recibir_caracteres("Escriba el nombre del nuevo producto: ")
            precioAgregar = recibir_entero("Escriba el precio del nuevo producto: $", 0)
            diccionarioAgregar = {'nombre': nombreAgregar, 'precio': precioAgregar}

            listaProductosVender.append(diccionarioAgregar)
            listaProductosVender_json = json.dumps(listaProductosVender, indent=2)
            with open("productos.txt", "w", encoding="utf-8") as nuevo:
                nuevo.write(listaProductosVender_json)
            print("Producto agregado")

        elif opcion == 2:

            with open("compras.txt", encoding="utf-8") as archivo:
                listaClientes = json.load(archivo)

            while True:
                ventas = {}
                diccionarioProductos = {}
                listaProductos = []
                descuento = 0.0
                costoEnvio = 0.0

                with open("productos.txt", encoding="utf-8") as archivo:
                    listaProductosVender = json.load(archivo)

                nombre = recibir_caracteres('\nEscriba el nombre del cliente: ', 20)
                ventas['nombre'] = nombre

                documento = recibir_entero('Escriba el documento: ')
                ventas['documento'] = documento

                subTotal = 0.0
                total = 0.0
                while True:

                    subSubTotal = 0.0

                    print(' ')
                    for i in listaProductosVender:
                        print(f"{listaProductosVender.index(i) + 1}. {i.get('nombre')} - ${i.get('precio')}")

                    diccionarioProductos = {}

                    producto = recibir_entero('\nSeleccione el producto: ', 0, len(listaProductosVender))
                    diccionarioProductos['producto'] = listaProductosVender[producto - 1]['nombre']

                    cantidad = recibir_entero('Escriba la cantidad del producto: ', 0)
                    diccionarioProductos['cantidad'] = cantidad

                    listaProductos.append(diccionarioProductos)
                    ventas['productos'] = listaProductos

                    subSubTotal += listaProductosVender[producto - 1]['precio'] * cantidad

                    if cantidad > 5:
                        descuento += subSubTotal * 0.1
                        subSubTotal -= descuento

                    subTotal += subSubTotal

                    opcion = recibir_entero('¿Desea ingresar otro producto? (1. SI, 2. NO): ', 0, 2)

                    if opcion == 2:
                        break

                total += subTotal

                lugar = recibir_entero('Escriba el tipo de lugar (1. Local, 2. Nacional, 3. Internacional): ', 0, 3)
                envio = recibir_entero('Escriba el tipo de envio (1. Express, 2. Normal): ', 0, 2)

                if envio == 1:
                    if total >= 1000000 and lugar == 1:
                        costoEnvio += normal[lugar - 1]
                        descuento += express[lugar - 1] - costoEnvio
                    elif total >= 1500000 and lugar == 2:
                        costoEnvio += normal[lugar - 1]
                        descuento += express[lugar - 1] - costoEnvio
                    elif total >= 2000000 and lugar == 3:
                        costoEnvio += normal[lugar - 1]
                        descuento += express[lugar - 1] - costoEnvio
                    else:
                        costoEnvio = express[lugar - 1]
                else:
                    if total >= 1000000 and lugar == 1:
                        costoEnvio += 0.0
                        descuento += normal[lugar - 1] - costoEnvio
                    elif total >= 1500000 and lugar == 2:
                        costoEnvio += 0.0
                        descuento += normal[lugar - 1] - costoEnvio
                    elif total >= 2000000 and lugar == 3:
                        costoEnvio += 0.0
                        descuento += normal[lugar - 1] - costoEnvio
                    else:
                        costoEnvio = normal[lugar - 1]

                ventas['descuento'] = descuento

                total += costoEnvio
                ventas['subTotal'] = total

                listaProductosOrdenada = ordenar_lista_dicc(listaProductos, 'cantidad')
                ventas['productos'] = listaProductosOrdenada



                listaClientes.append(ventas)
                listaClientes_json = json.dumps(listaClientes, indent=2)

                with open("compras.txt", "w", encoding="utf-8") as nuevo:
                    nuevo.write(listaClientes_json)

                opcion = recibir_entero('¿Ingresar otro registro? (1. SI, 2. NO): ', 0, 2)
                if opcion == 2:
                    break

        elif opcion == 3:

            with open("compras.txt", encoding="utf-8") as archivo:
                listaClientes = json.load(archivo)

            mensaje = f"\n{'CLIENTE':>20}{'PRODUCTO':>30}{'CANTIDAD':>20}{'DESCUENTO':>20}{'TOTAL':>20}\n"
            total = 0
            for cliente in range(len(listaClientes)):
                for i in range(len(listaClientes[cliente]['productos'])):
                    if i == 0:
                        mensaje += f"{listaClientes[cliente]['nombre']:>20}"
                    else:
                        mensaje += f"{'':>20}"
                    mensaje += f"{listaClientes[cliente]['productos'][i]['producto']:>30}"
                    mensaje += f"{listaClientes[cliente]['productos'][i]['cantidad']:>20}"
                    if i == 0:
                        mensaje += f"{listaClientes[cliente]['descuento']:>20}"
                    else:
                        mensaje += f"{'':>20}"
                    if i == 0:
                        mensaje += f"{listaClientes[cliente]['subTotal']:>20}\n"
                    else:
                        mensaje += f"{'':>20}\n"
                mensaje += '\n'
                total += listaClientes[cliente]['subTotal']

            mensaje += f"\n{'TOTAL VENTAS':>20}{total:>20}"

            print(mensaje)
