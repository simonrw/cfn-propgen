# cfn-propgen

Generate a "valid"[^1] CloudFormation resource (in yaml or json) for scaffolding mostly.

## Implementation

We ~steal~borrow the resource generation from the [cloudformation CLI](https://github.com/aws-cloudformation/cloudformation-cli/blob/e615ac892d311fe77a07a333a923364d5d4d5151/src/rpdk/core/contract/resource_generator.py#L56), which in turn uses Hypothesis to generate random values from a given set.

## Contributing

Set up your developer environment. If on nix, this is easy: `nix develop`. Otherwise:

```
python -m venv ./venv
source ./venv/bin/activate
pip install -r *requirements.txt
pip install -e .

# Then test
pytest
```


[^1]: the types are correct, and all required keys are present, but the values may not pass some validations, e.g. min length or letter case.

