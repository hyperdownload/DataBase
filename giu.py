from Utils.SceneManager import *
from Utils.database import *
from PIL import Image  # Importa Image desde PIL
import customtkinter as ctk

class Login(BaseScene):
    def __init__(self, parent, manager):
        super().__init__(parent, manager)
        
        self.manager=manager
        self.paleta_colores()

        self.login()

    def paleta_colores(self):
        self.color_p = "#fafafa"
        self.color_s = "#efefef"
        self.grey = "#EDEBE9"
        self.blue = "#0080ff"
        self.black = "#131313"
    def login(self):
        self.manager.title("Login")
        login_container = ctk.CTkFrame(self.manager, width = 400, height = 600, fg_color= self.color_p)
        login_container.place(x = 0, y = 0)
        
        bienvenida_lb = ctk.CTkLabel(login_container, text = "Welcome to back", font=('Plus Jakarta Sans', 28, 'bold'))
        bienvenida_lb.place(relx= 0.5, y=175, anchor= "center")

        user_lb = ctk.CTkLabel(login_container, text = "Usuario", font=('Plus Jakarta Sans', 16, 'bold'))
        user_lb.place(x = 58, y=250, anchor= "center")
        self.user_entry = ctk.CTkEntry(login_container, height = 35, width = 350, corner_radius = 20, placeholder_text = "Ingrese su nombre de usuario...")
        self.user_entry.place(relx=0.5, y=290, anchor= "center")

        password_lb = ctk.CTkLabel(login_container, text = "Contraseña", font=('Plus Jakarta Sans', 16, 'bold'))
        password_lb.place(x = 70, y=340, anchor= "center")
        self.password_entry = ctk.CTkEntry(login_container, height = 35, width = 350, corner_radius = 20, placeholder_text = "Ingrese su contraseña...")
        self.password_entry.place(relx=0.5, y=380, anchor= "center")

        submit = ctk.CTkButton(login_container, text = "Login", height = 35, width = 350, corner_radius = 20, fg_color = self.black, text_color = self.color_p, hover_color = "#454545", command = self.login_logic)
        submit.place(relx=0.5, y=430, anchor= "center")
    def login_logic(self):
        user = self.user_entry.get()
        password = self.password_entry.get()

        if hashlib.sha256(password.encode()).hexdigest() == get_user_details(get_user_id(user))[2]:
            print("AAAAAAA")
        else:
            print("naonao")
            
class Men_p(BaseScene):

    def __init__(self, parent, manager):
        super().__init__(parent, manager)

        self.manager=manager
        self.paleta_colores()
        self.header()
        self.main()

    def paleta_colores(self):
        self.color_p = "#fafafa"
        self.color_s = "#efefef"
        self.grey = "#EDEBE9"
        self.blue = "#0080ff"
        self.black = "#131313"


    def header(self):
        self.manager.title("Menu principal")
        self.btn_config = {'font': ('Plus jakarta Sans', 14, 'bold'), 'text_color': "#000000",'fg_color': "transparent", 'hover_color': "#dcdcdc", 'height': 35,}
        user_img = ctk.CTkImage(Image.open("img/person.png"), size=(20, 20))
        search_img = ctk.CTkImage(Image.open("img/search.png"), size=(20, 20))

        self.header_fr = ctk.CTkFrame(self.manager, fg_color= self.color_p, border_color= self.color_s, border_width=1, height= 70, width= 800)
        self.header_fr.place(relx = 0.5, y = 35, anchor= "center")

        self.name = ctk.CTkLabel(self.header_fr, text= "|Urbanvibe", font=('Plus Jakarta Sans', 28, 'bold'))
        self.name.place(x = 100, rely = 0.5, anchor= "center")

        self.user = ctk.CTkButton(self.header_fr, text= "", image = user_img, fg_color= "transparent", hover_color= "#dcdcdc", height= 35, width=35, cursor = "hand2")
        self.user.place(x=800 - 50, rely=0.5, anchor= "center")

        self.search = ctk.CTkButton(self.header_fr, text= "", image = search_img, fg_color= "transparent", hover_color= "#dcdcdc"
                                    , height= 35, width= 35, cursor = "hand2", command= self.search_logic)
        self.search.place_configure(x = 710, rely=0.5, anchor= "center")
        
        # -----------------------------------------------NAV------------------------------------------------
        self.nav = ctk.CTkFrame(self.header_fr, fg_color= self.color_p, height= 65, width= 406)
        self.nav.place(relx = 0.5, y = 35, anchor= "center")
        
        # Texto - Cordenadas X - imagenes - command - Width
        btn_nav = [("Stock", (406//2) -80, None, None,70), ("Home", 406//2, None,  None,70), ("Ventas", (406//2) +80, None, None,70)]
        for text, x_cord, img, command, width in btn_nav:
            button = ctk.CTkButton(self.nav, text= text, image = img, **self.btn_config, width= width , command= command)
            button.place(x = x_cord, rely = 0.5, anchor= "center")
    
    def search_logic(self):
        if hasattr(self, 'search_entry') and self.search_entry.winfo_ismapped(): #comprueba si existe y es visible
            self.search_entry.place_forget()
            self.search.configure(fg_color =  "transparent", hover_color = "#dcdcdc")
            self.nav.place(relx = 0.5, y = 35, anchor= "center")
            
        else:
            # self.nav.place_forget()
            self.search_entry = ctk.CTkEntry(self.header_fr, placeholder_text= "Buscar producto...", width= 155, height=35,
                                        corner_radius=35, border_color= "#252525", text_color= "#252525")
            self.search_entry.place_configure(x = 600, rely=0.5, anchor= "center") 
            self.search.configure(fg_color =  "#dcdcdc", hover_color = self.color_p)

    def main(self):
        self.main_fr = ctk.CTkScrollableFrame(self.manager, fg_color= self.color_p, height= 530, width= 780)
        self.main_fr.place(relx = 0.5,y = 341, anchor = "center")

        self.sucursal_fr = ctk.CTkFrame(self.main_fr, fg_color = self.color_p, height = 70, width = 780)
        self.sucursal_fr.grid(row=0, column=0, columnspan=2)
        self.sucursal_lb = ctk.CTkLabel(self.sucursal_fr, text = "Sucursal San Miguel", font=('Plus Jakarta Sans', 20, 'bold')) #Aca se reemplazara el texto por las sucursales de la bd
        self.sucursal_lb.place(x = (self.sucursal_lb.winfo_width())//2 + 115, rely = 0.5 , anchor= "center")

        self.h_grid1= 300
        self.h_grid2= 400
        self.altura_fr = self.h_grid1+self.h_grid2+50
        
        self.col_tabla()
        self.col_atajo()
        self.grafico()

    def col_tabla(self):
        self.width_tablas = 470
        
        self.tablas_frame = ctk.CTkFrame(self.main_fr, width= self.width_tablas, height= self.altura_fr, fg_color= self.color_p)
        self.tablas_frame.grid(row=1, column=0, padx = 12)

        self.tabla1 = ctk.CTkFrame(self.tablas_frame, width= self.width_tablas, height= self.h_grid1, fg_color= self.grey, corner_radius= 40)
        self.tabla1.place(x = 0, y = 0)

        self.tabla2 = ctk.CTkFrame(self.tablas_frame, width= self.width_tablas, height= self.h_grid2, fg_color= self.black, corner_radius= 40)
        self.tabla2.place(x = 0, y = 325)
    
    def cambiar_color(self, widget, text_color, fg_color, event=None):
        widget.configure(text_color=text_color, fg_color=fg_color)
    #--------------------------------------------------------------------------------------------------------------------------------------------

    def col_atajo(self):
        self.atajos_frame = ctk.CTkFrame(self.main_fr, width= 270, height= self.altura_fr, fg_color= self.color_p)
        self.atajos_frame.grid(row=1, column=1, padx = 12)

        #--------------------------------------------------------------------------------------------------------------------------------------------

        self.cargar_prod_lb = ctk.CTkLabel(self.atajos_frame, width= 270, height= self.h_grid1, fg_color= self.grey,
                                            corner_radius= 40)
        self.cargar_prod_lb.place(x = 0, y = 0)

        self.cargar_productos_txt = ctk.CTkLabel(self.cargar_prod_lb, text= "Cargar\nProductos", font=('Plus Jakarta Sans', 38, 'bold'), justify = "left")
        self.cargar_productos_txt.place(x = 35, y = 50)
        self.c_productos_btn = ctk.CTkButton(self.cargar_prod_lb, text= "Cargar", fg_color= self.black, text_color= self.color_p, corner_radius=25,
                                            width= 200, height= 50, font=('Plus Jakarta Sans', 24, 'bold'), hover_color= "#454545", command= self.cargar_producto_logica)
        self.c_productos_btn.place(relx = 0.5, y = self.h_grid1 -75, anchor = "center")

        self.c_productos_btn.bind("<Enter>", lambda event: self.cambiar_color(self.c_productos_btn, self.grey, "#454545", event))
        self.c_productos_btn.bind("<Leave>", lambda event: self.cambiar_color(self.c_productos_btn, self.grey, self.black, event))
        #--------------------------------------------------------------------------------------------------------------------------------------------

        self.ult_venta = ctk.CTkLabel(self.atajos_frame, width= 270, height= self.h_grid2, fg_color= self.black, corner_radius= 40)
        self.ult_venta.place(relx = 0.5, y = self.altura_fr- (self.h_grid2//2)-25, anchor= "center")

        self.ult_venta_txt = ctk.CTkLabel(self.ult_venta, text= "Registrar\nUltima venta", font=('Plus Jakarta Sans', 38, 'bold'), text_color= self.grey,
                                        justify = "center", wraplength= 200)
        self.ult_venta_txt.place(relx = 0.5, y = 150, anchor = "center")
        self.u_venta_btn = ctk.CTkButton(self.ult_venta, text= "Registrar", fg_color= self.grey, text_color= self.black, corner_radius=25,
                                            width= 200, height= 50, font=('Plus Jakarta Sans', 24, 'bold'), hover_color= "#454545")
        self.u_venta_btn.place(relx = 0.5, y = self.h_grid2 -75, anchor = "center")        

        self.u_venta_btn.bind("<Enter>", lambda event: self.cambiar_color(self.u_venta_btn, self.grey, "#454545", event))
        self.u_venta_btn.bind("<Leave>", lambda event: self.cambiar_color(self.u_venta_btn, self.black, self.grey, event))
        #--------------------------------------------------------------------------------------------------------------------------------------------
    def grafico(self):
        self.grafico = ctk.CTkLabel(self.main_fr, width= 765, height= self.h_grid2, fg_color= self.grey,
                                    corner_radius= 40, text = "Futuro grafico| proyecto en mantenimiento")
        self.grafico.grid(row=2, column=0, columnspan=2, ipady= 6)
        
    def cargar_producto_logica(self):
        for widget in self.main_fr.winfo_children():
            if widget != self.sucursal_fr:
                widget.destroy()
        lupa = ctk.CTkImage(Image.open("img/search.png"), size=(35, 35))
        
        self.cp_fr = ctk.CTkFrame(self.main_fr, fg_color = self.color_p, height = 85, width = self.x)
        self.cp_fr.grid(row=1, column=0)
        buscar_producto = ctk.CTkEntry(self.cp_fr, placeholder_text= "Buscar producto...", width= 600, height=50,
                                        corner_radius=35, border_color= "#dcdcdc", text_color= "#252525")
        buscar_producto.place(relx = 0.5, rely = 0.5, anchor= "center")
        bp_btn = ctk.CTkButton(self.cp_fr, text= "", image = lupa, fg_color= self.color_s, hover_color= "#dcdcdc"
                                    , height= 50, width= 50, corner_radius= 15, cursor = "hand2")
        bp_btn.place(relx = 0.68, rely = 0.5, anchor= "center")
    #--------------------------------------------------------------------------------------------------------------------------------------------
        tabla = ctk.CTkFrame(self.main_fr, fg_color = self.color_p, height = 1000, width = self.x)
        tabla.grid(row=2, column=0)

        self.tabla_stock = ctk.CTkFrame(tabla, width= 1450, height= 800, fg_color= self.black, corner_radius= 40)
        self.tabla_stock.place(relx = 0.5, rely = 0.42, anchor= "center")


if __name__ == "__main__":
    app = SceneManager()  # Crea una instancia del gestor de escenas
    x = (app.winfo_screenwidth() // 2)-(800 // 2)
    y = (app.winfo_screenheight() // 2)-(600 // 2)
    app.geometry(f"800x600+{x}+{y}")  # Establece el tamaño de la ventana
    app.resizable(False,False)

    # Añade las escenas al gestor
    
    app.add_scene("Men_p", Men_p)
    app.add_scene("Login", Login)

    # Inicia la aplicación con la primera escena visible
    app.switch_scene("Login")
    #app.force_switch_scene("Men_p")
    #app.switch_scene("Men_p")

    app.mainloop()  # Ejecuta el bucle principal de la aplicación