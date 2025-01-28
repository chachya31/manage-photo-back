from injector import Injector, inject, Module, provider
from .aws_cognito import AWS_Cognito
from usecase import interface as i_interface
import repository as repo


class DependencyInjector():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DependencyInjector, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.di = Injector([])

    async def update_injector(self, _class):
        self.di = Injector([_class])

    @inject
    def get_class(self, _class):
        return self.di.get(_class)


di_injector = DependencyInjector()

def get_aws_cognito() -> AWS_Cognito:
    return AWS_Cognito()

class RepositoryModule(Module):
    def __init__(self) -> None:
        pass

    @provider
    def movie_repo(self) -> i_interface.IMovieRepo:
        return repo.MovieRepo()

injector = Injector([RepositoryModule()])
