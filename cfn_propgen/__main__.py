import argparse
from typing import IO, Literal
import json

import yaml

from cfn_propgen import gen_service


class JsonFormatter:
    def dump(self, obj: dict, outfile: IO):
        json.dump(obj, outfile, indent=2)


class YamlFormatter:
    def dump(self, obj: dict, outfile: IO):
        yaml.safe_dump(obj, outfile)


class FormatterFactory:
    @staticmethod
    def for_format(format: Literal["yaml", "json"]) -> JsonFormatter | YamlFormatter:
        if format == "yaml":
            cls = YamlFormatter
        elif format == "json":
            cls = JsonFormatter
        else:
            raise ValueError(f"Invalid format {format}")

        return cls()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("resource_type", help="CloudFormation type name")
    parser.add_argument(
        "-f", "--format", choices=["json", "yaml"], default="yaml", help="Output format"
    )
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        default="-",
        type=argparse.FileType("w"),
        help="File to output to (default: stdout)",
    )
    args = parser.parse_args()

    definition = gen_service.for_type(args.resource_type)

    FormatterFactory.for_format(args.format).dump(definition, args.output)
