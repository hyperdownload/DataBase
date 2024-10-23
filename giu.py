import contextlib
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
				with contextlib.suppress(Exception):
					if len(get_products_out_of_stock[0]) != 0:
						show_notification(app, "Hay productos sin stock.")
						text = ''.join(f"ID:{id}, name:{name}, brand:{brand}, stock:{stock}"for id, name, brand, stock in get_products_out_of_stock())
						notifications.append(NotificationPlaceHolder("Hay productos sin stock.", f"Los productos sin stock son:{text}", "stock"))
			elif hashlib.sha256(password.encode()).hexdigest() != get_user_details(get_user_id(user))[2]:
				self.user_entry.configure(border_color = "green")
				self.password_entry.configure(border_color = "red")

		except Exception as e:
			self.user_entry.configure(border_color = "red")
			self.password_entry.configure(border_color = "red")
			show_notification(app, "Usuario o contraseña incorrectos.")

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
									corner_radius= 40)
		self.grafico.grid(row=2, column=0, columnspan=2, ipady= 6)

		CTkChart(self.grafico, get_sales_per_categorie(), corner_radius=20, fg_color= color_s, stat_color= black, chart_fg_color= color_s,
         show_indicators=(False, False), stat_info_show=(True, True), chart_arrow="none",
		 indicator_line_color= blue, indicator_text_color= blue, stat_width=35,
         stat_title_color= blue, stat_text_color= '#FFFFFF', chart_axis_width=3, width=700, height= self.h_grid2 - 50).place( relx = 0.5, rely = 0.5, anchor = "center")
		
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
				if product.branch_name.lower() == app.get_variable('branch_user').lower():
					self.tv_stock.insert("",tk.END, text=f"{product.name}",
							values=(product.price,product.brand,product.size, product.description))
		else:
			self.tv_stock.delete(*self.tv_stock.get_children())
			products_in_stock = get_products_in_stock()
			for product in products_in_stock:
				if product.branch_name.lower() == app.get_variable('branch_user').lower():
					self.tv_stock.insert("",tk.END, text=f"{product.name}",
							values=(product.price,product.brand,product.size, product.description))
    
	def update_stock(self):
		focus = self.tv_stock.focus()
		name_product=self.tv_stock.item(focus,'text')
		try:
			record_restock(get_name_per_id(str(name_product)), app.get_variable("user_id"), app.get_variable("branch_user"), self.c_stock.get_and_clear())
			show_notification(app, f"Reestock exitoso\n stock actual: {get_stock_product(get_name_per_id(str(name_product)))}")
			#notifications = [n for n in notifications if n.tag != 'stock']
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

		self.buscar_producto.bind('<Key>', self.search)

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

		self.input_config = {'font': ('Plus jakarta Sans', 14, 'bold'),'fg_color': "transparent", 'width': 350, 'height': 50,'corner_radius':35, "border_color": "#dcdcdc", 'text_color': '#000000'}
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
											, corner_radius= 25, button_hover_color = grey, dropdown_fg_color= color_p, dropdown_text_color=black, command= self.credito)
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

		self.pago = ctk.CTkLabel(self.ticket_col, text_color = color_p, fg_color=black, text=f"Metodo de pago: {self.metodo_pago.get()}", font=('Plus Jakarta Sans', 16, 'bold'))
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
		if app.get_variable('user_role') != 'Normal user': 
			self._extracted_from_main_5()
	#--------------------------------------------------------------------------------------------------------------------------------------------
		tabla = ctk.CTkFrame(self.main_fr, fg_color=color_p, height=425, width=800)
		tabla.grid(row=3, column=0)
		self.tabla_venta = ctk.CTkFrame(tabla, width=675, height=400, fg_color=black, corner_radius=40)
		self.tabla_venta.place(relx=0.5, y=200, anchor="center")
		stockTreeView = ttk.Treeview(self.tabla_venta, columns=("cod_barra", "precio", "talle", "Fecha_act", "stock"))
		stockTreeView.place(relx=0.5, rely=0.5, anchor="center", width=625, height=350)
		[stockTreeView.column(col, width=width) for col, width in [("#0", 110), ("cod_barra", 40), ("precio", 40), ("talle", 30), ("Fecha_act", 115), ("stock", 30)]]
		stockTreeView.heading("#0", text="Producto", anchor=tk.CENTER)
		[stockTreeView.heading(col, text=col.replace("_", " ").capitalize(), anchor=tk.CENTER) for col in ["cod_barra", "precio", "talle", "Fecha_act", "stock"]]
		products_in_stock = get_products_in_stock()
		[stockTreeView.insert("", "end", text=product.name, values=(product.id, product.price, product.size, get_restock_date(product.id), product.stock)) if product.branch_name.lower() == app.get_variable("branch_user").lower() else None for product in products_in_stock]

	def _extracted_from_main_5(self):
		atajos = ctk.CTkFrame(self.main_fr, fg_color=color_p, height=75, width=800)
		atajos.grid(row=2, column=0)
		self.u_venta_btn = ctk.CTkButton(atajos, text="Cargar stock", fg_color=grey, text_color=black, corner_radius=25, width=100, height=50, font=('Plus Jakarta Sans', 16, 'bold'), hover_color="#454545", command=lambda: self.manager.switch_scene("C_producto"))
		self.u_venta_btn.place(x=135, y=25, anchor="center")
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
		
		atajos = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 75, width = 800)
		atajos.grid(row=2, column=0)
		
		self.u_venta_btn = ctk.CTkButton(atajos, text= "Nueva venta", fg_color= "#222325", text_color= color_p, corner_radius=25,
											width= 100, height= 50, font=('Plus Jakarta Sans', 16, 'bold'), hover_color= "#454545", command=lambda: self.manager.switch_scene("C_ventas"))
		self.u_venta_btn.place(x = 135, y= 25, anchor = "center")     
  
		self.u_export_btn = ctk.CTkButton(atajos, text= "Exportar ventas", fg_color= "#222325", text_color= color_p, corner_radius=25,
											width= 100, height= 50, font=('Plus Jakarta Sans', 16, 'bold'), hover_color= "#454545", command= lambda:export_to_file(self.manager))
		self.u_export_btn.place(x = 635, y= 25, anchor = "center")   

		self.u_venta_btn.bind("<Enter>", lambda event: self.cambiar_color(self.u_venta_btn, black, grey, event))
		self.u_venta_btn.bind("<Leave>", lambda event: self.cambiar_color(self.u_venta_btn, grey, "#222325", event))

		tabla = ctk.CTkFrame(self.main_fr, fg_color=color_p, height=425, width=800); tabla.grid(row=3, column=0)
		self.tabla_venta = ctk.CTkFrame(tabla, width=675, height=400, fg_color=black, corner_radius=40); self.tabla_venta.place(relx=0.5, y=200, anchor="center")
		treeview = ttk.Treeview(self.tabla_venta, columns=("Fecha", "Vendedor", "Categoria", "Precio", "Cantidad")); treeview.place(relx=0.5, rely=0.5, anchor="center", width=625, height=350)
		[treeview.column(col, width=width) for col, width in [("#0", 110), ("Fecha", 100), ("Vendedor", 100), ("Categoria", 50), ("Precio", 50), ("Cantidad", 50)]]
		treeview.heading("#0", text="Producto", anchor=tk.CENTER); [treeview.heading(col, text=col.replace("_", " ").capitalize(), anchor=tk.CENTER) for col in ["Fecha", "Vendedor", "Categoria", "Precio", "Cantidad"]]
		
		sales_data = get_all_sales()
	
		try:
			[treeview.insert("", "end", text=get_name_product(sale[1]), values=(sale[5], get_user_name(sale[2]), sale[7], sale[6], sale[4])) for sale in sales_data if sale[3].lower() == app.get_variable("branch_user").lower()]
		except AttributeError as e:
			print(f"Hubo un error {e}. Se asume name_product el usuario es {'Super admin, mostrando todas las sucursales.' if app.get_variable('branch_user') is None else app.get_variable('branch_user')}")
			[treeview.insert("", "end", text=get_name_product(sale[1]), values=(sale[5], get_user_name(sale[2]), sale[4], sale[6])) for sale in sales_data]
		
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
		self.sucursales_fr = ctk.CTkScrollableFrame(self.main_fr, height=240, width= 750, fg_color= color_p, scrollbar_button_color= color_p, scrollbar_button_hover_color= color_s)
		self.sucursales_fr.grid(row = 1, column = 0, columnspan=4, sticky = "ew")

		style_card = {'width': 235, 'height': 100, 'corner_radius': 20, 'fg_color': grey, 'font': ('Plus Jakarta Sans', 16, 'bold'), 'hover_color': color_s, 'text_color': black}
		cord = [(i, branch[0]) for i, branch in enumerate(get_all_branches())]
		for x, texts in cord:
			card = ctk.CTkButton(self.sucursales_fr, text = texts, command=lambda texts=texts: self.sucursal_vw(texts), **style_card)
			card.grid(row = 0, column = x,pady = 10, padx = 10, sticky="e")

		self.fr = ctk.CTkFrame(self.main_fr, height=100, width= 750, fg_color= color_p)
		self.fr.grid(row = 2, column = 0, columnspan=4, padx = 6, sticky = "ew")
		cord_functions = [(0, "Nuevos productos",lambda: app.switch_scene("New_stock")),(1, "Nuevo usuario",lambda: app.switch_scene("New_user"))]
		for x, text, command in cord_functions:
			card = ctk.CTkButton(self.fr, text = text, **style_card, command= command)
			card.configure(fg_color = black, hover_color = "#232323", text_color = color_p)
			card.grid(row = 0, column = x, padx = 10, pady = 15, sticky="e")
	def sucursal_vw(self, sucursal_name):
		app.clear_widget(self.sucursales_fr, self.fr)
		sucursal_name = get_branch_properties(sucursal_name)
		sales = get_all_sales_of_branch(sucursal_name[1])

		columns = ('ID', 'Producto', 'Usuario', 'Sucursal', 'Cantidad', 'Fecha', 'Precio', 'Categoría')
		
		self.treeview = ttk.Treeview(self.main_fr, columns=columns, show='headings')
		self.treeview.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10, pady=10)

		for col in columns:
			self.treeview.heading(col, text=col)
			self.treeview.column(col, anchor='center', width=100)

		for sale in sales:
			self.treeview.insert('', 'end', values=(sale[0], sale[1], sale[2], sale[3], sale[4], sale[5], f"${sale[6]:.2f}", sale[7]))

		text_info = (
			f"El nombre de la sucursal es: {sucursal_name[1]}\n"
			f"El ID es: {sucursal_name[0]}\n"
			f"Dirección: {sucursal_name[2]}\n"
			f"Usuarios en la sucursal: {', '.join([f'{user[0]}' for user in get_user_per_branch(sucursal_name[1])])}"
		)
		label_info = ctk.CTkLabel(self.main_fr, text=text_info, fg_color='#FFFFFF', text_color='black')
		label_info.grid(row=0, column=0, columnspan=4, sticky="ew", padx=10, pady=10)

class New_branch(BaseScene):
	def __init__(self, parent, manager):
		super().__init__(parent, manager)

		self.manager=manager
		self.header_fr = header(self.manager)
		self.main()
		self.manager.title("Nueva sucursal")
	def main(self):
		self.main_fr = ctk.CTkFrame(self.manager, fg_color=color_p, height=530, width=800)
		self.main_fr.place(relx=0.5, y=335, anchor="center")

		self.inputs_fr = ctk.CTkFrame(self.main_fr, width=400, height=295, fg_color=color_p, corner_radius=20, border_width=2, border_color=color_s)
		self.inputs_fr.place(relx=0.5, rely=0.5, anchor="center")

		ctk.CTkLabel(self.inputs_fr, text_color=black, text="Nueva sucursal", font=('Plus jakarta Sans', 28, 'bold')).place(relx=0.5, y=50, anchor="center")

		self.input_config = {'font': ('Plus jakarta Sans', 14, 'bold'),'fg_color': "transparent",'width': 350,'height': 50,'corner_radius': 35,'border_color': "#dcdcdc",'placeholder_text_color': "#BEBEBE"}

		self.branch_name=ClearableEntry(self.inputs_fr, placeholder_text= 'Ingrese nombre de la sucursal', **self.input_config)
		self.branch_name.place(relx=0.5, y=120, anchor="center")
		self.direction_branch=ClearableEntry(self.inputs_fr, placeholder_text= 'Ingrese direccion de la sucursal', **self.input_config)
		self.direction_branch.place(relx=0.5, y=180, anchor="center")

		self.new_product = ctk.CTkButton(self.inputs_fr, text="Crear sucursal", font=('Plus jakarta Sans', 14, 'bold'),height=50, width=350, corner_radius=35, fg_color=black, hover_color="#454545", command=self.new_product_def)
		self.new_product.place(relx=0.5, y=240, anchor="center")

	def new_product_def(self, event = None):
		nombre, direction = (self.branch_name.get_and_clear(),self.direction_branch.get_and_clear())
		if campos_vacios := [campo for campo, valor in {"nombre":nombre,"direction": direction,}.items()if not valor]:	show_notification(self.manager,f"Los siguientes campos están vacíos: {', '.join(campos_vacios)}")
		else:
			try:
				create_new_branch(nombre, direction)
				show_notification(app, "Nueva sucursal cargada con éxito")
			except Exception as e:
				show_notification(app, "Algo fallo.")
		
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
		self.inputs_fr = ctk.CTkFrame(self.main_fr, width= 400, height= 500, fg_color= color_p, corner_radius= 20, border_width= 2, border_color= color_s)
		self.inputs_fr.place(relx=0.5, rely=0.5, anchor="center")
		
		lb = ctk.CTkLabel(self.inputs_fr, text_color=black,text= "Nuevo producto", font= ('Plus jakarta Sans', 28, 'bold')).place(relx=0.5, y=35, anchor="center")

		self.input_config = {'font': ('Plus jakarta Sans', 14, 'bold'), 'text_color': "#000000",'fg_color': "transparent", 'width': 350, 'height': 50,'corner_radius':35, 'border_color': "#dcdcdc", 'placeholder_text_color': "#BEBEBE",}
		
		self.nombre_producto = ClearableEntry(self.inputs_fr, placeholder_text= 'Nombre del producto', **self.input_config)
		self.nombre_producto.place(relx=0.5, y=100, anchor="center")
		
		self.marca_produc= ClearableEntry(self.inputs_fr, placeholder_text= 'Marca del producto', **self.input_config)
		self.marca_produc.place(relx=0.5, y=160, anchor="center")
		
		self.talle_produc=ClearableEntry(self.inputs_fr, placeholder_text= 'Talle del producto', **self.input_config)
		self.talle_produc.place(x=111, y=220, anchor="center")
		self.talle_produc.configure(width = 173)
		
		self.cat_produc=ClearableEntry(self.inputs_fr, placeholder_text= 'Cat. del producto', **self.input_config)
		self.cat_produc.place(x=289, y=220, anchor="center")
		self.cat_produc.configure(width = 173)

		self.precio_produc = ClearableEntry(self.inputs_fr, placeholder_text= 'Precio', **self.input_config)
		self.precio_produc.place(x=111, y=280, anchor="center")
		self.precio_produc.configure(width = 173)

		self.stock_produc = ClearableEntry(self.inputs_fr, placeholder_text= 'Stock', **self.input_config)
		self.stock_produc.place(x=289, y=280, anchor="center")
		self.stock_produc.configure(width = 173)
  
		self.sucursal = ctk.CTkOptionMenu(self.inputs_fr, values=get_all_branch_names(), font=('Plus jakarta Sans', 14, 'bold'), text_color=black,width=350, height=50, fg_color="#f2f2f2", button_color="#efefef", corner_radius=25, button_hover_color=grey, dropdown_fg_color=color_p, dropdown_text_color=black)
		self.sucursal.place(relx=0.5, y=340, anchor="center")

		self.desc_produc=ctk.CTkTextbox(self.inputs_fr, width=350, height=10, fg_color=color_p, border_width=2, border_color= "#dcdcdc", text_color=black, font=('Plus jakarta Sans', 14, 'bold'), corner_radius=10,)
		self.desc_produc.place(relx=0.5, y=400, anchor="center")

		self.new_product = ctk.CTkButton(self.inputs_fr,text= "Subir producto", font= ('Plus jakarta Sans', 14, 'bold')
								,height=50, width = 350, corner_radius= 35, fg_color= black, hover_color= "#454545",
								command= self.new_product_def)
		self.new_product.place(relx = 0.5, y=460, anchor="center")
		self.stock_produc.bind('<Return>',self.new_product_def)

	def new_product_def(self, event = None):
		nombre, marca, talle, cat, precio, stock, sucursal, desc = (self.nombre_producto.get_and_clear(),self.marca_produc.get_and_clear(),self.talle_produc.get_and_clear(),self.cat_produc.get_and_clear(),self.precio_produc.get_and_clear(),self.stock_produc.get_and_clear(), self.sucursal.get(), self.desc_produc.get('1.0', ctk.END))
		self.desc_produc.delete('1.0', ctk.END)
		if campos_vacios := [campo for campo, valor in {"nombre": nombre,"marca": marca,"talle": talle,"precio": precio,"stock": stock, "sucursal": sucursal, "desc":desc, 'cat':cat,}.items()if not valor]:
			show_notification(app, f"Los siguientes campos están vacíos: {', '.join(campos_vacios)}")
		else:
			show_notification(app, "Nuevo producto cargado con éxito")
			add_product(Product(name=nombre, brand=marca, size=talle,category=cat, price=precio, stock=stock, branch_name=sucursal, description=desc))

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
		self.inputs_fr = ctk.CTkFrame(self.main_fr, width=400, height=475, fg_color=color_p, corner_radius=20, border_width=2, border_color=color_s)
		self.inputs_fr.place(relx=0.5, rely=0.5, anchor="center")

		ctk.CTkLabel(self.inputs_fr, text_color=black, text="Nuevo usuario", font=('Plus jakarta Sans', 28, 'bold')).place(relx=0.5, y=50, anchor="center")

		self.input_config = {'font': ('Plus jakarta Sans', 14, 'bold'),'fg_color': "transparent",'width': 350,'height': 50,'corner_radius': 35,'border_color': "#dcdcdc",'placeholder_text_color': "#BEBEBE"}

		fields = [('nombre_empleado', 'Ingrese nombre del empleado', 120),('correo_empleado', 'Ingrese correo electronico del empleado', 180),('contraseña', 'Ingrese contraseña', 240)]

		for attr, placeholder, y_pos in fields:
			setattr(self, attr, ClearableEntry(self.inputs_fr, text_color=black, placeholder_text=placeholder, **self.input_config))
			getattr(self, attr).place(relx=0.5, y=y_pos, anchor="center")

		if self.manager.get_variable('user_role') == 'Admin':
			values = ["Ingrese nivel de permisos", "Normal User"]
			values_branch = [self.manager.get_variable('branch_user')]
			print(self.manager.get_variable('branch_user'))
		else:
			values = ["Ingrese nivel de permisos", "Normal User", "Admin", "General Admin"]
			values_branch = get_all_branch_names()

		self.sucursal = ctk.CTkOptionMenu(self.inputs_fr, values= values_branch, font=('Plus jakarta Sans', 14, 'bold'), text_color=black,width=350, height=50, fg_color="#f2f2f2", button_color="#efefef", corner_radius=25, button_hover_color=grey, dropdown_fg_color=color_p, dropdown_text_color=black)
		self.sucursal.place(relx=0.5, y=300, anchor="center")

		self.permisos = ctk.CTkOptionMenu(self.inputs_fr, values=values, font=('Plus jakarta Sans', 14, 'bold'), text_color=black, width=350, height=50, fg_color="#f2f2f2", button_color="#efefef", corner_radius=25, button_hover_color=grey, dropdown_fg_color=color_p, dropdown_text_color=black)
		self.permisos.place(relx=0.5, y=360, anchor="center")

		self.new_product = ctk.CTkButton(self.inputs_fr, text="Cargar empleado", font=('Plus jakarta Sans', 14, 'bold'),height=50, width=350, corner_radius=35, fg_color=black, hover_color="#454545", command=self.new_product_def)
		self.new_product.place(relx=0.5, y=420, anchor="center")

	def new_product_def(self, event=None):
		nombre, correo, contraseña, permisos, sucursal = self.nombre_empleado.get_and_clear(), self.correo_empleado.get_and_clear(), self.contraseña.get_and_clear(), self.permisos.get(), self.sucursal.get_and_clear()
		if campos_vacios := [campo for campo, valor in {"nombre": nombre,"correo": correo,"contraseña": contraseña,"permisos": permisos, "sucursal": sucursal,}.items()if not valor]:	show_notification(self.manager, f"Los siguientes campos están vacíos: {', '.join(campos_vacios)}")
		elif permisos == "Ingrese nivel de permisos":
			show_notification(self.manager, "Asigne un rango válido.")
		else:
			permisos_map = {"Normal User": 1, "Admin": 2, "General Admin": 3}
			permisos = permisos_map.get(permisos)
			try:
				show_notification(self.manager, register_user(nombre, correo, contraseña, permisos, sucursal))
			except Exception as e:
				print(e)
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

		columns = [("#0", "Name", 120), 
				("email", "Email", 100), 
				("role_id", "Role_id", 30), 
				("Branch_id", "Branch", 50),]
		
		user_style = ttk.Style()
		user_style.configure("Custom.Treeview.Heading", background=color_p, foreground=black, font=("Arial", 12, "bold"), relief="flat")
		user_style.configure("Custom.Treeview", background=color_p, foreground=black, fieldbackground=color_p, borderwidth=0, relief="flat")
		user_style.map("Treeview.Heading", background=[("selected",  "#efefef"), ("active",  "#efefef")])

		self.tabla = ttk.Treeview(self.main_fr, selectmode=tk.BROWSE, columns=[col[0] for col in columns[1:]], style="Custom.Treeview")
		self.tabla.place(relx=0.5, rely=0.5, anchor="center", width=790, height=530)

		for col, heading, width in columns:
			self.tabla.column(col, width=width)
			self.tabla.heading(col, text=heading, anchor=tk.CENTER)

		# Obtener detalles de los usuarios e insertarlos en el Treeview
		users_details = get_all_users_details()
		for user in users_details:
			self.tabla.insert("", "end", text=user[1], values=(user[2], user[3], user[5], "N/A"))  # "N/A" para la fecha de registro

class Notifications(BaseScene):
	def __init__(self, parent, manager):
		super().__init__(parent, manager)

		self.manager=manager
		self.header_fr = header(self.manager)
		self.main()
		self.manager.title("Notificaciones")

	def main(self):
		self.main_fr = ctk.CTkFrame(self.manager, fg_color=color_p, height=530, width=800)
		self.main_fr.place(relx=0.5, y=335, anchor="center")
		self.noti_container = ctk.CTkScrollableFrame(self.main_fr, width= 400, height= 425, fg_color= color_p, corner_radius= 40, border_width= 2, border_color= color_s, scrollbar_button_color= grey, scrollbar_button_hover_color= color_s)
		self.noti_container.place(relx=0.5, rely=0.5, anchor="center")
		if len(notifications) != 0:
			for notification in notifications:
				card = Card(self.noti_container, notification.title, notification.text, notification.tag)
				card.grid(row = 1, column = 0,pady = 10, sticky="ew") 
		else:
			card = Card(self.noti_container, "Informacion", "No hay notificaciones pendientes.", "Muajajaj", width=400)
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
    ("New_stock", New_stock),("New_user",New_user), ("Users_nav", Users), ("Notifications_nav", Notifications), ("New_branch", New_branch),]

	for scene_name, scene_class in scenes:
		app.add_scene(scene_name, scene_class)
  
	# Inicia la aplicación con la primera escena visible
	app.switch_scene("Login")

	app.mainloop()  # Ejecuta el bucle principal de la aplicación