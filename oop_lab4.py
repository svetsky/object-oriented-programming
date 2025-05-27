from abc import ABC, abstractmethod

# region property changed listeners (логгер)
class IPropertyChangedListener(ABC):
    @abstractmethod
    def on_property_changed(self, obj, property_name):
        pass

# Примеры слушателей
class PropertyChangeLogger(IPropertyChangedListener):
    def on_property_changed(self, obj, property_name):
        print(f"[Изменение] Свойство '{property_name}' изменено на '{getattr(obj, property_name)}'")
# endregion

# region property changing listeners (слушатели валидации изменений свойства)
class IPropertyChangingListener(ABC):
    @abstractmethod
    def on_property_changing(self, obj, property_name, old_value, new_value):
        pass

class AgeValidator(IPropertyChangingListener):
    def on_property_changing(self, obj, property_name, old_value, new_value):
        if property_name == 'age':
            if not isinstance(new_value, int):
                print("[Ошибка] Возраст должен быть целым числом")
                return False
            if new_value < 0:
                print("[Ошибка] Возраст не может быть отрицательным")
                return False
            if new_value > 120:
                print("[Ошибка] Возраст не может быть больше 120")
                return False
        return True

class NameValidator(IPropertyChangingListener):
    def on_property_changing(self, obj, property_name, old_value, new_value):
        if property_name == 'name':
            if not isinstance(new_value, str):
                print("[Ошибка] Имя должно быть строкой")
                return False
            if len(new_value) < 2:
                print("[Ошибка] Имя должно содержать хотя бы 2 символа")
                return False
            if not new_value.replace(" ", "").isalpha():
                print("[Ошибка] Имя должно содержать только буквы и пробелы")
                return False
        return True
# endregion

# region notify data change
class INotifyDataChanged(ABC):
    @abstractmethod
    def add_property_changed_listener(self, listener):
        pass
    
    @abstractmethod
    def remove_property_changed_listener(self, listener):
        pass

# Базовый класс с уведомлениями об изменениях
class NotifyDataChanged(INotifyDataChanged):
    def __init__(self):
        self._listeners = []
    
    def add_property_changed_listener(self, listener: IPropertyChangedListener):
        if listener not in self._listeners:
            self._listeners.append(listener)
    
    def remove_property_changed_listener(self, listener: IPropertyChangedListener):
        if listener in self._listeners:
            self._listeners.remove(listener)
    
    def _notify_property_changed(self, property_name):
        for listener in self._listeners:
            listener.on_property_changed(self, property_name)

class INotifyDataChanging(ABC):
    @abstractmethod
    def add_property_changing_listener(self, listener):
        pass
    
    @abstractmethod
    def remove_property_changing_listener(self, listener):
        pass

# Базовый класс с валидацией изменений
class NotifyDataChanging(NotifyDataChanged, INotifyDataChanging):
    def __init__(self):
        super().__init__()
        self._changing_listeners = []
    
    def add_property_changing_listener(self, listener: IPropertyChangingListener):
        if listener not in self._changing_listeners:
            self._changing_listeners.append(listener)
    
    def remove_property_changing_listener(self, listener: IPropertyChangingListener):
        if listener in self._changing_listeners:
            self._changing_listeners.remove(listener)
    
    def _validate_property_change(self, property_name, old_value, new_value):
        for listener in self._changing_listeners:
            if not listener.on_property_changing(self, property_name, old_value, new_value):
                return False
        return True
# endregion

# Пример класса с отслеживаемыми свойствами
class Person(NotifyDataChanging):      
    def __init__(self, name: str, age: int):
        super().__init__()
        self._name = name
        self._age = age
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if self._validate_property_change('name', self._name, value):
            self._name = value
            self._notify_property_changed('name')
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if self._validate_property_change('age', self._age, value):
            self._age = value
            self._notify_property_changed('age')

# Демонстрация работы
if __name__ == "__main__":
    print("Создаем объект Person('Анна', 25)")
    person = Person("Анна", 25)
    
    print("\nРегистрируем слушатели и валидаторы...")
    logger = PropertyChangeLogger()
    age_validator = AgeValidator()
    name_validator = NameValidator()
    
    person.add_property_changed_listener(logger)
    person.add_property_changing_listener(age_validator)
    person.add_property_changing_listener(name_validator)
    
    print("\nПытаемся изменить имя на 'Мария'")
    person.name = "Мария"
    
    print("\nПытаемся изменить имя на 'Я' (слишком короткое)")
    person.name = "Я"
    
    print("\nПытаемся изменить имя на '123' (не буквы)")
    person.name = "123"
    
    print("\nПытаемся изменить возраст на 30")
    person.age = 30
    
    print("\nПытаемся изменить возраст на -5 (отрицательный)")
    person.age = -5
    
    print("\nПытаемся изменить возраст на 150 (слишком большой)")
    person.age = 150
    
    print("\nПытаемся изменить возраст на 'тридцать' (не число)")
    try:
        person.age = "тридцать"
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    
    print("\nТекущие значения свойств:")
    print(f"Имя: {person.name}")
    print(f"Возраст: {person.age}")