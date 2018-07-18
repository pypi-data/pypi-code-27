from data_access_layer import data_access_layer

# generate instance of dal
dal = data_access_layer.DataAccessLayer()

# create query
sql_query = "SELECT * FROM (SELECT new.product_id, new.name, new.available_from, sum(new.quantity) as quantity FROM " \
            "(SELECT products.*,orders.quantity FROM products inner join orders on " \
            "products.product_id=orders.product_id) new GROUP BY new.product_id, new.name, new.available_from) new2 " \
            "where new2.quantity < 10 AND CAST(new2.available_from AS DATE) < CAST('2018-06-01' AS DATE)"

data = dal.query_data(sql_query=sql_query)
print(data)
print('"' + data.name[0] + '" has only sold a total of ' + str(data.quantity[0]) + ' books')
dal.disconnect_from_database()