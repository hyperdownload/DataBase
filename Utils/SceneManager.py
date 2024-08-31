import customtkinter as ctk

class SceneManager(ctk.CTk):
    def __init__(self):
        """Inicializa el gestor de escenas.

        Establece el gestor de escenas como una ventana de `customtkinter` y 
        prepara un diccionario para almacenar las escenas y una referencia 
        a la escena actual.
        """
        super().__init__()
        self.scenes = {}  # Diccionario para almacenar las escenas añadidas
        self.current_scene = None  # Referencia a la escena actualmente visible

    def add_scene(self, name, scene_class):
        """Agrega una nueva escena al gestor.

        Args:
            name (str): Nombre identificador para la escena.
            scene_class (BaseScene): Clase de la escena que se añadirá.
        """
        scene = scene_class(self, self)  # Crea una instancia de la escena
        self.scenes[name] = scene  # Almacena la escena en el diccionario con el nombre proporcionado

    def switch_scene(self, name):
        """Cambia a una nueva escena.

        Oculta la escena actual y muestra la nueva escena especificada.

        Args:
            name (str): Nombre de la escena a la que se cambiará.
        """
        if self.current_scene:
            self.current_scene.pack_forget()  # Oculta la escena actual
        scene = self.scenes.get(name)  # Obtiene la nueva escena del diccionario
        if scene:
            scene.pack(fill='both', expand=True)  # Muestra la nueva escena
            self.current_scene = scene  # Actualiza la referencia a la escena actual
        else:
            print(f"Scene '{name}' no encontrada.")  # Mensaje en caso de que la escena no exista

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
