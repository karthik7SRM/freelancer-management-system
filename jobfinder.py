from customtkinter import *
import mysql.connector as m
from tkinter import messagebox
import csv


con = m.connect(host="localhost", username="root", password="karthik", database="freelance")
cur = con.cursor()


w = CTk()
w.title("FreeCon")
w.geometry("800x600")
w.resizable(False, False)


def toggle_theme():
    current_mode = get_appearance_mode()
    set_appearance_mode("Light" if current_mode == "Dark" else "Dark")


def mainwindow(role_name):
    def submit():
        if len(name_entry.get()) > 0:
            if name_entry.get().isalpha():
                if len(age_entry.get()) > 0:
                    if age_entry.get().isdigit():
                        if len(gender_entry.get()) > 0:
                            if gender_entry.get().isalpha():
                                if area_entry.get().isalpha():
                                    if len(skill1_entry.get()) > 0:
                                        if len(skill2_entry.get()) > 0:
                                            if len(skill3_entry.get()) > 0:
                                                data = [name_entry.get(), age_entry.get(), gender_entry.get(),
                                                        area_entry.get(), skill1_entry.get(), skill2_entry.get(),
                                                        skill3_entry.get()]


                                                with open("indian_freelancers_data.csv", "a", newline="") as f:
                                                    wri = csv.writer(f)
                                                    wri.writerow(data)


                                                cur.execute(
                                                    "INSERT INTO freelance (name, age, gender, area, skill1, skill2, skill3) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                                    (name_entry.get(), age_entry.get(), gender_entry.get(),
                                                     area_entry.get(), skill1_entry.get(), skill2_entry.get(),
                                                     skill3_entry.get()))
                                                con.commit()
                                                messagebox.showinfo("Success", "Data submitted successfully!")

    w.withdraw()
    wind = CTk()
    wind.title(f"{role_name} Dashboard")
    wind.geometry("800x600")


    wind.grid_columnconfigure(0, weight=1)
    wind.grid_columnconfigure(1, weight=3)


    topframe = CTkFrame(wind)
    topframe.grid(row=0, column=0, columnspan=2, pady=20)


    label = CTkLabel(topframe, text="Freelancer Dashboard", font=("Arial", 30, "bold"))
    label.pack()

    content_frame = CTkFrame(wind)
    content_frame.grid(row=1, column=0, columnspan=2, pady=20, padx=20, sticky="nsew")

    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_rowconfigure(1, weight=1)
    content_frame.grid_rowconfigure(2, weight=1)
    content_frame.grid_rowconfigure(3, weight=1)
    content_frame.grid_rowconfigure(4, weight=1)
    content_frame.grid_rowconfigure(5, weight=1)
    content_frame.grid_rowconfigure(6, weight=1)
    content_frame.grid_rowconfigure(7, weight=1)


    labels = ["Name", "Age", "Gender", "Area", "Skill1", "Skill2", "Skill3"]
    entries = []

    for idx, label_text in enumerate(labels):
        CTkLabel(content_frame, text=label_text, font=("Arial", 20, "bold")).grid(row=idx, column=0, sticky="e", padx=20, pady=5)
        entry = CTkEntry(content_frame, placeholder_text=f"Enter {label_text}", font=("Arial", 20, "bold"), width=300)
        entry.grid(row=idx, column=1, padx=20, pady=5, sticky="w")
        entries.append(entry)

    name_entry, age_entry, gender_entry, area_entry, skill1_entry, skill2_entry, skill3_entry = entries


    CTkButton(content_frame, text="Submit", font=("Arial", 20, "bold"), command=submit).grid(row=7, column=0, columnspan=2, pady=20)


    CTkButton(wind, text="Logout", font=("Arial", 20), command=lambda: [wind.destroy(), w.deiconify()]).grid(row=8, column=0, columnspan=2, pady=20)

    wind.mainloop()


def signin():
    n = name.get().strip()
    p = pwrd.get().strip()
    r = role.get()

    if not n or not p or r == "Select Role":
        messagebox.showerror(title="Error!", message="All fields are required!")
        return

    try:
        query = "SELECT password, role FROM data WHERE name = %s"
        cur.execute(query, (n,))
        result = cur.fetchone()

        if result:
            stored_password, stored_role = result
            if p == stored_password and r == stored_role:  # Match credentials
                messagebox.showinfo(title="Success", message="Signed In Successfully!")
                mainwindow(r)  # Open the main window based on the role
            else:
                messagebox.showerror(title="Error!", message="Invalid Credentials. Please Try Again!")
        else:
            messagebox.showerror(title="Error!", message="User not found!")
    except Exception as e:
        messagebox.showerror(title="Error!", message=f"An error occurred: {e}")


def signup():
    n = name.get().strip()
    p = pwrd.get().strip()
    r = role.get()

    if not n or not p or r == "Select Role":
        messagebox.showerror(title="Error!", message="All fields are required!")
        return

    try:

        query_check = "SELECT * FROM data WHERE name = %s"
        cur.execute(query_check, (n,))
        if cur.fetchone():
            messagebox.showerror(title="Error!", message="User already exists!")
            return


        query_insert = "INSERT INTO data (name, password, role) VALUES (%s, %s, %s)"
        cur.execute(query_insert, (n, p, r))
        con.commit()
        messagebox.showinfo(title="Success", message="Sign-Up Successful!")
    except Exception as e:
        messagebox.showerror(title="Error!", message=f"An error occurred: {e}")



top = CTkFrame(w)
top.pack(fill="x", padx=20, pady=10)
CTkLabel(top, text="FreeCon", font=("Arial", 30, "bold")).pack()

middle = CTkFrame(w)
middle.pack(fill="both", expand=True, padx=20, pady=10)

middle.grid_columnconfigure(0, weight=1, uniform="col")
middle.grid_columnconfigure(1, weight=2, uniform="col")


CTkLabel(middle, text="User Name", font=("Arial", 20, "bold")).grid(row=0, column=0, sticky="e", padx=10, pady=5)
name = CTkEntry(middle, placeholder_text="Enter UserName", font=("Arial", 20, "bold"), width=250)
name.grid(row=0, column=1, padx=10, pady=5, sticky="w")


CTkLabel(middle, text="Password", font=("Arial", 20, "bold")).grid(row=1, column=0, sticky="e", padx=10, pady=5)
pwrd = CTkEntry(middle, placeholder_text="Enter Password", font=("Arial", 20, "bold"), width=250, show="*")
pwrd.grid(row=1, column=1, padx=10, pady=5, sticky="w")


CTkLabel(middle, text="Role Name", font=("Arial", 20, "bold")).grid(row=2, column=0, sticky="e", padx=10, pady=5)
rol = StringVar(value="Select Role")
role = CTkOptionMenu(middle, values=["Freelancer", "Admin"], font=("Arial", 20, "bold"), width=250, variable=rol)
role.grid(row=2, column=1, padx=10, pady=5, sticky="w")


CTkButton(middle, text="Sign In", width=200, font=("Arial", 20, "bold"), command=signin).grid(row=3, column=0, padx=10, pady=10)


CTkButton(middle, text="Sign Up", width=200, font=("Arial", 20, "bold"), command=signup).grid(row=3, column=1, padx=10, pady=10)


CTkButton(middle, text="Toggle Theme", width=200, font=("Arial", 20, "bold"), command=toggle_theme).grid(row=4, column=0, padx=10, pady=10)


set_appearance_mode("Dark")

w.mainloop()