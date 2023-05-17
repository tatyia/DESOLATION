
from calendar import c
import sqlite3
import pwinput
import pyperclip
print('''

        ██████╗ ███████╗███████╗ ██████╗ ██╗      █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
        ██╔══██╗██╔════╝██╔════╝██╔═══██╗██║     ██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
        ██║  ██║█████╗  ███████╗██║   ██║██║     ███████║   ██║   ██║██║   ██║██╔██╗ ██║
        ██║  ██║██╔══╝  ╚════██║██║   ██║██║     ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
        ██████╔╝███████╗███████║╚██████╔╝███████╗██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
        ╚═════╝ ╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                                                
                                    
                                    Password Manager

                                 Created by Tarek Atyia
''')

text = "Press ENTER to continue"
centered = text.center(90)
input(centered)
print("\n")
connector = sqlite3.connect("users.db")
cursor = connector.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT)""")
connector.commit()


def PURGE():
    print("Are you sure? (THIS WILL DELETE EVERY USERNAME AND PASSWORD)")
    selector = input("Press ENTER to DELETE ALL USERS or 'm' to return to the Main Menu: ")
    if selector == '':
        cursor.execute("DELETE FROM users")
        connector.commit()
        print("All users successfully deleted.")
        whatnext = input("Return to main menu (m) or exit (q): ")
        if whatnext == 'm':
            main_menu()
        if whatnext == 'q':
            exit
    if selector == 'm':
        main_menu()


def display_user():
    search_term = input("Enter username or website you previously saved: ").lower()
    users = retrieve_info()
    found = False
    for user in users:
        if user[0].lower() == search_term or user[1].lower() == search_term:
            print("\n")
            print("USERNAME: ", user[0])
            print("PASSWORD: ", user[1])
            print("\n")
            yesno = input("Copy to clipboard (y/n)?: ")
            print("\n")
            password = user[1]
            if yesno == 'y':
                pyperclip.copy(password)
                print("password copied to clipboard!")
            if yesno == 'n':
                print("password not copied to clipboard")
            found = True
    if not found:
        print("No matching username or website found.")

    selection = input("Return to the main menu (m) or quit (q): ")
    if selection == 'm':
        main_menu()
    if selection == 'q':
        exit


def enter_info():
    username = input("Input a username / website to save: ")
    password = pwinput.pwinput(prompt = "Enter your password: ", mask = "*")
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    connector.commit()
    print('Successfully added username / password combination!')
    yesno = input("Would you like to copy the password to the clipboard? (y/n): ")
    if yesno == 'y':
        pyperclip.copy(password)
        print("Password added to clipboard.")
    if yesno == 'n':
        print("Password not copied to clipboard.")
    
    option = input("Return to the main menu (m) or exit (q)?: ")
    if option == 'm':
        main_menu()
    if option == 'q':
        exit

    print("\n")
def retrieve_info():
    cursor.execute("SELECT username, password FROM users")
    rows = cursor.fetchall()
    return rows

def printing():
    users = retrieve_info()
    if not users:
        print("DATABASE EMPTY")
    else:
        for user in users:
            print("USERNAME / WEBSITE: ", user[0])
            print("PASSWORD: ", user[1])
            print("\n")
    print('\n')
    selection = input("Return to the main menu (m) or quit (q): ")
    if selection == 'm':
        main_menu()
    if selection == 'q':
        exit
    
print("\n")


def delete_user():
    search_username = input("Enter the username you want to delete: ").lower()
    cursor.execute("SELECT id FROM users WHERE LOWER(username) = ?", (search_username,))
    row = cursor.fetchone()
    if row is None:
        print("Username not found.")
    else:
        user_id = row[0]
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        connector.commit()
        print("Username/password combination deleted.")

    selection = input("Return to the main menu (m) or quit (q): ")
    if selection == 'm':
        main_menu()
    if selection == 'q':
        exit


def main_menu():
    text1 = '''

                             __  __       _         __  __                  
                            |  \/  |     (_)       |  \/  |                 
                            | \  / | __ _ _ _ __   | \  / | ___ _ __  _   _ 
                            | |\/| |/ _` | | '_ \  | |\/| |/ _ \ '_ \| | | |
                            | |  | | (_| | | | | | | |  | |  __/ | | | |_| |
                            |_|  |_|\__,_|_|_| |_| |_|  |_|\___|_| |_|\__,_|
                                                        
    '''

    print("=======================================================================================================")
    print(text1)
    text2 = "\033[4m" + 'OPTIONS' + "\033[0m"
    print(text2.center(100))

    print("\n")

    print("1. Add username / password".center(90))
    print("2. Purge all usernames and passwords".center(90))
    print("3. Delete a username / password combination".center(90))
    print("4. Display all SAVED usernames / passwords".center(90))
    print("5. Display a username / password combination".center(90))
    print("6. PRESS 'q' to QUIT".center(90))
    print("\n")
    print("=======================================================================================================")

    print("\n")
    valid_input = ['1', '2', '3', '4', '5', 'q']
    selection = input('Enter an option: ')
    while selection not in valid_input:
        print("Invalid option, try again...")
        print("\n")
        selection = input("Enter an option: ")
    if selection == 'q':
        exit
    if selection == "1":
        print("\n")
        enter_info()
    if selection == '2':
        PURGE()
    if selection == '3':
        print('''''')
        delete_user()
    if selection == '4':
        print('\n')
        printing()
    
    if selection == '5':
        display_user()


main_menu()





connector.commit()
connector.close()