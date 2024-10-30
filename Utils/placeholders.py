import threading
import time
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from PIL import Image, ImageTk
from datetime import datetime

color_p = "#fafafa"
color_s = "#efefef"
grey = "#EDEBE9"
blue = "#0080ff"
black = "#131313"

class Slideout(ctk.CTkFrame):
    active_slideout = None  # Variable de clase para mantener referencia al slideout activo

    def __init__(self, parent, side="right", width=100, height=100, bg_color='#fafafa', text_color='#000000', text="", y_axis: float = 1.2, **kwargs):
        super().__init__(parent, width=width, height=height, bg_color='#fafafa', border_width=2, corner_radius=20, **kwargs)
        self.parent = parent
        self.side = side
        self.width = width
        self.text = text
        self.y_axis = y_axis
        self.text_color = text_color

        # Ajusta la altura según el contenido del texto
        self.adjust_height_to_text()

        # Configura la geometría y la posición inicial fuera de la pantalla
        self.place_initial_position()

        # Cambia el color de fondo
        self.configure(fg_color=bg_color)

        # Agrega texto
        self.text_label = ctk.CTkLabel(self, text=self.text, anchor="center", text_color=self.text_color, wraplength=self.width-20)  # wraplength evita overflow horizontal
        self.text_label.place(relx=0.5, rely=0.5, anchor="center")

        # Botón para cerrar el slideout
        self.close_button = ctk.CTkButton(self, text="×", width=25, height=25, bg_color="transparent", fg_color="transparent", text_color="Black", hover_color="#EDEBE9", font=('Arial', 16), command=self.slide_out)
        self.close_button.place(relx=0.95, rely=0.025, anchor="ne")

        # Verifica si ya hay un slideout activo
        if Slideout.active_slideout is not None and Slideout.active_slideout != self:
            Slideout.active_slideout.slide_out()
        Slideout.active_slideout = self  # Establece el nuevo slideout como el activo

    def adjust_height_to_text(self):
        """Ajusta la altura del slideout en función del contenido del texto."""
        lines = len(self.text) // (self.width // 10) + 1  # Aproxima el número de líneas
        self.height = max(100, min(300, lines * 25))  # Ajusta entre un mínimo y máximo de altura

    def place_initial_position(self):
        """Coloca el slideout en su posición inicial fuera de la pantalla."""
        if self.side == "right":
            self.place(x=self.parent.winfo_width(), y=(self.parent.winfo_height() - self.height) // self.y_axis)
        elif self.side == "left":
            self.place(x=-self.width, y=(self.parent.winfo_height() - self.height) // self.y_axis)

    def slide_in(self):
        # Ejecuta el movimiento en un hilo separado para no bloquear la elementna
        threading.Thread(target=self._animate_in).start()

    def slide_out(self):
        # Ejecuta el movimiento de salida en un hilo separado
        threading.Thread(target=self._animate_out).start()

    def _animate_in(self):
        if self.side == "right":
            # Desliza desde la derecha hacia la izquierda
            for x in range(self.parent.winfo_width(), self.parent.winfo_width() - self.width, -10):
                self._update_position(x)
        elif self.side == "left":
            # Desliza desde la izquierda hacia la derecha
            for x in range(-self.width, 0, 10):
                self._update_position(x)
        time.sleep(5)
        if Slideout.active_slideout != None:
            self.slide_out()

    def _update_position(self, x):
        """Actualiza la posición del slideout."""
        self.place(x=x, y=(self.parent.winfo_height() - self.height) // self.y_axis)
        self.update_idletasks()
        time.sleep(0.01)

    def _animate_out(self):
        if self.side == "right":
            # Desliza de regreso hacia la derecha (fuera de la pantalla)
            for x in range(self.parent.winfo_width() - self.width, self.parent.winfo_width(), 10):
                self._update_position(x)
        elif self.side == "left":
            # Desliza de regreso hacia la izquierda (fuera de la pantalla)
            for x in range(0, -self.width, -10):
                self._update_position(x)
        self.after(10, self.destroy)
        Slideout.active_slideout = None  # Libera la referencia del slideout activo

class Menu_user(ctk.CTkFrame):
    is_in_animation = False
    def __init__(self, parent, side="right", width=300, height=530, bg_color='#fafafa', text="", y_axis:float=1, **kwargs):
        super().__init__(parent, width=width, height=height, bg_color='#fafafa',border_width=1, border_color= "#EDEBE9",**kwargs)
        self.parent = parent
        self.side = side
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.text = text
        self.y_axis = y_axis
        self.is_active=False
		
        # Configura la geometría y la posición inicial fuera de la pantalla
        if self.side == "right":
            self.place(x=parent.winfo_width(), y=(parent.winfo_height() - self.height) // y_axis)  # Centra verticalmente
        elif self.side == "left":
            self.place(x=-self.width, y=(parent.winfo_height() - self.height) // y_axis)  # Centra verticalmente

        # Cambia el color de fondo
        self.configure(fg_color=self.bg_color)

        # Agrega texto
        self.text_label = ctk.CTkLabel(self, text=self.text, anchor="center")
        self.text_label.place(relx=0.5, rely=0.5, anchor="center")

       
    def slide_in(self):
        # Ejecuta el movimiento en un hilo separado para no bloquear la elementna
        if not Menu_user.is_in_animation:
            Menu_user.is_in_animation = not Menu_user.is_in_animation
            threading.Thread(target=self._animate_in).start()
        
    def slide_out(self):
        # Ejecuta el movimiento de salida en un hilo separado
        if not Menu_user.is_in_animation:
            Menu_user.is_in_animation = not Menu_user.is_in_animation
            threading.Thread(target=self._animate_out).start()

    def _animate_in(self):
        if self.side == "right":
            # Desliza desde la derecha hacia la izquierda
            for x in range(self.parent.winfo_width(), self.parent.winfo_width() - self.width, -10):
                self._extracted_from__animate_in_5(x)
        elif self.side == "left":
            # Desliza desde la izquierda hacia la derecha
            for x in range(-self.width, 0, 10):
                self._extracted_from__animate_in_5(x)
        Menu_user.is_in_animation = not Menu_user.is_in_animation

    def _extracted_from__animate_in_5(self, x):
        self.place(x=x, y=(self.parent.winfo_height() - self.height) // self.y_axis)  # Fuerza el valor de `y`
        self.update_idletasks()  # Asegurar que se actualice la interfaz
        time.sleep(0.01)
        
    def _animate_out(self):
        if self.side == "right":
            # Desliza de regreso hacia la derecha (fuera de la pantalla)
            for x in range(self.parent.winfo_width() - self.width, self.parent.winfo_width(), 10):
                self._extracted_from__animate_out_5(x)
        elif self.side == "left":
            # Desliza de regreso hacia la izquierda (fuera de la pantalla)
            for x in range(0, -self.width, -10):
                self._extracted_from__animate_out_5(x)
        Menu_user.is_in_animation = not Menu_user.is_in_animation

        # Elimina el frame una vez que esté fuera de la pantalla
        self.destroy()

    def _extracted_from__animate_out_5(self, x):
        self.place(x=x, y=(self.parent.winfo_height() - self.height) // self.y_axis)  # Fuerza el valor de `y`
        self.update_idletasks()
        time.sleep(0.01)

class NotificationPlaceHolder():
    def __init__(self, title:str, text:str, tag:str=None):
        self.title = title
        self.text = text     
        self.tag = tag
        
class Card(ctk.CTkFrame):
    def __init__(self, parent, title, text, tag, width=400, height=100, corner_radius = 10, bg_color= "#EDEBE9", text_color="#000000"):
        super().__init__(parent, width=width, height=height, fg_color=bg_color, corner_radius = corner_radius)  

        self.title = title
        self.full_text = text
        self.text_color = text_color
        self.initial_height = height
        self.is_expanded = False
        self.tag = tag
        
        self.title_label = ctk.CTkLabel(self, text=self.title, font=("Arial", 20, "bold"), text_color=text_color)
        self.title_label.pack(pady=10, padx=20, anchor="w")
        
        self.text_label = ctk.CTkLabel(self, text=self.full_text,font=("Arial", 12), text_color=text_color, wraplength=width-20)
        self.text_label.pack(pady=10, padx=10, anchor="w")
        
        self.text_label.update_idletasks()  
        text_height = self.text_label.winfo_reqheight() 
        if text_height > height - 60: 
            self.text_label.configure(text=self._truncate_text(self.full_text))  
            self.read_more_button = ctk.CTkButton(self, text="Leer más", fg_color = "#131313", hover_color= "#232323" , command=self.toggle_text)
            self.read_more_button.pack(side = "right", padx = 20,pady=5)
        else:
            self.read_more_button = None  
    
    def _truncate_text(self, text):
        max_lines = 4  
        lines = text.splitlines()
        return "\n".join(lines[:max_lines]) + ("..." if len(lines) > max_lines else "")
    
    def toggle_text(self):
        if self.is_expanded:
            self.text_label.configure(text=self._truncate_text(self.full_text))
            self.configure(height=self.initial_height)
            self.read_more_button.configure(text="Leer más")
        else:
            self.text_label.configure(text=self.full_text)
            full_height = self.text_label.winfo_reqheight() + 80  
            self.configure(height=full_height)
            self.read_more_button.configure(text="Leer menos")
        
        self.is_expanded = not self.is_expanded
        
class ClearableEntry(ctk.CTkEntry):
    def get_and_clear(self):
        value = self.get()  # Obtiene el valor del input
        self.delete(0, ctk.END)  # Borra el contenido del input
        return value  # Retorna el valor obtenido

class Table:
    def __init__(self, master: ttk.Widget, columns: list, color_tabla: str, color_frame: str, width: int = 775, height: int = 400, filterBool: bool = True):
        """
        Inicializa una tabla con protección contra overflow de texto en celdas.

        Args:
            master (tk.Widget): El contenedor donde se coloca la tabla.
            columns (list): Lista de columnas con el formato [(id_col, nombre_col, ancho_col)].
            color_tabla (str): Color de fondo de la tabla principal.
            color_frame (str): Color de fondo del frame contenedor.
            width (int): Ancho de la tabla en píxeles. Default: 775.
            height (int): Alto de la tabla en píxeles. Default: 400.
        """
        self.frame = ctk.CTkFrame(master, width=width, height=height, fg_color=color_tabla, corner_radius=40)
        self.frame.grid_propagate(False)

        # Configuracion de las columnas del Treeview
        self.treeview = ttk.Treeview(self.frame, columns=[col[0] for col in columns[1:]])
        if filterBool:
            self.treeview.place(relx=0.5, rely=0.55, anchor="center", width=width - 50, height=height - 50)
        else:
            self.treeview.place(relx=0.5, rely=0.46, anchor="center", width=width - 50, height=height - 50)
        # Definicion de columnas y encabezados
        for col_id, heading, col_width in columns:
            self.treeview.column(col_id, width=col_width, minwidth=col_width, anchor="w")
            self.treeview.heading(col_id, text=heading, anchor="w")

        if filterBool:
            self.column_var = tk.StringVar(value="Seleccionar columna")
            self.column_menu = ctk.CTkOptionMenu(self.frame, variable=self.column_var, values=[col[1] for col in columns], font=('Plus jakarta Sans', 14, 'bold'), text_color=black,fg_color=color_s, button_color=grey,
                                            button_hover_color=grey, dropdown_fg_color=color_p, dropdown_text_color=black)
            self.column_menu.place(relx=0.1, rely=0.02)

            self.sort_var = tk.StringVar(value="Selecc. tipo de orden")
            self.sort_menu = ctk.CTkOptionMenu(self.frame, variable=self.sort_var, values=["Ascending", "Descending"], font=('Plus jakarta Sans', 14, 'bold'), text_color=black,fg_color=color_s, button_color=grey,
                                            button_hover_color=grey, dropdown_fg_color=color_p, dropdown_text_color=black)
            self.sort_menu.place(relx=0.4, rely=0.02)

            self.sort_button = ctk.CTkButton(self.frame, width=60, text="Filtrar", corner_radius=20, fg_color='#FFFFFF', text_color=black, hover_color='#ADACAA', command=self.apply_sort)
            self.sort_button.place(relx=0.8, rely=0.02)

            self.filter_image = ImageP(self.frame,"./img/filter.png", height=25, width=25,x=20,y=13)
        self.full_data = []

    def insert(self, elements):
        """
        Inserta los datos de Elementos en la tabla.

        Args:
            elements (list): Lista de elementos, cada uno como lista con valores en el mismo orden que las columnas.
        """
        self.full_data = elements  
        self.treeview.delete(*self.treeview.get_children())

        for element in elements:
            if len(element) >= len(self.treeview["columns"]) + 1:
                text_value = element[0]  
                column_values = element[1:] 
                self.treeview.insert("", tk.END, text=text_value, values=column_values)
            else:
                print(f"Advertencia: La cantidad de valores {len(element)} no coincide con el número de columnas + text {len(self.treeview['columns']) + 1}")

    def apply_sort(self):
        """Ordena el Treeview según la columna y el tipo de orden seleccionados en los menús."""
        column_name = self.column_var.get()
        order_type = self.sort_var.get()

        column_index = next((i for i, col in enumerate(self.treeview["columns"], start=1) if self.treeview.heading(col, "text") == column_name), None)
        if column_index is None:
            return

        reverse = order_type == "Descending"

        try:
            sorted_data = sorted(self.full_data, key=lambda x: self._parse_value(x[column_index]), reverse=reverse)
            self.insert(sorted_data)
        except ValueError:
            print("Error: no se pudo ordenar la columna. Asegúrese de que los datos sean consistentes en el tipo de datos.")

    def _parse_value(self, value):
        """Intenta parsear el valor como int, float o fecha. Si falla, lo trata como texto."""
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                try:
                    return datetime.strptime(value, "%Y-%m-%d")
                except ValueError:
                    return value  # Mantiene el valor como texto si no es fecha, int o float

    def grid(self, *args, **kwargs):
        """
        Método para colocar el frame en el layout usando grid.

        Args:
            *args, **kwargs: Argumentos y parametros para el metodo grid de tkinter.
        """
        self.frame.grid(*args, **kwargs)

    def place(self, *args, **kwargs):
        """
        Método para colocar el frame en el layout usando place.

        Args:
            *args, **kwargs: Argumentos y parametros para el metodo place de tkinter.
        """
        self.frame.place(*args, **kwargs)

    def clear(self):
        """Elimina todas las filas actuales de la tabla."""
        for item in self.treeview.get_children():
            self.treeview.delete(item)
    
    def get_children(self):
        """Devuelve los elementos hijos del Treeview."""
        return self.treeview.get_children()
    
    def item(self, item_id, option=None, **kw):
        """
        Interactúa con los elementos del Treeview.

        Args:
            item_id (str): ID del elemento en el Treeview.
            option (str, opcional): Opción específica para obtener o establecer.
            **kw: Argumentos adicionales para modificar el elemento.
        
        Returns:
            dict o str: Información del elemento o valor de la opción especificada.
        """
        return self.treeview.item(item_id, option=option, **kw)

    def focus(self):
        """Devuelve el ID del elemento actualmente seleccionado en el Treeview."""
        return self.treeview.focus()
    
    def delete(self, item_id):
        """
        Elimina un elemento específico de la tabla dado su item_id.

        Args:
            item_id (str): ID del elemento en el Treeview a eliminar.
        """
        self.treeview.delete(item_id)
    
class ImageP:
    def __init__(self, manager: tk.Widget, image_path: str, height: int, width: int, x: int, y: int) -> None:
        self.x = x
        self.y = y
        img = Image.open(image_path)
        img = img.resize((width, height), Image.LANCZOS)
        self.render = ImageTk.PhotoImage(img)
        self.img = ctk.CTkLabel(manager, text='', image=self.render, bg_color='transparent')
        self.img.place(x=x, y=y)

    def configure_y(self, y):
        self.img.place(x=self.x, y=y)
    
    def animate_to(self, target_x: int, target_y: int, duration: float,smoothness:int=50) -> None:
        def animation():
            start_x, start_y = self.x, self.y
            delta_x = (target_x - start_x)
            delta_y = (target_y - start_y)
            steps = int(duration * smoothness)  
            step_delay = duration / steps

            for step in range(1, steps + 1):
                self.x = start_x + (delta_x * step / steps)
                self.y = start_y + (delta_y * step / steps)
                self.img.place(x=self.x, y=self.y)
                time.sleep(step_delay)
        
        animation_thread = threading.Thread(target=animation)
        animation_thread.daemon = True
        animation_thread.start()