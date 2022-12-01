import pandas as pd


class Export:
    def __init__(self, data: pd.DataFrame) -> None:
        self.df = data.transpose()

    def use_template_sort(self, template: str, multiply: float = 1.0, precision: int = 0) -> None:
        self.df = round(multiply * self.df.reindex(template), precision)

