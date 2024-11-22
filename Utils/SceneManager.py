import customtkinter as ctk
import logging
from difflib import get_close_matches
import threading
import traceback
import random
from Utils.functions import *

# Configuración del logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

class SceneManager(ctk.CTk):
    def __init__(self):
        """Inicializa el gestor de escenas."""
        super().__init__()
        self.scenes = {}  # Diccionario para almacenar las escenas añadidas
        self.variables = {}  # Variables almacenadas para interactuar con otras escenas
        self.scene_history = []  # Historial de escenas visitadas
        self.current_scene = None  # Referencia a la escena actual
        self.current_scene_name = None  # Nombre de la escena actual

        # Agrega una escena de error por defecto
        self.add_scene("Error", Error)
        logging.info("SceneManager inicializado correctamente.")

    def save_variable(self, variable_name: str, variable_value: any) -> None:
        """Almacena una variable en el gestor de escenas."""
        self.variables[variable_name] = variable_value
        logging.debug(f"Variable '{variable_name}' almacenada con valor: {variable_value}")

    def get_variable(self, variable_name: str) -> any:
        """Obtiene una variable almacenada en el gestor de escenas."""
        try:
            if var := self.variables.get(variable_name):
                logging.debug(f"Variable '{variable_name}' obtenida con valor: {var}")
                return var
            if close_matches := get_close_matches(
                variable_name, self.variables.keys(), n=1, cutoff=0.5
            ):
                suggestion = close_matches[0]
                raise NameError(f"Variable no definida. ¿Quizás quisiste decir '{suggestion}'?")
            else:
                raise NameError(f"Variable '{variable_name}' no está definida.")
        except NameError as e:
            logging.error(str(e))
            traceback.print_exc()
            raise

    def add_scene(self, name: str, scene_class: object) -> None:
        """Agrega una nueva escena al gestor."""
        if name in self.scenes:
            logging.warning(f"Escena '{name}' ya existe y no será añadida nuevamente.")
        else:
            self.scenes[name] = scene_class
            logging.info(f"Escena '{name}' añadida correctamente.")

    def switch_scene(self, name: str, bypass:bool=False) -> None:
        """Cambia a otra escena asegurando que la anterior sea eliminada completamente."""
        try:
            if name == self.current_scene_name and not bypass:
                logging.info(f"La escena actual ya es '{name}'. No se necesita cambiar.")
                return

            if not (scene_class := self.scenes.get(name)):
                logging.warning(f"Escena '{name}' no encontrada.")
                self.show_error()
                return

            self.scene_history.append(name)
            self.current_scene_name = name

            # Eliminar widgets de la escena actual
            if self.current_scene:
                self.current_scene.pack_forget()
                self.current_scene.place_forget()
                self.current_scene.grid_forget()

            # Instanciar y mostrar la nueva escena
            self.current_scene = scene_class(self, self)
            self.current_scene.pack(fill="both", expand=True)
            logging.info(f"Cambiado a la escena '{name}'.")
        except Exception as e:
            logging.error(f"Error al cambiar a la escena '{name}': {e}")
            traceback.print_exc()

    def show_error(self):
        """Muestra la escena de error predeterminada."""
        try:
            self.switch_scene("Error")
            logging.error("Mostrando escena de error.")
        except Exception as e:
            logging.critical(f"Error al mostrar la escena de error: {e}")
            traceback.print_exc()

    def clear_widget(self, *widgets):
        """Elimina todos los widgets o los hijos de los widgets dados."""
        try:
            for widget in widgets:
                for child in widget.winfo_children():
                    self._destroy_widget(child)
                self._destroy_widget(widget)
            logging.debug("Todos los widgets han sido eliminados correctamente.")
        except Exception as e:
            logging.error(f"Error al intentar eliminar widgets: {e}")
            traceback.print_exc()

    def _destroy_widget(self, widget):
        """Destruye un widget de forma segura."""
        widget.pack_forget()
        widget.grid_forget()
        widget.place_forget()
        widget.destroy()

    def refresh_current_scene(self):
        """Actualiza la escena actual recargándola."""
        try:
            if not self.current_scene_name:
                raise ValueError("No hay una escena actual para refrescar.")
            self.switch_scene(self.current_scene_name, True)
            logging.info(f"Escena '{self.current_scene_name}' refrescada correctamente.")
        except Exception as e:
            logging.error(f"Error al refrescar la escena: {e}")
            traceback.print_exc()

# Clase base para las escenas
class BaseScene(ctk.CTkFrame):
    def __init__(self, parent, manager):
        """Inicializa una escena base.

        Args:
            parent (ctk.CTk): Ventana principal o gestor de escenas.
            manager (SceneManager): Gestor de escenas que maneja esta escena.
        """
        super().__init__(parent)
        self.manager = manager 
        self.scene_name = self.__class__.__name__ 
        logging.info(f"Inicializando escena base '{self.scene_name}'.")
        
        try:
            self.initialize_components()
            logging.debug(f"Componentes inicializados para '{self.scene_name}'.")
        except Exception as e:
            logging.error(f"Error al inicializar componentes en '{self.scene_name}': {e}")
            raise

    def initialize_components(self):
        """Método para inicializar los componentes de la escena.

        Este método puede ser sobrescrito por clases que hereden de `BaseScene`.
        """
        logging.debug(f"No se sobrescribió 'initialize_components' en '{self.scene_name}'.")

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

class Error(BaseScene):
    def __init__(self, parent, manager, dict):
        """Inicializa la primera escena.

        Configura la interfaz para Scene1, incluyendo una etiqueta y un botón.

        Args:
            parent (ctk.CTk): Ventana principal o gestor de escenas.
            manager (SceneManager): Gestor de escenas que maneja esta escena.
        """
        super().__init__(parent, manager)

        self.manager = manager
        self.elements = []
        label = ctk.CTkLabel(self, text=f"Hubo un error: {dict["error"]}")
        label.pack(pady=20)  
        button = ctk.CTkButton(self, text="Volver", 
                              command=lambda: manager.switch_scene(dict["scene"]))
        button.pack(pady=20) 
        animation_thread = threading.Thread(target=self.something)
        animation_thread.daemon = True
        animation_thread.start()

    def something(self, quantity=15):
        for _ in range(quantity):
            self.elements.append(ImageP(self.manager,height=25,width=25, x=400, y=300, color='red'))
        while True:
            timea = random.randint(1,15)
            for element in self.elements:
                x = random.randint(1,800)
                y = random.randint(1,600)
                element.animate_to(x, y, timea, 100)
            time.sleep(timea+1)
            
if __name__ == "__main__":
    app = SceneManager()  # Crea una instancia del gestor de escenas
    app.geometry("400x300")  # Establece el tamaño de la ventana

    # Añade las escenas al gestor
    app.add_scene("Scene1", Scene1)

    # Inicia la aplicación con la primera escena visible
    app.switch_scene("Scene1")

    app.mainloop()  # Ejecuta el bucle principal de la aplicación