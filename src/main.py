import os
from service import create_user, login, consultar_clima, ver_historial_personal, estadisticas_globales, consejo_ia, acerca_de


def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\n=== Menú ===')
    print('1) Crear usuario')
    print('2) Iniciar sesión')
    print('3) Salir')


userid = None
name = None
password = None
logged_in_user = None


def main():
    global userid, name, password, logged_in_user
    while True:
        if not logged_in_user:
            menu()
            choice = input('Elija una opción: ').strip()
            if choice == '1':
                user = create_user()
                if user:
                    userid, name, password = user['userid'], user['name'], user['password']
                    logged_in_user = True
            elif choice == '2':
                user = login()
                if user:
                    userid, name, password = user['userid'], user['name'], user['password']
                    logged_in_user = True
                    print(f"Sesión iniciada como: {name}")
            elif choice == '3':
                print('Adiós')
                break
            else:
                print('Opción inválida')
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'\n=== GuardiánClima ITBA — {name} ===')
            print('1) Consultar clima actual')
            print('2) Ver mi historial personal por ciudad')
            print('3) Estadísticas globales de uso')
            print('4) Consejo IA: ¿Cómo me visto hoy?')
            print('5) Acerca de...')
            print('6) Cerrar sesión')
            choice = input('Elija una opción: ').strip()
            if choice == '1':
                consultar_clima(name)
            elif choice == '2':
                ver_historial_personal(name)
            elif choice == '3':
                estadisticas_globales()
            elif choice == '4':
                consejo_ia(name)
            elif choice == '5':
                acerca_de()
            elif choice == '6':
                userid = None
                name = None
                password = None
                logged_in_user = None
                print('Sesión cerrada.')
            else:
                print('Opción inválida')


if __name__ == '__main__':
    main()
