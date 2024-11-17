from injector import Injector, inject
from .aws_cognito import AWS_Cognito


class DependencyInjector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DependencyInjector, cls).__new__
            # cls._instance._initialize()
        return cls._instance

    # def _initialize(self):
    #     self.di = Injector([])

    async def update_injector(self, _class):
        self.di = Injector([_class])

    @inject
    def get_class(self, _class):
        return self.di.get(_class)


di_injector = DependencyInjector()


def get_aws_cognito() -> AWS_Cognito:
    return AWS_Cognito()
