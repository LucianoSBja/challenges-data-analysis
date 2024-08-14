import json
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Tarea(ABC):
    def __init__(self, descripcion, fecha_vencimiento, estado="pendiente"):
        self.descripcion = descripcion
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado

    @abstractmethod
    def actualizar_estado(self):
        pass

    @abstractmethod
    def descripcion_completa(self):
        pass

class TareaSimple(Tarea):
    def __init__(self, descripcion, fecha_vencimiento, prioridad, estado="pendiente"):
        super().__init__(descripcion, fecha_vencimiento, estado)
        self.prioridad = prioridad

    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def descripcion_completa(self):
        return f"Tarea Simple: {self.descripcion}, Vencimiento: {self.fecha_vencimiento}, Estado: {self.estado}, Prioridad: {self.prioridad}"

class TareaRecurrente(Tarea):
    def __init__(self, descripcion, fecha_vencimiento, frecuencia, estado="pendiente"):
        super().__init__(descripcion, fecha_vencimiento, estado)
        self.frecuencia = frecuencia

    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        if nuevo_estado == "completada":
            self.fecha_vencimiento = (datetime.strptime(self.fecha_vencimiento, "%Y-%m-%d") + timedelta(days=self.frecuencia)).strftime("%Y-%m-%d")
            self.estado = "pendiente"

    def descripcion_completa(self):
        return f"Tarea Recurrente: {self.descripcion}, Vencimiento: {self.fecha_vencimiento}, Estado: {self.estado}, Frecuencia: cada {self.frecuencia} días"

class SistemaTareas:
    def __init__(self):
        self.tareas = []

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

    def eliminar_tarea(self, indice):
        if 0 <= indice < len(self.tareas):
            del self.tareas[indice]
        else:
            raise ValueError("Índice de tarea no válido")

    def actualizar_tarea(self, indice, **kwargs):
        if 0 <= indice < len(self.tareas):
            tarea = self.tareas[indice]
            for key, value in kwargs.items():
                setattr(tarea, key, value)
        else:
            raise ValueError("Índice de tarea no válido")

    def buscar_tarea(self, indice):
        if 0 <= indice < len(self.tareas):
            return self.tareas[indice]
        else:
            return None

    def guardar_en_json(self, filename):
        with open(filename, 'w') as f:
            json.dump([{**t.__dict__, 'tipo': t.__class__.__name__} for t in self.tareas], f)

    def cargar_desde_json(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.tareas = []
            for item in data:
                if item['tipo'] == 'TareaSimple':
                    self.tareas.append(TareaSimple(item['descripcion'], item['fecha_vencimiento'], item['prioridad'], item['estado']))
                elif item['tipo'] == 'TareaRecurrente':
                    self.tareas.append(TareaRecurrente(item['descripcion'], item['fecha_vencimiento'], item['frecuencia'], item['estado']))

def main():
    sistema = SistemaTareas()

    while True:
        print("\n1. Agregar tarea")
        print("2. Eliminar tarea")
        print("3. Actualizar tarea")
        print("4. Buscar tarea")
        print("5. Mostrar todas las tareas")
        print("6. Guardar en JSON")
        print("7. Cargar desde JSON")
        print("8. Salir")

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == '1':
                tipo = input("Tipo de tarea (1: Simple, 2: Recurrente): ")
                descripcion = input("Descripción de la tarea: ")
                fecha_vencimiento = input("Fecha de vencimiento (YYYY-MM-DD): ")
                
                if tipo == '1':
                    prioridad = input("Prioridad (alta/media/baja): ")
                    tarea = TareaSimple(descripcion, fecha_vencimiento, prioridad)
                elif tipo == '2':
                    frecuencia = int(input("Frecuencia en días: "))
                    tarea = TareaRecurrente(descripcion, fecha_vencimiento, frecuencia)
                else:
                    raise ValueError("Tipo de tarea no válido")

                sistema.agregar_tarea(tarea)
                print("Tarea agregada con éxito")

            elif opcion == '2':
                indice = int(input("Índice de la tarea a eliminar: "))
                sistema.eliminar_tarea(indice)
                print("Tarea eliminada con éxito")

            elif opcion == '3':
                indice = int(input("Índice de la tarea a actualizar: "))
                nuevo_estado = input("Nuevo estado (pendiente/en progreso/completada): ")
                sistema.tareas[indice].actualizar_estado(nuevo_estado)
                print("Tarea actualizada con éxito")

            elif opcion == '4':
                indice = int(input("Índice de la tarea a buscar: "))
                tarea = sistema.buscar_tarea(indice)
                if tarea:
                    print(tarea.descripcion_completa())
                else:
                    print("Tarea no encontrada")

            elif opcion == '5':
                for i, tarea in enumerate(sistema.tareas):
                    print(f"{i}: {tarea.descripcion_completa()}")

            elif opcion == '6':
                sistema.guardar_en_json("tareas.json")
                print("Tareas guardadas en JSON")

            elif opcion == '7':
                sistema.cargar_desde_json("tareas.json")
                print("Tareas cargadas desde JSON")

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