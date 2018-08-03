import factory

from tests.models import ExampleModel


class ExampleModelFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('word')
    field1 = factory.Faker('word')

    class Meta:
        model = ExampleModel
