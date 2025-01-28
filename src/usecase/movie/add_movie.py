from injector import inject, singleton
from logging import getLogger

from domain.entity.movie import MovieForm, Movie, MovieInfo
from usecase import Usecase
from usecase.interface.i_movie_repo import IMovieRepo


LOGGER = getLogger(__name__)

@singleton
class AddMovieListUsecase(Usecase):

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
        movie_info: MovieInfo = MovieInfo(
            plot=body.plot,
            rating=body.rating
        )
        movie: Movie = Movie(
            year=body.year,
            title=body.title,
            info=movie_info
        )
        return self.__movie_repo.add_movie(movie)