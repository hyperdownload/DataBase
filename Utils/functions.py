import customtkinter as ctk
from PIL import Image  # Importa Image desde PIL
color_p = "#fafafa"
color_s = "#efefef"
grey = "#EDEBE9"
blue = "#0080ff"
black = "#131313"

def create_scrollable_frame(manager, color_p, branch_user, fg_color="black", font=('Plus Jakarta Sans', 20, 'bold')):
    # Crea el CTkScrollableFrame
    main_fr = ctk.CTkScrollableFrame(manager, fg_color=color_p, height=530, width=780)
    main_fr.place(relx=0.5, y=341, anchor="center")

    # Crea el frame de la sucursal dentro del scrollable frame
    sucursal_fr = ctk.CTkFrame(main_fr, fg_color=color_p, height=70, width=780)
    sucursal_fr.grid(row=0, column=0, columnspan=4)

    # Crea la etiqueta de la sucursal
    sucursal_lb = ctk.CTkLabel(sucursal_fr, text_color=fg_color, text=f'Sucursal {branch_user}', font=font)
    sucursal_lb.place(x=(sucursal_lb.winfo_width()) // 2 + 115, rely=0.5, anchor="center")
    
    return main_fr, sucursal_fr, sucursal_lb

def header(manager)->any:
    btn_config = {'font': ('Plus jakarta Sans', 14, 'bold'), 'text_color': "#000000",'fg_color': "transparent", 'hover_color': "#dcdcdc", 'height': 35,}
    user_img = ctk.CTkImage(Image.open("img/person.png"), size=(20, 20))

    header_fr = ctk.CTkFrame(manager, fg_color=color_p, border_color=color_s, border_width=1, height=70, width=800)
    header_fr.place(relx=0.5, y=35, anchor="center")

    name = ctk.CTkLabel(header_fr, text="|Urbanvibe", text_color=black, font=('Plus Jakarta Sans', 28, 'bold'))
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

def levenshtein_distance(s1: str, s2: str) -> int:
    """Calcula la distancia de Levenshtein entre dos cadenas."""
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    # Crea una lista que representa la distancia desde la cadena vacía hasta cada prefijo de s1
    distances = range(len(s1) + 1)

    # Itera sobre cada carácter de s2
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            cost = 0 if c1 == c2 else 1
            distances_.append(min(
                distances[i1] + cost,    # Costo de sustitución o coincidencia
                distances[i1 + 1] + 1,   # Costo de eliminación
                distances_[-1] + 1       # Costo de inserción
            ))
        distances = distances_

    return distances[-1]

def normalize_string(s: str) -> str:
    """Normaliza una cadena para eliminar espacios en blanco adicionales y convertir a minúsculas."""
    return ''.join(c for c in s.lower().strip() if c.isalnum())

def fuzzy_match(s1: str, s2: str) -> float:
    """Calcula una puntuación de coincidencia difusa entre dos cadenas basándose en Levenshtein."""
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0  # Cadenas vacías coinciden completamente
    distance = levenshtein_distance(s1, s2)
    return 1 - (distance / max_len)  # Puntuación entre 0 y 1

def search_function(product_list: list, search: str, max_distance: int = 8, threshold: float = 0.4) -> list:
    """Mejora la precisión de la búsqueda utilizando coincidencias difusas y normalización."""
    search_normalized = normalize_string(search)
    result = []

    for product in product_list:
        product_name_normalized = normalize_string(product.name)
        
        # Coincidencia difusa con ponderación
        match_score = fuzzy_match(search_normalized, product_name_normalized)
        
        # Si la puntuación de coincidencia es mayor que el umbral, considera el producto como coincidencia
        if match_score >= threshold:
            result.append((product, match_score))
    
    # Ordena los resultados por la puntuación de coincidencia
    result.sort(key=lambda x: x[1], reverse=True)

    # Devuelve solo la lista de productos
    return [product for product, score in result]
