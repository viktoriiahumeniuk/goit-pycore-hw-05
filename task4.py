def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as error:
            return str(error)
        except IndexError:
            return "Enter user name."

    return inner


def parse_input(user_input):
    parts = user_input.lower().split()
    command, *args = parts or [""]
    return command, args


@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")

    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")

    name, phone = args

    if name not in contacts:
        raise KeyError(name)

    contacts[name] = phone
    return "Contact updated."


@input_error
def show_contact(args, contacts):
    name = args[0]

    if len(args) > 1:
        raise ValueError("Enter only one user name.")

    return contacts[name]


@input_error
def show_all_contacts(contacts):
    if not contacts:
        return "No contacts found."

    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


@input_error
def handle_command(command, args, contacts):
    if command in ("hello", "all", "exit", "close") and args:
        raise ValueError("This command does not take arguments.")

    if command in ("exit", "close"):
        return None
    if command == "hello":
        return "How can I help you?"
    if command == "add":
        return add_contact(args, contacts)
    if command == "change":
        return change_contact(args, contacts)
    if command == "phone":
        return show_contact(args, contacts)
    if command == "all":
        return show_all_contacts(contacts)

    raise ValueError("Invalid command.")


def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        response = handle_command(command, args, contacts)

        if response is None:
            print("Good bye!")
            break

        print(response)


if __name__ == "__main__":
    main()