# Configuration ORM for Python applications

![Test Status](https://github.com/onexay/py-configorm/actions/workflows/python-package.yml/badge.svg)

A python library which provides ORM like semantics to application configuration. At present, it provides the expected functionality but requires some more work in terms of error handling. 

The library works on the concept of configuration sources. Currently following sources are supported, 

1. TOML
2. JSON
3. YAML
4. DotEnv
5. Environment Variables

User defines a application settings schema by subclassing from Pydantic `BaseModel` class. User can choose one or more configuration sources to create a Pydantic object based on application configuration schema.

Library will then try to read from all provided configuration sources and merge them to build the pydantic application configuration object.

`Name of keys in configuration sources and confguration schema MUST match. It would have been nice to decouple two, but for the intended functionality, it's a minor enhancement.`

Configuration sources are provided as a list of objects and precedence and priority of sources is determined by ordering of the sources in the list, e.g. first source in the list has lowest precendence, last one has the highest.

If the configuration supports, library provides ability to save functionality for the application configuration object. By default, write capability is disabled.

| Configuration Source | Read | Read-Write |
|--|--|--|
| `TOML` | Yes | Yes |
| `JSON` | Yes | Yes |
| `YAML` | Yes | Yes |
| `DotEnv` | Yes | No |
| `Environment Variable` | Yes | Yes |

Here is an example:

```json
    {
        "Service": {
            "Host": "localhost",
            "Port": 18080
        },
    }
```

```python

class TestServiceConfig(BaseModel):
    Host: str = Field(..., description="Host running the service")
    Port: int = Field(..., description="Port bound to the service")


class TestConfig(ConfigSchema):
    Service: TestServiceConfig = Field(..., description="Service configuration")

json_source = JSONSource(file_path=Path(config_file_json))

cfg_orm = ConfigORM(schema=TestConfig, sources=[json_source])

cfg: TestConfig = cfg_orm.load_config()

print(cfg)

```