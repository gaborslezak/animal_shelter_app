import sqlite3
import pandas
import time

class Animal:
    def __init__(self, name: str, animal_type: str, date_of_birth: str, size: str, color: str) -> None:
        self.name = name
        self.animal_type = animal_type
        self.date_of_birth = date_of_birth
        self.size = size
        self.color = color

class ShelterManager:
    def __init__(self, database_path) -> None:
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS animal_database
                            (name TEXT, animal_type TEXT, date_of_birth TEXT, size TEXT, color TEXT) ''')
        self.conn.commit()

    def add_animal(self, animal):
        self.cur.execute("INSERT INTO animal_database VALUES(?, ?, ?, ?, ?)", (animal.name, animal.animal_type, animal.date_of_birth, animal.size, animal.color) )
        self.conn.commit()

    def print_all_animals_basic_details(self):
        animals = {}
        self.cur.execute("SELECT * FROM animal_database")
        rows = self.cur.fetchall()
        print(rows)
        for animal in rows:
            animals[animal[0]] = [animal[1], animal[2], animal[3], animal[4]]
        animal_data = pandas.DataFrame(animals).T
        animal_data.reset_index(inplace=True)
        animal_data.columns = ["---NAME---", "--TYPE--", "--DATE OF BIRTH--", "--Size--", "--Color--"]
        print(animal_data)

    def print_details_of_one_animal(self, animal_name):
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
            print(rows)
            for row in rows:
                print("Name = ", row[0])
                print("Type  = ", row[1])
                print("Date of Birth  = ", row[2])
                print("Size  = ", row[3])
                print("Color  = ", row[4])
            print("-------------------------------------------")
            print(f"------End of {animal_name} details--------")
            print("-------------------------------------------")
            print("")
            print("")

    def change_name_of_animal(self, animal_name):
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

    def change_type_of_animal(self, animal_name):
        print("")
        new_animal_type = input(f"What's the type of the {animal_name}?").upper()
        type_change_query = ("UPDATE animal_database SET animal_type = ? WHERE name =?")
        self.cur.execute(type_change_query, (new_animal_type, animal_name))
        self.conn.commit()
        time.sleep(1)
        print(f"{animal_name}'s details has been changed. Type: {new_animal_type}.")
        time.sleep(1)
        print(f"Printing {animal_name}'s details:")
        time.sleep(2)
        self.print_details_of_one_animal(animal_name)
    
    def change_dob_of_animal(self, animal_name):
        print("")
        new_animal_dob = input(f"What is correct the date of birth of {animal_name}").upper()
        dob_change_query = ("UPDATE animal_database SET date_of_birth = ? WHERE name =?")
        self.cur.execute(dob_change_query, (new_animal_dob, animal_name))
        self.conn.commit()
        time.sleep(1)
        print(f"{animal_name}'s date of birth has been changed to {new_animal_dob}.")
        time.sleep(1)
        print(f"Printing {animal_name}'s details:")
        time.sleep(2)
        self.print_details_of_one_animal(animal_name)

    def update_animal_information(self):
        print("")
        self.print_all_animals_basic_details()
        animal_name = input("Which animal's information would you like to change?").upper()
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

    def main_menu(self):
        print("Welcome to our ANIMAL SHELTER management system!")
        print("------------------------------------------------")
        print("Type '0' to create a database.")
        print("Type '1' to enter a newly rescued animal.")
        print("Type '2' to print every animal's basic details.")
        print("Type '3' to print all details of an animal. You can search by animal's name.")
        print("Type '4' to change the details of an animal.")
        print("Type '10' to exit the program.")
        select_menu = input("What would you like to do? ")
        match select_menu:
            case "0":
                self.create_table()
            case "1":
                enter_animal_name = input("Enter the name of the animal: ").upper()
                enter_animal_type = input("Enter the animal's type (CAT or DOG): ").upper()
                enter_animal_date_of_birth = input("Enter the date of birth (or an estimate): ").upper()
                enter_animal_size = input("Enter the animal's size (SMALL-MEDIUM-LARGE): ").upper()
                enter_animal_color = input("Enter the animal's color: ").upper()
                given_animal = Animal(enter_animal_name, enter_animal_type, enter_animal_date_of_birth, enter_animal_size, enter_animal_color)
                self.add_animal(given_animal)
            case "2":
                self.print_all_animals_basic_details()
            case "3":
                animal_name = input("Which animal would you like to get more information? Please enter the name of the animal.").upper()
                self.print_details_of_one_animal(animal_name)
            case "4":
                self.update_animal_information()
            case "10":
                exit(0)

if __name__ == "__main__":
    shelter_manager = ShelterManager("animals.db")
    while True:
        shelter_manager.main_menu()