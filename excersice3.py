try:
    username = input("Enter Username: ").strip()
    age_input = input("Enter Age: ").strip()
    
    age = int(age_input)  # This can raise ValueError if not a number

    with open("users.txt", "a") as file:  # "a" = append mode
        file.write(f"{username} - {age}\n")
    
    print("Data saved successfully!")
    
except ValueError:
    print("Error: Age must be a valid number!")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    
finally:
    print("\n--- Saved Users ---")
    try:
        with open("users.txt", "r") as file:
            content = file.read()
            if content.strip():  # If file has content
                print(content.strip())
            else:
                print("No users saved yet.")
    except FileNotFoundError:
        print("No users saved yet. (File not found)")
    
    print("\nSystem complete.")