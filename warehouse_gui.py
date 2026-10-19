import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from mysql.connector import Error
from datetime import datetime

class WarehouseManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Warehouse Management System")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Database connection variables
        self.host = "localhost"
        self.user = "root"  # MySQL username
        self.password = os.environ.get("MYSQL_PASSWORD", "")  # set MYSQL_PASSWORD before running
        self.database = "warehouse_management"
        
        # MySQL Connection
        self.connection = None
        self.connect_to_database()
        
        # Load categories for dropdown
        self.categories = self.load_categories()
        
        # Create UI
        self.create_widgets()
        
        # Load initial data
        self.load_products()    
    def connect_to_database(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            if self.connection.is_connected():
                print("Connected to MySQL database")
                return True
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error connecting to MySQL database: {e}")
            return False
    
    def execute_query(self, query, params=None):
        """Execute SQL query and handle exceptions"""
        try:
            if self.connection is None or not self.connection.is_connected():
                if not self.connect_to_database():
                    return None
                    
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                self.connection.commit()
                return cursor.rowcount
            else:
                return cursor.fetchall()
                
        except Error as e:
            messagebox.showerror("Query Error", f"Error executing query: {e}")
            return None
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
    
    def create_widgets(self):
        """Create the user interface elements"""
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        
        # Products Tab
        self.products_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.products_frame, text="Products")
        
        # Create products interface
        self.create_products_interface()
        
        # Add more tabs as needed (Orders, Suppliers, etc.)
        # self.orders_frame = ttk.Frame(self.notebook)
        # self.notebook.add(self.orders_frame, text="Orders")
        
        self.notebook.pack(expand=1, fill="both")
        
        # Bottom status bar
        self.status_bar = ttk.Label(self.root, text="Ready", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_categories(self):
        """Load categories from database"""
        query = "SELECT category_id, name FROM Categories"
        return self.execute_query(query) or []

    def create_products_interface(self):
        """Create the products management interface"""
        # Button frame
        btn_frame = ttk.Frame(self.products_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # CRUD Buttons
        ttk.Button(btn_frame, text="Add Product", command=self.add_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Product", command=self.delete_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.load_products).pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = ttk.Frame(self.products_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.search_entry.bind("<KeyRelease>", self.search_products)
        
        # Products treeview
        columns = ("id", "name", "category", "description", "price", "stock")
        self.tree = ttk.Treeview(self.products_frame, columns=columns, show="headings")
        
        # Configure columns and headings
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("category", text="Category")
        self.tree.heading("description", text="Description")
        self.tree.heading("price", text="Price")
        self.tree.heading("stock", text="Total Stock")
        
        self.tree.column("id", width=50)
        self.tree.column("name", width=150)
        self.tree.column("category", width=100)
        self.tree.column("description", width=250)
        self.tree.column("price", width=100)
        self.tree.column("stock", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.products_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double-click to edit
        self.tree.bind("<Double-1>", lambda event: self.edit_product())
    
    def load_products(self):
        """Load products from database into treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch products with joined data
        query = """
        SELECT 
            p.product_id,
            p.name,
            COALESCE(c.name, 'Uncategorized') as category,
            COALESCE(d.details, 'No description') as description,
            COALESCE(pr.amount, 0.00) as price,
            COALESCE(pr.currency, 'USD') as currency,
            COALESCE(SUM(s.quantity), 0) as total_stock
        FROM Products p
        LEFT JOIN Categories c ON p.category_id = c.category_id
        LEFT JOIN Descriptions d ON p.description_id = d.description_id
        LEFT JOIN Prices pr ON p.price_id = pr.price_id
        LEFT JOIN Stock s ON p.product_id = s.product_id
        GROUP BY p.product_id, p.name, c.name, d.details, pr.amount, pr.currency
        ORDER BY p.product_id DESC
        """
        
        products = self.execute_query(query)
        
        if products:
            for product in products:
                formatted_price = f"{product[4]} {product[5]}"
                values = (product[0], product[1], product[2], product[3], formatted_price, product[6])
                self.tree.insert("", tk.END, values=values)
        
        self.status_bar.config(text=f"{len(self.tree.get_children())} products loaded")

    def search_products(self, event=None):
        """Search products based on name, category, or description"""
        search_term = self.search_var.get().strip().lower()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if search_term:
            # Fetch filtered products
            query = """
            SELECT 
                p.product_id,
                p.name,
                COALESCE(c.name, 'Uncategorized') as category,
                COALESCE(d.details, 'No description') as description,
                COALESCE(pr.amount, 0.00) as price,
                COALESCE(pr.currency, 'USD') as currency,
                COALESCE(SUM(s.quantity), 0) as total_stock
            FROM Products p
            LEFT JOIN Categories c ON p.category_id = c.category_id
            LEFT JOIN Descriptions d ON p.description_id = d.description_id
            LEFT JOIN Prices pr ON p.price_id = pr.price_id
            LEFT JOIN Stock s ON p.product_id = s.product_id
            WHERE LOWER(p.name) LIKE %s 
               OR LOWER(COALESCE(c.name, '')) LIKE %s
               OR LOWER(COALESCE(d.details, '')) LIKE %s
            GROUP BY p.product_id, p.name, c.name, d.details, pr.amount, pr.currency
            ORDER BY p.product_id DESC
            """
            search_pattern = f"%{search_term}%"
            params = (search_pattern, search_pattern, search_pattern)
            products = self.execute_query(query, params)
        else:
            # If no search term, load all products
            self.load_products()
            return
            
        if products:
            for product in products:
                formatted_price = f"{product[4]} {product[5]}"
                values = (product[0], product[1], product[2], product[3], formatted_price, product[6])
                self.tree.insert("", tk.END, values=values)
                
        self.status_bar.config(text=f"{len(self.tree.get_children())} products found")
    
    def add_product(self):
        """Add a new product"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Product")
        dialog.geometry("500x450")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        # Category dropdown
        ttk.Label(dialog, text="Category:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        category_var = tk.StringVar()
        category_menu = ttk.Combobox(dialog, textvariable=category_var, width=27)
        category_menu['values'] = [cat[1] for cat in self.categories]
        if self.categories:
            category_menu.current(0)
        category_menu.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Description:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        desc_var = tk.StringVar()
        desc_entry = ttk.Entry(dialog, textvariable=desc_var, width=30)
        desc_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Price:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        price_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=price_var, width=30).grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Currency:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        currency_var = tk.StringVar(value="USD")
        ttk.Entry(dialog, textvariable=currency_var, width=30).grid(row=4, column=1, padx=10, pady=5)
        
        # Warehouse selection
        ttk.Label(dialog, text="Warehouse:").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
        warehouses = self.execute_query("SELECT warehouse_id, name FROM Warehouses")
        warehouse_var = tk.StringVar()
        warehouse_menu = ttk.Combobox(dialog, textvariable=warehouse_var, width=27)
        warehouse_menu['values'] = [w[1] for w in warehouses] if warehouses else []
        if warehouses:
            warehouse_menu.current(0)
        warehouse_menu.grid(row=5, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Initial Quantity:").grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
        quantity_var = tk.StringVar(value="0")
        ttk.Entry(dialog, textvariable=quantity_var, width=30).grid(row=6, column=1, padx=10, pady=5)
        
        def save_product():
            try:
                # Validate inputs
                name = name_var.get().strip()
                if not name:
                    raise ValueError("Name cannot be empty")
                
                category_name = category_var.get().strip()
                if not category_name:
                    raise ValueError("Please select a category")
                
                description = desc_var.get().strip()
                if not description:
                    raise ValueError("Description cannot be empty")
                
                try:
                    price = float(price_var.get().strip())
                    if price < 0:
                        raise ValueError
                except ValueError:
                    raise ValueError("Price must be a positive number")
                
                currency = currency_var.get().strip()
                if not currency:
                    raise ValueError("Currency cannot be empty")
                
                try:
                    quantity = int(quantity_var.get().strip())
                    if quantity < 0:
                        raise ValueError
                except ValueError:
                    raise ValueError("Quantity must be a non-negative integer")
                
                warehouse_name = warehouse_var.get().strip()
                if not warehouse_name:
                    raise ValueError("Please select a warehouse")
                
                # Start transaction
                cursor = self.connection.cursor()
                
                try:
                    # 1. Get category_id
                    category_id = next(cat[0] for cat in self.categories if cat[1] == category_name)
                    
                    # 2. Insert description
                    cursor.execute("INSERT INTO Descriptions (details) VALUES (%s)", (description,))
                    description_id = cursor.lastrowid
                    
                    # 3. Insert price
                    cursor.execute("INSERT INTO Prices (amount, currency) VALUES (%s, %s)", (price, currency))
                    price_id = cursor.lastrowid
                    
                    # 4. Insert product
                    cursor.execute("""
                        INSERT INTO Products (name, category_id, description_id, price_id)
                        VALUES (%s, %s, %s, %s)
                    """, (name, category_id, description_id, price_id))
                    product_id = cursor.lastrowid
                    
                    # 5. Get warehouse_id and its first location
                    warehouse_id = next(w[0] for w in warehouses if w[1] == warehouse_name)
                    cursor.execute("""
                        SELECT location_id FROM Locations 
                        WHERE warehouse_id = %s 
                        LIMIT 1
                    """, (warehouse_id,))
                    location_result = cursor.fetchone()
                    
                    if location_result:
                        location_id = location_result[0]
                        # 6. Insert initial stock
                        cursor.execute("""
                            INSERT INTO Stock (product_id, warehouse_id, location_id, quantity)
                            VALUES (%s, %s, %s, %s)
                        """, (product_id, warehouse_id, location_id, quantity))
                    
                    # 7. Add to history
                    cursor.execute("""
                        INSERT INTO History (product_id, action, action_date)
                        VALUES (%s, %s, %s)
                    """, (product_id, 'Product created', datetime.now().date()))
                    
                    self.connection.commit()
                    messagebox.showinfo("Success", "Product added successfully")
                    dialog.destroy()
                    self.load_products()
                    
                except Error as e:
                    self.connection.rollback()
                    messagebox.showerror("Database Error", str(e))
                    
                finally:
                    cursor.close()
                    
            except ValueError as e:
                messagebox.showerror("Validation Error", str(e))
            except StopIteration:
                messagebox.showerror("Error", "Invalid category or warehouse selected")
        
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Save", command=save_product).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).grid(row=0, column=1, padx=10)
        dialog.wait_window()
    

    def delete_product(self):
        """Delete selected product"""
        selected_item = self.tree.selection()
        print(f"[DEBUG] Selected item for delete: {selected_item}")
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a product to delete")
            print("[DEBUG] No product selected for deletion.")
            return

        product_id_str = self.tree.item(selected_item[0], "values")[0]
        product_name = self.tree.item(selected_item[0], "values")[1]
        print(f"[DEBUG] Selected product_id_str: {product_id_str}, product_name: {product_name}")
        try:
            product_id = int(product_id_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid product ID selected for deletion.")
            print(f"[DEBUG] Invalid product ID for deletion: {product_id_str}")
            return

        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{product_name}' (ID: {product_id})?"):
            print(f"[DEBUG] Deletion cancelled by user for product_id: {product_id}")
            return
        
        try:
            # Simplified delete (assumes ON DELETE CASCADE is set up for related tables like Descriptions, Prices, Stock, History)
            print(f"[DEBUG] Attempting to delete product_id: {product_id}")
            query = "DELETE FROM Products WHERE product_id = %s"
            params = (product_id,)
            result = self.execute_query(query, params)
            print(f"[DEBUG] Delete query result: {result}")

            if result is not None:
                messagebox.showinfo("Success", "Product deleted successfully")
                self.load_products()
                print(f"[DEBUG] Product {product_id} deleted and products reloaded.")
            else:
                messagebox.showerror("Delete Error", "Failed to delete product.")
                print(f"[DEBUG] Delete failed for product_id: {product_id}")
        except Exception as e:
            messagebox.showerror("Delete Error", f"Exception: {e}")
            print(f"[DEBUG] Exception during delete: {e}")


    def __del__(self):
        """Close database connection when app closes"""
        if hasattr(self, 'connection') and self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

def main():
    root = tk.Tk()
    
    app = WarehouseManagementSystem(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.__del__(), root.destroy()))
    root.mainloop()

if __name__ == "__main__":
    main()
