from cfn_propgen import gen_service

def test_generate_minimal_service():
    template = gen_service.for_type("AWS::SSM::Parameter")

    assert set(template["Properties"].keys()) == set(["Type", "Value"])
