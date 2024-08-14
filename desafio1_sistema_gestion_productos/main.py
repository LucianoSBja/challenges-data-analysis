import json
from abc import ABC, abstractmethod

class Producto(ABC):
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    @abstractmethod
    def descripcion(self):
        pass

class ProductoElectronico(Producto):
    def __init__(self, nombre, precio, cantidad, marca, garantia):
        super().__init__(nombre, precio, cantidad)
        self.marca = marca
        self.garantia = garantia

    def descripcion(self):
        return f"Producto electrónico: {self.nombre}, Marca: {self.marca}, Garantía: {self.garantia} meses"

class ProductoAlimenticio(Producto):
    def __init__(self, nombre, precio, cantidad, fecha_caducidad):
        super().__init__(nombre, precio, cantidad)
        self.fecha_caducidad = fecha_caducidad

    def descripcion(self):
        return f"Producto alimenticio: {self.nombre}, Fecha de caducidad: {self.fecha_caducidad}"

class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def eliminar_producto(self, nombre):
        self.productos = [p for p in self.productos if p.nombre != nombre]

    def actualizar_producto(self, nombre, **kwargs):
        for producto in self.productos:
            if producto.nombre == nombre:
                for key, value in kwargs.items():
                    setattr(producto, key, value)

    def buscar_producto(self, nombre):
        return next((p for p in self.productos if p.nombre == nombre), None)

    def guardar_en_json(self, filename):
        with open(filename, 'w') as f:
            json.dump([p.__dict__ for p in self.productos], f)

    def cargar_desde_json(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.productos = []
            for item in data:
                if 'marca' in item:
                    self.productos.append(ProductoElectronico(**item))
                elif 'fecha_caducidad' in item:
                    self.productos.append(ProductoAlimenticio(**item))

def main():
    inventario = Inventario()

    while True:
        print("\n1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto")
        print("5. Mostrar todos los productos")
        print("6. Guardar en JSON")
        print("7. Cargar desde JSON")
        print("8. Salir")

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == '1':
                tipo = input("Tipo de producto (1: Electrónico, 2: Alimenticio): ")
                nombre = input("Nombre: ")
                precio = float(input("Precio: "))
                cantidad = int(input("Cantidad: "))

                if tipo == '1':
                    marca = input("Marca: ")
                    garantia = int(input("Garantía (meses): "))
                    producto = ProductoElectronico(nombre, precio, cantidad, marca, garantia)
                elif tipo == '2':
                    fecha_caducidad = input("Fecha de caducidad: ")
                    producto = ProductoAlimenticio(nombre, precio, cantidad, fecha_caducidad)
                else:
                    raise ValueError("Tipo de producto no válido")

                inventario.agregar_producto(producto)
                print("Producto agregado con éxito")

            elif opcion == '2':
                nombre = input("Nombre del producto a eliminar: ")
                inventario.eliminar_producto(nombre)
                print("Producto eliminado con éxito")

            elif opcion == '3':
                nombre = input("Nombre del producto a actualizar: ")
                precio = float(input("Nuevo precio: "))
                cantidad = int(input("Nueva cantidad: "))
                inventario.actualizar_producto(nombre, precio=precio, cantidad=cantidad)
                print("Producto actualizado con éxito")

            elif opcion == '4':
                nombre = input("Nombre del producto a buscar: ")
                producto = inventario.buscar_producto(nombre)
                if producto:
                    print(producto.descripcion())
                else:
                    print("Producto no encontrado")

            elif opcion == '5':
                for producto in inventario.productos:
                    print(producto.descripcion())

            elif opcion == '6':
                inventario.guardar_en_json("inventario.json")
                print("Inventario guardado en JSON")

            elif opcion == '7':
                inventario.cargar_desde_json("inventario.json")
                print("Inventario cargado desde JSON")

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