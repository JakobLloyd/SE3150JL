class Warehouse:
	def __init__(self):
		self.prod_list = {}
	
	def add_product(self,product,count):
		self.prod_list[product] = count

	def add_amt(self, product, qty):
		self.prod_list[product] += qty

	def deduct_amt(self, product,qty):
		if qty  > self.prod_list[product]:
			return False
		self.prod_list[product] -= qty 
		return True

	def get_inventory(self,product):
		return self.prod_list[product]


class Order:
	def __init__(self, warehouse_in):
			self.warehouse = warehouse_in

	def place_order(self,product, qty):
		
		result = self.warehouse.deduct_amt(product, qty)
		if result:
			print(f"Order: {qty} {product} succeeded.")
			return True
		else:
			print(f"Order: {qty} {product} failed - low stock.")
			return False



