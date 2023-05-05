from . import services


class Generator:
    def sns(self) -> dict:
        return services.sns.generate()

gen_service = Generator()
