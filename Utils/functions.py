import customtkinter as ctk
from PIL import Image  # Importa Image desde PIL
color_p = "#fafafa"
color_s = "#efefef"
grey = "#EDEBE9"
blue = "#0080ff"
black = "#131313"

def header(manager)->any:
    btn_config = {'font': ('Plus jakarta Sans', 14, 'bold'), 'text_color': "#000000",'fg_color': "transparent", 'hover_color': "#dcdcdc", 'height': 35,}
    user_img = ctk.CTkImage(Image.open("img/person.png"), size=(20, 20))

    header_fr = ctk.CTkFrame(manager, fg_color=color_p, border_color=color_s, border_width=1, height=70, width=800)
    header_fr.place(relx=0.5, y=35, anchor="center")

    name = ctk.CTkLabel(header_fr, text="|Urbanvibe", font=('Plus Jakarta Sans', 28, 'bold'))
    name.place(x=100, rely=0.5, anchor="center")

    user = ctk.CTkButton(header_fr, text="", image=user_img, fg_color="transparent", hover_color="#dcdcdc", height=35, width=35, cursor="hand2")
    user.place(x=800 - 50, rely=0.5, anchor="center")
    
    # NAV Frame
    nav = ctk.CTkFrame(header_fr, fg_color=color_p, height=65, width=406)
    nav.place(relx=0.5, y=35, anchor="center")

    # Los botones
    btn_nav = [("Stock", (406 // 2) - 80, None, lambda: manager.switch_scene("Stock_nav"), 70),
               ("Home", 406 // 2, None, lambda: manager.switch_scene("Men_p"), 70),
               ("Ventas", (406 // 2) + 80, None, lambda: manager.switch_scene("Ventas_nav"), 70)]
    
    for text, x_cord, img, command, width in btn_nav:
        button = ctk.CTkButton(nav, text=text, image=img, **btn_config, width=width, command=command)
        button.place(x=x_cord, rely=0.5, anchor="center")

    return header_fr

def predict_search(product_list: list, search: str, max_distance: int = 3) -> list:
    """Predice sugerencias de búsqueda basadas en la similitud de cadenas.
    
    La función devuelve una lista de productos cuyo nombre es similar al texto de búsqueda
    basado en la distancia de Levenshtein.
    
    Args:
        product_list (list): Lista de objetos de producto a buscar.
        search (str): Cadena de búsqueda actual o texto ingresado por el usuario.
        max_distance (int): Margen de error permitido para considerar una coincidencia.
    
    Returns:
        list: Lista de productos sugeridos.
    """
    suggestions = []
    
    # Itera sobre cada producto en la lista
    for product in product_list:
        # Calcula la distancia de Levenshtein entre la búsqueda y el nombre del producto
        distance = levenshtein_distance(search.lower(), product.name.lower())
        
        # Si la distancia es menor o igual al margen de error permitido, considera el producto como una sugerencia
        if distance <= max_distance:
            suggestions.append(product)
    
    # Ordena las sugerencias por la distancia de Levenshtein (menor distancia primero)
    suggestions.sort(key=lambda x: levenshtein_distance(search.lower(), x.name.lower()))
    
    return suggestions

def levenshtein_distance(s1: str, s2: str) -> int:
    """Calcula la distancia de Levenshtein entre dos cadenas.
    
    La distancia de Levenshtein es el número mínimo de ediciones (inserciones,
    eliminaciones o sustituciones) necesarias para transformar una cadena en otra.
    """
    # Asegura que s1 sea la cadena más corta para optimizar el cálculo
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    # Crea una lista que representa la distancia desde la cadena vacía hasta cada prefijo de s1
    distances = range(len(s1) + 1)
    
    # Itera sobre cada carácter de s2
    for i2, c2 in enumerate(s2):
        # Inicializa una nueva lista de distancias para la fila actual
        distances_ = [i2 + 1]
        
        # Itera sobre cada carácter de s1
        for i1, c1 in enumerate(s1):
            # Determina el costo de sustitución (0 si los caracteres son iguales, 1 si son diferentes)
            cost = 0 if c1 == c2 else 1
            
            # Calcula la distancia mínima para la posición actual
            distances_.append(min(
                distances[i1] + cost,    # Costo de sustitución o coincidencia
                distances[i1 + 1] + 1,   # Costo de eliminación
                distances_[-1] + 1       # Costo de inserción
            ))
        
        # Actualiza la lista de distancias para la siguiente iteración
        distances = distances_
    
    # La última posición de la lista de distancias contiene la distancia de Levenshtein
    return distances[-1]

def search_function(product_list: list, search: str, max_distance: int = 3) -> list:
    result = []
    
    for product in product_list:
        # Calcula la distancia de Levenshtein entre la búsqueda y el nombre del producto
        distance = levenshtein_distance(search.lower(), product.name.lower())
        
        # Si la distancia es menor o igual al margen de error permitido, considera el producto como una coincidencia
        if distance <= max_distance:
            result.append(product)
    
    return result