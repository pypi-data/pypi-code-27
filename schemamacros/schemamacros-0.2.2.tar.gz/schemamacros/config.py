import typing
import attr
from attr import validators as v
import yaml
import os


@attr.s(repr=False)
class TemplateDir(str):

    def __repr__(self):
        return self.path

    def __str__(self):
        return self.__repr__()

    path: str = attr.ib()

    @path.validator
    def check(self, attribute, value):
        if not os.path.isdir(value):
            raise ValueError("The path %s is not a directory", value)



@attr.s
class TargetConfig(object):
    schema_template: str = attr.ib(validator=v.instance_of(str))
    transaction: bool = attr.ib(
        validator=v.instance_of(bool),
        default=False
    )
    variables: typing.Mapping[str, str] = attr.ib(default={})


@attr.s
class ConfigInternal(object):
    template_directories: typing.List[TemplateDir] = attr.ib(
        validator=v.instance_of(list),
        convert=lambda x: list(map(TemplateDir, x)),
        default=[]
    )

    template_packages: typing.List[str] = attr.ib(default=list())
    variables: typing.Mapping[str, str] = attr.ib(default=dict())

    targets: typing.Mapping[str, TargetConfig] = attr.ib(default=dict())


@attr.s
class ConfigfileVersion1(object):
    version: str = attr.ib(validator=v.in_(["1", "1.0"]))

    schema_template: str = attr.ib(validator=v.instance_of(str))

    output: str = attr.ib(validator=attr.validators.instance_of(str))

    template_directories: typing.List[TemplateDir] = attr.ib(
        validator=v.instance_of(list)
    )

    template_packages: typing.List[str] = attr.ib(default=list())

    transaction: bool = attr.ib(
        validator=v.instance_of(bool),
        default=False
    )

    variables: typing.Mapping[str, str] = attr.ib(default=dict())

    def extract(self) -> ConfigInternal:
        target_config = TargetConfig(
            transaction=self.transaction,
            schema_template=self.schema_template,
            variables={}
        )
        config = ConfigInternal(
            template_directories=self.template_directories,
            template_packages=self.template_packages,
            variables=self.variables,
            targets={self.output: target_config}
        )
        return config


@attr.s
class ConfigfileVersion12(object):
    version: str = attr.ib(validator=v.in_(["1.2", "1.1"]))
    template_directories: typing.List[TemplateDir] = attr.ib(
        validator=v.instance_of(list),
        default=[]
    )

    template_packages: typing.List[str] = attr.ib(default=list())
    variables: typing.Mapping[str, str] = attr.ib(default=dict())
    targets: typing.Mapping[str, TargetConfig] = attr.ib(default=dict())

    def extract(self) -> ConfigInternal:
        config = ConfigInternal(
            template_directories=self.template_directories,
            template_packages=self.template_packages,
            variables=self.variables,
            targets={t: TargetConfig(**v)
                     for t, v in self.targets.items()}
        )
        return config


CONFIG_FILE_VERSIONS = {
    "1": ConfigfileVersion1,
    "1.0": ConfigfileVersion1,
    "1.1": ConfigfileVersion12,
    "1.2": ConfigfileVersion12
}


def build_config_inner(config_dict) -> ConfigInternal:
    if "version" not in config_dict:
        raise ValueError("Config does not have a version")

    version = str(config_dict["version"])

    if version not in CONFIG_FILE_VERSIONS:
        raise ValueError("Version %s is not supported", version)

    versioned_config = CONFIG_FILE_VERSIONS[version](**config_dict)

    return versioned_config.extract()


def yaml_load(yaml_text):
    return build_config_inner(yaml.load(yaml_text))
