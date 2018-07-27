from decimal import Decimal
from six.moves.urllib.parse import urlparse, parse_qs
import eopayment

def test_tipi():
    p = eopayment.Payment('tipi', {'numcli': '12345'})
    payment_id, kind, url = p.request(amount=Decimal('123.12'),
            exer=9999,
            refdet=999900000000999999,
            objet='tout a fait',
            email='info@entrouvert.com',
            urlcl='http://example.com/tipi/test',
            saisie='T')
    parsed_qs = parse_qs(urlparse(url).query)
    assert parsed_qs['objet'][0].startswith('tout a fait ')
    assert parsed_qs['montant'] == ['12312']
    assert parsed_qs['saisie'] == ['T']
    assert parsed_qs['mel'] == ['info@entrouvert.com']
    assert parsed_qs['numcli'] == ['12345']
    assert parsed_qs['exer'] == ['9999']
    assert parsed_qs['refdet'] == ['999900000000999999']

    response = p.response('objet=tout+a+fait&montant=12312&saisie=T&mel=info%40entrouvert.com&numcli=12345&exer=9999&refdet=999900000000999999&resultrans=P')
    assert response.signed  # ...
    assert response.result == eopayment.PAID
