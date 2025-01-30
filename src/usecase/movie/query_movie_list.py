from injector import inject, singleton
from logging import getLogger

from domain.entity.movie import Movie
from usecase import Usecase
from usecase.interface.i_movie_repo import IMovieRepo


LOGGER = getLogger(__name__)

@singleton
class QueryMovieListUsecase(Usecase):

    @inject
    def __init__(
        self,
        movie_repo: IMovieRepo
    ):
        self.__movie_repo = movie_repo

    def execute(self, year):
        table_exists = self.__movie_repo.exists()
        if not table_exists:
            self.__movie_repo.create_table()
        list = self.__movie_repo.query_movies(year)
        movie_list = []
        for result in list:
            movie = Movie.to_dict(result)
            movie_list.append(movie)

        return movie_list