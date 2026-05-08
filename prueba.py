def palindromo():

    text = str(input("Ingrese un texto o una palabra: "))

    reverse = text.lower().replace( ' ' , '')

    print("Palabra invertida: " , reverse[::-1])

    if reverse == reverse[::-1]:
        print("Es un palíndromo")
    else:
        print("No es un palíndromo")
    

def calculadora():

    print( " --- Calculadora --- " )
    print("1. Suma , 2. Resta , 3. Multiplicación , 4. División , 5. Salir" )

    while True:

        opcion = int(input("Seleccione una opción: "))

        if opcion == 5:
            print("Saliendo de la calculadora...")
            break

        if opcion in (1,2,3,4):
            num1 = float(input("Ingrese el primer número: "))
            num2 = float(input("Ingrese el segundo número: "))
        if opcion == 1:
            print("Resultado: ", num1 + num2)
        elif opcion == 2:
            print("Resultado: ", num1 - num2)   
        elif opcion == 3:
            print("Resultado: ", num1 * num2)
        elif opcion == 4:
             if num2 != 0:
                print("Resultado: ", round(num1 / num2 , 2))
             else:
                print("Error: No se puede dividir por cero.")
        else:
            print("Opción no válida.")

calculadora()