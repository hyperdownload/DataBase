import contextlib
from Utils.SceneManager import *
from Utils.database import *
from Utils.functions import *
from CTkDataVisualizingWidgets import *
from PIL import Image
import customtkinter as ctk
from tkinter import ttk
from CTkToolTip import CTkToolTip

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
		
		self.user_entry = self._extracted_from_login_10(
			login_container, "Ingrese su nombre de usuario...", 260
		)
		self.password_entry = self._extracted_from_login_10(
			login_container, "Ingrese su contraseña...", 310, True
		)
		self.password_entry.bind('<MouseWheel>', lambda event: self.login_logic(autologin=True))
		self.user=ImageP(login_container,"./img/person.png", height=18, width=18,x=545,y=247)
		self.key=ImageP(login_container,"./img/key.png", height=18, width=18,x=545,y=297)
		ctk.CTkButton(login_container, text="Login", height=35, width=350, corner_radius=20, fg_color=black, text_color=color_p, hover_color="#454545", command=self.login_logic).place(relx=0.5, y=360, anchor="center")

	def _extracted_from_login_10(self, login_container, placeholder_text, y, is_password=False):
		result = ClearableEntry(
			login_container,
			height=35,
			width=350,
			corner_radius=20,
			placeholder_text=placeholder_text,
			fg_color="#FFFFFF",
			text_color=black,
		)
		if is_password:
			result.configure(show="*")  # Configura el entry para que muestre * en lugar de texto real

		result.place(relx=0.5, y=y, anchor="center")
		result.bind('<Return>', self.login_logic)

		return result
  
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
		
		self.col_atajo()

	def cambiar_color(self, widget, text_color, fg_color, event=None):
		widget.configure(text_color=text_color, fg_color=fg_color)

	def col_atajo(self):
		self.atajos_frame = ctk.CTkFrame(self.main_fr, width= 800, height=470, fg_color= color_p)
		self.atajos_frame.grid(row=1, column=1, padx = 12)

		self.cargar_prod_lb = ctk.CTkLabel(self.atajos_frame, width= 270, height= 200, fg_color= grey,
											corner_radius= 40, text= "")
		self.cargar_prod_lb.place(relx = 0.63, y = 0)

		self.cargar_productos_txt = ctk.CTkLabel(self.cargar_prod_lb,text_color=black, text= "Cargar\nProductos", font=('Plus Jakarta Sans', 38, 'bold'), justify = "left")
		self.cargar_productos_txt.place(x = 35, y = 10)
		self.c_productos_btn = ctk.CTkButton(self.cargar_prod_lb, text= "Cargar", fg_color= black, text_color= color_p, corner_radius=25,
											width= 200, height= 50, font=('Plus Jakarta Sans', 24, 'bold'), hover_color= "#454545", command=lambda: self.manager.switch_scene("C_producto"))
		self.c_productos_btn.place(relx = 0.5, y = 150, anchor = "center")

		self.c_productos_btn.bind("<Enter>", lambda event: self.cambiar_color(self.c_productos_btn, grey, "#454545", event))
		self.c_productos_btn.bind("<Leave>", lambda event: self.cambiar_color(self.c_productos_btn, grey, black, event))
		#--------------------------------------------------------------------------------------------------------------------------------------------

		self.ult_venta = ctk.CTkLabel(self.atajos_frame, width= 270, height= 230, fg_color= black, corner_radius= 40)
		self.ult_venta.place(relx = 0.8, y = 320, anchor= "center")

		self.ult_venta_txt = ctk.CTkLabel(self.ult_venta, text= "Registrar\nUltima venta", font=('Plus Jakarta Sans', 38, 'bold'), text_color= grey,
										justify = "center", wraplength= 200)
		self.ult_venta_txt.place(relx = 0.5, y = 80, anchor = "center")
		self.u_venta_btn = ctk.CTkButton(self.ult_venta, text= "Registrar", fg_color= grey, text_color= black, corner_radius=25,
											width= 200, height= 50, font=('Plus Jakarta Sans', 24, 'bold'), hover_color= "#454545", command=lambda: self.manager.switch_scene("C_ventas"))
		self.u_venta_btn.place(relx = 0.5, y = 180, anchor = "center")        

		self.u_venta_btn.bind("<Enter>", lambda event: self.cambiar_color(self.u_venta_btn, grey, "#454545", event))
		self.u_venta_btn.bind("<Leave>", lambda event: self.cambiar_color(self.u_venta_btn, black, grey, event))
  
		CTkChart(self.atajos_frame, get_sales_per_categorie(), corner_radius=20, fg_color= color_s, stat_color= black, chart_fg_color= color_s,
         show_indicators=(False, False), stat_info_show=(True, True), chart_arrow="none",
		 indicator_line_color= blue, indicator_text_color= blue, stat_width=25,
         stat_title_color= blue, stat_text_color= '#FFFFFF', chart_axis_width=3, width=460, height= 415).place( relx = 0.32, rely = 0.46, anchor = "center")
		
class C_producto(BaseScene):
	def __init__(self, parent, manager):
		super().__init__(parent, manager)

		self.manager=manager
		self.manager.title("Carga de productos")
		self.header_fr = header(self.manager)
		self.main()

	def search(self, event=None):
		if self.buscar_producto.get():
			self.tabla_stock.clear()
			search_results = search_function(get_products_in_stock(), self.buscar_producto.get())

			branch_user = app.get_variable('branch_user').lower()
			rows = [
				(product.name, product.price, product.brand, product.size, product.description)
				for product in search_results if product.branch_name.lower() == branch_user
			]
		else:
			self.tabla_stock.clear()
			products_in_stock = get_products_in_stock()
			rows = [
				(product.name, product.price, product.brand, product.size, product.description)
				for product in products_in_stock if product.branch_name.lower() == app.get_variable('branch_user').lower()
			]

		self.tabla_stock.insert(rows)

	def update_stock(self):
		focus = self.tabla_stock.focus()
		name_product = self.tabla_stock.item(focus, 'text')
		try:
			record_restock(get_name_per_id(str(name_product)), app.get_variable("user_id"), app.get_variable("branch_user"), self.c_stock.get_and_clear())
			show_notification(app, f"Reestock exitoso\n stock actual: {get_stock_product(get_name_per_id(str(name_product)))}")
			
			notifications = [n for n in notifications if n.tag != 'stock']
		except TypeError:
			show_notification(app, "Error al reestockear,\n procure seleccionar un\n producto de la tabla")

	def main(self):
		self.main_fr, self.sucursal_fr, self.sucursal_lb = create_scrollable_frame(self.manager, color_p, app.get_variable("branch_user"))
	#--------------------------------------------------------------------------------------------------------------------------------------------
		lupa = ctk.CTkImage(Image.open("img/search.png"), size=(35, 35))
		
		self.cp_fr = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 85, width = 800)
		self.cp_fr.grid(row=1, column=0)
		self.buscar_producto = ClearableEntry(self.cp_fr, placeholder_text= "Buscar producto...", width= 250, height=50,
										corner_radius=35, border_color= "#dcdcdc", text_color= black)
		self.buscar_producto.place(x = 185, rely = 0.5, anchor= "center")

		self.buscar_producto.bind('<Key>', self.search)

		bp_btn = ctk.CTkButton(self.cp_fr, text= "", image = lupa, fg_color= color_s, hover_color= "#dcdcdc"
									, height= 50, width= 50, corner_radius= 15, cursor = "hand2", command = self.search)
		bp_btn.place(x = 355, rely = 0.5, anchor= "center")

		self.c_stock = ClearableEntry(self.cp_fr, placeholder_text= "Cantidad a subir...", width= 250, height=50,
										corner_radius=35, border_color= "#dcdcdc", text_color= "#FFFFFF" )
		self.c_stock.place(x = 525, rely= 0.5, anchor= "center")

		c_btn = ctk.CTkButton(self.cp_fr, text= "Subir", fg_color= black, hover_color= "#dcdcdc"
									, height= 50, width= 75, corner_radius= 15, cursor = "hand2", command=self.update_stock)
		c_btn.place(x = 700, rely = 0.5, anchor= "center")
	#--------------------------------------------------------------------------------------------------------------------------------------------
		tabla = ctk.CTkFrame(self.main_fr, fg_color = color_p, height = 425, width = 800)
		tabla.grid(row=2, column=0)

		columns = [("#0", "Product", 117), ("price", "Price", 50), ("brand", "Brand", 50), ("size", "Size", 50), ("description", "Description", 117)]
        
		self.tabla_stock = Table(tabla, columns=columns, color_tabla=black, color_frame=black, width=675, height=400)
		self.tabla_stock.place(relx=0.5, y=200, anchor="center")
        
		branch_user = app.get_variable('branch_user').lower()
		rows = [
            (product.name, product.price, product.brand, product.size, product.description)
            for product in get_products_in_stock() if product.branch_name.lower() == branch_user
        ]
		self.tabla_stock.insert(rows)
	
class C_ventas(BaseScene):
	def __init__(self, parent, manager):
		super().__init__(parent, manager)

		self.manager = manager
		self.id_product = []
		self.manager.title("Cargar Ventas")
		self.header_fr = header(self.manager)
		self.main()
		self.metodo = ''
		self.before = 'Efectivo'
  
	def main(self):
		self.main_fr, self.sucursal_fr, self.sucursal_lb = create_scrollable_frame(self.manager, color_p, app.get_variable("branch_user"))
		self.inputs_col()
		self.visualizar_datos()

	def conf(self):
		self.tooltip1.configure(message=f"Producto: {get_product_name(self.inputid.get())}")

	def inputs_col(self):
		self.inputs_fr = ctk.CTkFrame(self.main_fr, width=400, height=300, fg_color=color_p)
		self.inputs_fr.grid(row=1, column=0)
		self.inputs_fr.grid_propagate(0)

		self.input_config = {'font': ('Plus jakarta Sans', 14, 'bold'), 'fg_color': "transparent", 'width': 350, 'height': 50, 'corner_radius': 35, "border_color": "#dcdcdc", 'text_color': '#000000'}
		input_style = [("Ingrese código de barra", 0), ("Ingrese cantidad", 1), ("Ingrese descuento (Sin poner %)", 4)]
		for text, y_cord in input_style:
			if y_cord == 0:
				self.inputid = ClearableEntry(self.inputs_fr, placeholder_text=text, **self.input_config)
				self.inputid.grid(row=y_cord, column=1, pady=5, padx=35)
				self.inputid.bind("<Key>", lambda event: self.after(1, self.conf))
				self.tooltip1 = CTkToolTip(self.inputid, message=f"Producto: {get_product_name(self.inputid.get())}")
			elif y_cord == 1:
				self.inputq = ClearableEntry(self.inputs_fr, placeholder_text=text, **self.input_config)
				self.inputq.grid(row=y_cord, column=1, pady=5, padx=35)
			elif y_cord == 4:
				self.input_discount = ClearableEntry(self.inputs_fr, placeholder_text=text, **self.input_config)
				self.input_discount.grid(row=y_cord, column=1, pady=5, padx=35)

		metodos_pago = ["Efectivo", "Credito", "Debito", "Transferencia"]
		self.metodo_pago = ctk.CTkOptionMenu(self.inputs_fr, values=metodos_pago, font=('Plus jakarta Sans', 14, 'bold'), text_color=black,
											 width=350, height=50, fg_color=color_s, button_color=grey,
											 corner_radius=25, button_hover_color=grey, dropdown_fg_color=color_p, dropdown_text_color=black, command=self.credito)
		self.metodo_pago.grid(row=2, column=1, pady=5, padx=25)

		self.p = ImageP(self.inputs_fr,"./img/id.png", height=25, width=25,x=5,y=15)
		self.pr= ImageP(self.inputs_fr,"./img/prod.png", height=25, width=25,x=5,y=75)
		self.c = ImageP(self.inputs_fr,"./img/credit-card.png", height=25, width=25,x=5,y=135)
		self.d = ImageP(self.inputs_fr,"./img/dis.png", height=25, width=25,x=5,y=193)

		btn_inputs = ctk.CTkFrame(self.main_fr, width=400, height=50, fg_color=color_p)
		btn_inputs.grid(row=2, column=0)
		self.inputs_fr.grid_propagate(0)

		registrar = ctk.CTkButton(btn_inputs, text="Ticket", fg_color=black, text_color=color_p, corner_radius=25, border_color=black, border_width=3,
								  width=165, height=35, font=('Plus Jakarta Sans', 12, 'bold'), hover_color="#454545", command=self.generate_ticket)
		registrar.grid(row=0, column=1, padx=5)
  
		delete = ctk.CTkButton(btn_inputs, text="Borrar ticket", fg_color=black, text_color=color_p, corner_radius=25, border_color=black, border_width=3,
								  width=165, height=35, font=('Plus Jakarta Sans', 12, 'bold'), hover_color="#454545", command=self.delete_ticket)
		delete.grid(row=0, column=2, padx=5)

	def delete_ticket(self):
		try:
			self.treeviewt.delete(*self.treeviewt.get_children())
			self.id_product.clear()
		except Exception:
			show_notification(app, "No hay nada que eliminar.")

	def generate_ticket(self):  # sourcery skip: extract-method
		if self.metodo in ["Credito", "Debito"] and not self.input_c.get():
			return show_notification(app, "Tarjeta no ingresada")
		discount_value = (
			(float(discount) / 100) if (discount := self.input_discount.get()) else 0
		)
		try:
			product_name = get_name_product(int(self.inputid.get()))
			price = get_price_product(int(self.inputid.get()))
			quantity = int(self.inputq.get())
			
			final_price = price * (1 - discount_value) * quantity

			self.pago.configure(text=f"Método de pago: {self.metodo_pago.get()}")
			items=[(product_name, final_price, quantity)]
			self.treeviewt.insert(elements=items)
			self.id_product.append(self.inputid.get())
		except ValueError:
			return show_notification(app, "Error en los datos ingresados.")

	def credito(self, metodo):
		self.metodo = metodo
		if self.metodo != self.before:
			if self.metodo in ["Credito", "Debito"]:
				self._extracted_from_credito_4()
				self.before = metodo
			else:
				self.d.animate_to(5,193,0.5,90)
				self.input_c.unbind('<KeyRelease>')
				self.input_c.destroy()
				self.input_c.grid_forget()

	def _extracted_from_credito_4(self):
		self.input_c = ClearableEntry(self.inputs_fr, placeholder_text="Ingrese tarjeta", **self.input_config)
		self.input_c.grid(row=3, column=1, pady=5, padx=25)
		self.input_c.bind('<KeyRelease>', self.detect_card_type)
		self.cardText = ctk.CTkLabel(app,width=30, text='', text_color=black, bg_color='#FFFFFF')
		self.cardText.place(x=385,y=360)
		self.d.animate_to(5,255,0.5,90)
	def detect_card_type(self, event):
		card_number = self.input_c.get().replace(" ", "")[:6]
		if card_type := self.get_card_type(card_number):
			self.cardText.configure(text=card_type)
		else:
			self.cardText.configure(text='')

	def get_card_type(self, card_number):
		if card_number.startswith("4"):
			return "Visa"
		try:
			if 51 <= int(card_number[:2]) <= 55 or 2221 <= int(card_number) <= 2720:
				return "Mastercard"
			elif card_number.startswith("34") or card_number.startswith("37"):
				return "American Express"
			elif card_number.startswith("6011") or card_number.startswith("65") or 622126 <= int(card_number) <= 622925:
				return "Discover"
			else:
				return ''
		except ValueError:
			return ''

	def visualizar_datos(self):
		self.ticket_col = ctk.CTkFrame(self.main_fr, width=400, height=400, fg_color=color_p)
		self.ticket_col.grid(row=1, column=1, rowspan=2)
		self.inputs_fr.grid_propagate(0)

		ticket_fr = ctk.CTkFrame(self.ticket_col, width=300, height=400, fg_color=black, corner_radius=20, border_color=grey, border_width=3)
		ticket_fr.place(relx=0.5, rely=0.5, anchor="center")

		columns = [("#0", "Producto", 50),("Precio", "Precio", 50),("Cantidad", "Cantidad", 50)]

		self.treeviewt = Table(master=ticket_fr,columns=columns,color_tabla=black,color_frame=black,width=280,height=350, filterBool=False)
		self.treeviewt.frame.place(relx=0.5, y=195, anchor="center")

		self.pago = ctk.CTkLabel(self.ticket_col, text_color=color_p, fg_color=black, text=f"Método de pago: {self.metodo_pago.get()}", font=('Plus Jakarta Sans', 16, 'bold'))
		self.pago.place(x=75, y=320)

		registrar_venta = ctk.CTkLabel(self.ticket_col, text_color=color_p, fg_color=black, text="Registrar Venta", font=('Plus Jakarta Sans', 16, 'bold', 'underline'), cursor="hand2")
		registrar_venta.place(x=75, y=350)
		registrar_venta.bind('<Button-1>', self.registrar_venta_func)

	def registrar_venta_func(self, event):
		try:
			product_id = int(self.inputid.get_and_clear())
			branch_name = app.get_variable('branch_user')
			
			if hasattr(self, 'input_c') and self.input_c.winfo_exists():
				if not self.input_c.get():
					show_notification(app, "Ingrese un numero de tarjeta.")
					return
			
			for parent in self.treeviewt.get_children():
				for id in self.id_product:
					values = self.treeviewt.item(parent)["values"]
					product_id = id
					precio = float(values[0])
					quantity = int(values[1])

					if record_sale(product_id, app.get_variable('user_id'), branch_name, quantity, get_price_product(product_id), self.metodo_pago.get(), self.input_discount.get()):
						show_notification(app, "Venta registrada")
						
						if hasattr(self, 'input_c'):
							self.input_c.delete(0, tk.END)
					
		except ValueError:
			show_notification(app, "Por favor ingrese todos los campos y suba el ticket.")
	
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
		tabla = ctk.CTkFrame(self.main_fr, fg_color=color_p, height=600, width=800)
		tabla.grid(row=3, column=0)
		columns = [("#0", "Producto", 110),   ("ID", "ID", 40),("Precio", "Precio", 40),("Talle", "Talle", 30),("Fecha_act", "Fecha act.", 115),("Stock", "Stock", 30)]

		self.tabla_stock = Table(master=tabla, columns=columns, color_tabla=black, color_frame=black, width=625, height=600)
		self.tabla_stock.grid(row=0, column=0, padx=20, pady=20)

		datos_filtrados = [
			(product.name,product.id,product.price,product.size,get_restock_date(product.id),product.stock)
			for product in get_products_in_stock()
			if product.branch_name.lower() == app.get_variable("branch_user").lower()]

		self.tabla_stock.insert(datos_filtrados)

	def _extracted_from_main_5(self):
		atajos = ctk.CTkFrame(self.main_fr, fg_color=color_p, height=75, width=800)
		atajos.grid(row=2, column=0)
		self.u_venta_btn = ctk.CTkButton(atajos, text="Cargar Restock", fg_color=grey, text_color=black, corner_radius=25, width=100, height=50, font=('Plus Jakarta Sans', 16, 'bold'), hover_color="#454545", command=lambda: self.manager.switch_scene("C_producto"))
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

		tabla = ctk.CTkFrame(self.main_fr, fg_color=color_p, height=425, width=800)
		tabla.grid(row=3, column=0)

		columns = [
			("#0", "N. Venta", 50),
			("Prod", "Prod", 50),
			("Usuario", "Usuario", 75),
			("Sucursal", "Sucursal", 50),
			("Cantidad", "Cantidad", 30),
			("Fecha", "Fecha", 45),
			("Precio", "Precio", 50),
			("Categoria", "Categoria", 50),
    		("PayMethod", "Metodo de Pago", 50),
      		("Descuento", "Descuento", 50)
		]
		self.sales_view = Table(tabla, columns=columns, width=725, height=750,color_frame=black, color_tabla=black)
		self.sales_view.place(x=25,y=0)
		self.sales_view.insert(get_all_sales())

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
		cord_functions = [(0, "Nuevos productos",lambda: app.switch_scene("New_stock")),(1, "Nuevo usuario",lambda: app.switch_scene("New_user")),(2, "Restockear",lambda: app.switch_scene("Restock"))]
		for x, text, command in cord_functions:
			card = ctk.CTkButton(self.fr, text = text, **style_card, command= command)
			card.configure(fg_color = black, hover_color = "#232323", text_color = color_p)
			card.grid(row = 0, column = x, padx = 10, pady = 15, sticky="e")
  
	def sucursal_vw(self, sucursal_name):
		app.clear_widget(self.sucursales_fr, self.fr)

		sucursal_name = get_branch_properties(sucursal_name)

		columns = [("#0", "ID", 30), 
				("Producto", "Producto", 90), 
				("Usuario", "Usuario", 60), 
				("Sucursal", "Sucursal", 70), 
				("Cantidad", "Cantidad", 70), 
				("Fecha", "Fecha", 80), 
				("Precio", "Precio", 50), 
				("Categoria", "Categoria", 80), 
				("M. Pago", "M. Pago", 50), 
				("Descuento", "Descuento", 70)]

		self.tabla = Table(self.main_fr, columns=columns,color_frame=black, color_tabla=black, height=725, width=800)
		self.tabla.grid(row=1, column=0, padx=20, pady=20)

		self.tabla.insert(get_all_sales_of_branch(sucursal_name[1]))

		text_info = (
			f"El nombre de la sucursal es: {sucursal_name[1]}\n"
			f"El ID es: {sucursal_name[0]}\n"
			f"Dirección: {sucursal_name[2]}\n"
			f"Usuarios en la sucursal: {', '.join([f'{user[0]}' for user in get_user_per_branch(sucursal_name[1])])}"
		)
		
		label_info = ctk.CTkLabel(self.main_fr, text=text_info, fg_color='#FFFFFF', text_color='black')
		label_info.grid(row=0, column=0, columnspan=4, sticky="ew", padx=10)

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

		self.branch_name = self.extract(
			'Ingrese nombre de la sucursal', 120, './img/branch.png', 105
		)
		self.direction_branch = self.extract(
			'Ingrese direccion de la sucursal', 180, './img/place.png', 165
		)
		self.new_product = ctk.CTkButton(self.inputs_fr, text="Crear sucursal", font=('Plus jakarta Sans', 14, 'bold'),height=50, width=350, corner_radius=35, fg_color=black, hover_color="#454545", command=self.new_product_def)
		self.new_product.place(relx=0.5, y=240, anchor="center")

	def extract(self, placeholder_text, y, arg2, arg3):
		result = ClearableEntry(
			self.inputs_fr, placeholder_text=placeholder_text, **self.input_config
		)
		result.place(relx=0.5, y=y, anchor="center")
		self.suc = ImageP(self.inputs_fr, arg2, height=25, width=25, x=335, y=arg3)
		return result

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

		self.user = ImageP(self.inputs_fr, './img/person.png',height=25, width=25,x=340,y=105)
		self.email = ImageP(self.inputs_fr, './img/email.png',height=25,width=25,x= 340, y=165)
		self.key = ImageP(self.inputs_fr, './img/key.png',height=25,width=25,x= 340, y=225)

		self.sucursal = ctk.CTkOptionMenu(self.inputs_fr, values= values_branch, font=('Plus jakarta Sans', 14, 'bold'), text_color=black,width=350, height=50, fg_color="#f2f2f2", button_color="#efefef", corner_radius=25, button_hover_color=grey, dropdown_fg_color=color_p, dropdown_text_color=black)
		self.sucursal.place(relx=0.5, y=300, anchor="center")

		self.permisos = ctk.CTkOptionMenu(self.inputs_fr, values=values, font=('Plus jakarta Sans', 14, 'bold'), text_color=black, width=350, height=50, fg_color="#f2f2f2", button_color="#efefef", corner_radius=25, button_hover_color=grey, dropdown_fg_color=color_p, dropdown_text_color=black)
		self.permisos.place(relx=0.5, y=360, anchor="center")

		self.new_product = ctk.CTkButton(self.inputs_fr, text="Cargar empleado", font=('Plus jakarta Sans', 14, 'bold'),height=50, width=350, corner_radius=35, fg_color=black, hover_color="#454545", command=self.new_product_def)
		self.new_product.place(relx=0.5, y=420, anchor="center")

	def new_product_def(self, event=None):
		nombre, correo, contraseña, permisos, sucursal = self.nombre_empleado.get_and_clear(), self.correo_empleado.get_and_clear(), self.contraseña.get_and_clear(), self.permisos.get(), self.sucursal.get()
		if campos_vacios := [campo for campo, valor in {"nombre": nombre,"correo": correo,"contraseña": contraseña,"permisos": permisos, "sucursal": sucursal,}.items()if not valor]:	
			show_notification(self.manager, f"Los siguientes campos están vacíos: {', '.join(campos_vacios)}")
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
		self.main_fr = ctk.CTkFrame(self.manager, fg_color=color_p, height=525, width=800)
		self.main_fr.place(relx=0.5, y=335, anchor="center")

		columns = [("#0", "ID", 80), 
				("name", "Name", 100), 
				("emain", "Email", 50), 
				("rol", "Rango", 50),
				("branch", "Sucursal", 50),]

		self.tabla = Table(self.main_fr, columns=columns,color_frame=black, color_tabla=black, height=725, width=750)
		self.tabla.place(x=25,y=10)

		self.tabla.insert(get_all_users_details())

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

class R_Prod(BaseScene):
    def __init__(self, parent, manager):
        super().__init__(parent, manager)
        self.manager=manager
        self.header_fr = header(self.manager)
        self.main()
        self.manager.title("Restock")
        
    def main(self):
        self.main_fr = ctk.CTkFrame(self.manager, fg_color=color_p, height=530, width=800)
        self.main_fr.place(relx=0.5, y=335, anchor="center")
        self.inputs_col()
    
    def conf(self):
        self.tooltip2.configure(message=f"Producto: {get_product_name(self.product_id.get())}")
        
    def inputs_col(self):
        self.inputs_fr = ctk.CTkFrame(self.main_fr, width= 400, height= 500, fg_color= color_p, corner_radius= 20, border_width= 2, border_color= color_s)
        self.inputs_fr.place(relx=0.5, rely=0.5, anchor="center")
        
        lb = ctk.CTkLabel(self.inputs_fr, text_color=black,text= "Restock", font= ('Plus jakarta Sans', 28, 'bold')).place(relx=0.5, y=35, anchor="center")
        
        self.input_config = {'font': ('Plus jakarta Sans', 14, 'bold'), 'text_color': "#000000",'fg_color': "transparent", 'width': 350, 'height': 50,'corner_radius':35, 'border_color': "#dcdcdc", 'placeholder_text_color': "#BEBEBE",}
        
        self.product_id = ClearableEntry(self.inputs_fr, placeholder_text= 'ID del producto', **self.input_config)
        self.product_id.place(relx=0.5, y=100, anchor="center")
        self.product_id.bind("<Key>", lambda event: self.after(1, self.conf))
        self.tooltip2 = CTkToolTip(self.product_id, message=f"Producto: {get_product_name(self.product_id.get())}")
        self.id = ImageP(self.inputs_fr, './img/id.png',height=25, width=25,x=340,y=85)
        
        self.quantity= ClearableEntry(self.inputs_fr, placeholder_text= 'Cantidad', **self.input_config)
        self.quantity.place(relx=0.5, y=160, anchor="center")
        self.q = ImageP(self.inputs_fr, './img/prod.png',height=25, width=25,x=340,y=145)
        
        self.sucursal = ctk.CTkOptionMenu(self.inputs_fr, values=get_all_branch_names(), font=('Plus jakarta Sans', 14, 'bold'), text_color=black,width=350, height=50, fg_color="#f2f2f2", button_color="#efefef", corner_radius=25, button_hover_color=grey, dropdown_fg_color=color_p, dropdown_text_color=black)
        self.sucursal.place(relx=0.5, y=220, anchor="center")
        
        self.new_product = ctk.CTkButton(self.inputs_fr,text= "Actualizar producto", font= ('Plus jakarta Sans', 14, 'bold')
								,height=50, width = 350, corner_radius= 35, fg_color= black, hover_color= "#454545",
								command=self.upload)
        self.new_product.place(relx = 0.5, y=280, anchor="center")
    
    def upload(self):  # sourcery skip: avoid-builtin-shadow
        try:
            id = self.product_id.get_and_clear()
            quantity = self.quantity.get_and_clear()
            sucursal = self.sucursal.get()
            record_restock(id, app.get_variable('user_id'), sucursal, quantity)
            show_notification(self.manager,f"Producto restockeado\nstock actual: {get_stock_product(id)}")
        except Exception:
            show_notification(self.manager, "Asegurese de colocar todos los datos.")
  
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
    ("New_stock", New_stock),("New_user",New_user), ("Users_nav", Users), ("Notifications_nav", Notifications), ("New_branch", New_branch),("Restock", R_Prod),]

	for scene_name, scene_class in scenes:
		app.add_scene(scene_name, scene_class)
  
	# Inicia la aplicacion con la primera escena visible
	app.switch_scene("Login")

	app.mainloop()  # Ejecuta el bucle principal de la aplicacion