import json
from abc import ABC, abstractmethod
from datetime import datetime

class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def to_dict(self):
        return {"nombre": self.nombre, "precio": self.precio}

class Venta(ABC):
    def __init__(self, fecha, cliente, productos):
        self.fecha = fecha
        self.cliente = cliente
        self.productos = productos

    @abstractmethod
    def calcular_total(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass

class VentaOnline(Venta):
    def __init__(self, fecha, cliente, productos, direccion_envio):
        super().__init__(fecha, cliente, productos)
        self.direccion_envio = direccion_envio

    def calcular_total(self):
        return sum(producto.precio for producto in self.productos) + 5  # Costo de envío

    def descripcion(self):
        return f"Venta Online - Fecha: {self.fecha}, Cliente: {self.cliente}, Total: ${self.calcular_total()}, Envío a: {self.direccion_envio}"

class VentaLocal(Venta):
    def __init__(self, fecha, cliente, productos, sucursal):
        super().__init__(fecha, cliente, productos)
        self.sucursal = sucursal

    def calcular_total(self):
        return sum(producto.precio for producto in self.productos)

    def descripcion(self):
        return f"Venta Local - Fecha: {self.fecha}, Cliente: {self.cliente}, Total: ${self.calcular_total()}, Sucursal: {self.sucursal}"

class SistemaVentas:
    def __init__(self):
        self.ventas = []

    def agregar_venta(self, venta):
        self.ventas.append(venta)

    def eliminar_venta(self, indice):
        if 0 <= indice < len(self.ventas):
            del self.ventas[indice]
        else:
            raise ValueError("Índice de venta no válido")

    def actualizar_venta(self, indice, **kwargs):
        if 0 <= indice < len(self.ventas):
            venta = self.ventas[indice]
            for key, value in kwargs.items():
                setattr(venta, key, value)
        else:
            raise ValueError("Índice de venta no válido")

    def buscar_venta(self, indice):
        if 0 <= indice < len(self.ventas):
            return self.ventas[indice]
        else:
            return None

    def guardar_en_json(self, filename):
        def venta_to_dict(venta):
            venta_dict = venta.__dict__.copy()
            venta_dict['productos'] = [p.to_dict() for p in venta.productos]
            venta_dict['tipo'] = venta.__class__.__name__
            return venta_dict

        with open(filename, 'w') as f:
            json.dump([venta_to_dict(v) for v in self.ventas], f, default=str)

    def cargar_desde_json(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.ventas = []
            for item in data:
                productos = [Producto(**p) for p in item['productos']]
                if item['tipo'] == 'VentaOnline':
                    self.ventas.append(VentaOnline(item['fecha'], item['cliente'], productos, item['direccion_envio']))
                elif item['tipo'] == 'VentaLocal':
                    self.ventas.append(VentaLocal(item['fecha'], item['cliente'], productos, item['sucursal']))

def main():
    sistema = SistemaVentas()

    while True:
        print("\n1. Agregar venta")
        print("2. Eliminar venta")
        print("3. Actualizar venta")
        print("4. Buscar venta")
        print("5. Mostrar todas las ventas")
        print("6. Guardar en JSON")
        print("7. Cargar desde JSON")
        print("8. Salir")

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == '1':
                tipo = input("Tipo de venta (1: Online, 2: Local): ")
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cliente = input("Nombre del cliente: ")
                
                productos = []
                while True:
                    nombre_producto = input("Nombre del producto (o 'fin' para terminar): ")
                    if nombre_producto.lower() == 'fin':
                        break
                    precio_producto = float(input("Precio del producto: "))
                    productos.append(Producto(nombre_producto, precio_producto))

                if tipo == '1':
                    direccion_envio = input("Dirección de envío: ")
                    venta = VentaOnline(fecha, cliente, productos, direccion_envio)
                elif tipo == '2':
                    sucursal = input("Sucursal: ")
                    venta = VentaLocal(fecha, cliente, productos, sucursal)
                else:
                    raise ValueError("Tipo de venta no válido")

                sistema.agregar_venta(venta)
                print("Venta agregada con éxito")

            elif opcion == '2':
                indice = int(input("Índice de la venta a eliminar: "))
                sistema.eliminar_venta(indice)
                print("Venta eliminada con éxito")

            elif opcion == '3':
                indice = int(input("Índice de la venta a actualizar: "))
                cliente = input("Nuevo nombre del cliente: ")
                sistema.actualizar_venta(indice, cliente=cliente)
                print("Venta actualizada con éxito")

            elif opcion == '4':
                indice = int(input("Índice de la venta a buscar: "))
                venta = sistema.buscar_venta(indice)
                if venta:
                    print(venta.descripcion())
                else:
                    print("Venta no encontrada")

            elif opcion == '5':
                for i, venta in enumerate(sistema.ventas):
                    print(f"{i}: {venta.descripcion()}")

            elif opcion == '6':
                sistema.guardar_en_json("ventas.json")
                print("Ventas guardadas en JSON")

            elif opcion == '7':
                sistema.cargar_desde_json("ventas.json")
                print("Ventas cargadas desde JSON")

            elif opcion == '8':
                break

            else:
                print("Opción no válida")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()