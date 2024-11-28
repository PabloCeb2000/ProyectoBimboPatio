import os
import django
import pandas as pd

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bimbo.settings")
django.setup()

# Importar el modelo después de configurar Django
from bimboC.models import Product, OutGoingOrder, ActiveStock, ReserveStock, StockOBLPN, Pending

# Cargar el archivo Excel
def populate_products(file_path):
    try:
        # Procesar la hoja "Pendientes por recibir"
        pendientes_df = pd.read_excel(file_path, sheet_name="Items")
        for _, row in pendientes_df.iterrows():
            item = row['ITEM']
            description = row['DESCRIPCION']

            # Crear o actualizar el producto
            Product.objects.get_or_create(
                product=item,
                defaults={'description': description}  # Si existe, no actualiza 'description'
            )
        
        print("Datos de 'Productos' cargados correctamente.")


    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

def populate_outgoing_orders(file_path):
    try:
        # Leer la hoja "ordenes"
        orders_df = pd.read_excel(file_path, sheet_name="ordenes")

        for _, row in orders_df.iterrows():
            # Extraer datos del Excel
            order_number = row['Orden']
            article = row['Articulo']
            description = row['Descripcion de articulo']
            order_date = row['Fecha de caducidad de comprobante']
            price = row['Precio de venta']
            creation_date = row['Fecha de Creacion']
            detail = row['Detalle de orden - Campo personalizado 5']
            og_quantity = row['Cantidad de orden original']
            requested_quantity = row['Cantidad solicitada']
            assigned_quantity = row['Cantidad asignada']
            packed_quantity = row['Cantidad empaquetada']
            status = row['orderdtlstatus']

            # Buscar o crear el producto relacionado
            product, _ = Product.objects.get_or_create(
                product=article,
                defaults={'description': description}
            )

            # Convertir las fechas al formato adecuado
            order_date = pd.to_datetime(order_date).date() if pd.notna(order_date) else None
            creation_date = pd.to_datetime(creation_date).date() if pd.notna(creation_date) else None

            # Crear la orden (sin evitar duplicados)
            OutGoingOrder.objects.create(
                order_number=order_number,
                product=product,
                status=status,
                order_date=order_date,
                price=price,
                creation_date=creation_date,
                detail=detail,
                og_quantity=og_quantity,
                requested_quantity=requested_quantity,
                assigned_quantity=assigned_quantity,
                packed_quantity=packed_quantity,
            )

        print("Datos de 'OutgoingOrders' cargados correctamente.")


    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

def populate_active_stock(file_path):
    try:
        # Leer la hoja "stock activo"
        active_stock_df = pd.read_excel(file_path, sheet_name="existencia")

        for _, row in active_stock_df.iterrows():
            # Extraer datos del Excel
            article = row['PRODUCTO']
            description = row['DESCRIPCIÓN DEL PRODUCTO']
            available = row['DISPONIBLE']
            assigned = row['ASIGNADO']
            total_active = row['TOTAL EN ACTIVO']

            # Buscar o crear el producto relacionado
            product, _ = Product.objects.get_or_create(
                product=article,
                defaults={'description': description}
            )

            # Crear el stock activo (sin evitar duplicados)
            ActiveStock.objects.create(
                product=product,
                available=available,
                assigned=assigned,
                total_active=total_active,
            )

        print("Datos de 'ActiveStock' cargados correctamente.")

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

def populate_reserve_stock(file_path):
    try:
        # Leer la hoja "stock de reserva"
        reserve_stock_df = pd.read_excel(file_path, sheet_name="existencia")

        for _, row in reserve_stock_df.iterrows():
            # Extraer datos del Excel
            article = row['PRODUCTO']
            description = row['DESCRIPCIÓN DEL PRODUCTO']
            received = row['RECIBIDO']
            located = row['UBICADO']
            partially_assigned = row['PARCIALMENTE ASIGNADO']
            assigned = row['ASIGNADO']
            lost = row['PERDIDO']
            total_reserve = row['TOTAL EN RESERVA']

            # Buscar o crear el producto relacionado
            product, _ = Product.objects.get_or_create(
                product=article,
                defaults={'description': description}
            )

            # Crear el stock de reserva (sin evitar duplicados)
            ReserveStock.objects.create(
                product=product,
                received=received,
                located=located,
                partially_assigned=partially_assigned,
                assigned=assigned,
                lost=lost,
                total_reserve=total_reserve,
            )

        print("Datos de 'ReserveStock' cargados correctamente.")

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

def populate_stock_oblpn(file_path):
    try:
        # Leer la hoja "stock de reserva"
        stock_oblpn_df = pd.read_excel(file_path, sheet_name="existencia")

        for _, row in stock_oblpn_df.iterrows():
            # Extraer datos del Excel
            article = row['PRODUCTO']
            description = row['DESCRIPCIÓN DEL PRODUCTO']
            picking = row['EN PICKING']
            packed = row['EMPACADO']
            loaded = row['CARGADO']
            total_oblpn = row['TOTAL OBLPN']

            # Buscar o crear el producto relacionado
            product, _ = Product.objects.get_or_create(
                product=article,
                defaults={'description': description}
            )

            # Crear el stock de OBLPN (sin evitar duplicados)
            StockOBLPN.objects.create(
                product=product,
                picking=picking,
                packed=packed,
                loaded=loaded,
                total_oblpn=total_oblpn,
            )

        print("Datos de 'StockOBLPN' cargados correctamente.")

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")


def populate_pending(file_path):
    try:
        # Leer la hoja "Pendientes por recibir"
        pendientes_df = pd.read_excel(file_path, sheet_name="Pendientes por recibir detalle")
        for _, row in pendientes_df.iterrows():
            close_dt = row['FECHA DE CIERRE']
            embark = row['CARGA']
            order = row['ORDEN']
            send_dt = row['FECHA DE ENVIO']
            product = row['ITEM']
            description = row['DESCRIPCION']
            quantity = row['CANTIDAD']
            lpn = row['LPN']
            
            # Buscar o crear el producto relacionado
            product, _ = Product.objects.get_or_create(
                product=product,
                defaults={'description': description}
            )

            # Convertir las fechas al formato adecuado
            close_dt = pd.to_datetime(close_dt).date() if pd.notna(close_dt) else None
            send_dt = pd.to_datetime(send_dt).date() if pd.notna(send_dt) else None

            # Crear el stock de Pending (sin evitar duplicados)
            Pending.objects.create(
                close_dt=close_dt,
                embark=embark,
                order=order,
                product=product,
                send_dt=send_dt,
                quantity=quantity,
                lpn=lpn,
                status='En ruta'
            )
        
        print("Datos de 'Pendientes por recibir' cargados correctamente.")


    except Exception as e:
        print(f"Error al insertar: {e}, datos: {order}")

if __name__ == "__main__":
    # Ruta al archivo Excel
    file_path = "DatosFinal.xlsx"      
    populate_products(file_path)
    populate_outgoing_orders(file_path)
    populate_active_stock(file_path)
    populate_reserve_stock(file_path)
    populate_stock_oblpn(file_path)
    populate_pending(file_path)

