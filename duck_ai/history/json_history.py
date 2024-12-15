from pathlib import Path

from pydantic_core import ValidationError

from .history import History
from duck_ai.models import ModelType, Message, Data, HistoryModel


class JsonHistory(History):

    def __init__(self,
                 path_file: str,
                 model: ModelType = ModelType.GPT4o, 
        ) -> None:
        super().__init__(model)
        self.path_file = path_file

        try:
            with open(self.path_file, 'r') as file:
                self.data = HistoryModel.model_validate_json(file.read())
        except ValidationError as e:
            self._create_storage()
            self.data = HistoryModel(model=model, messages=[], vqd='1')
            self._save_storage()


    @property
    def vqd(self) -> str:
        return self.data.vqd
    
    
    @vqd.setter
    def vqd(self, new_vqd: str) -> None:
        self.data.vqd = new_vqd
        self._save_storage()


    @vqd.getter
    def vqd(self) -> str:
        return self.data.vqd


    def _check_storage(self) -> bool:
        file_path = Path(self.path_file)
        return file_path.is_file()
    

    def _create_storage(self) -> None:
        file_path = Path(self.path_file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()


    def add_message(self, message: Message) -> None:
        self.data.messages.append(message)
        self._save_storage()


    def get_data_json(self) -> Data:
        with open(self.path_file, 'r') as file:
            return Data.model_validate_json(file.read()).model_dump_json()
        

    def _save_storage(self) -> None:
        with open(self.path_file, 'w') as file:
            file.write(self.data.model_dump_json(indent=4))

    
    def _clear_storage(self, path_file: str) -> None:
        with open(path_file, 'w') as file:
            file.write('')
