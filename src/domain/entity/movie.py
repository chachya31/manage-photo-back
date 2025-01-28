import json

from typing import Annotated, Any
from annotated_types import MinLen, MaxLen, Ge, Le
from pydantic import BaseModel, EmailStr, Field, model_validator
from pydantic.dataclasses import dataclass

@dataclass
class MovieInfo:
    plot: str
    rating: float

@dataclass
class Movie:
    year: int
    title: str
    info: MovieInfo

    @staticmethod
    def to_dict(dict: Any) -> "Movie":
        for key, value in dict.items():
            if key == "PK":
                year = int(value.split("|")[1])
            elif key == "SK":
                title = value
            elif key == "info":
                for k, v in value.items():
                    if k == "plot":
                        plot = v
                    elif k == "rating":
                        rating = v
        movie_info = MovieInfo(plot=plot, rating=rating)
        movie = Movie(year, title, movie_info)
        return movie

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value: Any) -> Any:
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    
    def __post_init__(self):
        print(f'Second: {self.info}')

class MovieForm(BaseModel):
    year: Annotated[int, Field(ge=1972, le=2100)]
    title: Annotated[str, MaxLen(30)]
    plot: Annotated[str, MaxLen(30)]
    rating: Annotated[float, Field(ge=0, le=5)]

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value: Any) -> Any:
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value