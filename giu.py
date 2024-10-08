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
		login_container = ctk.CTkFrame(self.manager, width=800, height=600, fg_color=color_p)
		login_container.place(x=0, y=0)
		
		labels = [("Welcome to back", 185, 28), ("Urbanlive", 215, 16)]
		for text, y_pos, font_size in labels:
			ctk.CTkLabel(login_container, text=text, font=('Plus Jakarta Sans', font_size, 'bold'), text_color=black if font_size == 28 else "#BEBEBE").place(relx=0.5, y=y_pos, anchor="center")

		self.user_entry = ClearableEntry(login_container, height=35, width=350, corner_radius=20, placeholder_text="Ingrese su nombre de usuario...")
		self.user_entry.place(relx=0.5, y=260, anchor="center")
		self.user_entry.bind('<Return>', self.login_logic)

		self.password_entry = ClearableEntry(login_container, height=35, width=350, corner_radius=20, placeholder_text="Ingrese su contraseña...")
		self.password_entry.place(relx=0.5, y=310, anchor="center")
		self.password_entry.bind('<Return>', self.login_logic)
		self.password_entry.bind('<MouseWheel>', lambda event: self.login_logic(autologin=True))

		ctk.CTkButton(login_container, text="Login", height=35, width=350, corner_radius=20, fg_color=black, text_color=color_p, hover_color="#454545", command=self.login_logic).place(relx=0.5, y=360, anchor="center")
  
	def login_logic(self, event=None, autologin=False):
		if not autologin:
			user = self.user_entry.get_and_clear()
			password = self.password_entry.get_and_clear()
		else:
			user = 'carlos@example.com'
			password = 'superadmin789'
		try:
			if hashlib.sha256(password.encode()).hexdigest() == get_user_details(get_user_id(user))[2]:
				self._extracted_from_login_logic_10(user, "Men_p")
			if hashlib.sha256(password.encode()).hexdigest() == get_user_details(get_user_id(user))[2] and app.get_variable('user_role') == 'General Admin':
				self._extracted_from_login_logic_10(user, "Men_p_admin")
				r = dynamic_thread_executor([(get_products_out_of_stock, ())])
				if len(r[0][0]) != 0:
					show_notification(app, "Hay productos sin stock.")
					text = ''.join(f"ID:{id}, name:{name}, brand:{brand}, stock:{stock}"for id, name, brand, stock in get_products_out_of_stock())
					notifications.append(NotificationPlaceHolder("Hay productos sin stock.", f"Los productos sin stock son:{text}"))
			elif hashlib.sha256(password.encode()).hexdigest() != get_user_details(get_user_id(user))[2]:
				self.user_entry.configure(border_color = "green")
				self.password_entry.configure(border_color = "red")

		except Exception as e:
			self.user_entry.configure(border_color = "red")
			self.password_entry.configure(border_color = "red")
			show_notification(app, "Usuario o contraseña incorrectos.")
			print(e)

	def _extracted_from_login_logic_10(self, user, arg1):
		app.save_variable("user_role",get_user_details(get_user_id(user))[1])
		app.save_variable("branch_user",get_user_details(get_user_id(user))[3])
		app.save_variable("user_id", get_user_id(user))

		self.manager.switch_scene(arg1)
			
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

	def col_atajo(self):
		self.atajos_frame = ctk.CTkFrame(self.main_fr, width= 270, height= self.altura_fr, fg_color= color_p)
		self.atajos_frame.grid(row=1, column=1, padx = 12)

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
		print(app.get_variable("user_bran"))

	def search(self, event = None):
		if self.buscar_producto.get_and_clear():
			self.tv_stock.delete(*self.tv_stock.get_children())
			search=search_function(get_products_in_stock(),self.buscar_producto.get_and_clear())
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
		focus = self.tv_stock.focus()
		name_product=self.tv_stock.item(focus,'text')
		try:
			record_restock(get_name_per_id(str(name_product)), app.get_variable("user_id"), app.get_variable("branch_user"), self.c_stock.get_and_clear())
			show_notification(app, f"Reestock exitoso\n stock actual: {get_stock_product(get_name_per_id(str(name_product)))}")
		except TypeError:
			show_notification(app, "Error al reestockear\n procure seleccionar un\n producto de la tabla")

	def main(self):
		self.main_fr, self.sucursal_fr, self.sucursal_lb = create_scrollable_frame(self.manager, color_p, app.get_variable("branch_user"))
	#--------------------------------------------------------------------------------------------------------------------------------------------
		lupa = ctk.CTkImage(Image.open("img/search.png"), size=(35, 35))
		
		self.cp_fr = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 85, width = 800)
		self.cp_fr.grid(row=1, column=0)
		self.buscar_producto = ClearableEntry(self.cp_fr, placeholder_text= "Buscar producto...", width= 250, height=50,
										corner_radius=35, border_color= "#dcdcdc", text_color= "#252525")
		self.buscar_producto.place(x = 185, rely = 0.5, anchor= "center")

		app.bind('<Key>', self.search)

		bp_btn = ctk.CTkButton(self.cp_fr, text= "", image = lupa, fg_color= color_s, hover_color= "#dcdcdc"
									, height= 50, width= 50, corner_radius= 15, cursor = "hand2", command = self.search)
		bp_btn.place(x = 355, rely = 0.5, anchor= "center")

		self.c_stock = ClearableEntry(self.cp_fr, placeholder_text= "Subir producto...", width= 250, height=50,
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

		products_in_stock = get_products_in_stock()
		for product in products_in_stock:
			if product.branch_name.lower() == app.get_variable('branch_user').lower():
				self.tv_stock.insert("",tk.END, text=f"{product.name}",
						values=(product.price,product.brand,product.size, product.description))
	
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
				self.inputid = ClearableEntry(self.inputs_fr, placeholder_text= text, **self.input_config)
				self.inputid.grid(row = y_cord, column = 1, pady = 5, padx = 25)
			elif y_cord==1:
				self.inputq = ClearableEntry(self.inputs_fr, placeholder_text= text, **self.input_config)
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
		self.pago.configure(text = f"Metodo de pago: {self.metodo_pago.get_and_clear()}")
		self.treeviewt.insert(
			"",
			tk.END,
			text=get_name_product(int(self.inputid.get_and_clear())),
			values=(get_price_product(int(self.inputid.get_and_clear())), int(self.inputq.get_and_clear()))
		)
		self.id_product.append(self.inputid.get_and_clear())
		
	def credito(self,aguanteriver):
		if aguanteriver == "Credito":
			self.input_c = ClearableEntry(self.inputs_fr, placeholder_text= "Ingrese tarjeta", **self.input_config)
			self.input_c.grid(row = 3, column = 1, pady = 5, padx = 25)
		if aguanteriver == "Debito":
			self.input_c.destroy()
			self.input_c = ClearableEntry(self.inputs_fr, placeholder_text= "Ingrese tarjeta", **self.input_config)
			self.input_c.grid(row = 3, column = 1, pady = 5, padx = 25)
		elif aguanteriver != "Credito":
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

		self.pago = ctk.CTkLabel(self.ticket_col, text_color = color_p, fg_color=black, text=f"Metodo de pago: {self.metodo_pago.get_and_clear()}", font=('Plus Jakarta Sans', 16, 'bold'))
		self.pago.place(x=75, y=320)

		registrar_venta = ctk.CTkLabel(self.ticket_col, text_color = color_p, fg_color=black, text="Registrar Venta", font=('Plus Jakarta Sans', 16, 'bold', 'underline'), cursor = "hand2")
		registrar_venta.place(x=75, y=350)
		registrar_venta.bind('<Button-1>', self.registrar_venta_func)

	def registrar_venta_func(self, event):
		product_id = int(self.inputid.get_and_clear())  
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
		tabla = ctk.CTkFrame(self.main_fr, fg_color=color_p, height=425, width=800); tabla.grid(row=3, column=0)
		self.tabla_venta = ctk.CTkFrame(tabla, width=675, height=400, fg_color=black, corner_radius=40); self.tabla_venta.place(relx=0.5, y=200, anchor="center")
		stockTreeView = ttk.Treeview(self.tabla_venta, columns=("cod_barra", "precio", "talle", "Fecha_act", "stock")); stockTreeView.place(relx=0.5, rely=0.5, anchor="center", width=625, height=350)
		[stockTreeView.column(col, width=width) for col, width in [("#0", 110), ("cod_barra", 40), ("precio", 40), ("talle", 30), ("Fecha_act", 115), ("stock", 30)]]
		stockTreeView.heading("#0", text="Producto", anchor=tk.CENTER); [stockTreeView.heading(col, text=col.replace("_", " ").capitalize(), anchor=tk.CENTER) for col in ["cod_barra", "precio", "talle", "Fecha_act", "stock"]]
		products_in_stock = get_products_in_stock()
		[stockTreeView.insert("", "end", text=product.name, values=(product.id, product.price, product.size, get_restock_date(product.id), product.stock)) if product.branch_name.lower() == app.get_variable("branch_user").lower() else stockTreeView.insert("", "end", text=product.name, values=(product.id, product.price, product.size, get_restock_date(product.id), product.stock)) for product in products_in_stock]
		atajos = ctk.CTkFrame(self.main_fr, fg_color=color_p, height=75, width=800); atajos.grid(row=2, column=0)
		if app.get_variable('user_role') == 'Admin': self.u_venta_btn = ctk.CTkButton(atajos, text="Cargar stock", fg_color=grey, text_color=black, corner_radius=25, width=100, height=50, font=('Plus Jakarta Sans', 16, 'bold'), hover_color="#454545", command=lambda: self.manager.switch_scene("C_producto")); self.u_venta_btn.place(x=135, y=25, anchor="center"); self.u_venta_btn.bind("<Enter>", lambda event: self.cambiar_color(self.u_venta_btn, grey, black, event)); self.u_venta_btn.bind("<Leave>", lambda event: self.cambiar_color(self.u_venta_btn, black, grey, event))
	
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
			print(f"Hubo un error {e}. Se asume name_product el usuario es {'Super admin, mostrando todas las sucursales.' if app.get_variable('branch_user') is None else app.get_variable('branch_user')}")
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
		self.main_fr.configure(scrollbar_button_color= color_p, scrollbar_button_hover_color= color_s)
		self.sucursales_fr()
	
	def sucursales_fr(self):
		sucursales_fr = ctk.CTkScrollableFrame(self.main_fr, height=240, width= 750, fg_color= color_p, scrollbar_button_color= color_p, scrollbar_button_hover_color= color_s)
		sucursales_fr.grid(row = 1, column = 0, columnspan=4, sticky = "ew")

		style_card = {'width': 235, 'height': 100, 'corner_radius': 20, 'fg_color': grey, 'font': ('Plus Jakarta Sans', 16, 'bold'), 'hover_color': color_s, 'text_color': black}
		cord = [(0, "San Miguel"),(1, "Jose c Paz"),(2, "Retiro")]
		for x, text in cord:
			card = ctk.CTkButton(sucursales_fr, text = text, **style_card)
			card.grid(row = 0, column = x,pady = 10, padx = 10, sticky="e")

		fr = ctk.CTkFrame(self.main_fr, height=100, width= 750, fg_color= color_p)
		fr.grid(row = 2, column = 0, columnspan=4, padx = 6, sticky = "ew")
		cord_functions = [(0, "Nuevos productos",lambda: app.switch_scene("New_stock")),(1, "Nuevo usuario",lambda: app.switch_scene("New_user"))]
		for x, text, command in cord_functions:
			card = ctk.CTkButton(fr, text = text, **style_card, command= command)
			card.configure(fg_color = black, hover_color = "#232323", text_color = color_p)
			card.grid(row = 0, column = x, padx = 10, pady = 15, sticky="e")

class New_stock(BaseScene):
	def __init__(self, parent, manager):
		super().__init__(parent, manager)

		self.manager=manager
		self.header_fr = header(self.manager)
		self.main()
		self.manager.title("Subir productos")

	def main(self):
		self.main_fr = ctk.CTkFrame(self.manager, fg_color=color_p, height=530, width=800)
		self.main_fr.place(relx=0.5, y=335, anchor="center")
		self.inputs_col()
	def inputs_col(self):
		self.inputs_fr = ctk.CTkFrame(self.main_fr, width= 400, height= 475, fg_color= color_p, corner_radius= 20, border_width= 2, border_color= color_s)
		self.inputs_fr.place(relx=0.5, rely=0.5, anchor="center")
		
		lb = ctk.CTkLabel(self.inputs_fr, text_color=black,text= "Nuevo producto", font= ('Plus jakarta Sans', 28, 'bold')).place(relx=0.5, y=65, anchor="center")

		self.input_config = {'font': ('Plus jakarta Sans', 14, 'bold'),'fg_color': "transparent", 'width': 350, 'height': 50,'corner_radius':35, 'border_color': "#dcdcdc", 'placeholder_text_color': "#BEBEBE",}
		
		self.nombre_producto = ClearableEntry(self.inputs_fr, placeholder_text= 'Ingrese nombre del producto', **self.input_config)
		self.nombre_producto.place(relx=0.5, y=150, anchor="center")
		
		self.marca_produc= ClearableEntry(self.inputs_fr, placeholder_text= 'Ingrese marca del producto', **self.input_config)
		self.marca_produc.place(relx=0.5, y=210, anchor="center")
		
		self.talle_produc=ClearableEntry(self.inputs_fr, placeholder_text= 'Ingrese talle del producto', **self.input_config)
		self.talle_produc.place(relx=0.5, y=270, anchor="center")
		
		self.precio_produc = ClearableEntry(self.inputs_fr, placeholder_text= 'Ingrese precio', **self.input_config)
		self.precio_produc.place(x=111, y=330, anchor="center")
		self.precio_produc.configure(width = 173)

		self.stock_produc = ClearableEntry(self.inputs_fr, placeholder_text= 'Ingrese stock', **self.input_config)
		self.stock_produc.place(x=289, y=330, anchor="center")
		self.stock_produc.configure(width = 173)

		self.new_product = ctk.CTkButton(self.inputs_fr,text= "Subir producto", font= ('Plus jakarta Sans', 14, 'bold')
								,height=50, width = 350, corner_radius= 35, fg_color= black, hover_color= "#454545",
								command= self.new_product_def)
		self.new_product.place(relx = 0.5, y=390, anchor="center")
		self.stock_produc.bind('<Return>',self.new_product_def)

	def new_product_def(self, event = None):
		# Obtener los valores de los inputs
		nombre, marca, talle, precio, stock = (self.nombre_producto.get_and_clear(),self.marca_produc.get_and_clear(),self.talle_produc.get_and_clear(),self.precio_produc.get_and_clear(),self.stock_produc.get_and_clear())

		if campos_vacios := [campo for campo, valor in {"nombre": nombre,"marca": marca,"talle": talle,"precio": precio,"stock": stock,}.items()if not valor]:
			show_notification(app, f"Los siguientes campos están vacíos: {', '.join(campos_vacios)}")
		else:
			show_notification(app, "Nuevo producto cargado con éxito")
			print(nombre, marca, talle, precio, stock)

class New_user(BaseScene):
	def __init__(self, parent, manager):
		super().__init__(parent, manager)
		self.manager=manager
		self.header_fr = header(self.manager)
		self.main()
		self.manager.title("Nuevo usuario")

	def main(self):
		self.main_fr = ctk.CTkFrame(self.manager, fg_color=color_p, height=530, width=800)
		self.main_fr.place(relx=0.5, y=335, anchor="center")
		self.inputs_col()
	def inputs_col(self):
		self.inputs_fr = ctk.CTkFrame(self.main_fr, width= 400, height= 475, fg_color= color_p, corner_radius= 20, border_width= 2, border_color= color_s)
		self.inputs_fr.place(relx=0.5, rely=0.5, anchor="center")
		
		lb = ctk.CTkLabel(self.inputs_fr, text_color=black,text= "Nuevo usuario", font= ('Plus jakarta Sans', 28, 'bold')).place(relx=0.5, y=65, anchor="center")

		self.input_config = {'font': ('Plus jakarta Sans', 14, 'bold'),'fg_color': "transparent", 'width': 350, 'height': 50,'corner_radius':35, 'border_color': "#dcdcdc", 'placeholder_text_color': "#BEBEBE",}
		
		self.nombre_empleado = ClearableEntry(self.inputs_fr, text_color=black,placeholder_text= 'Ingrese nombre del empleado', **self.input_config)
		self.nombre_empleado.place(relx=0.5, y=150, anchor="center")
		
		self.correo_empleado= ClearableEntry(self.inputs_fr, text_color=black, placeholder_text= 'Ingrese correo electronico del empleado', **self.input_config)
		self.correo_empleado.place(relx=0.5, y=210, anchor="center")
		
		self.contraseña=ClearableEntry(self.inputs_fr, text_color=black, placeholder_text= 'Ingrese contraseña', **self.input_config)
		self.contraseña.place(relx=0.5, y=270, anchor="center")

		rangos = ["Ingrese nivel de permisos", "Normal User", "Admin","General Admin"]
		self.permisos = ctk.CTkOptionMenu(self.inputs_fr, values = rangos, font= ('Plus jakarta Sans', 14, 'bold'), text_color= black
											, width = 350, height = 50, fg_color = "#f2f2f2", button_color = "#efefef"
											, corner_radius= 25, button_hover_color = grey, dropdown_fg_color= color_p, dropdown_text_color=black)
		self.permisos.place(relx = 0.5, y=330, anchor="center")

		self.new_product = ctk.CTkButton(self.inputs_fr,text= "Cargar empleado", font= ('Plus jakarta Sans', 14, 'bold')
								,height=50, width = 350, corner_radius= 35, fg_color= black, hover_color= "#454545",
								command= self.new_product_def)
		self.new_product.place(relx = 0.5, y=390, anchor="center")
		self.contraseña.bind('<Return>',self.new_product_def)

	def new_product_def(self, event=None):
		nombre, correo, contraseña, permisos = self.nombre_empleado.get_and_clear(), self.correo_empleado.get_and_clear(), self.contraseña.get_and_clear(), self.permisos.get()
		if campos_vacios := [campo for campo, valor in {"nombre": nombre,"correo": correo,"contraseña": contraseña,"permisos": permisos,}.items()if not valor]:	show_notification(self.manager, f"Los siguientes campos están vacíos: {', '.join(campos_vacios)}")
		elif permisos == "Ingrese nivel de permisos":
			show_notification(self.manager, "Asigne un rango válido")
		else:
			permisos_map = {"Normal User": 1, "Admin": 2, "General Admin": 3}
			permisos = permisos_map.get(permisos)
			try:
				show_notification(self.manager, register_user(nombre, correo, contraseña, permisos, "Retiro"))
			except Exception:
				show_notification(self.manager, "Hubo un error al registrar el empleado")

class Users(BaseScene):
	def __init__(self, parent, manager):
		super().__init__(parent, manager)

		self.manager=manager
		self.header_fr = header(self.manager)
		self.main()
		self.manager.title("Usuarios")

	def main(self):
		self.main_fr = ctk.CTkFrame(self.manager, fg_color=color_p, height=530, width=800)
		self.main_fr.place(relx=0.5, y=335, anchor="center")
		# lb = ctk.CTkLabel(self.main_fr, text_color=black, text = "En mantenimiento").place(relx=0.5, rely=0.5, anchor="center")
		# for notification in notifications:
		# 	card = Card(self.main_fr, notification.title, notification.text)
		# 	card.pack()  
		self.noti_container = ctk.CTkScrollableFrame(self.main_fr, width= 400, height= 425, fg_color= color_p, corner_radius= 40, border_width= 2, border_color= color_s, scrollbar_button_color= grey, scrollbar_button_hover_color= color_s)
		self.noti_container.place(relx=0.5, rely=0.5, anchor="center")

		style_card = {'width': 360, 'height': 100, 'corner_radius': 20, 'fg_color': grey, 'font': ('Plus Jakarta Sans', 16, 'bold'), 'text_color': black}
		# cord = [(0, "San Miguel"),(1, "Jose c Paz"),(2, "Retiro")]
		# for x, text in cord:
		# 	card = ctk.CTkLabel(self.noti_container, text = text, **style_card)
		# 	card.grid(row = x, column = 0,pady = 10, sticky="ew")

		for notification in notifications:
			card = Card(self.noti_container, notification.title, notification.text)
			card.grid(row = 1, column = 0,pady = 10, sticky="ew") 

if __name__ == "__main__":
	notifications=[]
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
    ("New_stock", New_stock),("New_user",New_user), ("Users_nav", Users), ("Notifications_nav", Users)]

	for scene_name, scene_class in scenes:
		app.add_scene(scene_name, scene_class)
  
	# Inicia la aplicación con la primera escena visible
	app.switch_scene("Login")

	app.mainloop()  # Ejecuta el bucle principal de la aplicación