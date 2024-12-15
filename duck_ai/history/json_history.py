from pathlib import Path

from .history import History
from duck_ai.models import ModelType, Message, Data, HistoryModel

# TODO Дописать init
# TODO Добавить обработку ошибок

class JsonHistory(History):

    def __init__(self,
                 path_file: str,
                 model: ModelType = ModelType.GPT4o, 
        ) -> None:
        super().__init__(model)
        self.path_file = path_file

        if self.check_storage():
            with open(self.path_file, 'r') as file:
                # try:
                self.data = HistoryModel.model_validate_json(file.read())
                # except Exception as e:
                #     print(e)
        else:
            self.create_storage()
            self.data = HistoryModel(model=model, messages=[], vqd='1')
            self.save_storage()


    def check_storage(self) -> bool:
        file_path = Path(self.path_file)
        return file_path.is_file()
    
    def create_storage(self) -> None:
        file_path = Path(self.path_file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()


    def add_message(self, message: Message) -> None:
        self.data.messages.append(message)
        self.save_storage()


    def get_data_json(self) -> Data:
        with open(self.path_file, 'r') as file:
            return Data.model_validate_json(file.read()).model_dump_json()
        

    def save_storage(self) -> None:
        with open(self.path_file, 'w') as file:
            file.write(self.data.model_dump_json(indent=4))

    
    def clear_storage(self, path_file: str) -> None:
        with open(path_file, 'w') as file:
            file.write('')
