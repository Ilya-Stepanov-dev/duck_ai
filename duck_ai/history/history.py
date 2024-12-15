from duck_ai.models import Data, Message, Role, ModelType

# TODO доделать класс Histoty. Сделать его универсальным

class History():

    def __init__(self, model: ModelType) -> None:
        self.model = model
    
    def add_message(self):
        raise NotImplementedError
    
    def save_storage(self) -> None:
        raise NotImplementedError
    

    def load_storage(self) -> None:
        raise NotImplementedError
    

    def clear_storage(self) -> None:
        raise NotImplementedError
    