from injector import inject, singleton
from logging import getLogger

from domain.entity.movie import Movie
from usecase import Usecase
from usecase.interface.i_movie_repo import IMovieRepo


LOGGER = getLogger(__name__)

@singleton
class GetMovieDetailUsecase(Usecase):

    @inject
    def __init__(
        self,
        movie_repo: IMovieRepo
    ):
        self.__movie_repo = movie_repo

    def execute(self, year: int, title: str):
        table_exists = self.__movie_repo.exists()
        if not table_exists:
            self.__movie_repo.create_table()
        result = self.__movie_repo.get_movie(year, title)
        if result is None:
            return None
        
        movie = Movie.to_dict(result)

        return movie