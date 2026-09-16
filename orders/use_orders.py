from orders import Order, Warehouse

warehouse = Warehouse()
warehouse.add_product('pocket knife', 10)
warehouse.add_product('flashlight',10)

order = Order(warehouse)

order.place_order('flashlight',10)
order.place_order('pocket knife',50)

flashlights = warehouse.get_inventory('flashlight')
knives = warehouse.get_inventory('pocket knife')

print(f"remaining stock: flashlights: {flashlights} ")
print(f"remaining stock: pocket knives: {knives} ")
