import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

# List to store each invoice line item
invoice_items = []

# Function to add items to the table
def add_item():
    try:
        size = entry_size.get()
        description = entry_description.get()
        square_ft = float(convert_to_meters(float(entry_square_ft.get()), unit_var.get()))
        rate = float(entry_rate.get())
        quantity = int(entry_quantity.get())

        amount = square_ft * rate * quantity
        s_no = len(invoice_items) + 1  # Serial number based on item count

        # Append item details as a tuple
        invoice_items.append((s_no, size, description, square_ft, rate, quantity, amount))

        # Insert into Treeview table
        tree.insert("", "end", values=(s_no, size, description, square_ft, rate, quantity, amount))
        
        # Clear entry fields
        entry_size.delete(0, tk.END)
        entry_description.delete(0, tk.END)
        entry_square_ft.delete(0, tk.END)
        entry_rate.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)
        
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

# Function to calculate total amount
def calculate_total():
    total = sum(item[-1] for item in invoice_items)
    label_total.config(text=f"Total Amount: ${total:.2f}")
    return total

# Function to generate PDF invoice
def generate_invoice():
    total = calculate_total()
    filename = "invoice.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "HVAC Ducting Invoice")
    
    # Add Logo
    try:
        c.drawImage("images.png", 450, 770, width=80, height=50)
    except:
        print("Logo not found. Make sure 'images.png' is in the correct directory.")
    
    # Customer Information
    c.setFont("Helvetica", 12)
    c.drawString(100, 760, f"Customer Name: {entry_name.get()}")
    c.drawString(100, 740, f"Address: {entry_address.get()}")
    c.drawString(100, 720, f"Contact: {entry_contact.get()}")
    c.drawString(100, 700, f"Email: {entry_email.get()}")

    # Table Headers
    c.setFont("Helvetica-Bold", 10)
    y_position = 680
    c.drawString(50, y_position, "S.No")
    c.drawString(100, y_position, "Size")
    c.drawString(180, y_position, "Description")
    c.drawString(280, y_position, "Sq.Ft")
    c.drawString(340, y_position, "Rate")
    c.drawString(400, y_position, "Quantity")
    c.drawString(470, y_position, "Amount")

    # Table Rows
    c.setFont("Helvetica", 10)
    y_position -= 20
    for item in invoice_items:
        c.drawString(50, y_position, str(item[0]))
        c.drawString(100, y_position, str(item[1]))
        c.drawString(180, y_position, item[2])
        c.drawString(280, y_position, f"{item[3]:.2f}")
        c.drawString(340, y_position, f"{item[4]:.2f}")
        c.drawString(400, y_position, str(item[5]))
        c.drawString(470, y_position, f"${item[6]:.2f}")
        y_position -= 20

    # Total Amount
    y_position -= 20
    c.drawString(400, y_position, f"Total Amount: ${total:.2f}")

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(100, 50, "Thank you for your business!")
    
    # Save PDF
    c.save()
    messagebox.showinfo("Invoice Generated", f"Invoice saved as {filename}")
    if os.name == "nt":
        os.startfile(filename, "print")

# Unit conversion function
def convert_to_meters(value, unit):
    if unit == "inches":
        return value * 0.0254
    elif unit == "centimeters":
        return value / 100
    else:
        return value  # assume meters

# Set up main GUI
root = tk.Tk()
root.title("HVAC Ducting Bill Calculator")
root.geometry("600x600")

# Customer Information
ttk.Label(root, text="Customer Information", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
ttk.Label(root, text="Name:").grid(row=1, column=0, sticky="w")
entry_name = ttk.Entry(root, width=30)
entry_name.grid(row=1, column=1)

ttk.Label(root, text="Address:").grid(row=2, column=0, sticky="w")
entry_address = ttk.Entry(root, width=30)
entry_address.grid(row=2, column=1)

ttk.Label(root, text="Contact Number:").grid(row=3, column=0, sticky="w")
entry_contact = ttk.Entry(root, width=30)
entry_contact.grid(row=3, column=1)

ttk.Label(root, text="Email:").grid(row=4, column=0, sticky="w")
entry_email = ttk.Entry(root, width=30)
entry_email.grid(row=4, column=1)

# Measurement unit dropdown
unit_var = tk.StringVar(value="meters")
ttk.Label(root, text="Select Unit:").grid(row=5, column=0, sticky="w")
unit_dropdown = ttk.Combobox(root, textvariable=unit_var, values=["meters", "inches", "centimeters"])
unit_dropdown.grid(row=5, column=1)

# Item input fields
ttk.Label(root, text="Size:").grid(row=6, column=0, sticky="w")
entry_size = ttk.Entry(root, width=30)
entry_size.grid(row=6, column=1)

ttk.Label(root, text="Description:").grid(row=7, column=0, sticky="w")
entry_description = ttk.Entry(root, width=30)
entry_description.grid(row=7, column=1)

ttk.Label(root, text="Square Feet:").grid(row=8, column=0, sticky="w")
entry_square_ft = ttk.Entry(root, width=30)
entry_square_ft.grid(row=8, column=1)

ttk.Label(root, text="Rate:").grid(row=9, column=0, sticky="w")
entry_rate = ttk.Entry(root, width=30)
entry_rate.grid(row=9, column=1)

ttk.Label(root, text="Quantity:").grid(row=10, column=0, sticky="w")
entry_quantity = ttk.Entry(root, width=30)
entry_quantity.grid(row=10, column=1)

# Add Item Button
ttk.Button(root, text="Add Item", command=add_item).grid(row=11, column=1, pady=10)

# Treeview for displaying items
tree = ttk.Treeview(root, columns=("S.No", "Size", "Description", "Sq.Ft", "Rate", "Quantity", "Amount"), show="headings")
for col in ("S.No", "Size", "Description", "Sq.Ft", "Rate", "Quantity", "Amount"):
    tree.heading(col, text=col)
tree.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

# Total label
label_total = ttk.Label(root, text="Total Amount: $0.00", font=("Arial", 12, "bold"))
label_total.grid(row=13, column=0, columnspan=2, pady=10)

# Generate Invoice Button
ttk.Button(root, text="Generate Invoice", command=generate_invoice).grid(row=14, column=0, columnspan=2, pady=20)

root.mainloop()