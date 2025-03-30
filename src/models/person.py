from abc import ABC
from datetime import datetime

class Person(ABC):
  def __init__(self, name: str, birthdate: datetime):
    self._name = name
    self._birthdate = birthdate if isinstance(birthdate, datetime) else None

  @property
  def name(self) -> str:
    return self._name

  @name.setter
  def name(self, name: str) -> None:
    self._name = name
  
  @property
  def birthdate(self) -> datetime:
    return self._birthdate

  @birthdate.setter
  def birthdate(self, birthdate: datetime) -> None:
    self._birthdate = birthdate

  @property
  def age(self) -> int:
    if self._birthdate is None: return

    today = datetime.now()

    return (today - self._birthdate).days // 365
