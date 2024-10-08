import threading
import time
import customtkinter as ctk

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
        # Ejecuta el movimiento en un hilo separado para no bloquear la ventana
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
        # Ejecuta el movimiento en un hilo separado para no bloquear la ventana
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

    # TODO Rename this here and in `_animate_in`
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
    def __init__(self, title, text):
        self.title = title
        self.text = text     
        
class Card(ctk.CTkFrame):
    def __init__(self, parent, title, text, width=400, height=100, corner_radius = 10, bg_color= "#EDEBE9", text_color="#000000"):
        super().__init__(parent, width=width, height=height, fg_color=bg_color, corner_radius = corner_radius)  

        self.title = title
        self.full_text = text
        self.text_color = text_color
        self.initial_height = height
        self.is_expanded = False
        
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