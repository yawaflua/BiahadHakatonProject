from models.Apps import HousingApp


def main():
    app = HousingApp()

    while True:
        print("\n1. Register as Volunteer")
        print("2. Register as Evacuee")
        print("3. Add Apartment")
        print("4. Search Apartments")
        print("5. Exit")

        choice = input("Choose option: ")

        if choice == '1':
            name = input("Full name: ")
            contact = input("Contact info: ")
            app.register_volunteer(name, contact)
            print("Volunteer registered successfully!")

        elif choice == '2':
            name = input("Full name: ")
            contact = input("Contact info: ")
            region = input("Region (north/south): ").lower()
            how_much_peoples = int(input("How many people in family?: "))
            app.register_evacuee(name, contact, region, how_much_peoples)
            print("Evacuee registered successfully!")

        elif choice == '3':
            name = input("Volunteer name: ")
            volunteer = next((v for v in app.volunteers if v.name == name), None)
            if volunteer:
                location = input("Apartment location: ")
                rooms = int(input("Number of rooms: "))
                has_mamad = input("Has safe room? (yes/no): ").lower() == 'yes'
                price = input("Payment terms: ")
                regions = input("Accepts residents from (north/south/all): ")
                app.add_apartment(volunteer.name, location, rooms, has_mamad, price, regions)
                print("Apartment added to system!")

        elif choice == '4':
            name = input("Evacuee name: ")
            evacuee = next((e for e in app.needys if e.name == name), None)
            if evacuee:
                apartments = app.search_apartments(evacuee.name)
                if apartments:
                    print("\nAvailable apartments:")
                    for i, apt in enumerate(apartments, 1):
                        print(f"{i}. {apt}")
                    selection = int(input("Select apartment (number): ")) - 1
                    if app.book_apartment(apartments[selection].id, evacuee.name):
                        print("Apartment booked successfully!")
                    else:
                        print("Apartment no longer available")
                else:
                    print("No matching apartments found")

        elif choice == '5':
            print("Thank you for using the Housing Match App!")
            break
        else:
            print("Write, please only numbers, provided in start message")


if __name__ == "__main__":
    main()
