import sqlite3
import pandas

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
        animal_data.columns = ["Animal\'s name", "Animal's Type", "Date of Birth", "Size", "Color"]
        print(animal_data)

    def main_menu(self):
        print("Welcome to our ANIMAL SHELTER management system!")
        print("------------------------------------------------")
        print("Type '0' to create a database.")
        print("Type '1' to enter a newly rescued animal.")
        print("Type '2' to print every animal's basic details.")
        print("Type '10' to exit the program.")
        select_menu = input("What would you like to do? ")
        match select_menu:
            case "0":
                self.create_table()
            case "1":
                enter_animal_name = input("Enter the name of the animal: ")
                enter_animal_type = input("Enter the animal's type (CAT or DOG): ")
                enter_animal_date_of_birth = input("Enter the date of birth (or an estimate): ")
                enter_animal_size = input("Enter the animal's size (SMALL-MEDIUM-LARGE): ")
                enter_animal_color = input("Enter the animal's color: ")
                given_animal = Animal(enter_animal_name, enter_animal_type, enter_animal_date_of_birth, enter_animal_size, enter_animal_color)
                self.add_animal(given_animal)
            case "2":
                self.print_all_animals_basic_details()
            case "10":
                exit(0)

if __name__ == "__main__":
    shelter_manager = ShelterManager("animals.db")
    while True:
        shelter_manager.main_menu()