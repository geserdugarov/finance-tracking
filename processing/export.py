import pandas as pd


class Export:
    def __init__(self, data: pd.DataFrame) -> None:
        self.df = data.transpose()

    def use_template_sort(self, template: str) -> None:
        self.df = self.df.reindex(template)

