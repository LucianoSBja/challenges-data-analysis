import json
from abc import ABC, abstractmethod
from datetime import datetime

class CuentaBancaria(ABC):
    def __init__(self, numero_cuenta, titular, saldo=0):
        self.numero_cuenta = numero_cuenta
        self.titular = titular
        self.saldo = saldo
        self.fecha_apertura = datetime.now().strftime("%Y-%m-%d")

    @abstractmethod
    def depositar(self, monto):
        pass

    @abstractmethod
    def retirar(self, monto):
        pass

    @abstractmethod
    def descripcion(self):
        pass

class CuentaCorriente(CuentaBancaria):
    def __init__(self, numero_cuenta, titular, saldo=0, limite_sobregiro=1000):
        super().__init__(numero_cuenta, titular, saldo)
        self.limite_sobregiro = limite_sobregiro

    def depositar(self, monto):
        self.saldo += monto

    def retirar(self, monto):
        if self.saldo + self.limite_sobregiro >= monto:
            self.saldo -= monto
        else:
            raise ValueError("Fondos insuficientes")

    def descripcion(self):
        return f"Cuenta Corriente - Número: {self.numero_cuenta}, Titular: {self.titular}, Saldo: ${self.saldo}, Límite de sobregiro: ${self.limite_sobregiro}"

class CuentaAhorro(CuentaBancaria):
    def __init__(self, numero_cuenta, titular, saldo=0, tasa_interes=0.01):
        super().__init__(numero_cuenta, titular, saldo)
        self.tasa_interes = tasa_interes

    def depositar(self, monto):
        self.saldo += monto

    def retirar(self, monto):
        if self.saldo >= monto:
            self.saldo -= monto
        else:
            raise ValueError("Fondos insuficientes")

    def aplicar_interes(self):
        interes = self.saldo * self.tasa_interes
        self.saldo += interes

    def descripcion(self):
        return f"Cuenta de Ahorro - Número: {self.numero_cuenta}, Titular: {self.titular}, Saldo: ${self.saldo}, Tasa de interés: {self.tasa_interes*100}%"

class SistemaBancario:
    def __init__(self):
        self.cuentas = []

    def crear_cuenta(self, cuenta):
        self.cuentas.append(cuenta)

    def eliminar_cuenta(self, numero_cuenta):
        self.cuentas = [c for c in self.cuentas if c.numero_cuenta != numero_cuenta]

    def actualizar_cuenta(self, numero_cuenta, **kwargs):
        for cuenta in self.cuentas:
            if cuenta.numero_cuenta == numero_cuenta:
                for key, value in kwargs.items():
                    if hasattr(cuenta, key):
                        setattr(cuenta, key, value)
                return True
        return False

    def buscar_cuenta(self, numero_cuenta):
        return next((c for c in self.cuentas if c.numero_cuenta == numero_cuenta), None)

    def guardar_en_json(self, filename):
        with open(filename, 'w') as f:
            json.dump([{**c.__dict__, 'tipo': c.__class__.__name__} for c in self.cuentas], f, default=str)

    def cargar_desde_json(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.cuentas = []
            for item in data:
                if item['tipo'] == 'CuentaCorriente':
                    self.cuentas.append(CuentaCorriente(item['numero_cuenta'], item['titular'], item['saldo'], item['limite_sobregiro']))
                elif item['tipo'] == 'CuentaAhorro':
                    self.cuentas.append(CuentaAhorro(item['numero_cuenta'], item['titular'], item['saldo'], item['tasa_interes']))

def main():
    sistema = SistemaBancario()

    while True:
        print("\n1. Crear cuenta")
        print("2. Eliminar cuenta")
        print("3. Actualizar cuenta")
        print("4. Buscar cuenta")
        print("5. Depositar")
        print("6. Retirar")
        print("7. Mostrar todas las cuentas")
        print("8. Guardar en JSON")
        print("9. Cargar desde JSON")
        print("10. Salir")

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == '1':
                tipo = input("Tipo de cuenta (1: Corriente, 2: Ahorro): ")
                numero_cuenta = input("Número de cuenta: ")
                titular = input("Titular de la cuenta: ")
                saldo_inicial = float(input("Saldo inicial: "))
                
                if tipo == '1':
                    limite_sobregiro = float(input("Límite de sobregiro: "))
                    cuenta = CuentaCorriente(numero_cuenta, titular, saldo_inicial, limite_sobregiro)
                elif tipo == '2':
                    tasa_interes = float(input("Tasa de interés (decimal): "))
                    cuenta = CuentaAhorro(numero_cuenta, titular, saldo_inicial, tasa_interes)
                else:
                    raise ValueError("Tipo de cuenta no válido")

                sistema.crear_cuenta(cuenta)
                print("Cuenta creada con éxito")

            elif opcion == '2':
                numero_cuenta = input("Número de cuenta a eliminar: ")
                sistema.eliminar_cuenta(numero_cuenta)
                print("Cuenta eliminada con éxito")

            elif opcion == '3':
                numero_cuenta = input("Número de cuenta a actualizar: ")
                cuenta = sistema.buscar_cuenta(numero_cuenta)
                if cuenta:
                    print(f"Actualizando cuenta: {cuenta.descripcion()}")
                    titular = input("Nuevo titular de la cuenta (dejar en blanco para no cambiar): ")
                    saldo = input("Nuevo saldo (dejar en blanco para no cambiar): ")
                    
                    actualizaciones = {}
                    if titular:
                        actualizaciones['titular'] = titular
                    if saldo:
                        actualizaciones['saldo'] = float(saldo)
                    
                    if isinstance(cuenta, CuentaCorriente):
                        limite_sobregiro = input("Nuevo límite de sobregiro (dejar en blanco para no cambiar): ")
                        if limite_sobregiro:
                            actualizaciones['limite_sobregiro'] = float(limite_sobregiro)
                    elif isinstance(cuenta, CuentaAhorro):
                        tasa_interes = input("Nueva tasa de interés (dejar en blanco para no cambiar): ")
                        if tasa_interes:
                            actualizaciones['tasa_interes'] = float(tasa_interes)
                    
                    if sistema.actualizar_cuenta(numero_cuenta, **actualizaciones):
                        print("Cuenta actualizada con éxito")
                    else:
                        print("No se pudo actualizar la cuenta")
                else:
                    print("Cuenta no encontrada")

            elif opcion == '4':
                numero_cuenta = input("Número de cuenta a buscar: ")
                cuenta = sistema.buscar_cuenta(numero_cuenta)
                if cuenta:
                    print(cuenta.descripcion())
                else:
                    print("Cuenta no encontrada")

            elif opcion == '5':
                numero_cuenta = input("Número de cuenta: ")
                monto = float(input("Monto a depositar: "))
                cuenta = sistema.buscar_cuenta(numero_cuenta)
                if cuenta:
                    cuenta.depositar(monto)
                    print("Depósito realizado con éxito")
                else:
                    print("Cuenta no encontrada")

            elif opcion == '6':
                numero_cuenta = input("Número de cuenta: ")
                monto = float(input("Monto a retirar: "))
                cuenta = sistema.buscar_cuenta(numero_cuenta)
                if cuenta:
                    cuenta.retirar(monto)
                    print("Retiro realizado con éxito")
                else:
                    print("Cuenta no encontrada")

            elif opcion == '7':
                for cuenta in sistema.cuentas:
                    print(cuenta.descripcion())

            elif opcion == '8':
                sistema.guardar_en_json("cuentas_bancarias.json")
                print("Cuentas guardadas en JSON")

            elif opcion == '9':
                sistema.cargar_desde_json("cuentas_bancarias.json")
                print("Cuentas cargadas desde JSON")

            elif opcion == '10':
                break

            else:
                print("Opción no válida")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()