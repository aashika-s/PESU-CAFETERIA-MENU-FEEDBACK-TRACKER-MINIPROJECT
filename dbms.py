


# # --- PESU Cafeteria Menu & Feedback Tracker ---
# # FINAL VERSION - Includes Login/Logout & Role-Based UI
# # NEW: Students can update their own reviews

# import tkinter as tk
# from tkinter import messagebox, simpledialog
# import ttkbootstrap as ttk
# from ttkbootstrap.constants import *
# import mysql.connector
# from mysql.connector import Error

# # --- Global Connection Object ---
# db_connection = None

# # --- DATABASE HELPER FUNCTIONS ---

# def connect_to_database(username, password):
#     """Establishes the global database connection."""
#     global db_connection
#     try:
#         # Close any existing connection
#         if db_connection and db_connection.is_connected():
#             db_connection.close()
            
#         db_connection = mysql.connector.connect(
#             host='localhost', database='cafeteria_db', user=username, password=password
#         )
#         if db_connection.is_connected():
#             return True
#     except Error as e:
#         messagebox.showerror("Connection Error", f"The error '{e}' occurred")
#         return False

# def execute_query(query, data=None):
#     """For INSERT, UPDATE, DELETE queries."""
#     if not db_connection or not db_connection.is_connected():
#         messagebox.showerror("Error", "Database not connected.")
#         return False
#     cursor = db_connection.cursor()
#     try:
#         cursor.execute(query, data)
#         db_connection.commit()
#         return True
#     except Error as e:
#         db_connection.rollback()
#         messagebox.showerror("Query Error", str(e))
#         return False

# def execute_read_query(query, data=None):
#     """For SELECT queries."""
#     if not db_connection or not db_connection.is_connected():
#         messagebox.showerror("Error", "Database not connected.")
#         return None
#     cursor = db_connection.cursor(buffered=True)
#     try:
#         cursor.execute(query, data)
#         return cursor.fetchall()
#     except Error as e:
#         messagebox.showerror("Read Query Error", str(e))
#         return None

# # --- MAIN APPLICATION CLASS ---

# class CafeteriaApp(ttk.Window):
#     def __init__(self):
#         super().__init__(themename="flatly")
#         self.title("PESU Cafeteria Management System")
#         self.geometry("1200x800")
        
#         # --- NEW: User state variables ---
#         self.current_username = None
#         self.current_user_role = None # "Admin" or "Student"
        
#         self.show_login_screen()

#     def show_login_screen(self):
#         """Displays the initial username/password prompt."""
#         for widget in self.winfo_children(): widget.destroy()
        
#         # Reset user state
#         self.current_username = None
#         self.current_user_role = None
#         global db_connection
#         if db_connection and db_connection.is_connected():
#             db_connection.close()
#             db_connection = None
        
#         login_frame = ttk.Frame(self, padding="50")
#         login_frame.pack(expand=True)
        
#         ttk.Label(login_frame, text="Cafeteria Login", font=("Helvetica", 18, "bold")).pack(pady=10)
        
#         # --- NEW: Username field ---
#         ttk.Label(login_frame, text="Username:", font=("Helvetica", 12)).pack(pady=(10,0))
#         self.user_entry = ttk.Entry(login_frame, width=30)
#         self.user_entry.pack(pady=5)
#         self.user_entry.insert(0, "root") # Default to root for easy testing

#         ttk.Label(login_frame, text="Password:", font=("Helvetica", 12)).pack(pady=(10,0))
#         self.password_entry = ttk.Entry(login_frame, show="*", width=30)
#         self.password_entry.pack(pady=5)
        
#         self.password_entry.bind('<Return>', self.login)
#         ttk.Button(login_frame, text="Connect", command=self.login, bootstyle="success").pack(pady=20, ipadx=20)
        
#         self.user_entry.focus_set()

#     def login(self, event=None):
#         """Handles the login attempt and role detection."""
#         username = self.user_entry.get()
#         password = self.password_entry.get()
        
#         if not username or not password:
#             messagebox.showerror("Error", "Username and Password are required.")
#             return

#         if connect_to_database(username, password):
#             self.current_username = username
#             self.determine_user_role() # --- NEW: Set the role ---
            
#             messagebox.showinfo("Success", f"Welcome, {username}!\nYou are logged in as: {self.current_user_role}")
#             self.create_main_ui()
#         else:
#             self.password_entry.delete(0, tk.END)

#     def determine_user_role(self):
#         """Checks user grants to determine their role."""
#         if self.current_username == 'root':
#             self.current_user_role = "Admin"
#             return

#         grants = execute_read_query(f"SHOW GRANTS FOR '{self.current_username}'@'localhost'")
#         if grants:
#             grant_str = str(grants)
#             # Check for broad admin privileges
#             if "ALL PRIVILEGES" in grant_str or "UPDATE" in grant_str.upper() and "STAFF" in grant_str.upper(): # A more specific admin check
#                 self.current_user_role = "Admin"
#             # Check for specific student privileges
#             elif "INSERT" in grant_str.upper() and "ORDERS" in grant_str.upper():
#                 self.current_user_role = "Student"
#             else:
#                 self.current_user_role = "Student" # Default to restricted
#         else:
#             self.current_user_role = "Student" # Default to restricted if no grants found

#     def logout(self):
#         """Logs out the current user and returns to login screen."""
#         self.show_login_screen()

#     def create_main_ui(self):
#         """Creates the main dashboard UI based on user role."""
#         for widget in self.winfo_children(): widget.destroy()
        
#         main_pane = ttk.PanedWindow(self, orient=HORIZONTAL)
#         main_pane.pack(fill=BOTH, expand=True)

#         nav_frame = ttk.Frame(main_pane, padding=10)
#         main_pane.add(nav_frame, weight=1)

#         self.content_frame = ttk.Frame(main_pane, padding=20)
#         main_pane.add(self.content_frame, weight=4)

#         ttk.Label(nav_frame, text=f"Dashboard ({self.current_user_role})", font=("Helvetica", 16, "bold")).pack(pady=10, padx=10)
        
#         # --- ROLE-BASED BUTTONS ---
        
#         # Buttons all users can see
#         ttk.Button(nav_frame, text="Students", command=lambda: self.show_crud_ui("Student", ['SRN', 'Name', 'Email', 'Phone', 'CreatedAt']), bootstyle="info-outline").pack(fill=tk.X, pady=4)
#         ttk.Button(nav_frame, text="Food Items", command=lambda: self.show_crud_ui("FoodItem", ['ItemID', 'ItemName', 'Category', 'Price', 'IsActive'], pk_is_auto=True), bootstyle="info-outline").pack(fill=tk.X, pady=4)
#         ttk.Button(nav_frame, text="Reviews", command=lambda: self.show_crud_ui("Review", ['ReviewID', 'SRN', 'ItemID', 'Rating', 'Feedback', 'ReviewDate'], pk_is_auto=True), bootstyle="info-outline").pack(fill=tk.X, pady=4)

#         # Admin-only buttons
#         if self.current_user_role == "Admin":
#             ttk.Button(nav_frame, text="Staff", command=lambda: self.show_crud_ui("Staff", ['StaffID', 'Name', 'Email', 'Role', 'CreatedAt'], pk_is_auto=True), bootstyle="info-outline").pack(fill=tk.X, pady=4)
#             ttk.Button(nav_frame, text="Menus", command=lambda: self.show_menu_crud_ui(), bootstyle="info-outline").pack(fill=tk.X, pady=4)

#         ttk.Separator(nav_frame).pack(fill='x', pady=10)
        
#         # Buttons all users can see
#         ttk.Button(nav_frame, text="Place Order", command=self.show_transaction_ui, bootstyle="success-outline").pack(fill=tk.X, pady=4)
#         ttk.Button(nav_frame, text="Reports & Queries", command=self.show_reports_ui, bootstyle="success-outline").pack(fill=tk.X, pady=4)
        
#         # Admin-only buttons
#         if self.current_user_role == "Admin":
#             ttk.Separator(nav_frame).pack(fill='x', pady=10)
#             ttk.Button(nav_frame, text="DB Admin", command=self.show_admin_ui, bootstyle="warning-outline").pack(fill=tk.X, pady=4)
        
#         # --- NEW: Logout Button ---
#         ttk.Separator(nav_frame).pack(fill='x', pady=40)
#         ttk.Button(nav_frame, text="Log Out", command=self.logout, bootstyle="danger").pack(fill=tk.X, pady=4)
        
#         # Show default screen
#         self.show_crud_ui("Student", ['SRN', 'Name', 'Email', 'Phone', 'CreatedAt'])

#     def clear_content_frame(self):
#         """Clears the main content area."""
#         for widget in self.content_frame.winfo_children():
#             widget.destroy()

#     def show_crud_ui(self, table_name, columns, pk_is_auto=False):
#         """The generic UI, now with role-based button disabling."""
#         self.clear_content_frame()
#         pk_column = columns[0]
        
#         # --- ROLE-BASED ACCESS CONTROL ---
#         is_student = self.current_user_role == "Student"
        
#         # By default, all permissions are enabled (for Admin)
#         can_add = True
#         can_update = True
#         can_delete = True
        
#         if is_student:
#             # Default to no permissions for students
#             can_add = False
#             can_update = False
#             can_delete = False
            
#             # Exception: Students can add/update reviews
#             if table_name == "Review":
#                 can_add = True
#                 can_update = True
#                 can_delete = False # Students still can't delete reviews
#         # --- END OF CHANGED BLOCK ---

#         ttk.Label(self.content_frame, text=f"Manage {table_name}", font=("Helvetica", 20, "bold")).pack(pady=10, anchor="w")
        
#         tree_frame = ttk.Frame(self.content_frame)
#         tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
#         tree = ttk.Treeview(tree_frame, columns=columns, show='headings', bootstyle="primary")
#         for col in columns:
#             tree.heading(col, text=col.replace('_', ' ').title())
#             tree.column(col, width=120, anchor="w")
        
#         scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
#         tree.configure(yscrollcommand=scrollbar.set)
#         tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#         def refresh_tree():
#             for item in tree.get_children(): tree.delete(item)
#             records = execute_read_query(f"SELECT * FROM {table_name}")
#             if records:
#                 for record in records:
#                     tree.insert("", "end", values=[str(v) if v is not None else "" for v in record])

#         form_frame = ttk.Frame(self.content_frame, padding=10, bootstyle="light")
#         form_frame.pack(fill=tk.X, pady=10)
        
#         entries = {}
#         for i, col in enumerate(columns):
#             ttk.Label(form_frame, text=f"{col}:").grid(row=i, column=0, padx=5, pady=5, sticky='e')
#             entry = ttk.Entry(form_frame, width=40)
#             entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
#             entries[col] = entry

#         def clear_form():
#             tree.selection_remove(tree.selection())
#             for col, entry in entries.items():
#                 entry.config(state="normal")
#                 entry.delete(0, tk.END)
#             if pk_is_auto:
#                 entries[pk_column].insert(0, "(Auto-Generated)")
#                 entries[pk_column].config(state="readonly")
#             else:
#                 entries[pk_column].focus_set()

#         def on_item_select(event):
#             selected_items = tree.selection()
#             if not selected_items: return
            
#             for col, entry in entries.items():
#                 entry.config(state="normal")
#                 entry.delete(0, tk.END)

#             values = tree.item(selected_items[0])['values']
#             for i, col in enumerate(columns):
#                 entries[col].insert(0, values[i])
            
#             # --- CHANGED LOGIC HERE ---
#             if can_update: # Use can_update instead of can_modify
#                 entries[pk_column].config(state="readonly")
#             else:
#                 for entry in entries.values():
#                     entry.config(state="readonly")
        
#         tree.bind("<<TreeviewSelect>>", on_item_select)

#         def add_record():
#             cols = [c for c in columns if "At" not in c and not (pk_is_auto and c == pk_column)]
#             values = [entries[c].get() for c in cols]
#             query = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))})"
#             if execute_query(query, tuple(values)):
#                 refresh_tree(); clear_form(); messagebox.showinfo("Success", "Record added.")

#         def update_record():
#             # Note: A student could update someone else's review.
#             # A more complex app would add: WHERE SRN = self.current_srn
#             # For this demo, just enabling the button is enough.
#             if not tree.selection(): messagebox.showwarning("Warning", "Select a record to update."); return
#             pk_val = entries[pk_column].get()
#             cols = [c for c in columns if c != pk_column and "At" not in c]
#             values = [entries[c].get() for c in cols] + [pk_val]
#             query = f"UPDATE {table_name} SET {', '.join([f'{c} = %s' for c in cols])} WHERE {pk_column} = %s"
#             if execute_query(query, tuple(values)):
#                 refresh_tree(); clear_form(); messagebox.showinfo("Success", "Record updated.")
        
#         def delete_record():
#             if not tree.selection(): messagebox.showwarning("Warning", "Select a record to delete."); return
#             pk_val = entries[pk_column].get()
#             if messagebox.askyesno("Confirm", f"Delete record {pk_val}?"):
#                 if execute_query(f"DELETE FROM {table_name} WHERE {pk_column}=%s", (pk_val,)):
#                     refresh_tree(); clear_form(); messagebox.showinfo("Success", "Record deleted.")
        
#         btn_frame = ttk.Frame(self.content_frame)
#         btn_frame.pack(fill=tk.X, pady=10)
        
#         # --- ROLE-BASED BUTTON STATE ---
#         add_btn = ttk.Button(btn_frame, text="Add", command=add_record, bootstyle="success")
#         add_btn.pack(side=tk.LEFT, padx=5, ipadx=10)
#         if not can_add: add_btn.config(state="disabled")
            
#         update_btn = ttk.Button(btn_frame, text="Update", command=update_record, bootstyle="info")
#         update_btn.pack(side=tk.LEFT, padx=5, ipadx=10)
#         if not can_update: update_btn.config(state="disabled") # <<< CHANGED

#         delete_btn = ttk.Button(btn_frame, text="Delete", command=delete_record, bootstyle="danger")
#         delete_btn.pack(side=tk.LEFT, padx=5, ipadx=10)
#         if not can_delete: delete_btn.config(state="disabled") # <<< CHANGED

#         ttk.Button(btn_frame, text="Clear Form", command=clear_form, bootstyle="secondary").pack(side=tk.RIGHT, padx=5, ipadx=10)

#         refresh_tree(); clear_form()
    
#     # --- Custom UI for Menu Management (Admin Only) ---
    
#     def show_menu_crud_ui(self):
#         """A custom CRUD UI for Menus, with a button to edit items."""
#         # This whole function is admin-only, so we don't need to check roles inside
#         self.clear_content_frame()
#         table_name = "Menu"
#         columns = ['MenuID', 'MenuDate', 'StaffID', 'Notes', 'CreatedAt']
#         pk_column = 'MenuID'
#         pk_is_auto = True

#         ttk.Label(self.content_frame, text=f"Manage {table_name}", font=("Helvetica", 20, "bold")).pack(pady=10, anchor="w")
        
#         tree_frame = ttk.Frame(self.content_frame)
#         tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
#         tree = ttk.Treeview(tree_frame, columns=columns, show='headings', bootstyle="primary")
#         for col in columns:
#             tree.heading(col, text=col.replace('_', ' ').title())
#             tree.column(col, width=120, anchor="w")
        
#         scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
#         tree.configure(yscrollcommand=scrollbar.set)
#         tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#         def refresh_tree():
#             for item in tree.get_children(): tree.delete(item)
#             records = execute_read_query(f"SELECT * FROM {table_name}")
#             if records:
#                 for record in records:
#                     tree.insert("", "end", values=[str(v) if v is not None else "" for v in record])

#         form_frame = ttk.Frame(self.content_frame, padding=10, bootstyle="light")
#         form_frame.pack(fill=tk.X, pady=10)
        
#         entries = {}
#         for i, col in enumerate(columns):
#             ttk.Label(form_frame, text=f"{col}:").grid(row=i, column=0, padx=5, pady=5, sticky='e')
#             entry = ttk.Entry(form_frame, width=40)
#             entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
#             entries[col] = entry

#         def clear_form():
#             tree.selection_remove(tree.selection())
#             for col, entry in entries.items():
#                 entry.config(state="normal")
#                 entry.delete(0, tk.END)
#             if pk_is_auto:
#                 entries[pk_column].insert(0, "(Auto-Generated)")
#                 entries[pk_column].config(state="readonly")
#             else:
#                 entries[pk_column].focus_set()

#         def on_item_select(event):
#             selected_items = tree.selection()
#             if not selected_items: return
            
#             for col, entry in entries.items():
#                 entry.config(state="normal")
#                 entry.delete(0, tk.END)

#             values = tree.item(selected_items[0])['values']
#             for i, col in enumerate(columns):
#                 entries[col].insert(0, values[i])
#             entries[pk_column].config(state="readonly")
        
#         tree.bind("<<TreeviewSelect>>", on_item_select)

#         def add_record():
#             cols = [c for c in columns if "At" not in c and not (pk_is_auto and c == pk_column)]
#             values = [entries[c].get() for c in cols]
#             query = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))})"
#             if execute_query(query, tuple(values)):
#                 refresh_tree(); clear_form(); messagebox.showinfo("Success", "Menu added.")

#         def update_record():
#             if not tree.selection(): messagebox.showwarning("Warning", "Select a menu to update."); return
#             pk_val = entries[pk_column].get()
#             cols = [c for c in columns if c != pk_column and "At" not in c]
#             values = [entries[c].get() for c in cols] + [pk_val]
#             query = f"UPDATE {table_name} SET {', '.join([f'{c} = %s' for c in cols])} WHERE {pk_column} = %s"
#             if execute_query(query, tuple(values)):
#                 refresh_tree(); clear_form(); messagebox.showinfo("Success", "Menu updated.")
        
#         def delete_record():
#             if not tree.selection(): messagebox.showwarning("Warning", "Select a menu to delete."); return
#             pk_val = entries[pk_column].get()
#             if messagebox.askyesno("Confirm", f"Delete menu {pk_val}? This will also delete all its items from MenuFood (due to CASCADE)."):
#                 if execute_query(f"DELETE FROM {table_name} WHERE {pk_column}=%s", (pk_val,)):
#                     refresh_tree(); clear_form(); messagebox.showinfo("Success", "Menu deleted.")
        
#         btn_frame = ttk.Frame(self.content_frame)
#         btn_frame.pack(fill=tk.X, pady=10)
#         ttk.Button(btn_frame, text="Add Menu", command=add_record, bootstyle="success").pack(side=tk.LEFT, padx=5, ipadx=10)
#         ttk.Button(btn_frame, text="Update Menu", command=update_record, bootstyle="info").pack(side=tk.LEFT, padx=5, ipadx=10)
#         ttk.Button(btn_frame, text="Delete Menu", command=delete_record, bootstyle="danger").pack(side=tk.LEFT, padx=5, ipadx=10)
#         ttk.Button(btn_frame, text="Clear Form", command=clear_form, bootstyle="secondary").pack(side=tk.RIGHT, padx=5, ipadx=10)
        
#         extra_btn_frame = ttk.Frame(self.content_frame)
#         extra_btn_frame.pack(fill=tk.X, pady=(10,0))
        
#         def open_editor():
#             selected_items = tree.selection()
#             if not selected_items:
#                 messagebox.showwarning("No Selection", "Please select a menu from the list to edit its items.")
#                 return
            
#             values = tree.item(selected_items[0])['values']
#             menu_id = values[columns.index('MenuID')]
#             menu_date = values[columns.index('MenuDate')]
#             self.open_menu_editor_window(menu_id, menu_date)

#         ttk.Button(extra_btn_frame, text="Edit Items on Selected Menu", command=open_editor, bootstyle="success").pack(fill=tk.X, ipady=5)

#         refresh_tree(); clear_form()

#     def open_menu_editor_window(self, menu_id, menu_date):
#         """A dual-list window to manage items on a specific menu."""
#         editor_win = ttk.Toplevel(self)
#         editor_win.title(f"Edit Items for Menu: {menu_date} (ID: {menu_id})")
#         editor_win.geometry("800x600")

#         main_frame = ttk.Frame(editor_win, padding=20)
#         main_frame.pack(fill=BOTH, expand=True)

#         available_frame = ttk.Frame(main_frame); available_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
#         ttk.Label(available_frame, text="Available Food Items", font=("Helvetica", 12, "bold")).pack(pady=5)
#         available_list = tk.Listbox(available_frame, selectmode=EXTENDED, exportselection=False, height=20, font=("Helvetica", 11))
#         available_list.pack(fill=BOTH, expand=True)

#         btn_frame = ttk.Frame(main_frame); btn_frame.pack(side=LEFT, fill=Y, padx=10)
#         add_btn = ttk.Button(btn_frame, text=">>", bootstyle="success-outline")
#         add_btn.pack(pady=20, anchor='s')
#         remove_btn = ttk.Button(btn_frame, text="<<", bootstyle="danger-outline")
#         remove_btn.pack(pady=20, anchor='n')

#         on_menu_frame = ttk.Frame(main_frame); on_menu_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)
#         ttk.Label(on_menu_frame, text="Items on This Menu", font=("Helvetica", 12, "bold")).pack(pady=5)
#         on_menu_list = tk.Listbox(on_menu_frame, selectmode=EXTENDED, exportselection=False, height=20, font=("Helvetica", 11))
#         on_menu_list.pack(fill=BOTH, expand=True)

#         available_items_map = {}
#         on_menu_items_map = {}

#         def refresh_lists():
#             available_list.delete(0, tk.END)
#             on_menu_list.delete(0, tk.END)
#             available_items_map.clear()
#             on_menu_items_map.clear()

#             on_menu_data = execute_read_query(
#                 "SELECT fi.ItemID, fi.ItemName FROM FoodItem fi JOIN MenuFood mf ON fi.ItemID = mf.ItemID WHERE mf.MenuID = %s", (menu_id,)
#             )
#             on_menu_ids = []
#             if on_menu_data:
#                 for item_id, item_name in on_menu_data:
#                     display_text = f"{item_id}: {item_name}"
#                     on_menu_list.insert(tk.END, display_text)
#                     on_menu_items_map[display_text] = item_id
#                     on_menu_ids.append(item_id)

#             all_items_data = execute_read_query("SELECT ItemID, ItemName FROM FoodItem")
#             if all_items_data:
#                 for item_id, item_name in all_items_data:
#                     if item_id not in on_menu_ids:
#                         display_text = f"{item_id}: {item_name}"
#                         available_list.insert(tk.END, display_text)
#                         available_items_map[display_text] = item_id

#         def add_items():
#             selected_texts = [available_list.get(i) for i in available_list.curselection()]
#             if not selected_texts: return
            
#             for text in selected_texts:
#                 item_id = available_items_map.get(text)
#                 if item_id:
#                     execute_query("INSERT INTO MenuFood (MenuID, ItemID) VALUES (%s, %s)", (menu_id, item_id))
#             refresh_lists()

#         def remove_items():
#             selected_texts = [on_menu_list.get(i) for i in on_menu_list.curselection()]
#             if not selected_texts: return
            
#             for text in selected_texts:
#                 item_id = on_menu_items_map.get(text)
#                 if item_id:
#                     execute_query("DELETE FROM MenuFood WHERE MenuID = %s AND ItemID = %s", (menu_id, item_id))
#             refresh_lists()
            
#         add_btn.config(command=add_items)
#         remove_btn.config(command=remove_items)
        
#         refresh_lists()

#     # --- Full implementations for other UI sections (Unchanged) ---
    
#     def show_reports_ui(self):
#         self.clear_content_frame()
#         ttk.Label(self.content_frame, text="Reports & Advanced Queries", font=("Helvetica", 20, "bold")).pack(pady=10, anchor='w')
#         notebook = ttk.Notebook(self.content_frame, bootstyle="primary")
#         notebook.pack(expand=True, fill="both", pady=10)

#         def create_query_tab(parent, title, desc, query, cols, data=None):
#             tab = ttk.Frame(parent, padding=10)
#             parent.add(tab, text=title)
#             ttk.Label(tab, text=desc, wraplength=700, font=("Helvetica", 10, "italic")).pack(fill='x', pady=(0,10), anchor='w')
#             tree = ttk.Treeview(tab, columns=cols, show='headings', bootstyle="info")
#             for c in cols: tree.heading(c, text=c); tree.column(c, anchor="w", width=150)
#             tree.pack(expand=True, fill="both")
#             records = execute_read_query(query, data)
#             if records:
#                 for r in records: tree.insert("", "end", values=r)

#         create_query_tab(notebook, "Aggregate", "Calculates average rating and review counts for each food item.", "SELECT * FROM ItemRatings", ['ItemID', 'ItemName', 'NumReviews', 'AvgRating'])
#         join_q = "SELECT s.Name, fi.ItemName, o.OrderDate FROM Student s JOIN Orders o ON s.SRN = o.SRN JOIN Order_Items oi ON o.OrderID = oi.OrderID JOIN FoodItem fi ON oi.ItemID = fi.ItemID WHERE fi.ItemName LIKE %s"
#         create_query_tab(notebook, "Join", "Finds students who ordered a specific item (e.g., Masala Dosa).", join_q, ['Student', 'Item', 'Date'], ('%Dosa%',))
#         nested_q = "SELECT ItemName, Price FROM FoodItem WHERE ItemID NOT IN (SELECT DISTINCT ItemID FROM Review)"
#         create_query_tab(notebook, "Nested", "Finds all food items that have never been reviewed.", nested_q, ['ItemName', 'Price'])
#         total_spent_q = """
#             SELECT s.SRN, s.Name, SUM(fi.Price * oi.Quantity) AS TotalAmountSpent
#             FROM Student s
#             JOIN Orders o ON s.SRN = o.SRN
#             JOIN Order_Items oi ON o.OrderID = oi.OrderID
#             JOIN FoodItem fi ON oi.ItemID = fi.ItemID
#             GROUP BY s.SRN, s.Name
#             ORDER BY TotalAmountSpent DESC
#         """
#         create_query_tab(notebook, "Student Totals", "Shows the total amount spent by each student, from highest to lowest.", total_spent_q, ['SRN', 'Name', 'Total Spent'])


#     def show_transaction_ui(self):
#         self.clear_content_frame()
#         frame = ttk.Frame(self.content_frame, padding="20")
#         frame.pack(expand=True, fill="both")
#         ttk.Label(frame, text="Place a New Order (Transaction)", font=("Helvetica", 18, "bold"), bootstyle="primary").pack(pady=10)
#         form = ttk.Frame(frame); form.pack(fill=tk.X, pady=10)
#         ttk.Label(form, text="Student SRN:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
#         srn = ttk.Entry(form); srn.grid(row=0, column=1, padx=5, pady=5, sticky='ew'); srn.insert(0, "PESU2021001") # Assumes this SRN exists
#         items_frame = ttk.Frame(frame); items_frame.pack(fill=tk.BOTH, expand=True, pady=10)
#         ttk.Label(items_frame, text="Items (ItemID, Quantity) - one per line:").pack(anchor='w')
#         items = tk.Text(items_frame, height=5, width=30, font=("Courier New", 10)); items.pack(fill='both', expand=True); items.insert(tk.END, "1, 2\n5, 1\n") # Assumes these ItemIDs exist

#         def place_order():
#             # Students can only place orders for themselves (A good future enhancement)
#             # For now, we assume the SRN field is correct
            
#             if not (srn.get() and items.get(1.0, tk.END).strip()): messagebox.showerror("Error", "All fields required."); return
#             try:
#                 db_connection.start_transaction()
#                 cursor = db_connection.cursor()
#                 cursor.execute("INSERT INTO Orders (SRN) VALUES (%s)", (srn.get(),))
#                 order_id = cursor.lastrowid
#                 for line in items.get(1.0, tk.END).strip().split('\n'):
#                     item_id, qty = map(str.strip, line.split(','))
#                     cursor.execute("INSERT INTO Order_Items (OrderID, ItemID, Quantity) VALUES (%s, %s, %s)", (order_id, item_id, qty))
#                 db_connection.commit()
#                 messagebox.showinfo("Success", f"Transaction Successful! OrderID: {order_id}")
#             except Exception as e:
#                 db_connection.rollback()
#                 messagebox.showerror("Failed", f"Transaction Rolled Back.\nError: {e}")
#         ttk.Button(frame, text="Submit Order", command=place_order, bootstyle="success").pack(pady=20, fill='x', ipady=5)

#     def show_admin_ui(self):
#         # This function is admin-only, so no role checks needed inside
#         self.clear_content_frame()
#         ttk.Label(self.content_frame, text="Database Administration", font=("Helvetica", 20, "bold")).pack(pady=10, anchor='w')
#         notebook = ttk.Notebook(self.content_frame); notebook.pack(expand=True, fill="both", pady=10)
#         tp_frame = ttk.Frame(notebook, padding="20"); notebook.add(tp_frame, text="Triggers, Procedures & Functions")
#         user_frame = ttk.Frame(notebook, padding="20"); notebook.add(user_frame, text="User Management")

#         # --- Triggers, Procedures, Functions Part ---
        
#         def create_trigger():
#             execute_query("DROP TRIGGER IF EXISTS before_review_update")
#             if execute_query("CREATE TRIGGER before_review_update BEFORE UPDATE ON Review FOR EACH ROW SET NEW.ReviewDate = NOW()"):
#                 messagebox.showinfo("Success", "Trigger 'before_review_update' created.")
        
#         def create_procedure():
#             execute_query("DROP PROCEDURE IF EXISTS GetStudentReviews")
#             if execute_query("CREATE PROCEDURE GetStudentReviews(IN s_srn VARCHAR(15)) BEGIN SELECT * FROM Review WHERE SRN = s_srn; END;"):
#                 messagebox.showinfo("Success", "Procedure 'GetStudentReviews' created.")

#         def create_function():
#             execute_query("DROP FUNCTION IF EXISTS GetStudentTotalSpent")
#             func_query = """
#             CREATE FUNCTION GetStudentTotalSpent(s_srn VARCHAR(15))
#             RETURNS DECIMAL(10, 2)
#             DETERMINISTIC
#             READS SQL DATA
#             BEGIN
#                 DECLARE total DECIMAL(10, 2);
#                 SELECT SUM(fi.Price * oi.Quantity)
#                 INTO total
#                 FROM Orders o
#                 JOIN Order_Items oi ON o.OrderID = oi.OrderID
#                 JOIN FoodItem fi ON oi.ItemID = fi.ItemID
#                 WHERE o.SRN = s_srn;
#                 RETURN IFNULL(total, 0.00);
#             END;
#             """
#             if execute_query(func_query):
#                 messagebox.showinfo("Success", "Function 'GetStudentTotalSpent' created.")
            
#         def call_procedure():
#             srn = simpledialog.askstring("Input", "Enter Student SRN to get reviews for:")
#             if not srn: return
#             reviews = execute_read_query("CALL GetStudentReviews(%s)", (srn,))
#             if reviews is not None:
#                 win = ttk.Toplevel(self); win.title(f"Reviews for {srn}")
#                 cols = ['ID', 'SRN', 'ItemID', 'Rating', 'Feedback', 'Date']
#                 tree = ttk.Treeview(win, columns=cols, show='headings'); tree.pack(expand=True, fill='both', padx=10, pady=10)
#                 for c in cols: tree.heading(c, text=c)
#                 if reviews:
#                     for r in reviews: tree.insert("", "end", values=r)
#                 else:
#                     ttk.Label(win, text="No reviews found.").pack(pady=20)
#             else:
#                  messagebox.showerror("Error", "Could not call procedure.")

#         def call_function():
#             srn = simpledialog.askstring("Input", "Enter Student SRN to get total spent:")
#             if not srn: return
            
#             query = "SELECT GetStudentTotalSpent(%s)"
#             result = execute_read_query(query, (srn,))
            
#             if result:
#                 total_spent = result[0][0]
#                 messagebox.showinfo("Result", f"Total amount spent by {srn}:\n\n₹ {total_spent}")
#             else:
#                 messagebox.showerror("Error", "Could not retrieve total.")

#         ttk.Button(tp_frame, text="Create/Reset Trigger", command=create_trigger, bootstyle="info").pack(pady=10, fill='x')
#         ttk.Button(tp_frame, text="Create/Reset Procedure", command=create_procedure, bootstyle="info").pack(pady=10, fill='x')
#         ttk.Button(tp_frame, text="Create/Reset Function (TotalSpent)", command=create_function, bootstyle="info").pack(pady=10, fill='x')
        
#         ttk.Separator(tp_frame).pack(fill='x', pady=10)
        
#         ttk.Button(tp_frame, text="Call GetStudentReviews Procedure", command=call_procedure, bootstyle="success").pack(pady=10, fill='x')
#         ttk.Button(tp_frame, text="Call GetStudentTotalSpent Function", command=call_function, bootstyle="success").pack(pady=10, fill='x')
        
#         # --- User Management Part (With Roles) ---
#         ttk.Label(user_frame, text="Create New DB User", font=("Helvetica", 16, "bold")).pack(pady=10)
        
#         ttk.Label(user_frame, text="Select Role:").pack(pady=(10,0), anchor='w')
#         self.role_var = tk.StringVar(value="Admin") # Default to Admin
#         role_combo = ttk.Combobox(user_frame, textvariable=self.role_var, values=["Admin", "Student"], state="readonly")
#         role_combo.pack(pady=5, fill='x')

#         ttk.Label(user_frame, text="Username:").pack(pady=(10,0), anchor='w')
#         user_entry = ttk.Entry(user_frame); user_entry.pack(pady=5, fill='x')
#         ttk.Label(user_frame, text="Password:").pack(pady=(10,0), anchor='w')
#         pass_entry = ttk.Entry(user_frame, show="*"); pass_entry.pack(pady=5, fill='x')
        
#         def create_user():
#             username, password, role = user_entry.get(), pass_entry.get(), self.role_var.get()
#             if not (username and password): messagebox.showerror("Error", "Fields cannot be empty."); return
            
#             try:
#                 execute_query(f"DROP USER IF EXISTS '{username}'@'localhost'")
#                 execute_query(f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}'")
                
#                 if role == "Admin":
#                      execute_query(f"GRANT ALL PRIVILEGES ON cafeteria_db.* TO '{username}'@'localhost'")
                
#                 elif role == "Student":
#                      execute_query(f"GRANT SELECT ON cafeteria_db.FoodItem TO '{username}'@'localhost'")
#                      execute_query(f"GRANT SELECT ON cafeteria_db.Menu TO '{username}'@'localhost'")
#                      execute_query(f"GRANT SELECT ON cafeteria_db.MenuFood TO '{username}'@'localhost'")
#                      execute_query(f"GRANT SELECT ON cafeteria_db.ItemRatings TO '{username}'@'localhost'")
#                      execute_query(f"GRANT SELECT (SRN, Name) ON cafeteria_db.Student TO '{username}'@'localhost'")
#                      execute_query(f"GRANT SELECT, INSERT, UPDATE ON cafeteria_db.Review TO '{username}'@'localhost'") # <<< CHANGED
#                      execute_query(f"GRANT INSERT ON cafeteria_db.Orders TO '{username}'@'localhost'")
#                      execute_query(f"GRANT INSERT ON cafeteria_db.Order_Items TO '{username}'@'localhost'")
                     
#                 messagebox.showinfo("Success", f"User '{username}' created with role: {role}.")
#             except Exception as e: 
#                 messagebox.showerror("Error", f"Could not create user: {e}")
                
#         ttk.Button(user_frame, text="Create User with Role", command=create_user, bootstyle="success").pack(pady=20, fill='x')

# # --- MAIN EXECUTION ---
# if __name__ == "__main__":
#     app = CafeteriaApp()
#     app.mainloop()


















# # --- PESU Cafeteria Menu & Feedback Tracker ---
# # FINAL VERSION - Includes Login/Logout, Role-Based UI, & Auto-Reconnect

# import tkinter as tk
# from tkinter import messagebox, simpledialog
# import ttkbootstrap as ttk
# from ttkbootstrap.constants import *
# import mysql.connector
# from mysql.connector import Error

# # --- Global Connection Object ---
# db_connection = None

# # --- DATABASE HELPER FUNCTIONS (WITH AUTO-RECONNECT) ---

# def connect_to_database(username, password):
#     """Establishes the global database connection for login."""
#     global db_connection
#     try:
#         # Close any existing connection
#         if db_connection and db_connection.is_connected():
#             db_connection.close()
            
#         db_connection = mysql.connector.connect(
#             host='localhost', database='cafeteria_db', user=username, password=password
#         )
#         if db_connection.is_connected():
#             return True
#     except Error as e:
#         messagebox.showerror("Connection Error", f"The error '{e}' occurred")
#         return False

# def execute_query(query, data=None):
#     """For INSERT, UPDATE, DELETE queries."""
#     try:
#         # --- FIX: Ping server to ensure connection is alive ---
#         # This will automatically reconnect if the connection was dropped
#         db_connection.ping(reconnect=True, attempts=3, delay=1)
#     except Error as e:
#         # If ping itself fails (e.g., server is truly down)
#         messagebox.showerror("Connection Error", f"Connection lost and could not reconnect: {e}")
#         return False

#     if not db_connection or not db_connection.is_connected():
#         messagebox.showerror("Error", "Database not connected.")
#         return False
        
#     cursor = db_connection.cursor()
#     try:
#         cursor.execute(query, data)
#         db_connection.commit()
#         cursor.close()
#         return True
#     except Error as e:
#         db_connection.rollback()
#         messagebox.showerror("Query Error", str(e))
#         cursor.close()
#         return False

# def execute_read_query(query, data=None):
#     """For SELECT queries."""
#     try:
#         # --- FIX: Ping server to ensure connection is alive ---
#         db_connection.ping(reconnect=True, attempts=3, delay=1)
#     except Error as e:
#         messagebox.showerror("Connection Error", f"Connection lost and could not reconnect: {e}")
#         return None

#     if not db_connection or not db_connection.is_connected():
#         messagebox.showerror("Error", "Database not connected.")
#         return None
        
#     cursor = db_connection.cursor(buffered=True)
#     try:
#         cursor.execute(query, data)
#         results = cursor.fetchall()
#         cursor.close()
#         return results
#     except Error as e:
#         messagebox.showerror("Read Query Error", str(e))
#         cursor.close()
#         return None

# # --- MAIN APPLICATION CLASS ---

# class CafeteriaApp(ttk.Window):
#     def __init__(self):
#         super().__init__(themename="flatly")
#         self.title("PESU Cafeteria Management System")
#         self.geometry("1200x800")
        
#         self.current_username = None
#         self.current_user_role = None # "Admin" or "Student"
        
#         self.show_login_screen()

#     def show_login_screen(self):
#         """Displays the initial username/password prompt."""
#         for widget in self.winfo_children(): widget.destroy()
        
#         # Reset user state
#         self.current_username = None
#         self.current_user_role = None
#         global db_connection
#         if db_connection and db_connection.is_connected():
#             db_connection.close()
#             db_connection = None
        
#         login_frame = ttk.Frame(self, padding="50")
#         login_frame.pack(expand=True)
        
#         ttk.Label(login_frame, text="Cafeteria Login", font=("Helvetica", 18, "bold")).pack(pady=10)
        
#         ttk.Label(login_frame, text="Username:", font=("Helvetica", 12)).pack(pady=(10,0))
#         self.user_entry = ttk.Entry(login_frame, width=30)
#         self.user_entry.pack(pady=5)
#         self.user_entry.insert(0, "root") # Default to root for easy testing

#         ttk.Label(login_frame, text="Password:", font=("Helvetica", 12)).pack(pady=(10,0))
#         self.password_entry = ttk.Entry(login_frame, show="*", width=30)
#         self.password_entry.pack(pady=5)
        
#         self.password_entry.bind('<Return>', self.login)
#         ttk.Button(login_frame, text="Connect", command=self.login, bootstyle="success").pack(pady=20, ipadx=20)
        
#         self.user_entry.focus_set()

#     def login(self, event=None):
#         """Handles the login attempt and role detection."""
#         username = self.user_entry.get()
#         password = self.password_entry.get()
        
#         if not username or not password:
#             messagebox.showerror("Error", "Username and Password are required.")
#             return

#         if connect_to_database(username, password):
#             self.current_username = username
#             self.determine_user_role() 
            
#             messagebox.showinfo("Success", f"Welcome, {username}!\nYou are logged in as: {self.current_user_role}")
#             self.create_main_ui()
#         else:
#             self.password_entry.delete(0, tk.END)

#     def determine_user_role(self):
#         """Checks user grants to determine their role."""
#         if self.current_username == 'root':
#             self.current_user_role = "Admin"
#             return

#         grants = execute_read_query(f"SHOW GRANTS FOR '{self.current_username}'@'localhost'")
#         if grants:
#             grant_str = str(grants)
#             if "ALL PRIVILEGES" in grant_str or "UPDATE" in grant_str.upper() and "STAFF" in grant_str.upper():
#                 self.current_user_role = "Admin"
#             elif "INSERT" in grant_str.upper() and "ORDERS" in grant_str.upper():
#                 self.current_user_role = "Student"
#             else:
#                 self.current_user_role = "Student" 
#         else:
#             self.current_user_role = "Student"

#     def logout(self):
#         """Logs out the current user and returns to login screen."""
#         self.show_login_screen()

#     def create_main_ui(self):
#         """Creates the main dashboard UI based on user role."""
#         for widget in self.winfo_children(): widget.destroy()
        
#         main_pane = ttk.PanedWindow(self, orient=HORIZONTAL)
#         main_pane.pack(fill=BOTH, expand=True)

#         nav_frame = ttk.Frame(main_pane, padding=10)
#         main_pane.add(nav_frame, weight=1)

#         self.content_frame = ttk.Frame(main_pane, padding=20)
#         main_pane.add(self.content_frame, weight=4)

#         ttk.Label(nav_frame, text=f"Dashboard ({self.current_user_role})", font=("Helvetica", 16, "bold")).pack(pady=10, padx=10)
        
#         # --- ROLE-BASED BUTTONS ---
        
#         ttk.Button(nav_frame, text="Students", command=lambda: self.show_crud_ui("Student", ['SRN', 'Name', 'Email', 'Phone', 'CreatedAt']), bootstyle="info-outline").pack(fill=tk.X, pady=4)
#         ttk.Button(nav_frame, text="Food Items", command=lambda: self.show_crud_ui("FoodItem", ['ItemID', 'ItemName', 'Category', 'Price', 'IsActive'], pk_is_auto=True), bootstyle="info-outline").pack(fill=tk.X, pady=4)
#         ttk.Button(nav_frame, text="Reviews", command=lambda: self.show_crud_ui("Review", ['ReviewID', 'SRN', 'ItemID', 'Rating', 'Feedback', 'ReviewDate'], pk_is_auto=True), bootstyle="info-outline").pack(fill=tk.X, pady=4)

#         if self.current_user_role == "Admin":
#             ttk.Button(nav_frame, text="Staff", command=lambda: self.show_crud_ui("Staff", ['StaffID', 'Name', 'Email', 'Role', 'CreatedAt'], pk_is_auto=True), bootstyle="info-outline").pack(fill=tk.X, pady=4)
#             ttk.Button(nav_frame, text="Menus", command=lambda: self.show_menu_crud_ui(), bootstyle="info-outline").pack(fill=tk.X, pady=4)

#         ttk.Separator(nav_frame).pack(fill='x', pady=10)
        
#         ttk.Button(nav_frame, text="Place Order", command=self.show_transaction_ui, bootstyle="success-outline").pack(fill=tk.X, pady=4)
#         ttk.Button(nav_frame, text="Reports & Queries", command=self.show_reports_ui, bootstyle="success-outline").pack(fill=tk.X, pady=4)
        
#         if self.current_user_role == "Admin":
#             ttk.Separator(nav_frame).pack(fill='x', pady=10)
#             ttk.Button(nav_frame, text="DB Admin", command=self.show_admin_ui, bootstyle="warning-outline").pack(fill=tk.X, pady=4)
        
#         ttk.Separator(nav_frame).pack(fill='x', pady=40)
#         ttk.Button(nav_frame, text="Log Out", command=self.logout, bootstyle="danger").pack(fill=tk.X, pady=4)
        
#         self.show_crud_ui("Student", ['SRN', 'Name', 'Email', 'Phone', 'CreatedAt'])

#     def clear_content_frame(self):
#         """Clears the main content area."""
#         for widget in self.content_frame.winfo_children():
#             widget.destroy()

#     def show_crud_ui(self, table_name, columns, pk_is_auto=False):
#         """The generic UI, now with role-based button disabling."""
#         self.clear_content_frame()
#         pk_column = columns[0]
        
#         is_student = self.current_user_role == "Student"
        
#         can_add = True
#         can_update = True
#         can_delete = True
        
#         if is_student:
#             can_add = False
#             can_update = False
#             can_delete = False
            
#             if table_name == "Review":
#                 can_add = True
#                 can_update = True
#                 can_delete = False 

#         ttk.Label(self.content_frame, text=f"Manage {table_name}", font=("Helvetica", 20, "bold")).pack(pady=10, anchor="w")
        
#         tree_frame = ttk.Frame(self.content_frame)
#         tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
#         tree = ttk.Treeview(tree_frame, columns=columns, show='headings', bootstyle="primary")
#         for col in columns:
#             tree.heading(col, text=col.replace('_', ' ').title())
#             tree.column(col, width=120, anchor="w")
        
#         scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
#         tree.configure(yscrollcommand=scrollbar.set)
#         tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#         def refresh_tree():
#             for item in tree.get_children(): tree.delete(item)
#             records = execute_read_query(f"SELECT * FROM {table_name}")
#             if records:
#                 for record in records:
#                     tree.insert("", "end", values=[str(v) if v is not None else "" for v in record])

#         form_frame = ttk.Frame(self.content_frame, padding=10, bootstyle="light")
#         form_frame.pack(fill=tk.X, pady=10)
        
#         entries = {}
#         for i, col in enumerate(columns):
#             ttk.Label(form_frame, text=f"{col}:").grid(row=i, column=0, padx=5, pady=5, sticky='e')
#             entry = ttk.Entry(form_frame, width=40)
#             entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
#             entries[col] = entry

#         def clear_form():
#             tree.selection_remove(tree.selection())
#             for col, entry in entries.items():
#                 entry.config(state="normal")
#                 entry.delete(0, tk.END)
#             if pk_is_auto:
#                 entries[pk_column].insert(0, "(Auto-Generated)")
#                 entries[pk_column].config(state="readonly")
#             else:
#                 entries[pk_column].focus_set()

#         def on_item_select(event):
#             selected_items = tree.selection()
#             if not selected_items: return
            
#             for col, entry in entries.items():
#                 entry.config(state="normal")
#                 entry.delete(0, tk.END)

#             values = tree.item(selected_items[0])['values']
#             for i, col in enumerate(columns):
#                 entries[col].insert(0, values[i])
            
#             if can_update:
#                 entries[pk_column].config(state="readonly")
#             else:
#                 for entry in entries.values():
#                     entry.config(state="readonly")
        
#         tree.bind("<<TreeviewSelect>>", on_item_select)

#         def add_record():
#             cols = [c for c in columns if "At" not in c and not (pk_is_auto and c == pk_column)]
#             values = [entries[c].get() for c in cols]
#             query = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))})"
#             if execute_query(query, tuple(values)):
#                 refresh_tree(); clear_form(); messagebox.showinfo("Success", "Record added.")

#         def update_record():
#             if not tree.selection(): messagebox.showwarning("Warning", "Select a record to update."); return
#             pk_val = entries[pk_column].get()
#             cols = [c for c in columns if c != pk_column and "At" not in c]
#             values = [entries[c].get() for c in cols] + [pk_val]
#             query = f"UPDATE {table_name} SET {', '.join([f'{c} = %s' for c in cols])} WHERE {pk_column} = %s"
#             if execute_query(query, tuple(values)):
#                 refresh_tree(); clear_form(); messagebox.showinfo("Success", "Record updated.")
        
#         def delete_record():
#             if not tree.selection(): messagebox.showwarning("Warning", "Select a record to delete."); return
#             pk_val = entries[pk_column].get()
#             if messagebox.askyesno("Confirm", f"Delete record {pk_val}?"):
#                 if execute_query(f"DELETE FROM {table_name} WHERE {pk_column}=%s", (pk_val,)):
#                     refresh_tree(); clear_form(); messagebox.showinfo("Success", "Record deleted.")
        
#         btn_frame = ttk.Frame(self.content_frame)
#         btn_frame.pack(fill=tk.X, pady=10)
        
#         add_btn = ttk.Button(btn_frame, text="Add", command=add_record, bootstyle="success")
#         add_btn.pack(side=tk.LEFT, padx=5, ipadx=10)
#         if not can_add: add_btn.config(state="disabled")
            
#         update_btn = ttk.Button(btn_frame, text="Update", command=update_record, bootstyle="info")
#         update_btn.pack(side=tk.LEFT, padx=5, ipadx=10)
#         if not can_update: update_btn.config(state="disabled")

#         delete_btn = ttk.Button(btn_frame, text="Delete", command=delete_record, bootstyle="danger")
#         delete_btn.pack(side=tk.LEFT, padx=5, ipadx=10)
#         if not can_delete: delete_btn.config(state="disabled")

#         ttk.Button(btn_frame, text="Clear Form", command=clear_form, bootstyle="secondary").pack(side=tk.RIGHT, padx=5, ipadx=10)

#         refresh_tree(); clear_form()
    
#     # --- Custom UI for Menu Management (Admin Only) ---
    
#     def show_menu_crud_ui(self):
#         self.clear_content_frame()
#         table_name = "Menu"
#         columns = ['MenuID', 'MenuDate', 'StaffID', 'Notes', 'CreatedAt']
#         pk_column = 'MenuID'
#         pk_is_auto = True

#         ttk.Label(self.content_frame, text=f"Manage {table_name}", font=("Helvetica", 20, "bold")).pack(pady=10, anchor="w")
        
#         tree_frame = ttk.Frame(self.content_frame)
#         tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
#         tree = ttk.Treeview(tree_frame, columns=columns, show='headings', bootstyle="primary")
#         for col in columns:
#             tree.heading(col, text=col.replace('_', ' ').title())
#             tree.column(col, width=120, anchor="w")
        
#         scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
#         tree.configure(yscrollcommand=scrollbar.set)
#         tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#         def refresh_tree():
#             for item in tree.get_children(): tree.delete(item)
#             records = execute_read_query(f"SELECT * FROM {table_name}")
#             if records:
#                 for record in records:
#                     tree.insert("", "end", values=[str(v) if v is not None else "" for v in record])

#         form_frame = ttk.Frame(self.content_frame, padding=10, bootstyle="light")
#         form_frame.pack(fill=tk.X, pady=10)
        
#         entries = {}
#         for i, col in enumerate(columns):
#             ttk.Label(form_frame, text=f"{col}:").grid(row=i, column=0, padx=5, pady=5, sticky='e')
#             entry = ttk.Entry(form_frame, width=40)
#             entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
#             entries[col] = entry

#         def clear_form():
#             tree.selection_remove(tree.selection())
#             for col, entry in entries.items():
#                 entry.config(state="normal")
#                 entry.delete(0, tk.END)
#             if pk_is_auto:
#                 entries[pk_column].insert(0, "(Auto-Generated)")
#                 entries[pk_column].config(state="readonly")
#             else:
#                 entries[pk_column].focus_set()

#         def on_item_select(event):
#             selected_items = tree.selection()
#             if not selected_items: return
            
#             for col, entry in entries.items():
#                 entry.config(state="normal")
#                 entry.delete(0, tk.END)

#             values = tree.item(selected_items[0])['values']
#             for i, col in enumerate(columns):
#                 entries[col].insert(0, values[i])
#             entries[pk_column].config(state="readonly")
        
#         tree.bind("<<TreeviewSelect>>", on_item_select)

#         def add_record():
#             cols = [c for c in columns if "At" not in c and not (pk_is_auto and c == pk_column)]
#             values = [entries[c].get() for c in cols]
#             query = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))})"
#             if execute_query(query, tuple(values)):
#                 refresh_tree(); clear_form(); messagebox.showinfo("Success", "Menu added.")

#         def update_record():
#             if not tree.selection(): messagebox.showwarning("Warning", "Select a menu to update."); return
#             pk_val = entries[pk_column].get()
#             cols = [c for c in columns if c != pk_column and "At" not in c]
#             values = [entries[c].get() for c in cols] + [pk_val]
#             query = f"UPDATE {table_name} SET {', '.join([f'{c} = %s' for c in cols])} WHERE {pk_column} = %s"
#             if execute_query(query, tuple(values)):
#                 refresh_tree(); clear_form(); messagebox.showinfo("Success", "Menu updated.")
        
#         def delete_record():
#             if not tree.selection(): messagebox.showwarning("Warning", "Select a menu to delete."); return
#             pk_val = entries[pk_column].get()
#             if messagebox.askyesno("Confirm", f"Delete menu {pk_val}? This will also delete all its items from MenuFood (due to CASCADE)."):
#                 if execute_query(f"DELETE FROM {table_name} WHERE {pk_column}=%s", (pk_val,)):
#                     refresh_tree(); clear_form(); messagebox.showinfo("Success", "Menu deleted.")
        
#         btn_frame = ttk.Frame(self.content_frame)
#         btn_frame.pack(fill=tk.X, pady=10)
#         ttk.Button(btn_frame, text="Add Menu", command=add_record, bootstyle="success").pack(side=tk.LEFT, padx=5, ipadx=10)
#         ttk.Button(btn_frame, text="Update Menu", command=update_record, bootstyle="info").pack(side=tk.LEFT, padx=5, ipadx=10)
#         ttk.Button(btn_frame, text="Delete Menu", command=delete_record, bootstyle="danger").pack(side=tk.LEFT, padx=5, ipadx=10)
#         ttk.Button(btn_frame, text="Clear Form", command=clear_form, bootstyle="secondary").pack(side=tk.RIGHT, padx=5, ipadx=10)
        
#         extra_btn_frame = ttk.Frame(self.content_frame)
#         extra_btn_frame.pack(fill=tk.X, pady=(10,0))
        
#         def open_editor():
#             selected_items = tree.selection()
#             if not selected_items:
#                 messagebox.showwarning("No Selection", "Please select a menu from the list to edit its items.")
#                 return
            
#             values = tree.item(selected_items[0])['values']
#             menu_id = values[columns.index('MenuID')]
#             menu_date = values[columns.index('MenuDate')]
#             self.open_menu_editor_window(menu_id, menu_date)

#         ttk.Button(extra_btn_frame, text="Edit Items on Selected Menu", command=open_editor, bootstyle="success").pack(fill=tk.X, ipady=5)

#         refresh_tree(); clear_form()

#     def open_menu_editor_window(self, menu_id, menu_date):
#         """A dual-list window to manage items on a specific menu."""
#         editor_win = ttk.Toplevel(self)
#         editor_win.title(f"Edit Items for Menu: {menu_date} (ID: {menu_id})")
#         editor_win.geometry("800x600")

#         main_frame = ttk.Frame(editor_win, padding=20)
#         main_frame.pack(fill=BOTH, expand=True)

#         available_frame = ttk.Frame(main_frame); available_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
#         ttk.Label(available_frame, text="Available Food Items", font=("Helvetica", 12, "bold")).pack(pady=5)
#         available_list = tk.Listbox(available_frame, selectmode=EXTENDED, exportselection=False, height=20, font=("Helvetica", 11))
#         available_list.pack(fill=BOTH, expand=True)

#         btn_frame = ttk.Frame(main_frame); btn_frame.pack(side=LEFT, fill=Y, padx=10)
#         add_btn = ttk.Button(btn_frame, text=">>", bootstyle="success-outline")
#         add_btn.pack(pady=20, anchor='s')
#         remove_btn = ttk.Button(btn_frame, text="<<", bootstyle="danger-outline")
#         remove_btn.pack(pady=20, anchor='n')

#         on_menu_frame = ttk.Frame(main_frame); on_menu_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)
#         ttk.Label(on_menu_frame, text="Items on This Menu", font=("Helvetica", 12, "bold")).pack(pady=5)
#         on_menu_list = tk.Listbox(on_menu_frame, selectmode=EXTENDED, exportselection=False, height=20, font=("Helvetica", 11))
#         on_menu_list.pack(fill=BOTH, expand=True)

#         available_items_map = {}
#         on_menu_items_map = {}

#         def refresh_lists():
#             available_list.delete(0, tk.END)
#             on_menu_list.delete(0, tk.END)
#             available_items_map.clear()
#             on_menu_items_map.clear()

#             on_menu_data = execute_read_query(
#                 "SELECT fi.ItemID, fi.ItemName FROM FoodItem fi JOIN MenuFood mf ON fi.ItemID = mf.ItemID WHERE mf.MenuID = %s", (menu_id,)
#             )
#             on_menu_ids = []
#             if on_menu_data:
#                 for item_id, item_name in on_menu_data:
#                     display_text = f"{item_id}: {item_name}"
#                     on_menu_list.insert(tk.END, display_text)
#                     on_menu_items_map[display_text] = item_id
#                     on_menu_ids.append(item_id)

#             all_items_data = execute_read_query("SELECT ItemID, ItemName FROM FoodItem")
#             if all_items_data:
#                 for item_id, item_name in all_items_data:
#                     if item_id not in on_menu_ids:
#                         display_text = f"{item_id}: {item_name}"
#                         available_list.insert(tk.END, display_text)
#                         available_items_map[display_text] = item_id

#         def add_items():
#             selected_texts = [available_list.get(i) for i in available_list.curselection()]
#             if not selected_texts: return
            
#             for text in selected_texts:
#                 item_id = available_items_map.get(text)
#                 if item_id:
#                     execute_query("INSERT INTO MenuFood (MenuID, ItemID) VALUES (%s, %s)", (menu_id, item_id))
#             refresh_lists()

#         def remove_items():
#             selected_texts = [on_menu_list.get(i) for i in on_menu_list.curselection()]
#             if not selected_texts: return
            
#             for text in selected_texts:
#                 item_id = on_menu_items_map.get(text)
#                 if item_id:
#                     execute_query("DELETE FROM MenuFood WHERE MenuID = %s AND ItemID = %s", (menu_id, item_id))
#             refresh_lists()
            
#         add_btn.config(command=add_items)
#         remove_btn.config(command=remove_items)
        
#         refresh_lists()

#     # --- Full implementations for other UI sections ---
    
#     def show_reports_ui(self):
#         self.clear_content_frame()
#         ttk.Label(self.content_frame, text="Reports & Advanced Queries", font=("Helvetica", 20, "bold")).pack(pady=10, anchor='w')
#         notebook = ttk.Notebook(self.content_frame, bootstyle="primary")
#         notebook.pack(expand=True, fill="both", pady=10)

#         def create_query_tab(parent, title, desc, query, cols, data=None):
#             tab = ttk.Frame(parent, padding=10)
#             parent.add(tab, text=title)
#             ttk.Label(tab, text=desc, wraplength=700, font=("Helvetica", 10, "italic")).pack(fill='x', pady=(0,10), anchor='w')
#             tree = ttk.Treeview(tab, columns=cols, show='headings', bootstyle="info")
#             for c in cols: tree.heading(c, text=c); tree.column(c, anchor="w", width=150)
#             tree.pack(expand=True, fill="both")
#             records = execute_read_query(query, data)
#             if records:
#                 for r in records: tree.insert("", "end", values=r)

#         create_query_tab(notebook, "Aggregate", "Calculates average rating and review counts for each food item.", "SELECT * FROM ItemRatings", ['ItemID', 'ItemName', 'NumReviews', 'AvgRating'])
#         join_q = "SELECT s.Name, fi.ItemName, o.OrderDate FROM Student s JOIN Orders o ON s.SRN = o.SRN JOIN Order_Items oi ON o.OrderID = oi.OrderID JOIN FoodItem fi ON oi.ItemID = fi.ItemID WHERE fi.ItemName LIKE %s"
#         create_query_tab(notebook, "Join", "Finds students who ordered a specific item (e.g., Masala Dosa).", join_q, ['Student', 'Item', 'Date'], ('%Dosa%',))
#         nested_q = "SELECT ItemName, Price FROM FoodItem WHERE ItemID NOT IN (SELECT DISTINCT ItemID FROM Review)"
#         create_query_tab(notebook, "Nested", "Finds all food items that have never been reviewed.", nested_q, ['ItemName', 'Price'])
#         total_spent_q = """
#             SELECT s.SRN, s.Name, SUM(fi.Price * oi.Quantity) AS TotalAmountSpent
#             FROM Student s
#             JOIN Orders o ON s.SRN = o.SRN
#             JOIN Order_Items oi ON o.OrderID = oi.OrderID
#             JOIN FoodItem fi ON oi.ItemID = fi.ItemID
#             GROUP BY s.SRN, s.Name
#             ORDER BY TotalAmountSpent DESC
#         """
#         create_query_tab(notebook, "Student Totals", "Shows the total amount spent by each student, from highest to lowest.", total_spent_q, ['SRN', 'Name', 'Total Spent'])


#     def show_transaction_ui(self):
#         self.clear_content_frame()
#         frame = ttk.Frame(self.content_frame, padding="20")
#         frame.pack(expand=True, fill="both")
#         ttk.Label(frame, text="Place a New Order (Transaction)", font=("Helvetica", 18, "bold"), bootstyle="primary").pack(pady=10)
#         form = ttk.Frame(frame); form.pack(fill=tk.X, pady=10)
#         ttk.Label(form, text="Student SRN:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
#         srn = ttk.Entry(form); srn.grid(row=0, column=1, padx=5, pady=5, sticky='ew'); srn.insert(0, "PESU2021001") # Assumes this SRN exists
#         items_frame = ttk.Frame(frame); items_frame.pack(fill=tk.BOTH, expand=True, pady=10)
#         ttk.Label(items_frame, text="Items (ItemID, Quantity) - one per line:").pack(anchor='w')
#         items = tk.Text(items_frame, height=5, width=30, font=("Courier New", 10)); items.pack(fill='both', expand=True); items.insert(tk.END, "1, 2\n5, 1\n") # Assumes these ItemIDs exist

#         def place_order():
#             if not (srn.get() and items.get(1.0, tk.END).strip()): messagebox.showerror("Error", "All fields required."); return
#             try:
#                 db_connection.start_transaction()
#                 cursor = db_connection.cursor()
#                 cursor.execute("INSERT INTO Orders (SRN) VALUES (%s)", (srn.get(),))
#                 order_id = cursor.lastrowid
#                 for line in items.get(1.0, tk.END).strip().split('\n'):
#                     item_id, qty = map(str.strip, line.split(','))
#                     cursor.execute("INSERT INTO Order_Items (OrderID, ItemID, Quantity) VALUES (%s, %s, %s)", (order_id, item_id, qty))
#                 db_connection.commit()
#                 messagebox.showinfo("Success", f"Transaction Successful! OrderID: {order_id}")
#             except Exception as e:
#                 db_connection.rollback()
#                 messagebox.showerror("Failed", f"Transaction Rolled Back.\nError: {e}")
#         ttk.Button(frame, text="Submit Order", command=place_order, bootstyle="success").pack(pady=20, fill='x', ipady=5)

#     def show_admin_ui(self):
#         # This function is admin-only, so no role checks needed inside
#         self.clear_content_frame()
#         ttk.Label(self.content_frame, text="Database Administration", font=("Helvetica", 20, "bold")).pack(pady=10, anchor='w')
#         notebook = ttk.Notebook(self.content_frame); notebook.pack(expand=True, fill="both", pady=10)
#         tp_frame = ttk.Frame(notebook, padding="20"); notebook.add(tp_frame, text="Triggers, Procedures & Functions")
#         user_frame = ttk.Frame(notebook, padding="20"); notebook.add(user_frame, text="User Management")

#         # --- Triggers, Procedures, Functions Part ---
        
#         def create_trigger():
#             execute_query("DROP TRIGGER IF EXISTS before_review_update")
#             if execute_query("CREATE TRIGGER before_review_update BEFORE UPDATE ON Review FOR EACH ROW SET NEW.ReviewDate = NOW()"):
#                 messagebox.showinfo("Success", "Trigger 'before_review_update' created.")
        
#         def create_procedure():
#             execute_query("DROP PROCEDURE IF EXISTS GetStudentReviews")
#             if execute_query("CREATE PROCEDURE GetStudentReviews(IN s_srn VARCHAR(15)) BEGIN SELECT * FROM Review WHERE SRN = s_srn; END;"):
#                 messagebox.showinfo("Success", "Procedure 'GetStudentReviews' created.")

#         def create_function():
#             execute_query("DROP FUNCTION IF EXISTS GetStudentTotalSpent")
#             func_query = """
#             CREATE FUNCTION GetStudentTotalSpent(s_srn VARCHAR(15))
#             RETURNS DECIMAL(10, 2)
#             DETERMINISTIC
#             READS SQL DATA
#             BEGIN
#                 DECLARE total DECIMAL(10, 2);
#                 SELECT SUM(fi.Price * oi.Quantity)
#                 INTO total
#                 FROM Orders o
#                 JOIN Order_Items oi ON o.OrderID = oi.OrderID
#                 JOIN FoodItem fi ON oi.ItemID = fi.ItemID
#                 WHERE o.SRN = s_srn;
#                 RETURN IFNULL(total, 0.00);
#             END;
#             """
#             if execute_query(func_query):
#                 messagebox.showinfo("Success", "Function 'GetStudentTotalSpent' created.")
            
#         def call_procedure():
#             srn = simpledialog.askstring("Input", "Enter Student SRN to get reviews for:")
#             if not srn: return
#             reviews = execute_read_query("CALL GetStudentReviews(%s)", (srn,))
#             if reviews is not None:
#                 win = ttk.Toplevel(self); win.title(f"Reviews for {srn}")
#                 cols = ['ID', 'SRN', 'ItemID', 'Rating', 'Feedback', 'Date']
#                 tree = ttk.Treeview(win, columns=cols, show='headings'); tree.pack(expand=True, fill='both', padx=10, pady=10)
#                 for c in cols: tree.heading(c, text=c)
#                 if reviews:
#                     for r in reviews: tree.insert("", "end", values=r)
#                 else:
#                     ttk.Label(win, text="No reviews found.").pack(pady=20)
#             else:
#                  messagebox.showerror("Error", "Could not call procedure.")

#         def call_function():
#             srn = simpledialog.askstring("Input", "Enter Student SRN to get total spent:")
#             if not srn: return
            
#             query = "SELECT GetStudentTotalSpent(%s)"
#             result = execute_read_query(query, (srn,))
            
#             if result:
#                 total_spent = result[0][0]
#                 messagebox.showinfo("Result", f"Total amount spent by {srn}:\n\n₹ {total_spent}")
#             else:
#                 messagebox.showerror("Error", "Could not retrieve total.")

#         ttk.Button(tp_frame, text="Create/Reset Trigger", command=create_trigger, bootstyle="info").pack(pady=10, fill='x')
#         ttk.Button(tp_frame, text="Create/Reset Procedure", command=create_procedure, bootstyle="info").pack(pady=10, fill='x')
#         ttk.Button(tp_frame, text="Create/Reset Function (TotalSpent)", command=create_function, bootstyle="info").pack(pady=10, fill='x')
        
#         ttk.Separator(tp_frame).pack(fill='x', pady=10)
        
#         ttk.Button(tp_frame, text="Call GetStudentReviews Procedure", command=call_procedure, bootstyle="success").pack(pady=10, fill='x')
#         ttk.Button(tp_frame, text="Call GetStudentTotalSpent Function", command=call_function, bootstyle="success").pack(pady=10, fill='x')
        
#         # --- User Management Part (With Roles) ---
#         ttk.Label(user_frame, text="Create New DB User", font=("Helvetica", 16, "bold")).pack(pady=10)
        
#         ttk.Label(user_frame, text="Select Role:").pack(pady=(10,0), anchor='w')
#         self.role_var = tk.StringVar(value="Admin") # Default to Admin
#         role_combo = ttk.Combobox(user_frame, textvariable=self.role_var, values=["Admin", "Student"], state="readonly")
#         role_combo.pack(pady=5, fill='x')

#         ttk.Label(user_frame, text="Username:").pack(pady=(10,0), anchor='w')
#         user_entry = ttk.Entry(user_frame); user_entry.pack(pady=5, fill='x')
#         ttk.Label(user_frame, text="Password:").pack(pady=(10,0), anchor='w')
#         pass_entry = ttk.Entry(user_frame, show="*"); pass_entry.pack(pady=5, fill='x')
        
#         def create_user():
#             username, password, role = user_entry.get(), pass_entry.get(), self.role_var.get()
#             if not (username and password): messagebox.showerror("Error", "Fields cannot be empty."); return
            
#             try:
#                 execute_query(f"DROP USER IF EXISTS '{username}'@'localhost'")
#                 execute_query(f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}'")
                
#                 if role == "Admin":
#                      execute_query(f"GRANT ALL PRIVILEGES ON cafeteria_db.* TO '{username}'@'localhost'")
                
#                 elif role == "Student":
#                      execute_query(f"GRANT SELECT ON cafeteria_db.FoodItem TO '{username}'@'localhost'")
#                      execute_query(f"GRANT SELECT ON cafeteria_db.Menu TO '{username}'@'localhost'")
#                      execute_query(f"GRANT SELECT ON cafeteria_db.MenuFood TO '{username}'@'localhost'")
#                      execute_query(f"GRANT SELECT ON cafeteria_db.ItemRatings TO '{username}'@'localhost'")
#                      execute_query(f"GRANT SELECT (SRN, Name) ON cafeteria_db.Student TO '{username}'@'localhost'") # Can see names, not contact info
#                      execute_query(f"GRANT SELECT, INSERT, UPDATE ON cafeteria_db.Review TO '{username}'@'localhost'") # Can add/update reviews
#                      execute_query(f"GRANT INSERT ON cafeteria_db.Orders TO '{username}'@'localhost'")
#                      execute_query(f"GRANT INSERT ON cafeteria_db.Order_Items TO '{username}'@'localhost'")
                     
#                 messagebox.showinfo("Success", f"User '{username}' created with role: {role}.")
#             except Exception as e: 
#                 messagebox.showerror("Error", f"Could not create user: {e}")
                
#         ttk.Button(user_frame, text="Create User with Role", command=create_user, bootstyle="success").pack(pady=20, fill='x')

# # --- MAIN EXECUTION ---
# if __name__ == "__main__":
#     app = CafeteriaApp()
#     app.mainloop()





















# --- PESU Cafeteria Menu & Feedback Tracker ---
# FINAL VERSION - Includes Login/Logout, Role-Based UI, Auto-Reconnect, & View Orders

import tkinter as tk
from tkinter import messagebox, simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import mysql.connector
from mysql.connector import Error

# --- Global Connection Object ---
db_connection = None

# --- DATABASE HELPER FUNCTIONS (WITH AUTO-RECONNECT) ---

def connect_to_database(username, password):
    """Establishes the global database connection for login."""
    global db_connection
    try:
        # Close any existing connection
        if db_connection and db_connection.is_connected():
            db_connection.close()
            
        db_connection = mysql.connector.connect(
            host='localhost', database='cafeteria_db', user=username, password=password
        )
        if db_connection.is_connected():
            return True
    except Error as e:
        messagebox.showerror("Connection Error", f"The error '{e}' occurred")
        return False

def execute_query(query, data=None):
    """For INSERT, UPDATE, DELETE queries."""
    try:
        # --- FIX: Ping server to ensure connection is alive ---
        db_connection.ping(reconnect=True, attempts=3, delay=1)
    except Error as e:
        messagebox.showerror("Connection Error", f"Connection lost and could not reconnect: {e}")
        return False

    if not db_connection or not db_connection.is_connected():
        messagebox.showerror("Error", "Database not connected.")
        return False
        
    cursor = db_connection.cursor()
    try:
        cursor.execute(query, data)
        db_connection.commit()
        cursor.close()
        return True
    except Error as e:
        db_connection.rollback()
        messagebox.showerror("Query Error", str(e))
        cursor.close()
        return False

def execute_read_query(query, data=None):
    """For SELECT queries."""
    try:
        # --- FIX: Ping server to ensure connection is alive ---
        db_connection.ping(reconnect=True, attempts=3, delay=1)
    except Error as e:
        messagebox.showerror("Connection Error", f"Connection lost and could not reconnect: {e}")
        return None

    if not db_connection or not db_connection.is_connected():
        messagebox.showerror("Error", "Database not connected.")
        return None
        
    cursor = db_connection.cursor(buffered=True)
    try:
        cursor.execute(query, data)
        results = cursor.fetchall()
        cursor.close()
        return results
    except Error as e:
        messagebox.showerror("Read Query Error", str(e))
        cursor.close()
        return None

# --- MAIN APPLICATION CLASS ---

class CafeteriaApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("PESU Cafeteria Management System")
        self.geometry("1200x800")
        
        self.current_username = None
        self.current_user_role = None # "Admin" or "Student"
        
        self.show_login_screen()

    def show_login_screen(self):
        """Displays the initial username/password prompt."""
        for widget in self.winfo_children(): widget.destroy()
        
        # Reset user state
        self.current_username = None
        self.current_user_role = None
        global db_connection
        if db_connection and db_connection.is_connected():
            db_connection.close()
            db_connection = None
        
        login_frame = ttk.Frame(self, padding="50")
        login_frame.pack(expand=True)
        
        ttk.Label(login_frame, text="Cafeteria Login", font=("Helvetica", 18, "bold")).pack(pady=10)
        
        ttk.Label(login_frame, text="Username:", font=("Helvetica", 12)).pack(pady=(10,0))
        self.user_entry = ttk.Entry(login_frame, width=30)
        self.user_entry.pack(pady=5)
        self.user_entry.insert(0, "root") # Default to root for easy testing

        ttk.Label(login_frame, text="Password:", font=("Helvetica", 12)).pack(pady=(10,0))
        self.password_entry = ttk.Entry(login_frame, show="*", width=30)
        self.password_entry.pack(pady=5)
        
        self.password_entry.bind('<Return>', self.login)
        ttk.Button(login_frame, text="Connect", command=self.login, bootstyle="success").pack(pady=20, ipadx=20)
        
        self.user_entry.focus_set()

    def login(self, event=None):
        """Handles the login attempt and role detection."""
        username = self.user_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and Password are required.")
            return

        if connect_to_database(username, password):
            self.current_username = username
            self.determine_user_role() 
            
            messagebox.showinfo("Success", f"Welcome, {username}!\nYou are logged in as: {self.current_user_role}")
            self.create_main_ui()
        else:
            self.password_entry.delete(0, tk.END)

    def determine_user_role(self):
        """Checks user grants to determine their role."""
        if self.current_username == 'root':
            self.current_user_role = "Admin"
            return

        grants = execute_read_query(f"SHOW GRANTS FOR '{self.current_username}'@'localhost'")
        if grants:
            grant_str = str(grants)
            if "ALL PRIVILEGES" in grant_str or "UPDATE" in grant_str.upper() and "STAFF" in grant_str.upper():
                self.current_user_role = "Admin"
            elif "INSERT" in grant_str.upper() and "ORDERS" in grant_str.upper():
                self.current_user_role = "Student"
            else:
                self.current_user_role = "Student" 
        else:
            self.current_user_role = "Student"

    def logout(self):
        """Logs out the current user and returns to login screen."""
        self.show_login_screen()

    def create_main_ui(self):
        """Creates the main dashboard UI based on user role."""
        for widget in self.winfo_children(): widget.destroy()
        
        main_pane = ttk.PanedWindow(self, orient=HORIZONTAL)
        main_pane.pack(fill=BOTH, expand=True)

        nav_frame = ttk.Frame(main_pane, padding=10)
        main_pane.add(nav_frame, weight=1)

        self.content_frame = ttk.Frame(main_pane, padding=20)
        main_pane.add(self.content_frame, weight=4)

        ttk.Label(nav_frame, text=f"Dashboard ({self.current_user_role})", font=("Helvetica", 16, "bold")).pack(pady=10, padx=10)
        
        # --- ROLE-BASED BUTTONS ---
        
        ttk.Button(nav_frame, text="Students", command=lambda: self.show_crud_ui("Student", ['SRN', 'Name', 'Email', 'Phone', 'CreatedAt']), bootstyle="info-outline").pack(fill=tk.X, pady=4)
        ttk.Button(nav_frame, text="Food Items", command=lambda: self.show_crud_ui("FoodItem", ['ItemID', 'ItemName', 'Category', 'Price', 'IsActive'], pk_is_auto=True), bootstyle="info-outline").pack(fill=tk.X, pady=4)
        ttk.Button(nav_frame, text="Reviews", command=lambda: self.show_crud_ui("Review", ['ReviewID', 'SRN', 'ItemID', 'Rating', 'Feedback', 'ReviewDate'], pk_is_auto=True), bootstyle="info-outline").pack(fill=tk.X, pady=4)

        if self.current_user_role == "Admin":
            ttk.Button(nav_frame, text="Staff", command=lambda: self.show_crud_ui("Staff", ['StaffID', 'Name', 'Email', 'Role', 'CreatedAt'], pk_is_auto=True), bootstyle="info-outline").pack(fill=tk.X, pady=4)
            ttk.Button(nav_frame, text="Menus", command=lambda: self.show_menu_crud_ui(), bootstyle="info-outline").pack(fill=tk.X, pady=4)
            ttk.Button(nav_frame, text="Orders", command=self.show_orders_crud_ui, bootstyle="info-outline").pack(fill=tk.X, pady=4) # <<< NEW

        ttk.Separator(nav_frame).pack(fill='x', pady=10)
        
        ttk.Button(nav_frame, text="Place Order", command=self.show_transaction_ui, bootstyle="success-outline").pack(fill=tk.X, pady=4)
        ttk.Button(nav_frame, text="Reports & Queries", command=self.show_reports_ui, bootstyle="success-outline").pack(fill=tk.X, pady=4)
        
        if self.current_user_role == "Admin":
            ttk.Separator(nav_frame).pack(fill='x', pady=10)
            ttk.Button(nav_frame, text="DB Admin", command=self.show_admin_ui, bootstyle="warning-outline").pack(fill=tk.X, pady=4)
        
        ttk.Separator(nav_frame).pack(fill='x', pady=40)
        ttk.Button(nav_frame, text="Log Out", command=self.logout, bootstyle="danger").pack(fill=tk.X, pady=4)
        
        self.show_crud_ui("Student", ['SRN', 'Name', 'Email', 'Phone', 'CreatedAt'])

    def clear_content_frame(self):
        """Clears the main content area."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_crud_ui(self, table_name, columns, pk_is_auto=False):
        """The generic UI, now with role-based button disabling."""
        self.clear_content_frame()
        pk_column = columns[0]
        
        is_student = self.current_user_role == "Student"
        
        can_add = True
        can_update = True
        can_delete = True
        
        if is_student:
            can_add = False
            can_update = False
            can_delete = False
            
            if table_name == "Review":
                can_add = True
                can_update = True
                can_delete = False 

        ttk.Label(self.content_frame, text=f"Manage {table_name}", font=("Helvetica", 20, "bold")).pack(pady=10, anchor="w")
        
        tree_frame = ttk.Frame(self.content_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', bootstyle="primary")
        for col in columns:
            tree.heading(col, text=col.replace('_', ' ').title())
            tree.column(col, width=120, anchor="w")
        
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def refresh_tree():
            for item in tree.get_children(): tree.delete(item)
            records = execute_read_query(f"SELECT * FROM {table_name}")
            if records:
                for record in records:
                    tree.insert("", "end", values=[str(v) if v is not None else "" for v in record])

        form_frame = ttk.Frame(self.content_frame, padding=10, bootstyle="light")
        form_frame.pack(fill=tk.X, pady=10)
        
        entries = {}
        for i, col in enumerate(columns):
            ttk.Label(form_frame, text=f"{col}:").grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            entries[col] = entry

        def clear_form():
            tree.selection_remove(tree.selection())
            for col, entry in entries.items():
                entry.config(state="normal")
                entry.delete(0, tk.END)
            if pk_is_auto:
                entries[pk_column].insert(0, "(Auto-Generated)")
                entries[pk_column].config(state="readonly")
            else:
                entries[pk_column].focus_set()

        def on_item_select(event):
            selected_items = tree.selection()
            if not selected_items: return
            
            for col, entry in entries.items():
                entry.config(state="normal")
                entry.delete(0, tk.END)

            values = tree.item(selected_items[0])['values']
            for i, col in enumerate(columns):
                entries[col].insert(0, values[i])
            
            if can_update:
                entries[pk_column].config(state="readonly")
            else:
                for entry in entries.values():
                    entry.config(state="readonly")
        
        tree.bind("<<TreeviewSelect>>", on_item_select)

        def add_record():
            cols = [c for c in columns if "At" not in c and not (pk_is_auto and c == pk_column)]
            values = [entries[c].get() for c in cols]
            query = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))})"
            if execute_query(query, tuple(values)):
                refresh_tree(); clear_form(); messagebox.showinfo("Success", "Record added.")

        def update_record():
            if not tree.selection(): messagebox.showwarning("Warning", "Select a record to update."); return
            pk_val = entries[pk_column].get()
            cols = [c for c in columns if c != pk_column and "At" not in c]
            values = [entries[c].get() for c in cols] + [pk_val]
            query = f"UPDATE {table_name} SET {', '.join([f'{c} = %s' for c in cols])} WHERE {pk_column} = %s"
            if execute_query(query, tuple(values)):
                refresh_tree(); clear_form(); messagebox.showinfo("Success", "Record updated.")
        
        def delete_record():
            if not tree.selection(): messagebox.showwarning("Warning", "Select a record to delete."); return
            pk_val = entries[pk_column].get()
            if messagebox.askyesno("Confirm", f"Delete record {pk_val}?"):
                if execute_query(f"DELETE FROM {table_name} WHERE {pk_column}=%s", (pk_val,)):
                    refresh_tree(); clear_form(); messagebox.showinfo("Success", "Record deleted.")
        
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        add_btn = ttk.Button(btn_frame, text="Add", command=add_record, bootstyle="success")
        add_btn.pack(side=tk.LEFT, padx=5, ipadx=10)
        if not can_add: add_btn.config(state="disabled")
            
        update_btn = ttk.Button(btn_frame, text="Update", command=update_record, bootstyle="info")
        update_btn.pack(side=tk.LEFT, padx=5, ipadx=10)
        if not can_update: update_btn.config(state="disabled")

        delete_btn = ttk.Button(btn_frame, text="Delete", command=delete_record, bootstyle="danger")
        delete_btn.pack(side=tk.LEFT, padx=5, ipadx=10)
        if not can_delete: delete_btn.config(state="disabled")

        ttk.Button(btn_frame, text="Clear Form", command=clear_form, bootstyle="secondary").pack(side=tk.RIGHT, padx=5, ipadx=10)

        refresh_tree(); clear_form()
    
    # --- Custom UI for Menu Management (Admin Only) ---
    
    def show_menu_crud_ui(self):
        self.clear_content_frame()
        table_name = "Menu"
        columns = ['MenuID', 'MenuDate', 'StaffID', 'Notes', 'CreatedAt']
        pk_column = 'MenuID'
        pk_is_auto = True

        ttk.Label(self.content_frame, text=f"Manage {table_name}", font=("Helvetica", 20, "bold")).pack(pady=10, anchor="w")
        
        tree_frame = ttk.Frame(self.content_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', bootstyle="primary")
        for col in columns:
            tree.heading(col, text=col.replace('_', ' ').title())
            tree.column(col, width=120, anchor="w")
        
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def refresh_tree():
            for item in tree.get_children(): tree.delete(item)
            records = execute_read_query(f"SELECT * FROM {table_name}")
            if records:
                for record in records:
                    tree.insert("", "end", values=[str(v) if v is not None else "" for v in record])

        form_frame = ttk.Frame(self.content_frame, padding=10, bootstyle="light")
        form_frame.pack(fill=tk.X, pady=10)
        
        entries = {}
        for i, col in enumerate(columns):
            ttk.Label(form_frame, text=f"{col}:").grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            entries[col] = entry

        def clear_form():
            tree.selection_remove(tree.selection())
            for col, entry in entries.items():
                entry.config(state="normal")
                entry.delete(0, tk.END)
            if pk_is_auto:
                entries[pk_column].insert(0, "(Auto-Generated)")
                entries[pk_column].config(state="readonly")
            else:
                entries[pk_column].focus_set()

        def on_item_select(event):
            selected_items = tree.selection()
            if not selected_items: return
            
            for col, entry in entries.items():
                entry.config(state="normal")
                entry.delete(0, tk.END)

            values = tree.item(selected_items[0])['values']
            for i, col in enumerate(columns):
                entries[col].insert(0, values[i])
            entries[pk_column].config(state="readonly")
        
        tree.bind("<<TreeviewSelect>>", on_item_select)

        def add_record():
            cols = [c for c in columns if "At" not in c and not (pk_is_auto and c == pk_column)]
            values = [entries[c].get() for c in cols]
            query = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))})"
            if execute_query(query, tuple(values)):
                refresh_tree(); clear_form(); messagebox.showinfo("Success", "Menu added.")

        def update_record():
            if not tree.selection(): messagebox.showwarning("Warning", "Select a menu to update."); return
            pk_val = entries[pk_column].get()
            cols = [c for c in columns if c != pk_column and "At" not in c]
            values = [entries[c].get() for c in cols] + [pk_val]
            query = f"UPDATE {table_name} SET {', '.join([f'{c} = %s' for c in cols])} WHERE {pk_column} = %s"
            if execute_query(query, tuple(values)):
                refresh_tree(); clear_form(); messagebox.showinfo("Success", "Menu updated.")
        
        def delete_record():
            if not tree.selection(): messagebox.showwarning("Warning", "Select a menu to delete."); return
            pk_val = entries[pk_column].get()
            if messagebox.askyesno("Confirm", f"Delete menu {pk_val}? This will also delete all its items from MenuFood (due to CASCADE)."):
                if execute_query(f"DELETE FROM {table_name} WHERE {pk_column}=%s", (pk_val,)):
                    refresh_tree(); clear_form(); messagebox.showinfo("Success", "Menu deleted.")
        
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="Add Menu", command=add_record, bootstyle="success").pack(side=tk.LEFT, padx=5, ipadx=10)
        ttk.Button(btn_frame, text="Update Menu", command=update_record, bootstyle="info").pack(side=tk.LEFT, padx=5, ipadx=10)
        ttk.Button(btn_frame, text="Delete Menu", command=delete_record, bootstyle="danger").pack(side=tk.LEFT, padx=5, ipadx=10)
        ttk.Button(btn_frame, text="Clear Form", command=clear_form, bootstyle="secondary").pack(side=tk.RIGHT, padx=5, ipadx=10)
        
        extra_btn_frame = ttk.Frame(self.content_frame)
        extra_btn_frame.pack(fill=tk.X, pady=(10,0))
        
        def open_editor():
            selected_items = tree.selection()
            if not selected_items:
                messagebox.showwarning("No Selection", "Please select a menu from the list to edit its items.")
                return
            
            values = tree.item(selected_items[0])['values']
            menu_id = values[columns.index('MenuID')]
            menu_date = values[columns.index('MenuDate')]
            self.open_menu_editor_window(menu_id, menu_date)

        ttk.Button(extra_btn_frame, text="Edit Items on Selected Menu", command=open_editor, bootstyle="success").pack(fill=tk.X, ipady=5)

        refresh_tree(); clear_form()

    def open_menu_editor_window(self, menu_id, menu_date):
        """A dual-list window to manage items on a specific menu."""
        editor_win = ttk.Toplevel(self)
        editor_win.title(f"Edit Items for Menu: {menu_date} (ID: {menu_id})")
        editor_win.geometry("800x600")

        main_frame = ttk.Frame(editor_win, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        available_frame = ttk.Frame(main_frame); available_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
        ttk.Label(available_frame, text="Available Food Items", font=("Helvetica", 12, "bold")).pack(pady=5)
        available_list = tk.Listbox(available_frame, selectmode=EXTENDED, exportselection=False, height=20, font=("Helvetica", 11))
        available_list.pack(fill=BOTH, expand=True)

        btn_frame = ttk.Frame(main_frame); btn_frame.pack(side=LEFT, fill=Y, padx=10)
        add_btn = ttk.Button(btn_frame, text=">>", bootstyle="success-outline")
        add_btn.pack(pady=20, anchor='s')
        remove_btn = ttk.Button(btn_frame, text="<<", bootstyle="danger-outline")
        remove_btn.pack(pady=20, anchor='n')

        on_menu_frame = ttk.Frame(main_frame); on_menu_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)
        ttk.Label(on_menu_frame, text="Items on This Menu", font=("Helvetica", 12, "bold")).pack(pady=5)
        on_menu_list = tk.Listbox(on_menu_frame, selectmode=EXTENDED, exportselection=False, height=20, font=("Helvetica", 11))
        on_menu_list.pack(fill=BOTH, expand=True)

        available_items_map = {}
        on_menu_items_map = {}

        def refresh_lists():
            available_list.delete(0, tk.END)
            on_menu_list.delete(0, tk.END)
            available_items_map.clear()
            on_menu_items_map.clear()

            on_menu_data = execute_read_query(
                "SELECT fi.ItemID, fi.ItemName FROM FoodItem fi JOIN MenuFood mf ON fi.ItemID = mf.ItemID WHERE mf.MenuID = %s", (menu_id,)
            )
            on_menu_ids = []
            if on_menu_data:
                for item_id, item_name in on_menu_data:
                    display_text = f"{item_id}: {item_name}"
                    on_menu_list.insert(tk.END, display_text)
                    on_menu_items_map[display_text] = item_id
                    on_menu_ids.append(item_id)

            all_items_data = execute_read_query("SELECT ItemID, ItemName FROM FoodItem")
            if all_items_data:
                for item_id, item_name in all_items_data:
                    if item_id not in on_menu_ids:
                        display_text = f"{item_id}: {item_name}"
                        available_list.insert(tk.END, display_text)
                        available_items_map[display_text] = item_id

        def add_items():
            selected_texts = [available_list.get(i) for i in available_list.curselection()]
            if not selected_texts: return
            
            for text in selected_texts:
                item_id = available_items_map.get(text)
                if item_id:
                    execute_query("INSERT INTO MenuFood (MenuID, ItemID) VALUES (%s, %s)", (menu_id, item_id))
            refresh_lists()

        def remove_items():
            selected_texts = [on_menu_list.get(i) for i in on_menu_list.curselection()]
            if not selected_texts: return
            
            for text in selected_texts:
                item_id = on_menu_items_map.get(text)
                if item_id:
                    execute_query("DELETE FROM MenuFood WHERE MenuID = %s AND ItemID = %s", (menu_id, item_id))
            refresh_lists()
            
        add_btn.config(command=add_items)
        remove_btn.config(command=remove_items)
        
        refresh_lists()

    # --- NEW: Custom UI for Viewing Orders (Admin Only) ---
    
    def show_orders_crud_ui(self):
        """A custom UI to view orders and their items."""
        self.clear_content_frame()
        table_name = "Orders"
        columns = ['OrderID', 'SRN', 'OrderDate']
        pk_column = 'OrderID'

        ttk.Label(self.content_frame, text=f"View All {table_name}", font=("Helvetica", 20, "bold")).pack(pady=10, anchor="w")
        
        tree_frame = ttk.Frame(self.content_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', bootstyle="primary")
        for col in columns:
            tree.heading(col, text=col.replace('_', ' ').title())
            tree.column(col, width=150, anchor="w")
        
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def refresh_tree():
            for item in tree.get_children(): tree.delete(item)
            # Sort by most recent orders first
            records = execute_read_query(f"SELECT * FROM {table_name} ORDER BY OrderDate DESC")
            if records:
                for record in records:
                    tree.insert("", "end", values=[str(v) if v is not None else "" for v in record])

        # --- Button Frame ---
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        def delete_record():
            if not tree.selection(): messagebox.showwarning("Warning", "Select an order to delete."); return
            selected_item = tree.selection()[0]
            pk_val = tree.item(selected_item)['values'][0]
            
            if messagebox.askyesno("Confirm", f"Delete order {pk_val}? This will also delete all items in this order (due to CASCADE)."):
                if execute_query(f"DELETE FROM {table_name} WHERE {pk_column}=%s", (pk_val,)):
                    refresh_tree(); messagebox.showinfo("Success", "Order deleted.")
        
        ttk.Button(btn_frame, text="Delete Selected Order", command=delete_record, bootstyle="danger").pack(side=tk.LEFT, padx=5, ipadx=10)
        
        # --- Extra Button Frame ---
        extra_btn_frame = ttk.Frame(self.content_frame)
        extra_btn_frame.pack(fill=tk.X, pady=(10,0))
        
        def open_editor():
            selected_items = tree.selection()
            if not selected_items:
                messagebox.showwarning("No Selection", "Please select an order from the list to view its items.")
                return
            
            values = tree.item(selected_items[0])['values']
            order_id = values[columns.index('OrderID')]
            order_date = values[columns.index('OrderDate')]
            self.open_order_items_window(order_id, order_date) # Call the new function

        ttk.Button(extra_btn_frame, text="View Items for Selected Order", command=open_editor, bootstyle="success").pack(fill=tk.X, ipady=5)

        refresh_tree()

    def open_order_items_window(self, order_id, order_date):
        """A simple Toplevel window to display the items in a specific order."""
        editor_win = ttk.Toplevel(self)
        editor_win.title(f"Items for Order #{order_id} (Date: {order_date})")
        editor_win.geometry("600x400")

        main_frame = ttk.Frame(editor_win, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        ttk.Label(main_frame, text=f"Showing Items for Order #{order_id}", font=("Helvetica", 14, "bold")).pack(pady=5)

        # --- Treeview to show items ---
        cols = ['ItemName', 'Quantity', 'Price', 'Subtotal']
        tree = ttk.Treeview(main_frame, columns=cols, show='headings', bootstyle="info")
        for c in cols: tree.heading(c, text=c); tree.column(c, anchor="w", width=120)
        tree.pack(expand=True, fill="both", pady=10)
        
        # --- Query to get items ---
        query = """
            SELECT fi.ItemName, oi.Quantity, fi.Price, (oi.Quantity * fi.Price) AS Subtotal
            FROM Order_Items oi
            JOIN FoodItem fi ON oi.ItemID = fi.ItemID
            WHERE oi.OrderID = %s
        """
        records = execute_read_query(query, (order_id,))
        
        total = 0.0
        if records:
            for r in records:
                tree.insert("", "end", values=r)
                total += float(r[3]) # Add subtotal to total

        # --- Show Total ---
        ttk.Label(main_frame, text=f"Order Total:  ₹ {total:.2f}", font=("Helvetica", 12, "bold")).pack(pady=10, anchor='e')
    
    # --- Full implementations for other UI sections ---
    
    def show_reports_ui(self):
        self.clear_content_frame()
        ttk.Label(self.content_frame, text="Reports & Advanced Queries", font=("Helvetica", 20, "bold")).pack(pady=10, anchor='w')
        notebook = ttk.Notebook(self.content_frame, bootstyle="primary")
        notebook.pack(expand=True, fill="both", pady=10)

        def create_query_tab(parent, title, desc, query, cols, data=None):
            tab = ttk.Frame(parent, padding=10)
            parent.add(tab, text=title)
            ttk.Label(tab, text=desc, wraplength=700, font=("Helvetica", 10, "italic")).pack(fill='x', pady=(0,10), anchor='w')
            tree = ttk.Treeview(tab, columns=cols, show='headings', bootstyle="info")
            for c in cols: tree.heading(c, text=c); tree.column(c, anchor="w", width=150)
            tree.pack(expand=True, fill="both")
            records = execute_read_query(query, data)
            if records:
                for r in records: tree.insert("", "end", values=r)

        create_query_tab(notebook, "Aggregate", "Calculates average rating and review counts for each food item.", "SELECT * FROM ItemRatings", ['ItemID', 'ItemName', 'NumReviews', 'AvgRating'])
        join_q = "SELECT s.Name, fi.ItemName, o.OrderDate FROM Student s JOIN Orders o ON s.SRN = o.SRN JOIN Order_Items oi ON o.OrderID = oi.OrderID JOIN FoodItem fi ON oi.ItemID = fi.ItemID WHERE fi.ItemName LIKE %s"
        create_query_tab(notebook, "Join", "Finds students who ordered a specific item (e.g., Masala Dosa).", join_q, ['Student', 'Item', 'Date'], ('%Dosa%',))
        nested_q = "SELECT ItemName, Price FROM FoodItem WHERE ItemID NOT IN (SELECT DISTINCT ItemID FROM Review)"
        create_query_tab(notebook, "Nested", "Finds all food items that have never been reviewed.", nested_q, ['ItemName', 'Price'])
        total_spent_q = """
            SELECT s.SRN, s.Name, SUM(fi.Price * oi.Quantity) AS TotalAmountSpent
            FROM Student s
            JOIN Orders o ON s.SRN = o.SRN
            JOIN Order_Items oi ON o.OrderID = oi.OrderID
            JOIN FoodItem fi ON oi.ItemID = fi.ItemID
            GROUP BY s.SRN, s.Name
            ORDER BY TotalAmountSpent DESC
        """
        create_query_tab(notebook, "Student Totals", "Shows the total amount spent by each student, from highest to lowest.", total_spent_q, ['SRN', 'Name', 'Total Spent'])


    def show_transaction_ui(self):
        self.clear_content_frame()
        frame = ttk.Frame(self.content_frame, padding="20")
        frame.pack(expand=True, fill="both")
        ttk.Label(frame, text="Place a New Order (Transaction)", font=("Helvetica", 18, "bold"), bootstyle="primary").pack(pady=10)
        form = ttk.Frame(frame); form.pack(fill=tk.X, pady=10)
        ttk.Label(form, text="Student SRN:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        srn = ttk.Entry(form); srn.grid(row=0, column=1, padx=5, pady=5, sticky='ew'); srn.insert(0, "PESU2021001") # Assumes this SRN exists
        items_frame = ttk.Frame(frame); items_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        ttk.Label(items_frame, text="Items (ItemID, Quantity) - one per line:").pack(anchor='w')
        items = tk.Text(items_frame, height=5, width=30, font=("Courier New", 10)); items.pack(fill='both', expand=True); items.insert(tk.END, "1, 2\n5, 1\n") # Assumes these ItemIDs exist

        def place_order():
            if not (srn.get() and items.get(1.0, tk.END).strip()): messagebox.showerror("Error", "All fields required."); return
            try:
                db_connection.start_transaction()
                cursor = db_connection.cursor()
                cursor.execute("INSERT INTO Orders (SRN) VALUES (%s)", (srn.get(),))
                order_id = cursor.lastrowid
                for line in items.get(1.0, tk.END).strip().split('\n'):
                    item_id, qty = map(str.strip, line.split(','))
                    cursor.execute("INSERT INTO Order_Items (OrderID, ItemID, Quantity) VALUES (%s, %s, %s)", (order_id, item_id, qty))
                db_connection.commit()
                messagebox.showinfo("Success", f"Transaction Successful! OrderID: {order_id}")
            except Exception as e:
                db_connection.rollback()
                messagebox.showerror("Failed", f"Transaction Rolled Back.\nError: {e}")
        ttk.Button(frame, text="Submit Order", command=place_order, bootstyle="success").pack(pady=20, fill='x', ipady=5)

    def show_admin_ui(self):
        # This function is admin-only, so no role checks needed inside
        self.clear_content_frame()
        ttk.Label(self.content_frame, text="Database Administration", font=("Helvetica", 20, "bold")).pack(pady=10, anchor='w')
        notebook = ttk.Notebook(self.content_frame); notebook.pack(expand=True, fill="both", pady=10)
        tp_frame = ttk.Frame(notebook, padding="20"); notebook.add(tp_frame, text="Triggers, Procedures & Functions")
        user_frame = ttk.Frame(notebook, padding="20"); notebook.add(user_frame, text="User Management")

        # --- Triggers, Procedures, Functions Part ---
        
        def create_trigger():
            execute_query("DROP TRIGGER IF EXISTS before_review_update")
            if execute_query("CREATE TRIGGER before_review_update BEFORE UPDATE ON Review FOR EACH ROW SET NEW.ReviewDate = NOW()"):
                messagebox.showinfo("Success", "Trigger 'before_review_update' created.")
        
        def create_procedure():
            execute_query("DROP PROCEDURE IF EXISTS GetStudentReviews")
            if execute_query("CREATE PROCEDURE GetStudentReviews(IN s_srn VARCHAR(15)) BEGIN SELECT * FROM Review WHERE SRN = s_srn; END;"):
                messagebox.showinfo("Success", "Procedure 'GetStudentReviews' created.")

        def create_function():
            execute_query("DROP FUNCTION IF EXISTS GetStudentTotalSpent")
            func_query = """
            CREATE FUNCTION GetStudentTotalSpent(s_srn VARCHAR(15))
            RETURNS DECIMAL(10, 2)
            DETERMINISTIC
            READS SQL DATA
            BEGIN
                DECLARE total DECIMAL(10, 2);
                SELECT SUM(fi.Price * oi.Quantity)
                INTO total
                FROM Orders o
                JOIN Order_Items oi ON o.OrderID = oi.OrderID
                JOIN FoodItem fi ON oi.ItemID = fi.ItemID
                WHERE o.SRN = s_srn;
                RETURN IFNULL(total, 0.00);
            END;
            """
            if execute_query(func_query):
                messagebox.showinfo("Success", "Function 'GetStudentTotalSpent' created.")
            
        def call_procedure():
            srn = simpledialog.askstring("Input", "Enter Student SRN to get reviews for:")
            if not srn: return
            reviews = execute_read_query("CALL GetStudentReviews(%s)", (srn,))
            if reviews is not None:
                win = ttk.Toplevel(self); win.title(f"Reviews for {srn}")
                cols = ['ID', 'SRN', 'ItemID', 'Rating', 'Feedback', 'Date']
                tree = ttk.Treeview(win, columns=cols, show='headings'); tree.pack(expand=True, fill='both', padx=10, pady=10)
                for c in cols: tree.heading(c, text=c)
                if reviews:
                    for r in reviews: tree.insert("", "end", values=r)
                else:
                    ttk.Label(win, text="No reviews found.").pack(pady=20)
            else:
                 messagebox.showerror("Error", "Could not call procedure.")

        def call_function():
            srn = simpledialog.askstring("Input", "Enter Student SRN to get total spent:")
            if not srn: return
            
            query = "SELECT GetStudentTotalSpent(%s)"
            result = execute_read_query(query, (srn,))
            
            if result:
                total_spent = result[0][0]
                messagebox.showinfo("Result", f"Total amount spent by {srn}:\n\n₹ {total_spent}")
            else:
                messagebox.showerror("Error", "Could not retrieve total.")

        ttk.Button(tp_frame, text="Create/Reset Trigger", command=create_trigger, bootstyle="info").pack(pady=10, fill='x')
        ttk.Button(tp_frame, text="Create/Reset Procedure", command=create_procedure, bootstyle="info").pack(pady=10, fill='x')
        ttk.Button(tp_frame, text="Create/Reset Function (TotalSpent)", command=create_function, bootstyle="info").pack(pady=10, fill='x')
        
        ttk.Separator(tp_frame).pack(fill='x', pady=10)
        
        ttk.Button(tp_frame, text="Call GetStudentReviews Procedure", command=call_procedure, bootstyle="success").pack(pady=10, fill='x')
        ttk.Button(tp_frame, text="Call GetStudentTotalSpent Function", command=call_function, bootstyle="success").pack(pady=10, fill='x')
        
        # --- User Management Part (With Roles) ---
        ttk.Label(user_frame, text="Create New DB User", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        ttk.Label(user_frame, text="Select Role:").pack(pady=(10,0), anchor='w')
        self.role_var = tk.StringVar(value="Admin") # Default to Admin
        role_combo = ttk.Combobox(user_frame, textvariable=self.role_var, values=["Admin", "Student"], state="readonly")
        role_combo.pack(pady=5, fill='x')

        ttk.Label(user_frame, text="Username:").pack(pady=(10,0), anchor='w')
        user_entry = ttk.Entry(user_frame); user_entry.pack(pady=5, fill='x')
        ttk.Label(user_frame, text="Password:").pack(pady=(10,0), anchor='w')
        pass_entry = ttk.Entry(user_frame, show="*"); pass_entry.pack(pady=5, fill='x')
        
        def create_user():
            username, password, role = user_entry.get(), pass_entry.get(), self.role_var.get()
            if not (username and password): messagebox.showerror("Error", "Fields cannot be empty."); return
            
            try:
                execute_query(f"DROP USER IF EXISTS '{username}'@'localhost'")
                execute_query(f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}'")
                
                if role == "Admin":
                     execute_query(f"GRANT ALL PRIVILEGES ON cafeteria_db.* TO '{username}'@'localhost'")
                
                elif role == "Student":
                     execute_query(f"GRANT SELECT ON cafeteria_db.FoodItem TO '{username}'@'localhost'")
                     execute_query(f"GRANT SELECT ON cafeteria_db.Menu TO '{username}'@'localhost'")
                     execute_query(f"GRANT SELECT ON cafeteria_db.MenuFood TO '{username}'@'localhost'")
                     execute_query(f"GRANT SELECT ON cafeteria_db.ItemRatings TO '{username}'@'localhost'")
                     execute_query(f"GRANT SELECT (SRN, Name) ON cafeteria_db.Student TO '{username}'@'localhost'") # Can see names, not contact info
                     execute_query(f"GRANT SELECT, INSERT, UPDATE ON cafeteria_db.Review TO '{username}'@'localhost'") # Can add/update reviews
                     execute_query(f"GRANT INSERT ON cafeteria_db.Orders TO '{username}'@'localhost'")
                     execute_query(f"GRANT INSERT ON cafeteria_db.Order_Items TO '{username}'@'localhost'")
                     
                messagebox.showinfo("Success", f"User '{username}' created with role: {role}.")
            except Exception as e: 
                messagebox.showerror("Error", f"Could not create user: {e}")
                
        ttk.Button(user_frame, text="Create User with Role", command=create_user, bootstyle="success").pack(pady=20, fill='x')

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    app = CafeteriaApp()
    app.mainloop()