from Utils.database import *
# Crea la base de datos y las tablas
create_database()

register_user('John Doe', 'john@example.com', 'password123', 1, 1)
register_user('Jane Smith', 'jane@example.com', 'admin456', 2, 2)
register_user('Carlos Torres', 'carlos@example.com', 'superadmin789', 3, 3)

product1 = Product('White T-shirt', 19.99, 'Brand X', 'M', None, 'White cotton t-shirt', "Un local", image_path='image1.jpg', stock=10)
product2 = Product('Blue Jeans', 39.99, 'Brand Y', 'L', None, 'Blue denim jeans', "dos", image_path='image1.jpg', stock=12)

add_product(product1)
add_product(product2)

user_id = get_user_id('john@example.com')
record_sale(1, user_id, 1, 2)  
user_id = get_user_id('jane@example.com')
record_restock(3, user_id, 2, 10) 

print(get_user_details(get_user_id('john@example.com')))

products_in_stock = get_products_in_stock()
for product in products_in_stock:
    print(f"Product: {product.name}, Price: {product.price}, Brand: {product.brand}, Size: {product.size}, Description: {product.description}, id:{product.id}")
