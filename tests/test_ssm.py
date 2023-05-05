from cfn_propgen import gen_service

def test_generate_minimal_service():
    definition = gen_service.ssm()

    assert definition["Type"] == "AWS::SSM::Parameter"
    assert set(definition["Properties"].keys()) == set(["Type", "Name"])