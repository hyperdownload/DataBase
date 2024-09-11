from Utils.SceneManager import *
from Utils.database import *
from PIL import Image  # Importa Image desde PIL
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

color_p = "#fafafa"
color_s = "#efefef"
grey = "#EDEBE9"
blue = "#0080ff"
black = "#131313"

class Login(BaseScene):
	def __init__(self, parent, manager):
		super().__init__(parent, manager)
		
		self.manager=manager

		self.login()

	def login(self):
		self.manager.title("Login")
		login_container = ctk.CTkFrame(self.manager, width = 800, height = 600, fg_color= color_p)
		login_container.place(x = 0, y = 0)
		
		bienvenida_lb = ctk.CTkLabel(login_container, text = "Welcome to back", font=('Plus Jakarta Sans', 28, 'bold'))
		bienvenida_lb.place(relx= 0.5, y=185, anchor= "center")
		user_lb = ctk.CTkLabel(login_container, text = "Urbanlive", font=('Plus Jakarta Sans', 16, 'bold'), text_color= "#BEBEBE")
		user_lb.place(relx = 0.5 , y=215, anchor= "center")

		self.user_entry = ctk.CTkEntry(login_container, height = 35, width = 350, corner_radius = 20, placeholder_text = "Ingrese su nombre de usuario...")
		self.user_entry.place(relx=0.5, y=260, anchor= "center")

		self.password_entry = ctk.CTkEntry(login_container, height = 35, width = 350, corner_radius = 20, placeholder_text = "Ingrese su contraseña...")
		self.password_entry.place(relx=0.5, y=310, anchor= "center")

		submit = ctk.CTkButton(login_container, text = "Login", height = 35, width = 350, corner_radius = 20, fg_color = black, text_color = color_p, hover_color = "#454545", command = self.login_logic)
		submit.place(relx=0.5, y=360, anchor= "center")
	def login_logic(self):
		user = self.user_entry.get()
		password = self.password_entry.get()
		print(get_user_details(get_user_id(user)))
		if hashlib.sha256(password.encode()).hexdigest() == get_user_details(get_user_id(user))[2]:
			app.save_variable("user_role",get_user_details(get_user_id(user))[1])
			app.save_variable("branch_user",get_user_details(get_user_id(user))[3])
			self.manager.switch_scene("Men_p")
		else:   #contraseña incorrecta
			self.password_entry.configure(border_color = "red")
			
		#except:
			#self.user_entry.configure(border_color = "red")
			
			
class Men_p(BaseScene):

	def __init__(self, parent, manager):
		super().__init__(parent, manager)

		self.manager=manager
		self.header()
		self.main()
		self.manager.title("Menu principal")

	def header(self):
		self.btn_config = {'font': ('Plus jakarta Sans', 14, 'bold'), 'text_color': "#000000",'fg_color': "transparent", 'hover_color': "#dcdcdc", 'height': 35,}
		user_img = ctk.CTkImage(Image.open("img/person.png"), size=(20, 20))
		search_img = ctk.CTkImage(Image.open("img/search.png"), size=(20, 20))

		self.header_fr = ctk.CTkFrame(self.manager, fg_color= color_p, border_color= color_s, border_width=1, height= 70, width= 800)
		self.header_fr.place(relx = 0.5, y = 35, anchor= "center")

		self.name = ctk.CTkLabel(self.header_fr, text= "|Urbanvibe", font=('Plus Jakarta Sans', 28, 'bold'))
		self.name.place(x = 100, rely = 0.5, anchor= "center")

		self.user = ctk.CTkButton(self.header_fr, text= "", image = user_img, fg_color= "transparent", hover_color= "#dcdcdc", height= 35, width=35, cursor = "hand2")
		self.user.place(x=800 - 50, rely=0.5, anchor= "center")

		self.search = ctk.CTkButton(self.header_fr, text= "", image = search_img, fg_color= "transparent", hover_color= "#dcdcdc"
									, height= 35, width= 35, cursor = "hand2", command= self.search_logic)
		self.search.place_configure(x = 710, rely=0.5, anchor= "center")
		
		# -----------------------------------------------NAV------------------------------------------------
		self.nav = ctk.CTkFrame(self.header_fr, fg_color= color_p, height= 65, width= 406)
		self.nav.place(relx = 0.5, y = 35, anchor= "center")
		
		# Texto - Cordenadas X - imagenes - command - Width
		btn_nav = [("Stock", (406//2) -80, None, lambda: self.manager.switch_scene("Stock_nav"),70), ("Home", 406//2, None, lambda: self.manager.switch_scene("Men_p"),70), ("Ventas", (406//2) +80, None, lambda: self.manager.switch_scene("Ventas_nav"),70)]
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
			self.search.configure(fg_color =  "#dcdcdc", hover_color = color_p)

	def main(self):
		self.main_fr = ctk.CTkScrollableFrame(self.manager, fg_color= color_p, height= 530, width= 780)
		self.main_fr.place(relx = 0.5,y = 341, anchor = "center")

		self.sucursal_fr = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 70, width = 780)
		self.sucursal_fr.grid(row=0, column=0, columnspan=2)
		self.sucursal_lb = ctk.CTkLabel(self.sucursal_fr, text = f'Sucursal {app.get_variable("branch_user")}', font=('Plus Jakarta Sans', 20, 'bold')) #Aca se reemplazara el texto por las sucursales de la bd
		self.sucursal_lb.place(x = (self.sucursal_lb.winfo_width())//2 + 115, rely = 0.5 , anchor= "center")

		self.h_grid1= 300
		self.h_grid2= 400
		self.altura_fr = self.h_grid1+self.h_grid2+50
		
		self.col_tabla()
		self.col_atajo()
		self.grafico()

	def col_tabla(self):
		self.width_tablas = 470
		
		self.tablas_frame = ctk.CTkFrame(self.main_fr, width= self.width_tablas, height= self.altura_fr, fg_color= color_p)
		self.tablas_frame.grid(row=1, column=0, padx = 12)

		self.tabla1 = ctk.CTkFrame(self.tablas_frame, width= self.width_tablas, height= self.h_grid1, fg_color= grey, corner_radius= 40)
		self.tabla1.place(x = 0, y = 0)

		self.tabla2 = ctk.CTkFrame(self.tablas_frame, width= self.width_tablas, height= self.h_grid2, fg_color= black, corner_radius= 40)
		self.tabla2.place(x = 0, y = 325)
	
	def cambiar_color(self, widget, text_color, fg_color, event=None):
		widget.configure(text_color=text_color, fg_color=fg_color)
	#--------------------------------------------------------------------------------------------------------------------------------------------

	def col_atajo(self):
		self.atajos_frame = ctk.CTkFrame(self.main_fr, width= 270, height= self.altura_fr, fg_color= color_p)
		self.atajos_frame.grid(row=1, column=1, padx = 12)

		#--------------------------------------------------------------------------------------------------------------------------------------------

		self.cargar_prod_lb = ctk.CTkLabel(self.atajos_frame, width= 270, height= self.h_grid1, fg_color= grey,
											corner_radius= 40, text= "")
		self.cargar_prod_lb.place(x = 0, y = 0)

		self.cargar_productos_txt = ctk.CTkLabel(self.cargar_prod_lb, text= "Cargar\nProductos", font=('Plus Jakarta Sans', 38, 'bold'), justify = "left")
		self.cargar_productos_txt.place(x = 35, y = 50)
		self.c_productos_btn = ctk.CTkButton(self.cargar_prod_lb, text= "Cargar", fg_color= black, text_color= color_p, corner_radius=25,
											width= 200, height= 50, font=('Plus Jakarta Sans', 24, 'bold'), hover_color= "#454545", command=lambda: self.manager.switch_scene("C_producto"))
		self.c_productos_btn.place(relx = 0.5, y = self.h_grid1 -75, anchor = "center")

		self.c_productos_btn.bind("<Enter>", lambda event: self.cambiar_color(self.c_productos_btn, grey, "#454545", event))
		self.c_productos_btn.bind("<Leave>", lambda event: self.cambiar_color(self.c_productos_btn, grey, black, event))
		#--------------------------------------------------------------------------------------------------------------------------------------------

		self.ult_venta = ctk.CTkLabel(self.atajos_frame, width= 270, height= self.h_grid2, fg_color= black, corner_radius= 40)
		self.ult_venta.place(relx = 0.5, y = self.altura_fr- (self.h_grid2//2)-25, anchor= "center")

		self.ult_venta_txt = ctk.CTkLabel(self.ult_venta, text= "Registrar\nUltima venta", font=('Plus Jakarta Sans', 38, 'bold'), text_color= grey,
										justify = "center", wraplength= 200)
		self.ult_venta_txt.place(relx = 0.5, y = 150, anchor = "center")
		self.u_venta_btn = ctk.CTkButton(self.ult_venta, text= "Registrar", fg_color= grey, text_color= black, corner_radius=25,
											width= 200, height= 50, font=('Plus Jakarta Sans', 24, 'bold'), hover_color= "#454545", command=lambda: self.manager.switch_scene("C_ventas"))
		self.u_venta_btn.place(relx = 0.5, y = self.h_grid2 -75, anchor = "center")        

		self.u_venta_btn.bind("<Enter>", lambda event: self.cambiar_color(self.u_venta_btn, grey, "#454545", event))
		self.u_venta_btn.bind("<Leave>", lambda event: self.cambiar_color(self.u_venta_btn, black, grey, event))
		#--------------------------------------------------------------------------------------------------------------------------------------------
	def grafico(self):
		self.grafico = ctk.CTkLabel(self.main_fr, width= 765, height= self.h_grid2, fg_color= grey,
									corner_radius= 40, text = "Futuro grafico| proyecto en mantenimiento")
		self.grafico.grid(row=2, column=0, columnspan=2, ipady= 6)
		

class C_producto(BaseScene):

	def __init__(self, parent, manager):
		super().__init__(parent, manager)

		self.manager=manager
		self.manager.title("Carga de productos")
		self.header()
		self.main()


	def header(self):
		self.btn_config = {'font': ('Plus jakarta Sans', 14, 'bold'), 'text_color': "#000000",'fg_color': "transparent", 'hover_color': "#dcdcdc", 'height': 35,}
		user_img = ctk.CTkImage(Image.open("img/person.png"), size=(20, 20))
		search_img = ctk.CTkImage(Image.open("img/search.png"), size=(20, 20))

		self.header_fr = ctk.CTkFrame(self.manager, fg_color= color_p, border_color= color_s, border_width=1, height= 70, width= 800)
		self.header_fr.place(relx = 0.5, y = 35, anchor= "center")

		self.name = ctk.CTkLabel(self.header_fr, text= "|Urbanvibe", font=('Plus Jakarta Sans', 28, 'bold'))
		self.name.place(x = 100, rely = 0.5, anchor= "center")

		self.user = ctk.CTkButton(self.header_fr, text= "", image = user_img, fg_color= "transparent", hover_color= "#dcdcdc", height= 35, width=35, cursor = "hand2")
		self.user.place(x=800 - 50, rely=0.5, anchor= "center")

		self.search = ctk.CTkButton(self.header_fr, text= "", image = search_img, fg_color= "transparent", hover_color= "#dcdcdc"
									, height= 35, width= 35, cursor = "hand2", command= self.search_logic)
		self.search.place_configure(x = 710, rely=0.5, anchor= "center")
		
		# -----------------------------------------------NAV------------------------------------------------
		self.nav = ctk.CTkFrame(self.header_fr, fg_color= color_p, height= 65, width= 406)
		self.nav.place(relx = 0.5, y = 35, anchor= "center")
		
		# Texto - Cordenadas X - imagenes - command - Width
		btn_nav = [("Stock", (406//2) -80, None, lambda: self.manager.switch_scene("Stock_nav"),70), ("Home", 406//2, None, lambda: self.manager.switch_scene("Men_p"),70), ("Ventas", (406//2) +80, None, lambda: self.manager.switch_scene("Ventas_nav"),70)]
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
			self.search.configure(fg_color =  "#dcdcdc", hover_color = color_p)

	def main(self):
		self.main_fr = ctk.CTkScrollableFrame(self.manager, fg_color= color_p, height= 530, width= 780)
		self.main_fr.place(relx = 0.5,y = 341, anchor = "center")

		self.sucursal_fr = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 70, width = 780)
		self.sucursal_fr.grid(row=0, column=0, columnspan=2)
		self.sucursal_lb = ctk.CTkLabel(self.sucursal_fr, text =  f'Sucursal {app.get_variable("branch_user")}', font=('Plus Jakarta Sans', 20, 'bold')) #Aca se reemplazara el texto por las sucursales de la bd
		self.sucursal_lb.place(x = (self.sucursal_lb.winfo_width())//2 + 115, rely = 0.5 , anchor= "center")
	#--------------------------------------------------------------------------------------------------------------------------------------------
		lupa = ctk.CTkImage(Image.open("img/search.png"), size=(35, 35))
		
		self.cp_fr = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 85, width = 800)
		self.cp_fr.grid(row=1, column=0)
		buscar_producto = ctk.CTkEntry(self.cp_fr, placeholder_text= "Buscar producto...", width= 250, height=50,
										corner_radius=35, border_color= "#dcdcdc", text_color= "#252525")
		buscar_producto.place(x = 185, rely = 0.5, anchor= "center")
		bp_btn = ctk.CTkButton(self.cp_fr, text= "", image = lupa, fg_color= color_s, hover_color= "#dcdcdc"
									, height= 50, width= 50, corner_radius= 15, cursor = "hand2")
		bp_btn.place(x = 355, rely = 0.5, anchor= "center")

		c_stock = ctk.CTkEntry(self.cp_fr, placeholder_text= "Subir producto...", width= 250, height=50,
										corner_radius=35, border_color= "#dcdcdc", text_color= "#252525" )
		c_stock.place(x = 525, rely= 0.5, anchor= "center")

		c_btn = ctk.CTkButton(self.cp_fr, text= "subir", fg_color= black, hover_color= "#dcdcdc"
									, height= 50, width= 75, corner_radius= 15, cursor = "hand2")
		c_btn.place(x = 700, rely = 0.5, anchor= "center")
	#--------------------------------------------------------------------------------------------------------------------------------------------
		tabla = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 425, width = 800)
		tabla.grid(row=2, column=0)

		self.tabla_stock = ctk.CTkFrame(tabla, width= 675, height= 400, fg_color= black, corner_radius= 40)
		self.tabla_stock.place(relx = 0.5, y= 200, anchor= "center")

		treeview = ttk.Treeview(self.tabla_stock, columns=("price", "brand", "size", "description"))
		treeview.place(relx = 0.5, rely= 0.5, anchor= "center", width = 625, height= 350)
		style = ttk.Style()
		style.theme_use("default")
		style.configure("Treeview.Heading", background= black, foreground="white", font=("Arial", 12, "bold"), relief = "flat")
		style.configure("Treeview", background= black, foreground="white", fieldbackground=black, borderwidth=0, relief = "flat")
		style.map("Treeview.Heading", background=[("selected", "#242424"), ("active", "#242424")])

		treeview.column("#0", width= 117)
		treeview.column("price", width= 50)
		treeview.column("brand", width= 50)
		treeview.column("size", width= 50)
		treeview.column("description", width= 117)

		treeview.heading("#0",text= "Product", anchor=tk.CENTER)
		treeview.heading("price",text= "Price", anchor=tk.CENTER)
		treeview.heading("brand",text= "Brand", anchor=tk.CENTER)
		treeview.heading("size",text= "Size", anchor=tk.CENTER)
		treeview.heading("description",text= "Description", anchor= tk.CENTER)

		products_in_stock = get_products_in_stock()
		for product in products_in_stock:
			treeview.insert("",tk.END, text=f"{product.name}",
					   values=(product.price,product.brand,product.size, product.description))
	#--------------------------------------------------------------------------------------------------------------------------------------------

class C_ventas(BaseScene):
	def __init__(self, parent, manager):
		super().__init__(parent, manager)

		self.manager=manager
		self.id_product = []
		self.manager.title("Cargar Ventas")
		self.header()
		self.main()

	def header(self):
		self.btn_config = {'font': ('Plus jakarta Sans', 14, 'bold'), 'text_color': "#000000",'fg_color': "transparent", 'hover_color': "#dcdcdc", 'height': 35,}
		user_img = ctk.CTkImage(Image.open("img/person.png"), size=(20, 20))
		search_img = ctk.CTkImage(Image.open("img/search.png"), size=(20, 20))

		self.header_fr = ctk.CTkFrame(self.manager, fg_color= color_p, border_color= color_s, border_width=1, height= 70, width= 800)
		self.header_fr.place(relx = 0.5, y = 35, anchor= "center")

		self.name = ctk.CTkLabel(self.header_fr, text= "|Urbanvibe", font=('Plus Jakarta Sans', 28, 'bold'))
		self.name.place(x = 100, rely = 0.5, anchor= "center")

		self.user = ctk.CTkButton(self.header_fr, text= "", image = user_img, fg_color= "transparent", hover_color= "#dcdcdc", height= 35, width=35, cursor = "hand2")
		self.user.place(x=800 - 50, rely=0.5, anchor= "center")

		self.search = ctk.CTkButton(self.header_fr, text= "", image = search_img, fg_color= "transparent", hover_color= "#dcdcdc"
									, height= 35, width= 35, cursor = "hand2", command= self.search_logic)
		self.search.place_configure(x = 710, rely=0.5, anchor= "center")
		
		# -----------------------------------------------NAV------------------------------------------------
		self.nav = ctk.CTkFrame(self.header_fr, fg_color= color_p, height= 65, width= 406)
		self.nav.place(relx = 0.5, y = 35, anchor= "center")
		
		# Texto - Cordenadas X - imagenes - command - Width
		btn_nav = [("Stock", (406//2) -80, None, lambda: self.manager.switch_scene("Stock_nav"),70), ("Home", 406//2, None, lambda: self.manager.switch_scene("Men_p"),70), ("Ventas", (406//2) +80, None, lambda: self.manager.switch_scene("Ventas_nav"),70)]
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
			self.search.configure(fg_color =  "#dcdcdc", hover_color = color_p)

	def main(self):
		self.main_fr = ctk.CTkScrollableFrame(self.manager, fg_color= color_p, height= 530, width= 780)
		self.main_fr.place(relx = 0.5,y = 341, anchor = "center")

		self.sucursal_fr = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 70, width = 780)
		self.sucursal_fr.grid(row=0, column=0, columnspan=2)
		self.sucursal_lb = ctk.CTkLabel(self.sucursal_fr, text =  f'Sucursal {app.get_variable("branch_user")}', font=('Plus Jakarta Sans', 20, 'bold')) #Aca se reemplazara el texto por las sucursales de la bd
		self.sucursal_lb.place(x = (self.sucursal_lb.winfo_width())//2 + 115, rely = 0.5 , anchor= "center")
	#--------------------------------------------------------------------------------------------------------------------------------------------
		self.inputs_col()
		self.visualizar_datos()

	def inputs_col(self):
		self.inputs_fr = ctk.CTkFrame(self.main_fr, width= 400, height= 300, fg_color= color_p)
		self.inputs_fr.grid(row=1, column=0)
		self.inputs_fr.grid_propagate(0)

		self.input_config = {'font': ('Plus jakarta Sans', 14, 'bold'),'fg_color': "transparent", 'width': 350, 'height': 50,'corner_radius':35, "border_color": "#dcdcdc"}
		input_style = [("Ingrese codigo de barra", 0), ("Ingrese cantidad", 1), ("Ingrese descuento",4)]
		for text, y_cord in input_style:
			if y_cord==0:
				self.inputid = ctk.CTkEntry(self.inputs_fr, placeholder_text= text, **self.input_config)
				self.inputid.grid(row = y_cord, column = 1, pady = 5, padx = 25)
			elif y_cord==1:
				self.inputq = ctk.CTkEntry(self.inputs_fr, placeholder_text= text, **self.input_config)
				self.inputq.grid(row = y_cord, column = 1, pady = 5, padx = 25)
			else:
				input = ctk.CTkEntry(self.inputs_fr, placeholder_text= text, **self.input_config)
				input.grid(row = y_cord, column = 1, pady = 5, padx = 25)

		borrar = ["Efectivo", "Credito", "Debito","Transferencia"]
		self.metodo_pago = ctk.CTkOptionMenu(self.inputs_fr, values = borrar, font= ('Plus jakarta Sans', 14, 'bold'), text_color= black
											, width = 350, height = 50, fg_color = color_s, button_color = grey
											, corner_radius= 25, button_hover_color = grey, dropdown_fg_color= color_p, command= self.credito)
		self.metodo_pago.grid(row = 2, column = 1, pady = 5, padx = 25)

		btn_inputs = ctk.CTkFrame(self.main_fr, width= 400, height= 50, fg_color= color_p)
		btn_inputs.grid(row=2, column=0)
		self.inputs_fr.grid_propagate(0)
	
		# new_prod = ctk.CTkButton(btn_inputs, text= "+ Producto", fg_color= color_p, text_color= black, corner_radius=25,border_color= black, border_width=3,
        #                                     width= 165, height= 35, font=('Plus Jakarta Sans', 12, 'bold'), hover_color= grey)
		# new_prod.grid(row = 0, column = 0,padx = 5)

		registrar = ctk.CTkButton(btn_inputs, text= "ticket", fg_color= black, text_color= color_p, corner_radius=25,border_color= black, border_width=3,
                                            width= 165, height= 35, font=('Plus Jakarta Sans', 12, 'bold'), hover_color= "#454545", command= self.generate_ticket)
		registrar.grid(row = 0, column = 1,padx = 5)

	def generate_ticket(self):
		self.pago.configure(text = f"Metodo de pago: {self.metodo_pago.get()}")
		self.treeviewt.insert(
			"",
			tk.END,
			text=get_name_product(int(self.inputid.get())),
			values=(get_price_product(int(self.inputid.get())), int(self.inputid.get()))
		)
		self.id_product.append(self.inputid.get())
		
	def credito(self,aguanteriver):
		if aguanteriver == "Credito":
			self.input_c = ctk.CTkEntry(self.inputs_fr, placeholder_text= "Ingrese tarjeta", **self.input_config)
			self.input_c.grid(row = 3, column = 1, pady = 5, padx = 25)
		if aguanteriver == "Debito":
			self.input_c.destroy()
			self.input_c = ctk.CTkEntry(self.inputs_fr, placeholder_text= "Ingrese tarjeta", **self.input_config)
			self.input_c.grid(row = 3, column = 1, pady = 5, padx = 25)
		elif aguanteriver != "Credito" and aguanteriver!= "Debito":
			self.input_c.destroy()
			self.metodo_pago.grid(row = 2, column = 1, pady = 5, padx = 25)
		
	def visualizar_datos(self):
		self.ticket_col = ctk.CTkFrame(self.main_fr, width= 400, height= 400, fg_color= color_p)
		self.ticket_col.grid(row=1, column=1, rowspan = 2)
		self.inputs_fr.grid_propagate(0)

		ticket_fr = ctk.CTkFrame(self.ticket_col, width= 300, height= 400, fg_color= color_p, corner_radius= 20, border_color= grey, border_width= 3)
		ticket_fr.place(relx = 0.5, rely = 0.5, anchor = "center")

		self.treeviewt = ttk.Treeview(ticket_fr, columns=("Precio", "Cantidad"))
		self.treeviewt.place(relx = 0.5, y= 195, anchor= "center", width = 280, height= 350)
		style = ttk.Style()
		style.theme_use("default")
		style.configure("Treeview.Heading", background= color_p, foreground=black, font=("Arial", 12, "bold"), relief = "flat")
		style.configure("Treeview", background= color_p, foreground= black, fieldbackground=color_p, borderwidth=0, relief = "flat")
		style.map("Treeview", background=[("selected", blue), ("active", blue)])

		self.treeviewt.column("#0", width= 50)
		self.treeviewt.column("Precio", width= 50)
		self.treeviewt.column("Cantidad", width= 50)

		self.treeviewt.heading("#0",text= "Producto", anchor=tk.CENTER)
		self.treeviewt.heading("Precio",text= "Precio", anchor=tk.CENTER)
		self.treeviewt.heading("Cantidad",text= "Cantidad", anchor=tk.CENTER)

		self.pago = ctk.CTkLabel(self.ticket_col, text = f"Metodo de pago: {self.metodo_pago.get()}", font=('Plus Jakarta Sans', 16, 'bold'))
		self.pago.place(x= 75, y = 320)
		registrar_venta = ctk.CTkLabel(self.ticket_col, text = "Registrar Venta", font=('Plus Jakarta Sans', 16, 'bold', 'underline'))
		registrar_venta.place(x= 75, y = 350)

		registrar_venta.bind('<Button-1>', self.registrar_venta_func)

	def registrar_venta_func(self, event):
		product_id = int(self.inputid.get())  
		branch_name = "Sucursal default"  

		for parent in self.treeviewt.get_children():
			for id in self.id_product:
				# Extrae los valores de cada fila del Treeview
				values = self.treeviewt.item(parent)["values"]

				# El primer valor en el Treeview es el producto (en la columna "#0")
				product_id = id  # El valor del producto en "#0"
				precio = float(values[0]) 
				quantity = int(values[1])  
				# Llama a la función para registrar la venta
				record_sale(product_id, 2, branch_name, quantity)
   
		#record_sale(int(self.inputq.get()),1,"dos",int(self.inputid.get()))
	
class Stock_nav(BaseScene):
	def __init__(self, parent, manager):
		super().__init__(parent, manager)

		self.manager=manager
		self.manager.title("Stock general")
		self.header()
		self.main()

	def header(self):
		self.btn_config = {'font': ('Plus jakarta Sans', 14, 'bold'), 'text_color': "#000000",'fg_color': "transparent", 'hover_color': "#dcdcdc", 'height': 35,}
		user_img = ctk.CTkImage(Image.open("img/person.png"), size=(20, 20))
		search_img = ctk.CTkImage(Image.open("img/search.png"), size=(20, 20))

		self.header_fr = ctk.CTkFrame(self.manager, fg_color= color_p, border_color= color_s, border_width=1, height= 70, width= 800)
		self.header_fr.place(relx = 0.5, y = 35, anchor= "center")

		self.name = ctk.CTkLabel(self.header_fr, text= "|Urbanvibe", font=('Plus Jakarta Sans', 28, 'bold'))
		self.name.place(x = 100, rely = 0.5, anchor= "center")

		self.user = ctk.CTkButton(self.header_fr, text= "", image = user_img, fg_color= "transparent", hover_color= "#dcdcdc", height= 35, width=35, cursor = "hand2")
		self.user.place(x=800 - 50, rely=0.5, anchor= "center")

		self.search = ctk.CTkButton(self.header_fr, text= "", image = search_img, fg_color= "transparent", hover_color= "#dcdcdc"
									, height= 35, width= 35, cursor = "hand2", command= self.search_logic)
		self.search.place_configure(x = 710, rely=0.5, anchor= "center")
		
		# -----------------------------------------------NAV------------------------------------------------
		self.nav = ctk.CTkFrame(self.header_fr, fg_color= color_p, height= 65, width= 406)
		self.nav.place(relx = 0.5, y = 35, anchor= "center")
		
		# Texto - Cordenadas X - imagenes - command - Width
		btn_nav = [("Stock", (406//2) -80, None, lambda: self.manager.switch_scene("Stock_nav"),70), ("Home", 406//2, None, lambda: self.manager.switch_scene("Men_p"),70), ("Ventas", (406//2) +80, None, lambda: self.manager.switch_scene("Ventas_nav"),70)]
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
			self.search.configure(fg_color =  "#dcdcdc", hover_color = color_p)
	def cambiar_color(self, widget, text_color, fg_color, event=None):
		widget.configure(text_color=text_color, fg_color=fg_color)

	def main(self):
		self.main_fr = ctk.CTkScrollableFrame(self.manager, fg_color= color_p, height= 530, width= 780)
		self.main_fr.place(relx = 0.5,y = 341, anchor = "center")

		self.sucursal_fr = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 70, width = 780)
		self.sucursal_fr.grid(row=0, column=0, columnspan=2)
		self.sucursal_lb = ctk.CTkLabel(self.sucursal_fr, text =  f'Sucursal {app.get_variable("branch_user")}', font=('Plus Jakarta Sans', 20, 'bold')) #Aca se reemplazara el texto por las sucursales de la bd
		self.sucursal_lb.place(x = (self.sucursal_lb.winfo_width())//2 + 115, rely = 0.5 , anchor= "center")
	#--------------------------------------------------------------------------------------------------------------------------------------------

		tabla = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 425, width = 800)
		tabla.grid(row=3, column=0)

		self.tabla_venta = ctk.CTkFrame(tabla, width= 675, height= 400, fg_color= black, corner_radius= 40)
		self.tabla_venta.place(relx = 0.5, y= 200, anchor= "center")

		treeview = ttk.Treeview(self.tabla_venta, columns=("cod_barra", "precio", "talle", "Fecha_act"))
		treeview.place(relx = 0.5, rely= 0.5, anchor= "center", width = 625, height= 350)
		style = ttk.Style()
		style.theme_use("default")
		style.configure("Treeview.Heading", background= black, foreground= color_p, font=("Arial", 12, "bold"), relief = "flat")
		style.configure("Treeview", background= black, foreground= color_p, fieldbackground=black, borderwidth=0, relief = "flat")
		style.map("Treeview.Heading", background=[("selected",  "#252525"), ("active",  "#252525")])

		treeview.column("#0", width= 110)
		treeview.column("cod_barra", width= 40)
		treeview.column("precio", width= 40)
		treeview.column("talle", width= 35)
		treeview.column("Fecha_act", width= 115)

		treeview.heading("#0",text= "Producto", anchor=tk.CENTER)
		treeview.heading("cod_barra",text= "Cod barra", anchor=tk.CENTER)
		treeview.heading("precio",text= "precio", anchor=tk.CENTER)
		treeview.heading("talle",text= "talle", anchor=tk.CENTER)
		treeview.heading("Fecha_act",text= "Fecha actualizacion", anchor= tk.CENTER)
	#--------------------------------------------------------------------------------------------------------------------------------------------
		atajos = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 75, width = 800)
		atajos.grid(row=2, column=0)

		
		self.u_venta_btn = ctk.CTkButton(atajos, text= "Cargar stock", fg_color= grey, text_color= black, corner_radius=25,
											width= 100, height= 50, font=('Plus Jakarta Sans', 16, 'bold'), hover_color= "#454545", command=lambda: self.manager.switch_scene("C_producto"))
		self.u_venta_btn.place(x = 135, y= 25, anchor = "center")        

		self.u_venta_btn.bind("<Enter>", lambda event: self.cambiar_color(self.u_venta_btn, grey, black, event))
		self.u_venta_btn.bind("<Leave>", lambda event: self.cambiar_color(self.u_venta_btn, black, grey, event))
	
class Ventas_nav(BaseScene):
	def __init__(self, parent, manager):
		super().__init__(parent, manager)

		self.manager=manager
		self.manager.title("Historial de ventas")
		self.header()
		self.main()

	def header(self):
		self.btn_config = {'font': ('Plus jakarta Sans', 14, 'bold'), 'text_color': "#000000",'fg_color': "transparent", 'hover_color': "#dcdcdc", 'height': 35,}
		user_img = ctk.CTkImage(Image.open("img/person.png"), size=(20, 20))
		search_img = ctk.CTkImage(Image.open("img/search.png"), size=(20, 20))

		self.header_fr = ctk.CTkFrame(self.manager, fg_color= color_p, border_color= color_s, border_width=1, height= 70, width= 800)
		self.header_fr.place(relx = 0.5, y = 35, anchor= "center")

		self.name = ctk.CTkLabel(self.header_fr, text= "|Urbanvibe", font=('Plus Jakarta Sans', 28, 'bold'))
		self.name.place(x = 100, rely = 0.5, anchor= "center")

		self.user = ctk.CTkButton(self.header_fr, text= "", image = user_img, fg_color= "transparent", hover_color= "#dcdcdc", height= 35, width=35, cursor = "hand2")
		self.user.place(x=800 - 50, rely=0.5, anchor= "center")

		self.search = ctk.CTkButton(self.header_fr, text= "", image = search_img, fg_color= "transparent", hover_color= "#dcdcdc"
									, height= 35, width= 35, cursor = "hand2", command= self.search_logic)
		self.search.place_configure(x = 710, rely=0.5, anchor= "center")
		
		# -----------------------------------------------NAV------------------------------------------------
		self.nav = ctk.CTkFrame(self.header_fr, fg_color= color_p, height= 65, width= 406)
		self.nav.place(relx = 0.5, y = 35, anchor= "center")
		
		# Texto - Cordenadas X - imagenes - command - Width
		btn_nav = [("Stock", (406//2) -80, None, lambda: self.manager.switch_scene("Stock_nav"),70), ("Home", 406//2, None, lambda: self.manager.switch_scene("Men_p"),70), ("Ventas", (406//2) +80, None, lambda: self.manager.switch_scene("Ventas_nav"),70)]
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
			self.search.configure(fg_color =  "#dcdcdc", hover_color = color_p)

	def cambiar_color(self, widget, text_color, fg_color, event=None):
		widget.configure(text_color=text_color, fg_color=fg_color)
	def main(self):
		self.main_fr = ctk.CTkScrollableFrame(self.manager, fg_color=color_p, height=530, width=780)
		self.main_fr.place(relx=0.5, y=341, anchor="center")

		self.sucursal_fr = ctk.CTkFrame(self.main_fr, fg_color=color_p, height=70, width=780)
		self.sucursal_fr.grid(row=0, column=0, columnspan=2)
		self.sucursal_lb = ctk.CTkLabel(self.sucursal_fr, text=f'Sucursal {app.get_variable("branch_user")}', font=('Plus Jakarta Sans', 20, 'bold'))
		self.sucursal_lb.place(x=(self.sucursal_lb.winfo_width())//2 + 115, rely=0.5, anchor="center")

		#--------------------------------------------------------------------------------------------------------------------------------------------

		tabla = ctk.CTkFrame(self.main_fr, fg_color=color_p, height=425, width=800)
		tabla.grid(row=3, column=0)

		self.tabla_venta = ctk.CTkFrame(tabla, width=675, height=400, fg_color=grey, corner_radius=40)
		self.tabla_venta.place(relx=0.5, y=200, anchor="center")

		treeview = ttk.Treeview(self.tabla_venta, columns=("Fecha", "Vendedor", "Estado", "Precio"))
		treeview.place(relx=0.5, rely=0.5, anchor="center", width=625, height=350)
		style = ttk.Style()
		style.theme_use("default")
		style.configure("Treeview.Heading", background=grey, foreground=black, font=("Arial", 12, "bold"), relief="flat")
		style.configure("Treeview", background=grey, foreground=black, fieldbackground=grey, borderwidth=0, relief="flat")
		style.map("Treeview.Heading", background=[("selected", color_p), ("active", color_p)])

		treeview.column("#0", width=110)
		treeview.column("Fecha", width=100)
		treeview.column("Vendedor", width=100)
		treeview.column("Estado", width=100)
		treeview.column("Precio", width=100)

		treeview.heading("#0", text="Producto", anchor=tk.CENTER)
		treeview.heading("Fecha", text="Fecha", anchor=tk.CENTER)
		treeview.heading("Vendedor", text="Vendedor", anchor=tk.CENTER)
		treeview.heading("Estado", text="Estado", anchor=tk.CENTER)
		treeview.heading("Precio", text="Precio", anchor=tk.CENTER)

		# Obtiene los datos de la base de datos
		sales_data = get_all_sales()

		# Inserta los datos en el Treeview
		for sale in sales_data:
			treeview.insert("", "end", text=get_name_product(sale[1]), values=(sale[5], get_user_name(sale[2]), sale[4], sale[6]))
   
		'''
  			Falta traducir los datos crudos a texto ademas de que no existe la columna
            de cantidad 
  		'''
   
	#--------------------------------------------------------------------------------------------------------------------------------------------
		atajos = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 75, width = 800)
		atajos.grid(row=2, column=0)

		
		self.u_venta_btn = ctk.CTkButton(atajos, text= "Nueva venta", fg_color= "#222325", text_color= color_p, corner_radius=25,
											width= 100, height= 50, font=('Plus Jakarta Sans', 16, 'bold'), hover_color= "#454545", command=lambda: self.manager.switch_scene("C_ventas"))
		self.u_venta_btn.place(x = 135, y= 25, anchor = "center")        

		self.u_venta_btn.bind("<Enter>", lambda event: self.cambiar_color(self.u_venta_btn, black, grey, event))
		self.u_venta_btn.bind("<Leave>", lambda event: self.cambiar_color(self.u_venta_btn, grey, "#222325", event))

if __name__ == "__main__":
	app = SceneManager()  # Crea una instancia del gestor de escenas
	x = (app.winfo_screenwidth() // 2)-(800 // 2)
	y = (app.winfo_screenheight() // 2)-(600 // 2)
	app.geometry(f"800x600+{x}+{y}")  # Establece el tamaño de la ventana
	app.resizable(False,False)

	# Añade las escenas al gestor
	app.add_scene("Stock_nav", Stock_nav)
	app.add_scene("Ventas_nav", Ventas_nav)
	app.add_scene("C_ventas", C_ventas)
	app.add_scene("C_producto", C_producto)
	app.add_scene("Men_p", Men_p)
	app.add_scene("Login", Login)
  
	# Inicia la aplicación con la primera escena visible
	app.switch_scene("Login")

	app.mainloop()  # Ejecuta el bucle principal de la aplicación