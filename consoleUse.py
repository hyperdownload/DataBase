from Utils import database
# Crea la base de datos y las tablas
database.create_database()

# Ejemplo de registro
database.register_user('John Doe', 'john@example.com', 'password123', 1, 1)
database.register_user('Jane Smith', 'jane@example.com', 'admin456', 2, 2)
database.register_user('Carlos Torres', 'carlos@example.com', 'superadmin789', 3, 3)

# Subida de productos ejemplo
product1 = database.Product('White T-shirt', 19.99, 'Brand X', 'M', 'image1.jpg', 'White cotton t-shirt', 1)
product2 = database.Product('Blue Jeans', 39.99, 'Brand Y', 'L', 'image1.jpg', 'Blue denim jeans', 2)

database.add_product(product1)
database.add_product(product2)

# Ejemplo de guardar y restockear productos
user_id = database.get_user_id('john@example.com')
database.record_sale(1, user_id, 1, 2)  
user_id = database.get_user_id('jane@example.com')
database.record_restock(2, user_id, 2, 10)  
menu=["0-Salir", "1-Cargar producto"]
for text in menu:
    print(text)
input = input("ingresar opcion:")
while input != 0: