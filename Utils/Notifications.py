import threading
import time
import customtkinter as ctk

class Slideout(ctk.CTkFrame):
    def __init__(self, parent, side="right", width=100, height=100, bg_color='#fafafa', text="", y_axis:float=1.2, **kwargs):
        super().__init__(parent, width=width, height=height, bg_color='#fafafa',border_width=2, corner_radius=20,**kwargs)
        self.parent = parent
        self.side = side
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.text = text
        self.y_axis = y_axis
		
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

        # Botón para cerrar el slideout
        self.close_button = ctk.CTkButton(self, text="×", width=25, height=25, fg_color= "transparent", text_color= "Black", hover_color= "#EDEBE9", font=('Arial', 16),command=self.slide_out)
        self.close_button.place(relx=0.95, rely=0.05, anchor="ne")  # Colocar en la esquina superior derecha

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
                self.place(x=x, y=(self.parent.winfo_height() - self.height) // self.y_axis)  # Fuerza el valor de `y`
                self.update_idletasks()  # Asegurar que se actualice la interfaz
                time.sleep(0.01)
        elif self.side == "left":
            # Desliza desde la izquierda hacia la derecha
            for x in range(-self.width, 0, 10):
                self.place(x=x, y=(self.parent.winfo_height() - self.height) // self.y_axis)  # Fuerza el valor de `y`
                self.update_idletasks()  # Asegura que se actualice la interfaz
                time.sleep(0.01)

    def _animate_out(self):
        if self.side == "right":
            # Desliza de regreso hacia la derecha (fuera de la pantalla)
            for x in range(self.parent.winfo_width() - self.width, self.parent.winfo_width(), 10):
                self.place(x=x, y=(self.parent.winfo_height() - self.height) // self.y_axis)  # Fuerza el valor de `y`
                self.update_idletasks()
                time.sleep(0.01)
        elif self.side == "left":
            # Desliza de regreso hacia la izquierda (fuera de la pantalla)
            for x in range(0, -self.width, -10):
                self.place(x=x, y=(self.parent.winfo_height() - self.height) // self.y_axis)  # Fuerza el valor de `y`
                self.update_idletasks()
                time.sleep(0.01)

        # Elimina el frame una vez que esté fuera de la pantalla
        self.destroy()
    

class Menu_user(ctk.CTkFrame):
    def __init__(self, parent, side="right", width=300, height=530, bg_color='#fafafa', text="", y_axis:float=1, **kwargs):
        super().__init__(parent, width=width, height=height, bg_color='#fafafa',border_width=1,**kwargs)
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

        # Botón para cerrar el slideout
        self.close_button = ctk.CTkButton(self, text="×", width=25, height=25, fg_color= "transparent", text_color= "Black", hover_color= "#EDEBE9", font=('Arial', 16),command=self.slide_out)
        self.close_button.place(relx=0.95, rely=0.05, anchor="ne")  # Colocar en la esquina superior derecha

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
                self.place(x=x, y=(self.parent.winfo_height() - self.height) // self.y_axis)  # Fuerza el valor de `y`
                self.update_idletasks()  # Asegurar que se actualice la interfaz
                time.sleep(0.01)
        elif self.side == "left":
            # Desliza desde la izquierda hacia la derecha
            for x in range(-self.width, 0, 10):
                self.place(x=x, y=(self.parent.winfo_height() - self.height) // self.y_axis)  # Fuerza el valor de `y`
                self.update_idletasks()  # Asegura que se actualice la interfaz
                time.sleep(0.01)

    def _animate_out(self):
        if self.side == "right":
            # Desliza de regreso hacia la derecha (fuera de la pantalla)
            for x in range(self.parent.winfo_width() - self.width, self.parent.winfo_width(), 10):
                self.place(x=x, y=(self.parent.winfo_height() - self.height) // self.y_axis)  # Fuerza el valor de `y`
                self.update_idletasks()
                time.sleep(0.01)
        elif self.side == "left":
            # Desliza de regreso hacia la izquierda (fuera de la pantalla)
            for x in range(0, -self.width, -10):
                self.place(x=x, y=(self.parent.winfo_height() - self.height) // self.y_axis)  # Fuerza el valor de `y`
                self.update_idletasks()
                time.sleep(0.01)

        # Elimina el frame una vez que esté fuera de la pantalla
        self.destroy()
