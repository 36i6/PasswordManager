from tkinter import *
from tkinter import messagebox
import random
import json

# ---------------------------- SAVE PASSWORD ------------------------------- #


def add():
    confirm = False
    website = website_entry.get()
    login = login_entry.get()
    password = password_entry.get()
    if len(website) == 0 or len(login) == 0 or len(password) == 0:
        messagebox.showerror(title="Oops", message="Fill all fields moron!")
    else:
        confirm = messagebox.askokcancel(title=website, message="Are you sure to save?")
    if confirm:
        website_entry.delete(0, END)
        login_entry.delete(0, END)
        password_entry.delete(0, END)
        new_data = {
            website: {
                "login": login,
                "password": password,
            },
        }
        try:
            data_file = open("data.json", mode="r")
            data = json.load(data_file)
            data.update(new_data)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                data = new_data
                json.dump(data, data_file, indent=4)
        except json.decoder.JSONDecodeError:
            with open("data.json", mode="w") as data_file:
                data = new_data
                json.dump(data, data_file, indent=4)
        else:
            data_file.close()
            data_file = open("data.json", mode="w")
            json.dump(data, data_file, indent=4)
            data_file.close()

        messagebox.showinfo(title=website, message="Password successfully added!")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
symbols = ['C', '8', 'b', 'W', 'u', 'm', '7', 'H', 'Z', 'B', '1', 'U', 'z', 'Y', 'h', 'N', 'f', 'x', 'J', 'g', 'V',
           'P', 'p', 'L', 'w', 'e', '%', '#', '2', 'X', '9', 'j', '+', 'q', 'd', 'k', '(', 'n', 'F', ')', 'T', 'E',
           'A', 'G', 'c', 't', 'a', 'I', '&', 'K', '6', 'R', 'l', 'o', 'Q', 'O', 'y', 'v', '*', '!', 'M', '3', '5',
           'S', '$', 's', 'D', '4', 'i', '0', 'r']


def generate_pass():
    generated_password = ''
    for _ in range(12):
        generated_password += random.choice(symbols)
    password_entry.delete(0, END)
    password_entry.clipboard_clear()
    password_entry.clipboard_append(generated_password)


# ---------------------------- SEARCH ------------------------------- #


def search():
    website = website_entry.get()
    try:
        with open("data.json", mode='r') as data_file:
            data = json.load(data_file)
            login = data[website].get("login")
            password = data[website].get("password")
    except FileNotFoundError:
        messagebox.showerror(title="Oops", message="There are no any passwords:)")
    except json.decoder.JSONDecodeError:
        messagebox.showerror(title="Oops", message="There are no any passwords:)")
    except KeyError:
        messagebox.showerror(title="Oops", message=f"No Entries found for {website}")
    else:
        messagebox.showinfo(title=f"{website}", message=f"Login: {login}\nPassword: {password}")


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# Canvas with Logo
canvas_logo = Canvas(width=200, height=200, highlightthickness=0)
image = PhotoImage(file="mypass.png")
canvas_logo.create_image(100, 100, image=image)
canvas_logo.grid(column=1, row=0, padx=(20, 20), pady=(20, 10))

# Website row
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
website_entry = Entry(width=29)
website_entry.grid(column=1, row=1, padx=(0, 2))
website_entry.focus()
search_button = Button(width=16, text="Search", command=search)
search_button.grid(column=2, row=1)

# Email row
login_label = Label(text="Email/Username:")
login_label.grid(column=0, row=2, padx=(0, 5))
login_entry = Entry(width=49)
login_entry.grid(column=1, row=2, columnspan=2)
login_entry.insert(END, "johndoe@email.domain")

# Password row
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
password_entry = Entry(width=29)
password_entry.grid(column=1, row=3, padx=(0, 4))
gen_pass_button = Button(text="Generate Password", command=generate_pass)
gen_pass_button.grid(column=2, row=3)

# Add Password to File
add_button = Button(width=46, text="Add", command=add)
add_button.grid(column=1, row=4, columnspan=2, pady=(1, 0))


window.mainloop()
