class VideoInformation:
    def __init__(self) -> None:
        self.summary = ""

    def add(self, text: str) -> None:
        print(text)
        self.summary += text
        self.summary += "\n"

    def __str__(self) -> str:
        return self.summary
