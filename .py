import datetime
import time

import openpyxl
import csv

import random
salas = {}
turnos = {1:"Matutino", 2:"Vespertino", 3:"Nocturno"}
numero_sala=0

clave_cliente=0
datos_clientes={}

datos_reservacion={}
reservaciones={0:[0,'0','0','0']}
folio_reservacion = 0

fecha_actual = datetime.date.today()
diferencia_dias = 2
fecha_reservacion_procesada = ""

lista_encontrados = []
reservaciones_posibles = []

try:
  with open("reservaciones.csv","r", newline="") as archivo:
      lector = csv.reader(archivo)
      next(lector)
      
      for Folio_de_reservacion, Sala, Nombre, Fecha_reservacion, Turno in lector:
          reservaciones[int(Folio_de_reservacion)] = (Sala, Nombre, Fecha_reservacion, Turno)
except FileNotFoundError:
  print("NO SE CUENTA CON RESERVACIONES PREVIAS REGISTRADAS, SE INICIARA DE 0")

try:
  with open("salas.csv","r", newline="") as archivo:
      lector = csv.reader(archivo)
      next(lector)
      
      for Numero_de_Sala, Nombre, Capacidad in lector:
          salas[int(Numero_de_Sala)] = [Nombre,Capacidad]
except FileNotFoundError:
  print("NO SE CUENTA CON SALAS PREVIAS REGISTRADAS, SE INICIARA DE 0")


try:
  with open("datos_clientes.csv","r", newline="") as archivo:
      lector = csv.reader(archivo)
      next(lector)
      
      for Numero_de_Cliente, Nombre in lector:
          datos_clientes[int(Numero_de_Cliente)] = Nombre
except FileNotFoundError:
  print("NO SE CUENTA CON CLIENTES PREVIOS REGISTRADOS, SE INICIARA DE 0")

submenu=0
while True:
    print("Bienvenidos al sistema para la reservacion de renta de espacios coworking")

    print("\t [A]Reservaciones")

    print("\t [B]Reportes")

    print("\t [C]Registrar una sala")

    print("\t [D]Registrar un cliente")

    print("\t [E]Salir")

    opcion=input("Elije la opcion deseada, oprimiendo la tecla de la letra que corresponda: ")
    print("*" * 60)

    if (not opcion.upper() in "ABCDE"):
            print("Opcion incorrecta, favor de volver a intentarlo")
            print("*" * 60)

    if (opcion.upper()== "A"):
        while True:
            print("\t [A]Registrar una nueva reservacion")
            print("\t [B]Modificar descripcion de una reservacion")
            print("\t [C]Consultar disponibilidad de una fecha")

            opcion2=input("Elije la opcion deseada, oprimiendo la tecla de la letra que corresponda: ")
            print("*" * 60)

            if (not opcion2.upper() in "ABC"):
                print("Opcion incorrecta, favor de volver a intentarlo")
                print("*" * 60)

            if (opcion2.upper()== "A"):
                respuesta = int(input("Ingresar su numero de cliente: "))
                print("*" * 60)
                        

                if respuesta in datos_clientes:
                    sala = int(input("Ingresa el numero de sala que sera utilizada: "))
                    print("*" * 60)
                    if sala in salas:
                        fecha_reservacion = input("¿Cual seria la fecha en que deseea realizar su reservacion? (DD/MM/AAAA): ")
                        print("*" * 60)
                        fecha_reservacion_procesada = datetime.datetime.strptime(fecha_reservacion, "%d/%m/%Y").date()
                        diferencia_dias=fecha_reservacion_procesada - fecha_actual
                        if diferencia_dias.days <=2:
                            print("La reservacion de una sala, tiene que ser por lo minimo 2 dias con anterioridad")
                            print("*" * 60)
                            break
                        else:
                            turno_reservacion = input("Favor de escribir como se muestra en las opciones, en que turno deseea su reservacion (Matutino/Vespertino/Nocturno): ")
                            print("*" * 60)
                            for valores in reservaciones.values():
                              print(".")
                            if valores[0] == sala and valores[2] == fecha_reservacion and valores[3] == turno_reservacion:
                                print("Lo sentimos, ya existe una reservacion para esta sala, en el dia y turno seleccionado")
                                print("*" * 60)
                                break
                            else:
                                folio_reservacion += 1
                                nombre_evento=input("¿Cual es el nombre de su evento?: ")
                                print("*" * 60)
                                reservaciones.update({folio_reservacion:(sala,nombre_evento,fecha_reservacion,turno_reservacion)})
                                print(f'El folio de su reservacion es {folio_reservacion}')
                                print("*" * 60)
                                break
                                            
                    else:
                      print("Sala seleccionada no existente")
                      print("*" * 60)
                      break
                else:
                    print("Para realizar una reservacion es necesario ser cliente registrado, favor de primero hacer su registro")
                    print("*" * 60)
                    break

            if (opcion2.upper()== "B"):
                folio_reservacion = int(input("¿Cual es el numero de folio de su reservacion?: "))
                recuperado=reservaciones.get(folio_reservacion) 
                if recuperado == None:
                    print("El numero de folio de reservacion no fue encontrado")
                    break
                else:
                    nuevo_nombre = input("¿Cual sera el nuevo nombre de su evento: ")
                    reservaciones.update({folio_reservacion:(sala,nuevo_nombre,fecha_reservacion,turno_reservacion)})
                    print("Cambio realizado exitosamente")
                    print("*" * 60)
                    break

            if (opcion2.upper()== "C"):
                fecha_buscada=input("Ingresa la fecha buscada:")
                print("*" * 60)
                for clave, valor in reservaciones.items():
                    if valor[2] == fecha_buscada:
                        lista_encontrados.append((valor[0],valor[3]))
                    
                reservaciones_encontradas=set(lista_encontrados)
                

                for sala in salas.keys():
                    for turno in turnos.items():
                        reservaciones_posibles.append((sala, turno[1]))
                
                combinaciones_reservaciones_posibles=set(reservaciones_posibles)
                total=  sorted(combinaciones_reservaciones_posibles - reservaciones_encontradas)
                print(f'LA DISPONIBILIDAD PARA EL DIA {fecha_buscada} ES LA SIGUIENTE: ')
                print("Sala        Turno")
                for datos in total:
                  print(f'{datos[0]}        {datos[1]} ')
                print("*" * 60)
                break
    
    if (opcion.upper()== "B"):
        while True:
            print("\t [A]Reporte en pantalla de reservaciones en una fecha")
            print("\t [B]Exportar reporte tabular en excel")

            opcion3=input("Elije la opcion deseada, oprimiendo la tecla de la letra que corresponda: ")
            print("*" * 60)

            if (not opcion3.upper() in "AB"):
                print("Opcion incorrecta, favor de volver a intentarlo")
                print("*" * 60)

            if (opcion3.upper()=="A"):
              fecha_mostrar= input("¿Cual seria la fecha en que deseea ver las reservaciones realizadas? (DD/MM/AAAA): ")
              print("*" * 60)
              print(f'RESERVACIONES DEL DIA {fecha_mostrar}')
              for valores in reservaciones.values():
                if valores[2] == fecha_mostrar:
                    # Accion despues de validar que si existe una fecha
                    print("*" * 60)
                    print("Sala     Nombre de reservacion       Fecha             Turno")
                    print(f'{valores[0]}           {valores[1]}                {valores[2]}           {valores[3]} ')
              break

            if (opcion3.upper()=="B"):
              wb = openpyxl.Workbook()
              hoja1 = wb.create_sheet("Hoja")
              hoja = wb.active
              # Crea la fila del encabezado con los títulos
              hoja.append(('Sala', 'Nombre del evento', 'Fecha', 'Turno'))
              fecha_exportar= input("¿Cual seria la fecha en que deseea realizar su reservacion? (DD/MM/AAAA):")
              print("*" * 60)
              for valores in reservaciones.values():
                if valores[2] == fecha_exportar:
                  # producto es una tupla con los valores de un producto 
                  hoja.append(valores)
                  wb.save('Reservaciones.xlsx')
              print("Datos exportados correctamente a un archivo de MsExcel")
              print("*" * 60)
              break


    if (opcion.upper()== "C"):
        while True:
          nombre_sala=input("Ingresa el nombre de la sala: ")
          print("*" * 60)
          if nombre_sala == "":
            print("El nombre de la sala no debe de omitirse, intentelo nuevamente")
            print("*" * 60)
          else:
            break
        while True:
          cap_sala=int(input("Ingresa la cantidad de aforo maximo de la sala: "))
          print("*" * 60)
          if cap_sala <=0:
            print("El cupo no puede omitirse y/o ser menor a 0, intentelo nuevamente ")
            print("*" * 60)
          else:
            break
        numero_sala += 1
        salas.update({numero_sala:[nombre_sala,cap_sala]})
        print(f'El numero de la sala {nombre_sala} sera {numero_sala}')
        print("*" * 60)

        
    if (opcion.upper()== "D"):
        while True:
          nombre_cliente=input("Ingrese su nombre completo: ")
          print("*" * 60)
          if nombre_cliente == "":
            print("El nombre del cliente no se debe de omitir, favor de intentarlo nuevamente")
            print("*" * 60)
          else:
            break
        clave_cliente+=1
        datos_clientes[clave_cliente]= nombre_cliente
        print(f'Su numero de cliente es {clave_cliente}')
        print("*" * 60)


    if (opcion.upper()== "E"):
      with open ("reservaciones.csv", "w", newline="") as archivo:
        grabador = csv.writer(archivo)
        grabador.writerow(("Folio_de_reservacion", "Sala", "Nombre", "Fecha_reservacion","Turno" ))
        grabador.writerows([(folio, valores[0], valores[1], valores[2], valores[3]) for folio, valores in reservaciones.items()])

      with open ("salas.csv", "w", newline="") as archivo:
        grabador = csv.writer(archivo)
        grabador.writerow(("Numero_de_Sala", "Nombre", "Capacidad"))
        grabador.writerows([(num_sala, valores[0], valores[1]) for num_sala, valores in salas.items()])

      with open ("datos_clientes.csv", "w", newline="") as archivo:
        grabador = csv.writer(archivo)
        grabador.writerow(("Numero_de_Cliente", "Nombre"))
        grabador.writerows([(num_cliente, valor[0]) for num_cliente, valor in datos_clientes.items()])

      print("¡Que tenga un bonito dia!")
      break
   
