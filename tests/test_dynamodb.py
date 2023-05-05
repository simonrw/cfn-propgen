from cfn_propgen import gen_service

def test_generate_minimal_service():
    template = gen_service.for_type("AWS::DynamoDB::Table")

    assert set(template["Properties"].keys()) == set(["KeySchema"])
