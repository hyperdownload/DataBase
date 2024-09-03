from Utils.SceneManager import *
from Utils.database import *
class Login(BaseScene):
    def __init__(self, parent, manager):
        super().__init__(parent, manager)
        
        self.manager=manager
        self.paleta_colores()

        self.login()

    def paleta_colores(self):
        self.color_p = "#000000"
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

        if hashlib.sha256(password.encode()).hexdigest()==get_user_details(get_user_id(user))[2]:
            print("LOGEAO")
        else:
            print("Usuario o contraseña erroneos")
if __name__ == "__main__":
    app = SceneManager()  # Crea una instancia del gestor de escenas
    x = (app.winfo_screenwidth() // 2)-(800 // 2)
    y = (app.winfo_screenheight() // 2)-(600 // 2)
    app.geometry(f"800x600+{x}+{y}")  # Establece el tamaño de la ventana
    app.resizable(False,False)

    # Añade las escenas al gestor
    app.add_scene("Login", Login)

    # Inicia la aplicación con la primera escena visible
    app.switch_scene("Login")

    app.mainloop()  # Ejecuta el bucle principal de la aplicación
