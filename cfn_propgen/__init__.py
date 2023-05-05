from . import services


class Generator:
    def sns(self) -> dict:
        return services.sns.generate()

    def ssm(self) -> dict:
        return services.ssm.generate()

gen_service = Generator()
