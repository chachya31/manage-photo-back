from injector import inject, singleton
from logging import getLogger

from domain.entity.movie import MovieForm, Movie, MovieInfo
from usecase import Usecase
from usecase.interface.i_movie_repo import IMovieRepo


LOGGER = getLogger(__name__)

@singleton
class AddMovieUsecase(Usecase):

    @inject
    def __init__(
        self,
        movie_repo: IMovieRepo
    ):
        self.__movie_repo = movie_repo

    def execute(self, body: MovieForm):
        table_exists = self.__movie_repo.exists()
        if not table_exists:
            self.__movie_repo.create_table()
        return self.__movie_repo.update_movie(body)