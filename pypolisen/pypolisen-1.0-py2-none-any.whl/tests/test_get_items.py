from pypolisen.Client import Client


client = Client()


def test_get_items():
    items = client.get_items(69)

    assert isinstance(items, list)
    assert len(items) > 0


def test_items():
    items = client.get_items(69)

    for item in items:
        assert 'HasImage' in item
        assert 'Headline' in item
        assert 'Preamble' in item
        assert 'PublishedDate' in item
        assert 'Url' in item
        assert 'ListItemType' in item
        assert 'ImageUrl' in item
        assert 'ImageDescription' in item
        assert 'HasTeaserText' in item
