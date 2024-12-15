from duck_ai.enums import ModelType

class History():

    def __init__(self, model: ModelType) -> None:
        self.model = model

    
    def add_message(self):
        raise NotImplementedError
    
    
    def _save_storage(self) -> None:
        raise NotImplementedError
    
    
    def _clear_storage(self) -> None:
        raise NotImplementedError
    