from fastapi import APIRouter, Form, status, Depends
from fastapi.security import OAuth2PasswordBearer
from injector import Injector

from core.dependencies import RepositoryModule
from domain.entity.question import Question
from domain.entity.movie import MovieForm
from usecase import Usecase
from usecase.movie.add_movie import AddMovieListUsecase
from usecase.movie.get_movie import GetMovieUsecase
from usecase.movie.get_movie_list import GetMovieListUsecase

movie_router = APIRouter(prefix="/api/v1/movie")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_injector() -> Injector:
    return Injector([
        RepositoryModule()
    ])

def get_movie_interactor(
    injector: Injector = Depends(get_injector)
):
    return injector.get(GetMovieListUsecase)

def add_movie_interactor(
    injector: Injector = Depends(get_injector)
):
    return injector.get(AddMovieListUsecase)

def get_movie_list_interactor(
    injector: Injector = Depends(get_injector)
):
    return injector.get(GetMovieListUsecase)

@movie_router.get("/query-movies", status_code=status.HTTP_200_OK, tags=["Movie"])
async def movie_list(
    year: str = Form(),
    token: str = Depends(oauth2_scheme),
    usecase: Usecase = Depends(get_movie_interactor)
):
    return usecase.execute(year)

@movie_router.get("/list", status_code=status.HTTP_200_OK, tags=["Movie"])
async def movie_list(
    token: str = Depends(oauth2_scheme),
    usecase: Usecase = Depends(get_movie_list_interactor)
):
    return usecase.execute()

@movie_router.put("/add", status_code=status.HTTP_201_CREATED, tags=["Movie"])
async def add_movie(
    form: MovieForm,
    token: str = Depends(oauth2_scheme),
    usecase: Usecase = Depends(add_movie_interactor)
):
    return usecase.execute(form)