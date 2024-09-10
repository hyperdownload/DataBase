import customtkinter as ctk
import threading

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
        self.current_scene = None  # Referencia a la escena actualmente visible

    def save_variable(self, variable_name:str, variable_value:any)->None:
        """Almacena una variable en el gestor de escenas."""
        self.variables[variable_name] = variable_value
        
    def get_variable(self, variable_name: str, default_value: any = None)->any:
        """Obtiene una variable almacenada en el gestor de escenas."""
        return self.variables.get(variable_name)

    '''def create_thread(self, task:function)->any:
        # Crea un hilo y le asigna la función my_task
        thread = threading.Thread(target=task)
        
        # Inicia el hilo
        thread.start()
        
        # Devuelve el hilo para que pueda ser gestionado externamente si es necesario
        return thread'''
        
    def add_scene(self, name:str, scene_class:object)->None:
        """Agrega una nueva escena al gestor."""
        if name in self.scenes:
            print(f"Escena '{name}' ya existe.")
        else:
            self.scenes[name] = scene_class

    def switch_scene(self, name:str)->None:
        """Cambia a otra escena asegurando que la anterior sea eliminada completamente."""
        if self.current_scene:
            self.current_scene.pack_forget()
            self.current_scene.place_forget()
            self.current_scene.grid_forget()

        # Cargar la nueva escena
        scene_class = self.scenes.get(name)
        if scene_class:
            self.current_scene = scene_class(self, self)
            self.current_scene.pack(fill='both', expand=True)
        else:
            print(f"Escena '{name}' no encontrada.")

    def force_switch_scene(self, name:str)->None:
        """Cambia de escena y fuerza la eliminación de la escena actual."""
        if self.current_scene:
            # Destruye todos los widgets de la escena actual
            for widget in self.current_scene.winfo_children():
                widget.destroy()

            self.current_scene.destroy()

        # Cargar la nueva escena
        scene_class = self.scenes.get(name)
        if scene_class:
            self.current_scene = scene_class(self, self)
            self.current_scene.pack(fill='both', expand=True)
        else:
            print(f"Escena '{name}' no encontrada.")
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

# Otro ejemplo de una escena
class Scene2(BaseScene):
    def __init__(self, parent, manager):
        """Inicializa la segunda escena.

        Configura la interfaz para Scene2, incluyendo una etiqueta y un botón.

        Args:
            parent (ctk.CTk): Ventana principal o gestor de escenas.
            manager (SceneManager): Gestor de escenas que maneja esta escena.
        """
        super().__init__(parent, manager)

        # Crea una etiqueta con texto para Scene2
        label = ctk.CTkLabel(self, text="This is Scene 2")
        label.pack(pady=20)  # Empaqueta la etiqueta con un relleno vertical

        # Crea un botón para cambiar a Scene1
        button = ctk.CTkButton(self, text="Go to Scene 1", 
                              command=lambda: manager.switch_scene("Scene1"))
        button.pack(pady=20)  # Empaqueta el botón con un relleno vertical

if __name__ == "__main__":
    app = SceneManager()  # Crea una instancia del gestor de escenas
    app.geometry("400x300")  # Establece el tamaño de la ventana

    # Añade las escenas al gestor
    app.add_scene("Scene1", Scene1)
    app.add_scene("Scene2", Scene2)

    # Inicia la aplicación con la primera escena visible
    app.switch_scene("Scene1")

    app.mainloop()  # Ejecuta el bucle principal de la aplicación
