from . import BaseEndpointTestCase


class MessageEndpointTestCase(BaseEndpointTestCase):
    def test_message_get(self):
        self.client._credentials = (
            '2zSiihsjuX5Eas6wv9kFAellKJk3CvS3xqcz7Uim',
            'uJJaW9AcwJhkKHXH6b9XkwWpYGwz6DrS7lALOzuh8NmRn0HUwqUMVmjwZXMn9BTFxy3WNNjk9GROYJ5efPmmvV3l99JsazvMILHJPKm0vC3obWXtr9yKIbmtAh7czhXG'
        )
        template = self.client.Templates.get('new_requisition_default')
        message = self.client.Messages.create({
            'fromEmail': 'yo@yo.com',
            'fromName': 'Yo',
            'to': 'raulgranadosr@gmail.com',
            'data': {
                'fromName': 'Max Llantas',
                'kind': 'NEW_REQUISITION',
                'object': {
                    'assignedName': 'Daniel',
                    'code': '1602',
                    'createdAt': '2017-05-25T15:59:51.627582Z',
                    'createdByName': 'Juan Pablo',
                    'items': [
                        {
                            'code': '3333',
                            'id': 3333,
                            'name': 'CAMARA POWER KING 1100 R22 TR78A',
                            'price': '553.31',
                            'qty': 2,
                            'unit': 'PZA',
                        }
                    ],
                    'kind': 'incoming',
                    'metadata': {
                        'comment': 'POR COMPRA A TBC\nFACTURA 3539109'
                    },
                    'status': 1,
                    'statusName': 'Iniciada',
                    'totalCost': '518.73',
                    'totalPrice': '553.31',
                    'totalProduction': '345.82',
                    'updatedAt': '2017-05-25T15:59:51.627686Z',
                },
            },
            'template': template.id,
            'subject': 'Nueva requisición'
        })

        print(message.id)
