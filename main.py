import tkinter as tk
import csv
from tkinter import messagebox
from tkinter import ttk


def create_main_window():
    root = tk.Tk()
    root.title("Car Inventory System")
    root.geometry("1200x400")

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    notebook = ttk.Notebook(root)
    notebook.grid(row=0, column=0, sticky="ew")

    cars_tab = ttk.Frame(notebook)
    customers_tab = ttk.Frame(notebook)
    notebook.add(cars_tab, text="Cars")
    notebook.add(customers_tab, text="Customers")

    cars_tab.grid_rowconfigure(0, weight=1)
    cars_tab.grid_columnconfigure(0, weight=3)
    cars_tab.grid_columnconfigure(1, weight=1)

    display_frame = ttk.Frame(cars_tab, relief="raised", borderwidth=2)
    display_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    tree = ttk.Treeview(
        display_frame, columns=("ID", "Make", "Model", "Year", "Price"), show="headings"
    )
    tree.heading("ID", text="ID")
    tree.heading("Make", text="Make")
    tree.heading("Model", text="Model")
    tree.heading("Year", text="Year")
    tree.heading("Price", text="Price")
    
    for col in ("ID", "Make", "Model", "Year", "Price"):
        tree.column(col, anchor="center", width=150)

    tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    display_frame.grid_rowconfigure(0, weight=1)
    display_frame.grid_columnconfigure(0, weight=1)

    crud_frame = ttk.Frame(cars_tab)
    crud_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    ttk.Button(crud_frame, command=lambda: add_car(tree), text="Add New Car").grid(
        row=0, column=0, pady=10, padx=5, sticky="ew"
    )
    ttk.Button(crud_frame, text="Edit Selected Car", command=lambda: edit_car(tree)).grid(
        row=1, column=0, pady=10, padx=5, sticky="ew"
    )
    ttk.Button(crud_frame, text="Delete Selected Car").grid(
        row=2, column=0, pady=10, padx=5, sticky="ew"
    )
    ttk.Button(crud_frame, text="Refresh List").grid(
        row=3, column=0, pady=10, padx=5, sticky="ew"
    )

    try:
        with open('cars.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                tree.insert('', 'end', values=row)
    except FileNotFoundError:
        pass

    return root
def edit_car (tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Xato", "Hechqanday mashina tanlamadingiz")
        return
    
    car_data = tree.item(selected_item)['values']
    car_id, make, model, year, price = car_data

    window = tk.Toplevel()
    window.title("Edit Car")
    window.geometry("300x250")

    ttk.Label(window, text="Marka: ").grid(row=0, column=0, padx=5, pady=5)
    make_input = ttk.Entry(window)
    make_input.grid(row=0, column=1)
    make_input.insert(0, make)

    ttk.Label(window, text="Model: ").grid(row=1, column=0, padx=5, pady=5)
    model_input = ttk.Entry(window)
    model_input.grid(row=1, column=1)
    model_input.insert(0, model)

    ttk.Label(window, text="Yil: ").grid(row=2, column=0, padx=5, pady=5)
    year_input = ttk.Entry(window)
    year_input.grid(row=2, column=1)
    year_input.insert(0, year)

    ttk.Label(window, text="Narxi: ").grid(row=3, column=0, padx=5, pady=5)
    price_input = ttk.Entry(window)
    price_input.grid(row=3, column=1)
    price_input.insert(0, price)

    # O'zgartirilgan avtomobilni saqlash funksiyasi
    def save_edited_car():
        new_make = make_input.get()
        new_model = model_input.get()
        new_year = year_input.get()
        new_price = price_input.get()

        if not all([new_make, new_model, new_year, new_price]):
            messagebox.showerror("Error", "Fill in all fields")
            return
        
        try:
            # CSV faylini o'qish
            with open('cars.csv', 'r') as file:
                reader = csv.reader(file)
                headers = next(reader)  # Bosh satrni o'qib olish
                cars = list(reader)

            # Tanlangan avtomobilni yangilash
            for i, car in enumerate(cars):
                if car[0] == car_id:
                    cars[i] = [car_id, new_make, new_model, new_year, new_price]

            # Yangilangan avtomobillarni CSV fayliga yozish
            with open('cars.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)  # Bosh satrni qayta yozish
                writer.writerows(cars)    # Barcha avtomobillarni qayta yozish

            # Treeview'ni yangilash
            tree.item(selected_item, values=(car_id, new_make, new_model, new_year, new_price))

            messagebox.showinfo("Success", "Car details updated successfully")
            window.destroy()  # Tahrirlash oynasini yopish
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Saqlash tugmasini qo'yish
    ttk.Button(window, text="Save Changes", command=save_edited_car).grid(row=4, column=0,
        columnspan=2, pady=20)

def add_car(tree):
    window = tk.Toplevel()
    window.title("Add new car")
    window.geometry("300x250")

    ttk.Label(window, text="Make: ").grid(row=0, column=0, padx=5, pady=5)
    make_input = ttk.Entry(window)
    make_input.grid(row=0, column=1)

    ttk.Label(window, text="Model: ").grid(row=1, column=0, padx=5, pady=5)
    model_input = ttk.Entry(window)
    model_input.grid(row=1, column=1)

    ttk.Label(window, text="Year: ").grid(row=2, column=0, padx=5, pady=5)
    year_input = ttk.Entry(window)
    year_input.grid(row=2, column=1)

    ttk.Label(window, text="Price: ").grid(row=3, column=0, padx=5, pady=5)
    price_input = ttk.Entry(window)
    price_input.grid(row=3, column=1)

    def save_car():
        make = make_input.get()
        model = model_input.get()
        year = year_input.get()
        price = price_input.get()

        if not all([make, model, year, price]):
            messagebox.showerror("Error", "Fill all fields")
            return

        try:
            try:
                with open('cars.csv', 'r') as file:
                    reader = csv.reader(file)
                    next(reader)

                    cars = list(reader)
                    next_id = str(len(cars) + 1)
            except FileNotFoundError:
                with open('cars.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Make", "Model", "Year", "Price"])
                    next_id = "1"
            
            with open('cars.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([next_id, make, model, year, price])

            # Insert the new car entry into the Treeview dynamically
            tree.insert('', 'end', values=(next_id, make, model, year, price))
            messagebox.showinfo("Success", "Car added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")
    
    ttk.Button(window, text='Save Car', command=save_car).grid(row=4, column=0,
        columnspan=2, pady=20)



def main():
    root = create_main_window()
    root.mainloop()


if __name__ == "__main__":
    main()
