import json
class JSONopener():
    '''Класс создает экземпляр JSON  и определяет метод чтения данных из файла'''
    def __init__(self, file):
        self.file = file
    def open_json(self):
        with open(self.file) as f:
            self.data = json.load(f)
        return self.data