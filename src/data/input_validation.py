from string import ascii_letters
import re

def validation():
    print("Please enter name, age and email.")
   
    while True:
        name = input("Name: ")
        valid = True
        allowed_chars = ascii_letters + "åäöÅÄÖ"
   
        if name == "-1":
            break

        for character in name:
            if character not in allowed_chars:
                valid = False
        if not valid:
            print("Please enter a valid name containing only alphabetical characters")
            continue

        if name == "":
            print("Please enter a name")
            continue
   
        while True:
            try:
                age = int(input("Age: "))
                if age < 1 or age > 120:
                    print("Please enter age between 1 and 120.")
                    continue
                break  # Valid age entered, break the loop
            except ValueError:
                print("Please enter a valid number for age.")

        while True:
            email = input("Email: ")
            # Basic email regex pattern
            email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"

            if re.match(email_pattern, email):
                break  # Valid email, break the loop
            else:
                print("Please enter a valid email address.")

        print(f"\nName: {name}\nAge: {age}\nEmail: {email}")
        print("Thank you!\n")
        break  # Ends the function after successful input

 
validation()