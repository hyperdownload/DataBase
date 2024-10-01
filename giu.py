from Utils.SceneManager import *
from Utils.database import *
from Utils.functions import *
from CTkDataVisualizingWidgets import *
from PIL import Image 
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
		
		bienvenida_lb = ctk.CTkLabel(login_container,text_color=black, text = "Welcome to back", font=('Plus Jakarta Sans', 28, 'bold'))
		bienvenida_lb.place(relx= 0.5, y=185, anchor= "center")
		user_lb = ctk.CTkLabel(login_container, text = "Urbanlive", font=('Plus Jakarta Sans', 16, 'bold'), text_color= "#BEBEBE")
		user_lb.place(relx = 0.5 , y=215, anchor= "center")

		self.user_entry = ctk.CTkEntry(login_container, height = 35, width = 350, corner_radius = 20, placeholder_text = "Ingrese su nombre de usuario...")
		self.user_entry.place(relx=0.5, y=260, anchor= "center")
		self.user_entry.bind('<Return>', self.login_logic)

		self.password_entry = ctk.CTkEntry(login_container, height = 35, width = 350, corner_radius = 20, placeholder_text = "Ingrese su contraseña...")
		self.password_entry.place(relx=0.5, y=310, anchor= "center")
		self.password_entry.bind('<Return>', self.login_logic)
		self.password_entry.bind('<MouseWheel>', lambda event:self.login_logic(autologin=True)) # Esta linea en algun momento hay que eliminarla

		submit = ctk.CTkButton(login_container, text = "Login", height = 35, width = 350, corner_radius = 20, fg_color = black, text_color = color_p, hover_color = "#454545", command = self.login_logic)
		submit.place(relx=0.5, y=360, anchor= "center")
  
	def login_logic(self, event=None, autologin=False):
		if not autologin:
			user = self.user_entry.get()
			password = self.password_entry.get()
		else:
			user = 'carlos@example.com'
			password = 'superadmin789'
		try:
			if hashlib.sha256(password.encode()).hexdigest() == get_user_details(get_user_id(user))[2]:
				app.save_variable("user_role",get_user_details(get_user_id(user))[1])
				app.save_variable("branch_user",get_user_details(get_user_id(user))[3])
				app.save_variable("user_id", get_user_id(user))
				
				self.manager.switch_scene("Men_p")

			if hashlib.sha256(password.encode()).hexdigest() == get_user_details(get_user_id(user))[2] and app.get_variable('user_role') == 'General Admin':
				app.save_variable("user_role",get_user_details(get_user_id(user))[1])
				app.save_variable("branch_user",get_user_details(get_user_id(user))[3])
				app.save_variable("user_id", get_user_id(user))
				
				self.manager.switch_scene("Men_p_admin")

			elif hashlib.sha256(password.encode()).hexdigest() != get_user_details(get_user_id(user))[2]:
				self.user_entry.configure(border_color = "green")
				self.password_entry.configure(border_color = "red")
	
		except:
			self.user_entry.configure(border_color = "red")
			self.password_entry.configure(border_color = "red")
			show_notification(app, "Usuario o contraseña incorrectos.")
			
class Men_p(BaseScene):
	def __init__(self, parent, manager):
		super().__init__(parent, manager)

		self.manager=manager
		self.header_fr = header(self.manager)
		self.main()
		self.manager.title("Menu principal")

	def main(self):
		self.main_fr, self.sucursal_fr, self.sucursal_lb = create_scrollable_frame(self.manager, color_p, app.get_variable("branch_user"))

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

		self.cargar_productos_txt = ctk.CTkLabel(self.cargar_prod_lb,text_color=black, text= "Cargar\nProductos", font=('Plus Jakarta Sans', 38, 'bold'), justify = "left")
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

		# value = {'JJ': 5, 'OO': 0, 'WW': 7, 'TT': 3, 'GG': 15, 'FF': 10, 'HH': 1, 'PP': 12, "AA": 4}
		value = {'Remeras': 5, 'Accesorios': 0, 'Vestidos': 7, 'Calzado': 3, 'Pantalones': 15}

		CTkChart(self.grafico, value, corner_radius=20, fg_color= color_s, stat_color= black, chart_fg_color= color_s,
         show_indicators=(False, True), stat_info_show=(False, True), chart_arrow="none",
		 indicator_line_color= blue, indicator_text_color= blue, stat_width=35,
         stat_title_color= blue, chart_axis_width=3, width=700, height= self.h_grid2 - 50).place( relx = 0.5, rely = 0.5, anchor = "center")
		
class C_producto(BaseScene):
	def __init__(self, parent, manager):
		super().__init__(parent, manager)

		self.manager=manager
		self.manager.title("Carga de productos")
		self.header_fr = header(self.manager)
		self.main()

	def search(self, event = None):
		if self.buscar_producto.get():
			self.tv_stock.delete(*self.tv_stock.get_children())
			search=search_function(get_products_in_stock(),self.buscar_producto.get())
			for product in search:
				self.tv_stock.insert("",tk.END, text=f"{product.name}",
						values=(product.price,product.brand,product.size, product.description))
		else:
			self.tv_stock.delete(*self.tv_stock.get_children())
			products_in_stock = get_products_in_stock()
			for product in products_in_stock:
				self.tv_stock.insert("",tk.END, text=f"{product.name}",
						values=(product.price,product.brand,product.size, product.description))
    
	def update_stock(self):
		s = self.tv_stock.focus()
		que=self.tv_stock.item(s,'values')
		print(que[3])
		print(get_name_per_id(self.tv_stock.item(que)), app.get_variable("user_id"), app.get_variable("branch_name"), self.c_stock.get())

	def main(self):
		self.main_fr, self.sucursal_fr, self.sucursal_lb = create_scrollable_frame(self.manager, color_p, app.get_variable("branch_user"))
	#--------------------------------------------------------------------------------------------------------------------------------------------
		lupa = ctk.CTkImage(Image.open("img/search.png"), size=(35, 35))
		
		self.cp_fr = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 85, width = 800)
		self.cp_fr.grid(row=1, column=0)
		self.buscar_producto = ctk.CTkEntry(self.cp_fr, placeholder_text= "Buscar producto...", width= 250, height=50,
										corner_radius=35, border_color= "#dcdcdc", text_color= "#252525")
		self.buscar_producto.place(x = 185, rely = 0.5, anchor= "center")

		app.bind('<Key>', self.search)

		bp_btn = ctk.CTkButton(self.cp_fr, text= "", image = lupa, fg_color= color_s, hover_color= "#dcdcdc"
									, height= 50, width= 50, corner_radius= 15, cursor = "hand2", command = self.search)
		bp_btn.place(x = 355, rely = 0.5, anchor= "center")

		self.c_stock = ctk.CTkEntry(self.cp_fr, placeholder_text= "Subir producto...", width= 250, height=50,
										corner_radius=35, border_color= "#dcdcdc", text_color= "#252525" )
		self.c_stock.place(x = 525, rely= 0.5, anchor= "center")

		c_btn = ctk.CTkButton(self.cp_fr, text= "subir", fg_color= black, hover_color= "#dcdcdc"
									, height= 50, width= 75, corner_radius= 15, cursor = "hand2", command=self.update_stock)
		c_btn.place(x = 700, rely = 0.5, anchor= "center")
	#--------------------------------------------------------------------------------------------------------------------------------------------
		tabla = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 425, width = 800)
		tabla.grid(row=2, column=0)

		self.tabla_stock = ctk.CTkFrame(tabla, width= 675, height= 400, fg_color= black, corner_radius= 40)
		self.tabla_stock.place(relx = 0.5, y= 200, anchor= "center")

		# Wuajajaja ya lo resumi

		columns = [("#0", "Product", 117), 
           ("price", "Price", 50), 
           ("brand", "Brand", 50), 
           ("size", "Size", 50), 
           ("description", "Description", 117)]

		self.tv_stock = ttk.Treeview(self.tabla_stock,selectmode=tk.BROWSE, columns=[col[0] for col in columns[1:]])
		self.tv_stock.place(relx=0.5, rely=0.5, anchor="center", width=625, height=350)
  
		for col, heading, width in columns:
			self.tv_stock.column(col, width=width)
			self.tv_stock.heading(col, text=heading, anchor=tk.CENTER)

		# Configuración de columnas
		# for col, width in [("#0",117), ("price",50), ("brand",50), ("size",50), ("description",117)]:
		# 	self.tv_stock.column(col, width = width)

		# Cabeceras de las columnas
		# self.tv_stock.heading("#0", text = "Producto", anchor=tk.CENTER)

		# for col in ["Price", "Brand", "Size", "Description"]:
		# 	self.tv_stock.heading(col, text=col.replace("_", " ").capitalize(), anchor=tk.CENTER)


		products_in_stock = get_products_in_stock()
		for product in products_in_stock:
			if product.branch_name.lower() == app.get_variable('branch_user').lower():
				self.tv_stock.insert("",tk.END, text=f"{product.name}",
						values=(product.price,product.brand,product.size, product.description))
	
		# for product in products_in_stock:
		# 	self.tv_stock.insert("", "end", text=product.name,values=( product.price, product.brand, product.description))
	#--------------------------------------------------------------------------------------------------------------------------------------------

class C_ventas(BaseScene):
	def __init__(self, parent, manager):
		super().__init__(parent, manager)

		self.manager=manager
		self.id_product = []
		self.manager.title("Cargar Ventas")
		self.header_fr = header(self.manager)
		self.main()

	def main(self):
		self.main_fr, self.sucursal_fr, self.sucursal_lb = create_scrollable_frame(self.manager, color_p, app.get_variable("branch_user"))
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


		borrar = ["Efectivo", "Credito", "Debito","Transferencia"]
		self.metodo_pago = ctk.CTkOptionMenu(self.inputs_fr, values = borrar, font= ('Plus jakarta Sans', 14, 'bold'), text_color= black
											, width = 350, height = 50, fg_color = color_s, button_color = grey
											, corner_radius= 25, button_hover_color = grey, dropdown_fg_color= color_p, command= self.credito)
		self.metodo_pago.grid(row = 2, column = 1, pady = 5, padx = 25)

		btn_inputs = ctk.CTkFrame(self.main_fr, width= 400, height= 50, fg_color= color_p)
		btn_inputs.grid(row=2, column=0)
		self.inputs_fr.grid_propagate(0)

		registrar = ctk.CTkButton(btn_inputs, text= "ticket", fg_color= black, text_color= color_p, corner_radius=25,border_color= black, border_width=3,
                                            width= 165, height= 35, font=('Plus Jakarta Sans', 12, 'bold'), hover_color= "#454545", command= self.generate_ticket)
		registrar.grid(row = 0, column = 1,padx = 5)

	def generate_ticket(self):
		self.pago.configure(text = f"Metodo de pago: {self.metodo_pago.get()}")
		self.treeviewt.insert(
			"",
			tk.END,
			text=get_name_product(int(self.inputid.get())),
			values=(get_price_product(int(self.inputid.get())), int(self.inputq.get()))
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
		self.ticket_col = ctk.CTkFrame(self.main_fr, width=400, height=400, fg_color=color_p)
		self.ticket_col.grid(row=1, column=1, rowspan=2)
		self.inputs_fr.grid_propagate(0)

		ticket_fr = ctk.CTkFrame(self.ticket_col, width=300, height=400, fg_color=black, corner_radius=20, border_color=grey, border_width=3)
		ticket_fr.place(relx=0.5, rely=0.5, anchor="center")

		self.treeviewt = ttk.Treeview(ticket_fr, columns=("Precio", "Cantidad"))
		self.treeviewt.place(relx=0.5, y=195, anchor="center", width=280, height=350)

		for col, width in zip(("#0", "Precio", "Cantidad"), [50, 50, 50]): # Descubri como usar zip :D
			self.treeviewt.column(col, width=width)
			self.treeviewt.heading(col, text=col if col != "#0" else "Producto", anchor=tk.CENTER)

		self.pago = ctk.CTkLabel(self.ticket_col, text_color = color_p, fg_color=black, text=f"Metodo de pago: {self.metodo_pago.get()}", font=('Plus Jakarta Sans', 16, 'bold'))
		self.pago.place(x=75, y=320)

		registrar_venta = ctk.CTkLabel(self.ticket_col, text_color = color_p, fg_color=black, text="Registrar Venta", font=('Plus Jakarta Sans', 16, 'bold', 'underline'), cursor = "hand2")
		registrar_venta.place(x=75, y=350)
		registrar_venta.bind('<Button-1>', self.registrar_venta_func)

	def registrar_venta_func(self, event):
		product_id = int(self.inputid.get())  
		branch_name = app.get_variable('branch_user') 

		for parent in self.treeviewt.get_children():
			for id in self.id_product:
				# Extrae los valores de cada fila del Treeview
				values = self.treeviewt.item(parent)["values"]

				# El primer valor en el Treeview es el producto (en la columna "#0")
				product_id = id  # El valor del producto en "#0"
				precio = float(values[0]) 
				quantity = int(values[1])  
				# Llama a la función para registrar la venta
				if record_sale(product_id, app.get_variable('user_id'), branch_name, quantity, get_price_product(product_id)):
					show_notification(app,"Venta registrada")
	
class Stock_nav(BaseScene):
	def __init__(self, parent, manager):
		super().__init__(parent, manager)

		self.manager=manager
		self.manager.title("Stock general")
		self.header_fr = header(self.manager)
		self.main()

	def cambiar_color(self, widget, text_color, fg_color, event=None):
		widget.configure(text_color=text_color, fg_color=fg_color)

	def main(self):
		self.main_fr, self.sucursal_fr, self.sucursal_lb = create_scrollable_frame(self.manager, color_p, app.get_variable("branch_user"))
	#--------------------------------------------------------------------------------------------------------------------------------------------
		tabla = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 425, width = 800)
		tabla.grid(row=3, column=0)

		self.tabla_venta = ctk.CTkFrame(tabla, width= 675, height= 400, fg_color= black, corner_radius= 40)
		self.tabla_venta.place(relx = 0.5, y= 200, anchor= "center")

		stockTreeView = ttk.Treeview(self.tabla_venta, columns=("cod_barra", "precio", "talle", "Fecha_act", "stock"))
		stockTreeView.place(relx = 0.5, rely= 0.5, anchor= "center", width = 625, height= 350)

		# Configuración de columnas
		for col, width in [("#0", 110), ("cod_barra", 40), ("precio", 40), ("talle", 30), ("Fecha_act", 115), ("stock",30)]:
			stockTreeView.column(col, width=width)
			
		# Cabeceras de las columnas
		stockTreeView.heading("#0", text="Producto", anchor=tk.CENTER)
		for col in ["cod_barra", "precio", "talle", "Fecha_act", "stock"]:
			stockTreeView.heading(col, text=col.replace("_", " ").capitalize(), anchor=tk.CENTER)

		products_in_stock = get_products_in_stock()
  
		for product in products_in_stock:
			try:
				if product.branch_name.lower()==app.get_variable("branch_user").lower():
					stockTreeView.insert("", "end", text=product.name,values=(product.id, product.price, product.size, get_restock_date(product.id),product.stock))
			except:
				print("Sucursal invalida.")
				stockTreeView.insert("", "end", text=product.name,values=(product.id, product.price, product.size, get_restock_date(product.id),product.stock))
	#--------------------------------------------------------------------------------------------------------------------------------------------
		atajos = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 75, width = 800)
		atajos.grid(row=2, column=0)

		if app.get_variable('user_role') == 'Admin':
		
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
		self.header_fr = header(self.manager)
		self.main()

	def cambiar_color(self, widget, text_color, fg_color, event=None):
		widget.configure(text_color=text_color, fg_color=fg_color)
  
	def main(self):
		self.main_fr, self.sucursal_fr, self.sucursal_lb = create_scrollable_frame(self.manager, color_p, app.get_variable("branch_user"))

		tabla = ctk.CTkFrame(self.main_fr, fg_color=color_p, height=425, width=800); tabla.grid(row=3, column=0)
		self.tabla_venta = ctk.CTkFrame(tabla, width=675, height=400, fg_color=black, corner_radius=40); self.tabla_venta.place(relx=0.5, y=200, anchor="center")
		treeview = ttk.Treeview(self.tabla_venta, columns=("Fecha", "Vendedor", "Estado", "Precio", "Cantidad")); treeview.place(relx=0.5, rely=0.5, anchor="center", width=625, height=350)
		[treeview.column(col, width=width) for col, width in [("#0", 110), ("Fecha", 100), ("Vendedor", 100), ("Estado", 50), ("Precio", 50), ("Cantidad", 50)]]
		treeview.heading("#0", text="Producto", anchor=tk.CENTER); [treeview.heading(col, text=col.replace("_", " ").capitalize(), anchor=tk.CENTER) for col in ["Fecha", "Vendedor", "Estado", "Precio", "Cantidad"]]
		
  		# Obtiene los datos de la base de datos
		sales_data = get_all_sales()
	
		# Inserta los datos en el Treeview
		try:
			[treeview.insert("", "end", text=get_name_product(sale[1]), values=(sale[5], get_user_name(sale[2]), sale[4], sale[6])) for sale in sales_data if sale[3].lower() == app.get_variable("branch_user").lower()]
		except AttributeError as e:
			print(f"Hubo un error {e}. Se asume que el usuario es {'Super admin, mostrando todas las sucursales.' if app.get_variable('branch_user') is None else app.get_variable('branch_user')}")
			[treeview.insert("", "end", text=get_name_product(sale[1]), values=(sale[5], get_user_name(sale[2]), sale[4], sale[6])) for sale in sales_data]
		
		atajos = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 75, width = 800)
		atajos.grid(row=2, column=0)
		
		self.u_venta_btn = ctk.CTkButton(atajos, text= "Nueva venta", fg_color= "#222325", text_color= color_p, corner_radius=25,
											width= 100, height= 50, font=('Plus Jakarta Sans', 16, 'bold'), hover_color= "#454545", command=lambda: self.manager.switch_scene("C_ventas"))
		self.u_venta_btn.place(x = 135, y= 25, anchor = "center")        

		self.u_venta_btn.bind("<Enter>", lambda event: self.cambiar_color(self.u_venta_btn, black, grey, event))
		self.u_venta_btn.bind("<Leave>", lambda event: self.cambiar_color(self.u_venta_btn, grey, "#222325", event))


# VENTANAS DE ADMINISTRADOR 

class Men_p_admin(BaseScene):
	def __init__(self, parent, manager):
		super().__init__(parent, manager)

		self.manager=manager
		self.header_fr = header(self.manager)
		self.main()
		self.manager.title("Menu admin")

	def main(self):
		self.main_fr, self.sucursal_fr, self.sucursal_lb = create_scrollable_frame(self.manager, color_p, app.get_variable("branch_user"))

		self.h_grid1= 300
		self.h_grid2= 400
		self.altura_fr = self.h_grid1+self.h_grid2+50
		
		self.sucursales_fr()
	
	def sucursales_fr(self):

		style_card = {'width': 235, 'height': 100, 'corner_radius': 20, 'fg_color': grey, 'font': ('Plus Jakarta Sans', 16, 'bold'), 'hover_color': color_s, 'text_color': black}
		cord = [(0, "San Miguel"),(1, "Jose c Paz"),(2, "Retiro")]
		for x, text in cord:
			card = ctk.CTkButton(self.main_fr, text = text, **style_card)
			card.grid(row = 1, column = x, sticky="e")

		new_stock = ctk.CTkButton(self.main_fr, text = "+ Nuevos productos", **style_card, command = lambda: app.switch_scene("New_stock"))
		new_stock.grid(row = 2, column = 0, sticky="e", pady = 15)

		
class New_stock(BaseScene):
	def __init__(self, parent, manager):
		super().__init__(parent, manager)

		self.manager=manager
		self.header_fr = header(self.manager)
		self.main()
		self.manager.title("Subir productos")

	def main(self):
		self.main_fr, self.sucursal_fr, self.sucursal_lb = create_scrollable_frame(self.manager, color_p, app.get_variable("branch_user"))
		self.inputs_col()
	def inputs_col(self):
		self.inputs_fr = ctk.CTkFrame(self.main_fr, width= 800, height= 300, fg_color= color_p)
		self.inputs_fr.grid(row=1, column=0)
		self.inputs_fr.grid_propagate(0)

		self.input_config = {'font': ('Plus jakarta Sans', 14, 'bold'),'fg_color': "transparent", 'width': 350, 'height': 50,'corner_radius':35, "border_color": "#dcdcdc"}

		self.nombre_producto = ctk.CTkEntry(self.inputs_fr, placeholder_text= 'Ingrese nombre del producto', **self.input_config)
		self.nombre_producto.grid(row = 1, column = 0, pady = 5, padx = 15)
		self.precio_produc = ctk.CTkEntry(self.inputs_fr, placeholder_text= 'Ingrese precio del producto', **self.input_config)
		self.precio_produc.grid(row = 1, column = 1, pady = 5)
		self.precio_produc.configure(width= 250)
		self.marca_produc= ctk.CTkEntry(self.inputs_fr, placeholder_text= 'Ingrese marca del producto', **self.input_config)
		self.marca_produc.grid(row = 2, column = 0, pady = 5, padx = 15)
		self.talle_produc=ctk.CTkEntry(self.inputs_fr, placeholder_text= 'Ingrese talle del producto', **self.input_config)
		self.talle_produc.grid(row = 2, column = 1, pady = 5)
		self.talle_produc.configure(width= 250)


if __name__ == "__main__":
	app = SceneManager()  # Crea una instancia del gestor de escenas
	x = (app.winfo_screenwidth() // 2)-(800 // 2)
	y = (app.winfo_screenheight() // 2)-(600 // 2)
	app.geometry(f"800x600+{x}+{y}")  # Establece el tamaño de la ventana
	app.resizable(False,False)
 
	style = ttk.Style()
	style.theme_use("default")
	style.configure("Treeview.Heading", background= black, foreground= color_p, font=("Arial", 12, "bold"), relief = "flat")
	style.configure("Treeview", background= black, foreground= color_p, fieldbackground=black, borderwidth=0, relief = "flat")
	style.map("Treeview.Heading", background=[("selected",  "#252525"), ("active",  "#252525")])

	# Añade las escenas al gestor
	scenes = [("Stock_nav", Stock_nav),("Ventas_nav", Ventas_nav),("C_ventas", C_ventas),("C_producto", C_producto),("Men_p", Men_p),("Login", Login),("Men_p_admin", Men_p_admin),
    ("New_stock", New_stock)]

	for scene_name, scene_class in scenes:
		app.add_scene(scene_name, scene_class)
  
	# Inicia la aplicación con la primera escena visible
	app.switch_scene("Login")

	app.mainloop()  # Ejecuta el bucle principal de la aplicación