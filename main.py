import os.path
import time
import re
import sqlite3
import pandas

database_path_sys = "animals.db"

class Animal:
    def __init__(self, name: str, animal_type: str, date_of_birth: str, size: str, color: str) -> None:
        '''Base class for the animals in the shelter'''
        self.name = name
        self.animal_type = animal_type
        self.date_of_birth = date_of_birth
        self.size = size
        self.color = color

class ShelterManager:
    def __init__(self, database_path: str) -> None:
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        '''Creates the database'''
        self.cur.execute('''CREATE TABLE IF NOT EXISTS animal_database
                            (name TEXT PRIMARY KEY, animal_type TEXT, date_of_birth TEXT, size TEXT, color TEXT) ''')
        self.conn.commit()
        print("")

    def determine_animal_type(self) -> str:
        '''Used to determine an animal's type in the database.'''
        while True:
                enter_animal_type = input("Enter the animal's type (CAT or DOG): ").upper()
                regex_type_pattern = r"^(cat|dog)$"
                if re.match(regex_type_pattern, enter_animal_type, re.IGNORECASE):
                    print(f"The animal's type is: {enter_animal_type}")
                    break
                else:
                    print("You have to enter one of these two option: CAT or DOG")
        return enter_animal_type
    
    def determine_animal_dob(self) -> str:
        '''Used to determine an animal's date of birth in the database.'''
        while True:
            print("Enter the date of birth (or an estimate),")
            enter_animal_date_of_birth = input("in the following format YYYY-MM-DD: ").upper()
            regex_date_pattern = r"^(\d{4})-(0[1-9]|1[0-2]|[1-9])-([1-9]|0[1-9]|[1-2]\d|3[0-1])$"
            if re.match(regex_date_pattern, enter_animal_date_of_birth):
                break
            else:
                print("You have to enter the DoB in the following format: YYYY-MM-DD")
                print("")
        return enter_animal_date_of_birth

    def determine_animal_size(self) -> str:
        '''Used to determine an animal's size in the database.'''
        while True:
            enter_animal_size = input("Enter the animal's size (SMALL-MEDIUM-LARGE): ").upper()
            regex_size_pattern = r"^(small|medium|large|)$"
            if re.match(regex_size_pattern, enter_animal_size, re.IGNORECASE):
                break
            else:
                print("You have to enter one of these options: SMALL, MEDIUM or LARGE")
        return enter_animal_size

    def add_animal(self):
        '''Used to add an animal into the database.'''
        try:
            enter_animal_name = input("Enter the name of the animal: ").upper()
            enter_animal_type = self.determine_animal_type()
            enter_animal_date_of_birth = self.determine_animal_dob()
            enter_animal_size = self.determine_animal_size()
            enter_animal_color = input("Enter the animal's color: ").upper()
            self.cur.execute("INSERT INTO animal_database VALUES(?, ?, ?, ?, ?)", (enter_animal_name, enter_animal_type, enter_animal_date_of_birth, enter_animal_size, enter_animal_color))
            self.conn.commit()
            print("")
            print(f"You have just added {enter_animal_name} to the database.")
            time.sleep(1)
            print(f"Printing {enter_animal_name}'s details:")
            time.sleep(1)
            self.print_details_of_one_animal(enter_animal_name)
            time.sleep(1)
            print("")
        except sqlite3.IntegrityError:
            print("")
            print("ERROR:")
            print("These database uses the animal's name as primary key.")
            print("Therefore only one animal can hold a name, each name must be unique!")
            print("")

    def print_all_animals_basic_details(self):
        '''Prints out the basic details of all animals from the database.'''
        print("")
        try:
            print("BASIC DETAILS OF ALL THE ANIMALS IN THE DATABASE:")
            print("")
            animals = {}
            self.cur.execute("SELECT * FROM animal_database")
            rows = self.cur.fetchall()
            for animal in rows:
                animals[animal[0]] = [animal[1], animal[2], animal[3], animal[4]]
            animal_data = pandas.DataFrame(animals).T
            animal_data.reset_index(inplace=True)
            animal_data.columns = ["---NAME---", "--TYPE--", "--DATE OF BIRTH--", "--Size--", "--Color--"]
            print(animal_data)
            print("")
        except Exception:
            print("")
            print("There was an error. There are no animals in the database.")
            print("")

    def print_details_of_one_animal(self, animal_name: str):
        '''Prints out the all the details of given animal.'''
        print("")
        animal_query = ("SELECT * FROM animal_database WHERE name = ?")
        self.cur.execute(animal_query, (animal_name,))
        rows = self.cur.fetchall()
        if not rows:
            print("")
            print("The system was not able to find the animal you are looking for.")
            print("Please check if you provided the correct name.")
            print("")
        else:
            print("")
            print("-------------------------------------------")
            print(f"Details of {animal_name}")
            print("-------------------------------------------")
            for row in rows:
                print("Name = ", row[0])
                time.sleep(.5)
                print("Type  = ", row[1])
                time.sleep(.5)
                print("Date of Birth  = ", row[2])
                time.sleep(.5)
                print("Size  = ", row[3])
                time.sleep(.5)
                print("Color  = ", row[4])
                time.sleep(.5)
            print("-------------------------------------------")
            print(f"------End of {animal_name}'s details--------")
            print("-------------------------------------------")
            print("")
            print("")
            print("Loading the main menu...")
            time.sleep(2)

    def change_name_of_animal(self, animal_name: str):
        '''Used to change the name of an animal'''
        try:
            print("")
            new_animal_name = input(f"What's the new name of {animal_name}?").upper()
            name_change_query = ("UPDATE animal_database SET name = ? WHERE name =?")
            self.cur.execute(name_change_query, (new_animal_name, animal_name))
            self.conn.commit()
            time.sleep(1)
            print(f"{animal_name}'s details has been changed to {new_animal_name}.")
            time.sleep(1)
            print(f"Printing {new_animal_name}'s details:")
            time.sleep(2)
            self.print_details_of_one_animal(new_animal_name)
        except sqlite3.IntegrityError:
            print("")
            print("ERROR:")
            print("These database uses the animal's name as primary key.")
            print("Therefore only one animal can hold a name, each name must be unique!")
            print("")

    def change_type_of_animal(self, animal_name: str):
        '''Used to change the type of an animal'''
        print("")
        new_animal_type = self.determine_animal_type()
        type_change_query = ("UPDATE animal_database SET animal_type = ? WHERE name =?")
        self.cur.execute(type_change_query, (new_animal_type, animal_name))
        self.conn.commit()
        time.sleep(1)
        print(f"{animal_name}'s details has been changed. Type: {new_animal_type}.")
        time.sleep(1)
        print(f"Printing {animal_name}'s details:")
        time.sleep(2)
        self.print_details_of_one_animal(animal_name)
    
    def change_dob_of_animal(self, animal_name: str):
        '''Used to change the date of birth of an animal'''
        print("")
        new_animal_dob = self.determine_animal_dob()
        dob_change_query = ("UPDATE animal_database SET date_of_birth = ? WHERE name =?")
        self.cur.execute(dob_change_query, (new_animal_dob, animal_name))
        self.conn.commit()
        time.sleep(1)
        print(f"{animal_name}'s date of birth has been changed to {new_animal_dob}.")
        time.sleep(1)
        print(f"Printing {animal_name}'s details:")
        time.sleep(2)
        self.print_details_of_one_animal(animal_name)

    def change_size_of_animal(self, animal_name: str):
        '''Used to change the size of an animal'''
        print("")
        new_animal_size = self.determine_animal_size()
        size_change_query = ("UPDATE animal_database SET size = ? WHERE name =?")
        self.cur.execute(size_change_query, (new_animal_size, animal_name))
        self.conn.commit()
        time.sleep(1)
        print(f"{animal_name}'s size has been changed to {new_animal_size}.")
        time.sleep(1)
        print(f"Printing {animal_name}'s details:")
        time.sleep(2)
        self.print_details_of_one_animal(animal_name)

    def change_color_of_animal(self, animal_name: str):
        '''Used to change the color of an animal'''
        print("")
        new_animal_color = input(f"What is the correct color of {animal_name}?").upper()
        color_change_query = ("UPDATE animal_database SET color = ? WHERE name =?")
        self.cur.execute(color_change_query, (new_animal_color, animal_name))
        self.conn.commit()
        time.sleep(1)
        print(f"{animal_name}'s color has been changed to {new_animal_color}.")
        time.sleep(1)
        print(f"Printing {animal_name}'s details:")
        time.sleep(2)
        self.print_details_of_one_animal(animal_name)

    def check_animal_in_db(self, animal_name):
        animal_query = ("SELECT * FROM animal_database WHERE name = ?")
        self.cur.execute(animal_query, (animal_name,))
        rows = self.cur.fetchall()
        if not rows:
            return True
        else:
            return False

    def update_animal_information(self):
        '''Updates to change the color of an animal'''
        print("")
        self.print_all_animals_basic_details()
        print("")
        animal_name = input("Which animal's information would you like to change? Enter the animal's name: ").upper()
        animal_query = ("SELECT * FROM animal_database WHERE name = ?")
        self.cur.execute(animal_query, (animal_name,))
        rows = self.cur.fetchall()
        if not rows:
            print("")
            print("There was a problem!")
            print(f"There is no {animal_name} in the database. Enter a correct one.")
            print("")
        else:
            print("")
            print(f"What data would you like to change on {animal_name} profile?")
            print("{:<15} {:<15} {:<15} {:<15} {:<15}".format("1. NAME", "2. TYPE", "3. DATE OF BIRTH", "4. SIZE", "5. COLOR"))
            select_data = input("Enter the data's number, that you would like to change.")
            match select_data:
                case "1":
                    self.change_name_of_animal(animal_name)
                case "2":
                    self.change_type_of_animal(animal_name)
                case "3":
                    self.change_dob_of_animal(animal_name)
                case "4":
                    self.change_size_of_animal(animal_name)
                case "5":
                    self.change_color_of_animal(animal_name)

    def delete_animal(self, animal_name: str):
        '''Deletes an animal from the database'''
        print("")
        print(f"You are going to delete all details of {animal_name}")
        animal_query = ("SELECT * FROM animal_database WHERE name = ?")
        self.cur.execute(animal_query, (animal_name,))
        rows = self.cur.fetchall()
        if not rows:
            print("")
            print("The system was not able to find the animal you are looking for.")
            print("Please check if you provided the correct name.")
            print("")
        else:
            print("Are you sure about this? You can't revert these changes")
            make_sure = input(f"Type DELETE (in uppercase) if you really would like to delete {animal_name} from the database: ")
            if make_sure == "DELETE":
                delete_query = ("DELETE FROM animal_database WHERE name = ?")
                self.cur.execute(delete_query, (animal_name,))
                self.conn.commit()
                print("")
                print(f"{animal_name} has been deleted from the database.")
                print("")
            else:
                print(f"{animal_name} was not deleted from the database.")
                print("")
                print("You have to enter DELETE in all uppercase, if you wish to delete an animal.")
                print("")
                time.sleep(1)

    def main_menu(self):
        '''Option selection screen'''
        print("Welcome to our ANIMAL SHELTER management system!")
        time.sleep(.5)
        print("------------------------------------------------")
        print("Type '1' to enter a newly rescued animal.")
        time.sleep(.5)
        print("Type '2' to print every animal's basic details.")
        time.sleep(.5)
        print("Type '3' to print all details of an animal. You can search by animal's name.")
        time.sleep(.5)
        print("Type '4' to change the details of an animal.")
        time.sleep(.5)
        print("Type '5' to delete an animal from the database")
        time.sleep(.5)
        print("Type '10' to exit the program.")
        time.sleep(.5)
        select_menu = input("What would you like to do? ")
        match select_menu:
            case "1":
                self.add_animal()
            case "2":
                self.print_all_animals_basic_details()
            case "3":
                animal_name = input("Which animal would you like to get more information? Please enter the name of the animal: ").upper()
                self.print_details_of_one_animal(animal_name)
            case "4":
                self.update_animal_information()
            case "5":
                print("")
                animal_name = input("Which animal would you like to delete? Please enter the name of the animal: ").upper()
                self.delete_animal(animal_name)
            case "10":
                self.conn.close()
                exit(0)

if __name__ == "__main__":
    while True:
        if os.path.isfile(database_path_sys) is False:
            print("Welcome to our ANIMAL SHELTER management system!")
            time.sleep(.5)
            print("------------------------------------------------")
            print("")
            print("Looks like you haven't created a database for your shelter yet.")
            print("What would you like to do?")
            print("Type '0' to create a database.")
            time.sleep(.5)
            print("Type '10' to exit the program")
            time.sleep(.5)
            select_menu = input("Enter 0 or 10: ")
            match select_menu:
                case "0":
                    print("")
                    print("You have created your database.")
                    time.sleep(0.5)
                    shelter_manager = ShelterManager("animals.db")
                case "10":
                    exit(0)
                case _:
                    print("")
                    print("Invalid option, try again.")
                    print("")
                    continue
        else:
            shelter_manager = ShelterManager("animals.db")
            while True:
                shelter_manager.main_menu()
