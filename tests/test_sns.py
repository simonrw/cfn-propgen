from cfn_propgen import gen_service

def test_generate_minimal_service():
    definition = gen_service.sns()

    assert definition["Type"] == "AWS::SNS::Topic"
    assert list(definition["Properties"].keys()) == []