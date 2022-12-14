import logging
import pandas as pd
from typing import List


logger = logging.getLogger(__name__)
logger.info("Loaded %s module." % __name__)


class Export:
    """
    Class for customized data, which should be exported.
    """
    def __init__(self, data: pd.DataFrame) -> None:
        """
        Initial data processing

        Parameters
        ----------
        data: pd.DataFrame of source data for export
        """
        self.df = data.transpose()
        logger.debug("Initial processing. Data for export was transposed.")

    def use_template_sort(self, template: List[str], multiply: float = 1.0, precision: int = 0) -> None:
        """
        Sorting data categories in accordance with a template.

        Parameters
        ----------
        template:  list of strings, which represent sorting in ascending order
        multiply:  multiplier, for instance, for changing sign of expenses or conversion to thousands
        precision: number of digits after decimal point
        """
        self.df = round(multiply * self.df.reindex(template), precision)
        logger.debug("Data for export was sorted by template.")

