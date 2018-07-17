from pypolisen.Client import Client


client = Client()


def test_get_suggestions():
    suggestions = client.get_suggestions('g')

    assert isinstance(suggestions, list)
    assert len(suggestions) > 0


def test_suggestions():
    suggestions = client.get_suggestions('g')

    for sugg in suggestions:
        assert 'Text' in sugg
        assert 'Value' in sugg
