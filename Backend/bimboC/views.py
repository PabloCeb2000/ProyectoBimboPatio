from rest_framework import viewsets
from .models import (
    Product, Truck, OutGoingOrder, ActiveStock, ReserveStock, StockOBLPN, Remission, Pending
)
from .serializers import (
    ProductSerializer, TruckSerializer, OutGoingOrderSerializer,
    ActiveStockSerializer, ReserveStockSerializer, StockOBLPNSerializer, 
    RemissionSerializer, PendingSerializer, 
    RemissionSerializer1, TruckSerializer1, PendingSerializer1
)
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django.shortcuts import get_object_or_404, render

from datetime import datetime
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
import oci
import os
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

#ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

class OutGoingOrderViewSet(viewsets.ModelViewSet):
    queryset = OutGoingOrder.objects.all()
    serializer_class = OutGoingOrderSerializer

class ActiveStockViewSet(viewsets.ModelViewSet):
    queryset = ActiveStock.objects.all()
    serializer_class = ActiveStockSerializer

class ReserveStockViewSet(viewsets.ModelViewSet):
    queryset = ReserveStock.objects.all()
    serializer_class = ReserveStockSerializer

class StockOBLPNViewSet(viewsets.ModelViewSet):
    queryset = StockOBLPN.objects.all()
    serializer_class = StockOBLPNSerializer

class RemissionViewSet(viewsets.ModelViewSet):
    queryset = Remission.objects.all()
    serializer_class = RemissionSerializer

class PendingViewSet(viewsets.ModelViewSet):
    queryset = Pending.objects.all()
    serializer_class = PendingSerializer

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'Trucks List': reverse('truck-list', request=request),
        'Orders List': reverse('order-list', request=request),
        'Products List': reverse('product-list', request=request),
    }
    return Response(api_urls)

# Funciónes para procesar el json recibido por oracle

# Función para extraer textos que cumplan con el patrón de identificación
def extract_truck_id_func(data):
    # Define el patrón que representa las identificaciones
    id_pattern = r"^[A-Z]{3}\d{4,5}$"

    # Itera sobre las páginas y palabras en el JSON
    for page in data.get("pages", []):
        for line in page.get("lines", []):
            text = line.get("text", "")
            text = text.replace(" ", "")
            # Si el texto coincide con el patrón, regresarlo
            if re.match(id_pattern, text):
                return text

#Función para extraer el texto del json sobre la información de la localización del camión
def extract_truck_location_func(data):
    # Define el patrón que representa las identificaciones
    id_pattern = r"^Zona.*"

    # Itera sobre las páginas y palabras en el JSON
    for page in data.get("pages", []):
        for line in page.get("lines", []):
            text = line.get("text", "")
            #text = text.replace(" ", "")
            # Si el texto coincide con el patrón, regresarlo
            if re.match(id_pattern, text):
                return text


#Función para actualizar la ubicación del camión basado en su identificación
def update_truck_location_func(truck_number, new_location):

    try:
        # Buscar el camión por truck_number
        truck = Truck.objects.get(truck_number=truck_number)

        # Actualizar la ubicación
        truck.location = new_location
        truck.save()  # Guardar cambios en la base de datos

        # Retornar datos actualizados
        return {
            "message": "Truck location updated successfully",
            "truck": {
                "truck_number": truck.truck_number,
                "location": truck.location,
            }
        }
    
    except ObjectDoesNotExist:
        # Si el camión no se encuentra
        return {"error": "Truck not found"}

#Función para recibir la información del camión y actualizar su ubicación en la base de datos
@api_view(['POST'])
@csrf_exempt
def getJSON(request):
    config = oci.config.from_file() #Es necesario tener un archivo de 'config' en la carpeta .oci
    object_storage_client = oci.object_storage.ObjectStorageClient(config)

    namespace_name = "axsrrd0wd0aa"
    bucket_name = "bucket-Text-Extraction-Results"

    data = json.loads(request.body)
    object_name = data.get('objectName')
    print(object_name)

    get_object_response = object_storage_client.get_object(
        namespace_name=namespace_name,
        bucket_name=bucket_name,
        object_name=object_name
    )

    try:
            print(get_object_response.data.text)
            object_content = json.loads(get_object_response.data.text)

            truck_location = extract_truck_location_func(object_content)
            truck_number = extract_truck_id_func(object_content)
            print(truck_location)
            print(truck_number)

            try:
                truck = Truck.objects.get(truck_number=truck_number)
                
                # Si el camión ya existe, actualizar su ubicación
                update_truck_location_func(truck_number, truck_location)
                #print(update_response)
                return Response({"detail": "Truck location updated successfully"}, status=status.HTTP_200_OK)
            
            except ObjectDoesNotExist:
                # Crear una nueva entrada en Truck
                truck = Truck.objects.create(
                    truck_number=truck_number,
                    location=truck_location,
                    status="En patio",
                    size="Grande"
                )
                print(truck)
                return Response({"detail": "Truck created successfully"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   

    return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
    

class TruckArrivalView(viewsets.ModelViewSet):
    queryset = Remission.objects.all()  # Required for ModelViewSet
    serializer_class = RemissionSerializer

    @action(detail=False, methods=['post'], url_path='retrieve-or-create')
    def retrieve_by_embark(self, request, *args, **kwargs):
        embark_value = request.data.get('embark', None)
        box_number = request.data.get('truck_number', None)
        date = request.data.get('date', None)

        if not embark_value:
            return Response({"detail": "Embark value is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not box_number:
            return Response({"detail": "Truck number (box_number) is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Buscar el camión
        try:
            truck = Truck.objects.get(truck_number=box_number)
        except Truck.DoesNotExist:
            return Response({"detail": "Truck with the provided box_number does not exist."}, status=status.HTTP_404_NOT_FOUND)


        # Actualizar el camión
        truck.status = "Cargado"
        truck.location = "CEDIS"
        truck.save()


        # Buscar o crear la remisión
        try:
            print(truck.truck_number)
            remission = Remission.objects.get(embark=embark_value)
            remission_created = False

        except Remission.DoesNotExist:
            print(truck)
            new_remission_data = {
                "embark": embark_value,
                "box_number_id": truck.truck_number,
                "date": date
            }
            serializer = self.get_serializer(data=new_remission_data)
            if serializer.is_valid():
                remission = serializer.save()
                remission_created = True
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        remission_serializer = RemissionSerializer(remission)

        #Buscar la orden pendiente con ese número de embarque
        pending_orders = Pending.objects.filter(embark=embark_value)
        if not pending_orders.exists():
            return Response({"detail": "The associated pending orders do not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        
        pending_orders.update(status="Disponible en CEDIS")

        return Response({
            "remission": remission_serializer.data,
            "remission_created": remission_created,
            "updated_truck": {
                "status": truck.status,  # Estado del camión
                "location": truck.location  # Ubicación del camión
            }
        }, status=status.HTTP_200_OK if not remission_created else status.HTTP_201_CREATED)


class TruckUnloadingView(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    @action(detail=False, methods=['post'], url_path='truck-unloading')
    def truck_unloading(self, request, *args, **kwargs):
        truck_number = request.data.get('truck_number')
        embark_value = request.data.get('embark')
        pit_number = request.data.get('pit_number')

        if not (embark_value and pit_number and truck_number):
            return Response({"detail": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar el camión
        try:
            truck = Truck.objects.get(truck_number=truck_number)
        except Truck.DoesNotExist:
            return Response({"detail": "Truck with the provided box_number does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener la ubicación por el atributo location (string)
        location = "Fosa " + str(pit_number)
        
        truck.status = "Vacio"
        truck.location = location

        #Buscar la orden pendiente con ese número de embarque
        try:
            remission = Remission.objects.get(embark=embark_value)
        except Remission.DoesNotExist:
            return Response({"detail": "The sepcified order do not exist"} , status=status.HTTP_404_NOT_FOUND)
        
        pending_orders = Pending.objects.filter(embark=embark_value)
        if not pending_orders.exists():
            return Response({"detail": "The associated pending orders do not exist."}, status=status.HTTP_404_NOT_FOUND)
        

        pending_orders.update(status="Disponible en almacén")
        truck.save()


        return Response({
            "updated_truck": "Vacio",
            "location": location

        }, status=status.HTTP_200_OK)

    
class TruckDepartureView(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    @action(detail=False, methods=['post'], url_path='truck-departure')
    def truck_departure(self, request, *args, **kwargs):

        truck_number = request.data.get('truck_number')

        if not truck_number:
            return Response({"detail": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar el camión
        try:
            truck = Truck.objects.get(truck_number=truck_number)
        except Truck.DoesNotExist:
            return Response({"detail": "Truck with the provided box_number does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        truck.status = "No disponible"
        truck.location = "En ruta"

        truck.save()
        
        return Response({"updated_truck":{
            "truck_status": truck.status.status,
            "truck_location": truck.location.location}}, status=status.HTTP_201_CREATED)
        


##############################3
###ALGORTIMO GENÉTICO ############
###################################



import pandas as pd
import random
# ALGORITMO GENÉTICO


def get_pending_dict(pending_status):
    #queryset = Pending.objects.get()
    serializer_class = PendingSerializer


    orders_dictionary = []
    if pending_status != "Todas":
    # Obtener todas las órdenes de la base de datos
        orders = Pending.objects.filter(status=pending_status).values("embark", "product_id", "quantity", "close_dt")
    else:
        orders = Pending.objects.all().values("embark", "product_id", "quantity", "close_dt")



    if not orders:
        return None
    # Convertir el QuerySet a un DataFrame
    df = pd.DataFrame(list(orders))
    df['close_dt'] = pd.to_datetime(df['close_dt'])
    # Obtener la fecha y hora actual
    now = datetime.now()

    # Calcular la diferencia en minutos y horas
    df['elapsed_minutes'] = (now - df['close_dt']).dt.total_seconds() / 60  # Convertir a minutos
    df['elapsed_hours'] = df['elapsed_minutes'] / 60  # Convertir a horas

    prices = OutGoingOrder.objects.all().values("product", "price")
    df_prices = pd.DataFrame(list(prices))
    df_prices = df_prices.drop_duplicates(subset='product')


    df = df.join(df_prices.set_index('product'), on='product_id')
    result = df.groupby(["embark", "product_id", "price", "close_dt", "elapsed_minutes", "elapsed_hours"]).agg(['sum']).reset_index()

    result.columns = [
        col[0] if col[1] == '' else f"{col[0]}_{col[1]}"  # Mantén las columnas originales o agrega sufijo solo si es necesario
        for col in result.columns
    ]
    result['price_x_quantity_sum'] = result.price * result.quantity_sum 
    # Convertir el resultado agrupado a una lista de diccionarios
    print(result.head(10))

    orders_dictionary = result.to_dict(orient="records")

    result_dict = result.groupby('embark').apply(
        lambda x: {
            "id": x['embark'].iloc[0],
            "productos": dict(zip(x['product_id'], x['quantity_sum'])),
            "valor": float(x['price_x_quantity_sum'].sum().round(2)),
            #"total_tiempo":  float(x['elapsed_hours'].iloc[0].round(2))# Sumar el dinero total por embarque
        }
    ).to_list()

    return(result_dict)



def get_outgoing_orders():
    outgoing_orders = OutGoingOrder.objects.all().values("order_number", "product", "status", "requested_quantity", "creation_date")
    df_outgoing_orders = pd.DataFrame(list(outgoing_orders))

    #Filtrar por order status
    df_outgoing_orders = df_outgoing_orders[df_outgoing_orders["status"] == 'Created']

    df_outgoing_orders['creation_date'] = pd.to_datetime(df_outgoing_orders['creation_date'])
    
    now = datetime.now()

    # Calcular la diferencia en minutos y horas
    df_outgoing_orders['elapsed_minutes'] = (now - df_outgoing_orders['creation_date']).dt.total_seconds() / 60  # Convertir a minutos
    df_outgoing_orders['elapsed_hours'] = df_outgoing_orders['elapsed_minutes'] / 60  # Convertir a horas


    # Asegúrate de no tener MultiIndex en las columnas
    df_outgoing_orders = df_outgoing_orders.groupby(["order_number", "product", "status", "creation_date", "elapsed_minutes", "elapsed_hours"]).sum().reset_index()
    
    df_filtered = df_outgoing_orders[df_outgoing_orders["order_number"] == 3077005]
    print(df_filtered)

    outgoing_dict = []

    for order_number, group in df_outgoing_orders.groupby("order_number"):
        productos = {str(row["product"]): row["requested_quantity"] for _, row in group.iterrows()}
        # Obtener un valor único para elapsed_hours del grupo actual
        elapsed_hours = group["elapsed_hours"].iloc[0]  # Usa el primer valor; asume que todos los productos de la orden tienen el mismo tiempo transcurrido

        # Crear el diccionario para esta orden
        outgoing_dict.append({
            "id": str(order_number),  # id es igual a order_number
            "productos": productos,
            "fecha_creacion": float(elapsed_hours)  # Convierte a float, si es necesario
        })
    return(outgoing_dict)


@csrf_exempt
@api_view(["POST"]) 
def priorize_trucks(request):
    
    try:
        num_fosas = request.data.get("num_fosas")
        order_status = request.data.get("status")
        peso_fecha = request.data.get("peso_fecha")
        peso_ganancia = request.data.get("peso_ganancia")
        peso_cantidad = request.data.get("peso_cantidad")

        if not isinstance(num_fosas, int) or num_fosas <= 0:
            return Response({"error": "num_fosas debe ser un número entero positivo."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(order_status, str) or order_status not in ["Todas", "Disponible en CEDIS", "En ruta"]:
            return Response({"error": "status debe ser un string válido ('pendiente', 'procesado', 'completado')."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(peso_fecha, (int, float)) or peso_fecha < 0.0:
            return Response({"error": "peso_fecha debe ser un número mayor o igual a 0."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(peso_ganancia, (int, float)) or peso_ganancia < 0.0:
            return Response({"error": "peso_ganancia debe ser un número mayor o igual a 0."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(peso_cantidad, (int, float)) or peso_cantidad < 0.0:
            return Response({"error": "cantidad debe ser un número entero positivo."}, status=status.HTTP_400_BAD_REQUEST)
        
   
    except Exception as e:
    # Manejo de errores inesperados
        return Response({"error": f"Se produjo un error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Parámetros generales
    MAX_CAMIONES_SIMULTANEOS = num_fosas
    NUM_GENERACIONES = 100
    TAMANO_POBLACION = 10
    PROB_MUTACION = 0.3

    # Pesos de la función de aptitud
    PESO_ORDENES_ANTIGUAS = peso_fecha
    PESO_VALOR_TOTAL = peso_ganancia
    PESO_CANTIDAD_PRODUCTOS = peso_cantidad

    camiones = get_pending_dict(order_status)

    if not camiones:
        return Response({"detail": "No hay camiones con ese status"}, status=status.HTTP_404_NOT_FOUND)
    
    ordenes = get_outgoing_orders()

    print(camiones)

    if len(camiones) < num_fosas:


        priorized_embarks = {}
        for camion in camiones:
            
            num_embark = camion['id']
            print(num_embark)

            try:
                pending = Pending.objects.filter(embark=num_embark).first()
                order_status = pending.status
                print(order_status)
            except Pending.DoesNotExist:
                # Si no existe el Pending, salta al siguiente individuo
                continue

            if order_status == "Disponible en CEDIS":
                try:
                    remission = Remission.objects.filter(embark=num_embark).first()
                    remission_truck_number = remission.box_number.truck_number

                    try:
                        truck = Truck.objects.get(truck_number=remission_truck_number)
                        truck_number = truck.truck_number
                        truck_location = truck.location
                    except Truck.DoesNotExist:
                        truck_number = "Sin camión asociado"
                        truck_location = "No disponible"

                except Remission.DoesNotExist:
                    truck_number = "Sin camión asociado"
                    truck_location = "No disponible"

            else:
                truck_number = "Sin camión asociado"
                truck_location = "No disponible"
            
            priorized_embarks[num_embark] = {
            "num_embark": num_embark,
            "status": order_status,
            "truck_number": truck_number,
            "truck_location": truck_location,
        }
            
        embarks = {"embarks": priorized_embarks}

        return Response(embarks,status=status.HTTP_200_OK)



    max_antiguedad = max(orden["fecha_creacion"] for orden in ordenes)
    max_valor_total = max(camion["valor"] for camion in camiones)
    max_cantidad_productos = max(sum(camion["productos"].values()) for camion in camiones) 

        
    # Función de aptitud con pesos
    def calcular_aptitud(individuo, camiones, ordenes):
        productos_satisfechos = {key: 0 for orden in ordenes for key in orden["productos"]}
        valor_total = 0
        antiguedad_total = 0
        cantidad_productos_utiles = 0

        # Calcular métricas
        for id_camion in individuo:
            camion = next(c for c in camiones if c["id"] == id_camion)
            valor_total += camion["valor"]
            for producto, cantidad in camion["productos"].items():
                if producto in productos_satisfechos:
                    productos_satisfechos[producto] += cantidad

        # Calcular productos satisfechos y antigüedad ponderada
        for orden in ordenes:
            for producto, cantidad in orden["productos"].items():
                satisfecha = min(productos_satisfechos.get(producto, 0), cantidad)
                antiguedad_total += satisfecha * (1 / orden["fecha_creacion"])  # Prioridad por antigüedad
                cantidad_productos_utiles += satisfecha

        antiguedad_total = antiguedad_total / max_antiguedad
        valor_total = valor_total / max_valor_total
        cantidad_productos_utiles = cantidad_productos_utiles / max_cantidad_productos

        # Combinar las métricas con los pesos
        puntuacion = (
            PESO_ORDENES_ANTIGUAS * antiguedad_total +
            PESO_VALOR_TOTAL * valor_total +
            PESO_CANTIDAD_PRODUCTOS * cantidad_productos_utiles
        )

        return puntuacion

    # Generar población inicial (sin repeticiones)
    def generar_poblacion(camiones, tamano):
        ids_camiones = [c["id"] for c in camiones]
        return [random.sample(ids_camiones, random.randint(1, min(len(ids_camiones), MAX_CAMIONES_SIMULTANEOS))) for _ in range(tamano)]

    # Selección por torneo
    def seleccion_torneo(poblacion, aptitudes, k=3):
        participantes = random.sample(range(len(poblacion)), k)
        ganador = max(participantes, key=lambda i: aptitudes[i])
        return poblacion[ganador]

    # Cruce (sin duplicados)
    def cruce(individuo1, individuo2):
        conjunto1 = set(individuo1)
        conjunto2 = set(individuo2)
        hijo = list(conjunto1.union(conjunto2))  # Unión de genes sin duplicados
        random.shuffle(hijo)
        return hijo[:MAX_CAMIONES_SIMULTANEOS], hijo[MAX_CAMIONES_SIMULTANEOS:]

    # Mutación (sin duplicados)
    def mutacion(individuo, camiones):
        if random.random() < PROB_MUTACION:
            ids_camiones = [c["id"] for c in camiones]
            if len(individuo) < MAX_CAMIONES_SIMULTANEOS:
                candidato = random.choice([id for id in ids_camiones if id not in individuo])
                individuo.append(candidato)
            else:
                individuo[random.randint(0, len(individuo) - 1)] = random.choice([id for id in ids_camiones if id not in individuo])
        return individuo

    # Algoritmo genético
    def algoritmo_genetico(camiones, ordenes, generaciones, tamano_poblacion):
        poblacion = generar_poblacion(camiones, tamano_poblacion)

        for _ in range(generaciones):
            aptitudes = [calcular_aptitud(ind, camiones, ordenes) for ind in poblacion]

            nueva_poblacion = []
            while len(nueva_poblacion) < tamano_poblacion:
                padre1 = seleccion_torneo(poblacion, aptitudes)
                padre2 = seleccion_torneo(poblacion, aptitudes)
                hijo1, hijo2 = cruce(padre1, padre2)
                nueva_poblacion.append(mutacion(hijo1, camiones))
                if len(nueva_poblacion) < tamano_poblacion:
                    nueva_poblacion.append(mutacion(hijo2, camiones))

            poblacion = nueva_poblacion  

                    # Mejor solución final
            aptitudes = [calcular_aptitud(ind, camiones, ordenes) for ind in poblacion]
            mejor_indice = aptitudes.index(max(aptitudes))
            return poblacion[mejor_indice], aptitudes[mejor_indice]

    mejor_individuo, mejor_aptitud = algoritmo_genetico(camiones, ordenes, NUM_GENERACIONES, TAMANO_POBLACION)

    
    priorized_embarks = {}

    
    priorized_embarks = {}

    for individuo in mejor_individuo:
        num_embark = individuo

        try:
            pending = Pending.objects.filter(embark=num_embark).first()
            order_status = pending.status
            print(order_status)
        except Pending.DoesNotExist:
            # Si no existe el Pending, salta al siguiente individuo
            continue

        if order_status == "Disponible en CEDIS":
            try:
                remission = Remission.objects.filter(embark=num_embark).first()
                remission_truck_number = remission.box_number.truck_number

                try:
                    truck = Truck.objects.get(truck_number=remission_truck_number)
                    truck_number = truck.truck_number
                    truck_location = truck.location
                except Truck.DoesNotExist:
                    truck_number = "Sin camión asociado"
                    truck_location = "No disponible"

            except Remission.DoesNotExist:
                truck_number = "Sin camión asociado"
                truck_location = "No disponible"

        else:
            truck_number = "Sin camión asociado"
            truck_location = "No disponible"

        priorized_embarks[num_embark] = {
            "num_embark": num_embark,
            "status": order_status,
            "truck_number": truck_number,
            "truck_location": truck_location,
        }

    embarks = {"embarks": priorized_embarks}
            

    
    return Response(embarks, status=status.HTTP_200_OK)



