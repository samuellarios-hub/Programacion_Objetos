def dividir(a, b):
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b

def calcular_promedio(numeros):
    if len(numeros) == 0:
        raise ValueError("La lista no puede estar vacía")
    return sum(numeros) / len(numeros)

try:
    print(dividir(10, 2))
    print(calcular_promedio([5, 10, 15]))
except ValueError as e:
    print(e)

    