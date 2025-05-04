from typing import Generic, TypeVar
from abc import ABC, abstractmethod

Model = TypeVar('Model')

class BaseController(ABC, Generic[Model]):
  @abstractmethod
  def get_all(self) -> list[Model]:
    pass

  @abstractmethod
  def get_by_id(self, id: int) -> Model:
    pass

  @abstractmethod
  def delete_by_id(self, id: int) -> None:
    pass

  @abstractmethod
  # TODO: find a way to type the data
  def update_by_id(self, id: int, *data) -> None:
    pass

  @abstractmethod
  def create(self, data: Model) -> int:
    pass
