import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sqlite3

class BDViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BD Viewer")

        # Frame para el archivo y la consulta
        frame_top = tk.Frame(root)
        frame_top.pack(fill=tk.X, padx=10, pady=10)

        # Botón para cargar archivo .bd
        self.btn_load = tk.Button(frame_top, text="Cargar archivo .bd", command=self.load_bd_file)
        self.btn_load.pack(side=tk.LEFT)

        # Campo para mostrar el nombre del archivo cargado
        self.lbl_filename = tk.Label(frame_top, text="Archivo no cargado.")
        self.lbl_filename.pack(side=tk.LEFT, padx=10)

        # Campo para consulta SQL
        self.query_entry = tk.Entry(frame_top, width=50)
        self.query_entry.pack(side=tk.LEFT, padx=10)

        # Botón para ejecutar la consulta
        self.btn_query = tk.Button(frame_top, text="Ejecutar Query", command=self.run_query)
        self.btn_query.pack(side=tk.LEFT)

        # Frame para la lista de tablas
        frame_left = tk.Frame(root)
        frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.table_listbox = tk.Listbox(frame_left)
        self.table_listbox.pack(fill=tk.Y, expand=True)
        self.table_listbox.bind("<<ListboxSelect>>", self.display_table_content)

        # Frame para la visualización de los elementos de la tabla seleccionada
        frame_right = tk.Frame(root)
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crea el Canvas y Scrollbars
        self.canvas = tk.Canvas(frame_right)
        self.scroll_x = tk.Scrollbar(frame_right, orient="horizontal", command=self.canvas.xview)
        self.scroll_y = tk.Scrollbar(frame_right, orient="vertical", command=self.canvas.yview)
        
        # Crea el Frame dentro del Canvas para contener el Treeview
        self.tree_frame = tk.Frame(self.canvas)
        self.tree_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.tree = ttk.Treeview(self.tree_frame, show='headings')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.create_window((0, 0), window=self.tree_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.conn = None

    def load_bd_file(self):
        if file_path := filedialog.askopenfilename(
            filetypes=[("SQLite Database Files", "*.db")]
        ):
            self.lbl_filename.config(text=file_path)
            self.connect_to_db(file_path)

    def connect_to_db(self, file_path):
        # Conecta a la base de datos SQLite
        try:
            if self.conn:
                self.conn.close()
            self.conn = sqlite3.connect(file_path)
            self.show_tables()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to connect to the database: {e}")

    def show_tables(self):
        # Limpias la lista de tablas
        self.table_listbox.delete(0, tk.END)

        # Obtiene la lista de tablas en la base de datos
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Añade las tablas a la lista
        for table in tables:
            self.table_listbox.insert(tk.END, table[0])

        cursor.close()

    def display_table_content(self, event):
        # Obtiene el nombre de la tabla seleccionada
        selected_table = self.table_listbox.get(self.table_listbox.curselection())

        # Limpia el Treeview
        self.tree.delete(*self.tree.get_children())

        # Obtiener las columnas y los datos de la tabla seleccionada
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({selected_table});")
        columns = [col[1] for col in cursor.fetchall()]

        cursor.execute(f"SELECT * FROM {selected_table};")
        rows = cursor.fetchall()

        # Configura las columnas en el Treeview
        self.tree["columns"] = columns
        self.tree.heading("#0", text="", anchor=tk.W)
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.W)
            self.tree.column(col, anchor=tk.W)

        # Inserta los datos en el Treeview
        for row in rows:
            self.tree.insert("", "end", values=row)

        cursor.close()

    def run_query(self):
        # Ejecuta una consulta SQL
        query = self.query_entry.get()
        if not query.strip():
            messagebox.showwarning("Warning", "Porfavor ingrese una Query")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            if query.strip().lower().startswith("select"):
                results = cursor.fetchall()
                self.show_query_results(results)
            else:
                self.conn.commit()
                messagebox.showinfo("Info", "Query ejecutada con exito")
                self.show_tables()
            cursor.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to execute query: {e}")

    def show_query_results(self, results):
        # Muestra los resultados de la consulta en el Treeview
        self.tree.delete(*self.tree.get_children())
        for row in results:
            self.tree.insert("", "end", values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = BDViewerApp(root)
    root.mainloop()
