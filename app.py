import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

class ManageFlowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ManageFlow - Product Inventory Management")
        
        self.filepath = 'products.csv'
        self.load_data()
        
        self.create_widgets()
        self.populate_table()
    
    def load_data(self):
        try:
            self.df = pd.read_csv(self.filepath)
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=['Product Id', 'Product Name', 'Brand', 'Quantity', 'updated_at', 'created_at'])
    
    def save_data(self):
        self.df.to_csv(self.filepath, index=False)
    
    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=('Product Id', 'Product Name', 'Brand', 'Quantity', 'updated_at', 'created_at'), show='headings')
        
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=0, width=100)
        
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Button(self.control_frame, text='Add New Product', command=self.add_product).pack(side=tk.LEFT, padx=10, pady=10)
        
        self.update_frame = tk.Frame(self.root)
        self.update_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(self.update_frame, text="Product Id:").pack(side=tk.LEFT, padx=5)
        self.product_id_entry = tk.Entry(self.update_frame, width=5)
        self.product_id_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(self.update_frame, text='+', command=self.increment_quantity).pack(side=tk.LEFT, padx=5)
        tk.Button(self.update_frame, text='-', command=self.decrement_quantity).pack(side=tk.LEFT, padx=5)
    
    def populate_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=tuple(row))
    
    def add_product(self):
        def submit():
            product_id = int(entry_product_id.get())
            product_name = entry_product_name.get()
            brand = entry_brand.get()
            quantity = int(entry_quantity.get())
            created_at = datetime.now().strftime('%Y-%m-%d')
            updated_at = created_at
            
            new_row = {'Product Id': product_id, 'Product Name': product_name, 'Brand': brand, 'Quantity': quantity, 'updated_at': updated_at, 'created_at': created_at}
            new_df = pd.DataFrame([new_row])
            self.df = pd.concat([self.df, new_df], ignore_index=True)
            self.save_data()
            self.populate_table()
            add_window.destroy()
        
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Product")
        
        tk.Label(add_window, text="Product Id:").grid(row=0, column=0, padx=10, pady=10)
        entry_product_id = tk.Entry(add_window)
        entry_product_id.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(add_window, text="Product Name:").grid(row=1, column=0, padx=10, pady=10)
        entry_product_name = tk.Entry(add_window)
        entry_product_name.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(add_window, text="Brand:").grid(row=2, column=0, padx=10, pady=10)
        entry_brand = tk.Entry(add_window)
        entry_brand.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(add_window, text="Quantity:").grid(row=3, column=0, padx=10, pady=10)
        entry_quantity = tk.Entry(add_window)
        entry_quantity.grid(row=3, column=1, padx=10, pady=10)
        
        tk.Button(add_window, text="Submit", command=submit).grid(row=4, column=0, columnspan=2, pady=10)
    
    def increment_quantity(self):
        product_id = self.product_id_entry.get()
        if product_id:
            self.update_quantity(product_id, 1)
    
    def decrement_quantity(self):
        product_id = self.product_id_entry.get()
        if product_id:
            self.update_quantity(product_id, -1)
    
    def update_quantity(self, product_id, amount):
        product_id = int(product_id)
        if product_id in self.df['Product Id'].values:
            self.df.loc[self.df['Product Id'] == product_id, 'Quantity'] += amount
            self.df.loc[self.df['Product Id'] == product_id, 'updated_at'] = datetime.now().strftime('%Y-%m-%d')
            self.save_data()
            self.populate_table()
        else:
            messagebox.showerror("Error", "Product ID not found")

if __name__ == "__main__":
    root = tk.Tk()
    app = ManageFlowApp(root)
    root.mainloop()
