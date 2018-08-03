import boto3
import decimal
dynamodb = boto3.resource('dynamodb')


def transform_node(node_data, format_from, format_to):
    for key in node_data.keys():
        if type(node_data[key]) == format_from:
            node_data[key] = format_to(node_data[key])
        elif type(node_data[key]) == dict:
            node_data[key] = _transform_data_types(
                node_data[key], format_from, format_to)
    return node_data


def _transform_data_types(data, format_from, format_to):
    if type(data) == list:
        data_total = []
        for ele in data:
            data_total.append(transform_node(ele, format_from, format_to))
    else:
        data_total = transform_node(data, format_from, format_to)
    return data_total


def json_decimal_to_float(data):
    """ convert all decimal.Decimal numbers in the json root to float
    """
    return _transform_data_types(data, format_from=decimal.Decimal, format_to=float)


def json_float_to_decimal(data):
    """ convert all float numbers in the json root to decimal.Decimal
    """
    return _transform_data_types(data, format_from=float, format_to=decimal.Decimal)


class ExceptionInvalidDynamoControllerType(Exception):
    """ Dynamo Type Not defined, this is a programming error """
    pass


class ExceptionInvalidDynamoControllerNotFound(Exception):
    """ Object not found in DB (404 error) """
    pass


class DynamoController(object):
    """ Generic Dynamo Access Controller
        - Error handling
        - response message/data normalization
    """

    TYPE_GET = "get"
    TYPE_CREATE = "create"
    TYPE_UPDATE = "update"
    TYPE_DELETE = "delete"

    def __init__(self, table_name, filter_by_username=True):
        """ Initialize Dynamo Controller

        Arguments:
            table_name {str} -- Dynamo table name
            filter_by_username {bool} -- If true, this controller will filter and validate username in session with handled records.
        """
        self.table = dynamodb.Table(table_name)
        self.filter_by_username = filter_by_username

    def get(self, primary_keys):
        """ return a the first element corresponding to the filter_data param """
        res = self._execute_operation(
            type=self.TYPE_GET, primary_keys=primary_keys)
        return res, res["status"]

    def create(self, data):
        """ Creates a new instance in the DB.
            - Overrides by primary key)
            - Returns the new/updated element
        """
        res = self._execute_operation(type=self.TYPE_CREATE, data=data)
        return res, res["status"]

    def update(self, primary_keys, data):
        """ Update an existing object in the database
            - Returns the updated object
        """
        res = self._execute_operation(
            type=self.TYPE_GET, primary_keys=primary_keys)
        if res["status"] != 200:
            return res
        res = self._execute_operation(
            type=self.TYPE_UPDATE, primary_keys=primary_keys, data=data)
        return res, res["status"]

    def delete(self, primary_keys):
        """ Deletes a set of objects, corresponding to filter_data
            - Delete the specific element
        """
        res = self._execute_operation(
            type=self.TYPE_GET, primary_keys=primary_keys)
        if res["status"] != 200:
            return res
        res = self._execute_operation(
            type=self.TYPE_DELETE, primary_keys=primary_keys)
        return res, res["status"]

    def _execute_operation(self, type, primary_keys=None, data=None):
        """ Execute the dynamo operation and return a proper response (success or error)
        """
        try:
            if type == self.TYPE_GET:
                d_res = self.table.get_item(Key=primary_keys)
                if "Item" in d_res:
                    data = d_res["Item"]
                else:
                    raise ExceptionInvalidDynamoControllerNotFound("Not Found")
                return self._transform_success_response(d_res, "Fetched", data)
            elif type == self.TYPE_CREATE:
                data = json_float_to_decimal(data)
                d_res = self.table.put_item(Item=data)
                return self._transform_success_response(d_res, "Created", data)
            elif type == self.TYPE_UPDATE:
                data = json_float_to_decimal(data)
                data.update(primary_keys)
                d_res = self.table.put_item(Item=data)
                return self._transform_success_response(d_res, "Updated", data)
            elif type == self.TYPE_DELETE:
                d_res = self.table.delete_item(Key=primary_keys)
                return self._transform_success_response(d_res, "Deleted", primary_keys)
            else:
                raise ExceptionInvalidDynamoControllerType(
                    "Type {} not defined in DynamoController".format(type))
        except ExceptionInvalidDynamoControllerType as e:
            return self._transform_error_response(e, code=500, message="Type not defined in controller")
        except ExceptionInvalidDynamoControllerNotFound as e:
            return self._transform_error_response(e, code=404, message="Element Not Found")
        except Exception as e:
            raise e
            return self._transform_error_response(e, code=500, message="Unexpected error")

    def _transform_success_response(self, response, message, data):
        data = json_decimal_to_float(data)
        return {
            "status": response['ResponseMetadata']['HTTPStatusCode'],
            "message": message,
            "results": data,
            #"raw_response": response
        }

    def _transform_error_response(self, e, code, message):
        return {
            "status": code,
            "message": message,
            "detail": str(e),
        }
