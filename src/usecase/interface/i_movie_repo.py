
from abc import ABC, abstractmethod

class IMovieRepo(ABC):
    @abstractmethod
    def exists(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """

    @abstractmethod
    def create_table(self):
        """_summary_
        """
    
    @abstractmethod
    def list_tables(self):
        """_summary_
        """

    @abstractmethod
    def add_movie(self, title, year, plot, rating):
        """_summary_

        Args:
            title (_type_): _description_
            year (_type_): _description_
            plot (_type_): _description_
            rating (_type_): _description_
        """
        raise NotImplementedError

    @abstractmethod
    def get_movie(self, title, year):
        """_summary_

        Args:
            title (_type_): _description_
            year (_type_): _description_
        """

    @abstractmethod
    def update_movie(self, title, year, rating, plot):
        """_summary_

        Args:
            title (_type_): _description_
            year (_type_): _description_
            rating (_type_): _description_
            plot (_type_): _description_
        """
        raise NotImplementedError

    @abstractmethod
    def query_movies(
        self,
        year,
    ):
        """_summary_

        Args:
            year (_type_): _description_
        """

    @abstractmethod
    def list_movie(self):
        """_summary_

        Raises:
            NotImplementedError: _description_
        """

    @abstractmethod
    def delete_movie(self, title, year):
        """_summary_

        Args:
            title (_type_): _description_
            year (_type_): _description_
        """
        raise NotImplementedError