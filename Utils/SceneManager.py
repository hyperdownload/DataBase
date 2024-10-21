import customtkinter as ctk
from difflib import get_close_matches
import threading
import traceback

class SceneManager(ctk.CTk):
    def __init__(self):
        """Inicializa el gestor de escenas.

        Establece el gestor de escenas como una ventana de `customtkinter` y 
        prepara un diccionario para almacenar las escenas y una referencia 
        a la escena actual.
        """
        super().__init__()
        self.scenes = {}  # Diccionario para almacenar las escenas añadidas
        self.variables = {} # Variables almacenadas para interactuar con otras escenas
        self.scene_history = [] # Se supone, un historial
        self.current_scene = None  # Referencia a la escena actualmente visible
        self.current_scene_name = None

    def save_variable(self, variable_name:str, variable_value:any)->None:
        """Almacena una variable en el gestor de escenas."""
        self.variables[variable_name] = variable_value
        
    def get_variable(self, variable_name: str) -> any:
        """Obtiene una variable almacenada en el gestor de escenas."""
        try:
            if var := self.variables.get(variable_name):
                return var
            if close_matches := get_close_matches(
                variable_name, self.variables.keys(), n=1, cutoff=0.5
            ):
                suggestion = close_matches[0]
                raise NameError(f"Esta variable no está definida. ¿Quisiste decir '{suggestion}'?")
            else:
                raise NameError("Esta variable no está definida.")
        except NameError as e:
            # Captura la traza del error y la imprime
            traceback.print_exc()
            # Relanza la excepción para no perder la traza original
            raise
       
    def add_scene(self, name:str, scene_class:object)->None:
        """Agrega una nueva escena al gestor."""
        if name in self.scenes:
            print(f"Escena '{name}' ya existe.")
        else:
            self.scenes[name] = scene_class

    def switch_scene(self, name:str) -> None:
        """Cambia a otra escena asegurando que la anterior sea eliminada completamente."""
        
        self.scene_history.append(name.__class__.__name__)
        self.current_scene_name = name
        if self.current_scene:
            self.current_scene.pack_forget()
            self.current_scene.place_forget()
            self.current_scene.grid_forget()

        if scene_class := self.scenes.get(name):
            self.current_scene = scene_class(self, self)
            self.current_scene.pack(fill='both', expand=True)
        else:
            print(f"Escena '{name}' no encontrada.")
    
    def clear_widget(self, *widgets):
        """Elimina todos los widgets o los hijos de los widgets dados."""
        try:
            for widget in widgets:
                # Si el widget tiene hijos, itera sobre ellos y los destruye
                for child in widget.winfo_children():
                    self._extracted_from_clear_widget_7(child)
                self._extracted_from_clear_widget_7(widget)
            print("Todos los elementos han sido eliminados.")
        except Exception as e:
            traceback.print_exc()
            print(f"Error al intentar eliminar el/los elemento(s): {e}")

    def _extracted_from_clear_widget_7(self, arg0):
        arg0.pack_forget()
        arg0.grid_forget()
        arg0.place_forget()
        arg0.destroy()

    def refresh_current_scene(self):
        """Actualiza la escena actual recargándola."""
        try:
            if not self.current_scene_name:
                raise ValueError("No hay una escena actual para refrescar.")
            self.clear_current_scene()
            self.switch_scene(self.current_scene_name)
            print(f"Escena '{self.current_scene_name}' refrescada con éxito.")
        except Exception as e:
            traceback.print_exc()
            print(f"Error al intentar refrescar la escena: {e}")

# Clase base para las escenas
class BaseScene(ctk.CTkFrame):
    def __init__(self, parent, manager):
        """Inicializa una escena base.

        Args:
            parent (ctk.CTk): Ventana principal o gestor de escenas.
            manager (SceneManager): Gestor de escenas que maneja esta escena.
        """
        super().__init__(parent)
        self.manager = manager  # Referencia al gestor de escenas (ventana principal)

# Ejemplo de una escena
class Scene1(BaseScene):
    def __init__(self, parent, manager):
        """Inicializa la primera escena.

        Configura la interfaz para Scene1, incluyendo una etiqueta y un botón.

        Args:
            parent (ctk.CTk): Ventana principal o gestor de escenas.
            manager (SceneManager): Gestor de escenas que maneja esta escena.
        """
        super().__init__(parent, manager)

        # Crea una etiqueta con texto para Scene1
        label = ctk.CTkLabel(self, text="This is Scene 1")
        label.pack(pady=20)  # Empaqueta la etiqueta con un relleno vertical

        # Crea un botón para cambiar a Scene2
        button = ctk.CTkButton(self, text="Go to Scene 2", 
                              command=lambda: manager.switch_scene("Scene2"))
        button.pack(pady=20)  # Empaqueta el botón con un relleno vertical

if __name__ == "__main__":
    app = SceneManager()  # Crea una instancia del gestor de escenas
    app.geometry("400x300")  # Establece el tamaño de la ventana

    # Añade las escenas al gestor
    app.add_scene("Scene1", Scene1)

    # Inicia la aplicación con la primera escena visible
    app.switch_scene("Scene1")

    app.mainloop()  # Ejecuta el bucle principal de la aplicación