class Chunk:

    def __init__(self, id, text, file_name):
        self.id = id
        self.text = text
        self.file_name = file_name

    def __str__(self):
        print(f"Chunk(id={self.id},text={self.text},file_name={self.file_name})")