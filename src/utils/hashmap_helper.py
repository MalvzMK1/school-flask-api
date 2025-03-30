class HashMap[K, V]:
  def __init__(self):
    self.__size = 0
    self.__elements: dict[K, V] = {}

  @property
  def size(self) -> int:
    return self.__size

  def add(self, key: K, value: V) -> None:
    if key not in self.__elements:
      self.__elements[key] = value

      self.__size += 1

  def remove(self, key: K) -> None:
    if key in self.__elements:
      self.__elements.pop(key)
      self.__size -= 1

  def get(self, key: K) -> V:
    return self.__elements[key] if key in self.__elements else None
  
  def to_list(self) -> list[V]:
    arr: list[V] = []

    for key in self.__elements:
      arr.append(self.__elements[key])

    return arr

  def __repr__(self):
    return self.__elements.__str__()
