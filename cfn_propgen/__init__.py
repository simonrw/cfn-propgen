from pathlib import Path
from urllib.request import urlretrieve
import json
import warnings
from zipfile import ZipFile


from . import generators


DATA_DIR = Path.home() / ".local" / "share" / "cfn-propgen"
SCHEMA_FILE = DATA_DIR.joinpath("cfn-schema.json")

REGION = "us-east-1"
ZIP_FILENAME = "CloudformationSchema.zip"
SOURCE_URL = f"https://schema.cloudformation.{REGION}.amazonaws.com/{ZIP_FILENAME}"


class Generator:
    def __init__(self, resources):
        self.resources = resources

    @classmethod
    def from_file(cls, path: Path):
        with path.open() as infile:
            return cls(json.load(infile))

    def for_type(self, type: str) -> dict:
        schema = self.resources[type]
        schema_generator = generators.ResourceGenerator(schema)
        # we ignore the warning about not using `example` in tests
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            props = schema_generator.generate_schema_strategy(schema).example()

        required_keys = schema.get("required", [])
        filtered_props = {
            key: value for (key, value) in props.items() if key in required_keys
        }
        return {"Type": type, "Properties": filtered_props}


gen_service = Generator.from_file(SCHEMA_FILE)


class SchemaFetcher:
    def __init__(self):
        self.ensure_schema()

    def ensure_schema(self):
        DATA_DIR.mkdir(exist_ok=True, parents=True)
        if not self.schema_fetched():
            self.fetch_schema()

    def schema_fetched(self) -> bool:
        return SCHEMA_FILE.is_file()

    def fetch_schema(self):
        # fetch zip file
        file_path, _ = urlretrieve(SOURCE_URL)
        # unpack zip file
        resource_definitions = {}
        # TODO: memory usage?!
        with open(file_path, "rb") as infile:
            z = ZipFile(infile)
            for name in z.namelist():
                with z.open(name) as f:
                    schema = json.load(f)

                typename = schema["typeName"]
                resource_definitions[typename] = schema

        # move to output path
        with SCHEMA_FILE.open("w") as outfile:
            json.dump(resource_definitions, outfile)


schema_fetcher = SchemaFetcher()
