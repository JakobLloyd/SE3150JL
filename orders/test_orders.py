from orders import Order

def describe_orders():
    def describe_place_order():
        def test_place_order_returns_true_when_warehouse_deduct_amt_returns_true(mocker):
            warehouse = mocker.Mock()
            warehouse.deduct_amt.return_value = True
            order = Order(warehouse)

            result = order.place_order("flashlight", 2)

            assert result is True
            warehouse.deduct_amt.assert_called_once_with("flashlight", 2)

        #in class
        def order_calls_warehouse(mocker):
            warehouse = mocker.Mock()
            order = Order(warehouse)

            mock_deduct = mocker.patch.object(order, 'deduct_amt', return_value=True)

            order.place_order("flashlight", 2)

            mock_deduct.assert_called_once()
        #all test should pass
