import logging
import pandas as pd
from typing import List


logger = logging.getLogger(__name__)
logger.info("Loaded %s module." % __name__)


def sort_by_template(data: pd.DataFrame, template: List[str]) -> pd.DataFrame:
    """
    Sorting data categories in accordance with a template.

    Parameters
    ----------
    template:  list of strings, which represent sorting in ascending order
    multiply:  multiplier, for instance, for changing sign of expenses or conversion to thousands
    precision: number of digits after decimal point
    """
    data = data.transpose()
    logger.debug("Initial processing. Data for export was transposed.")
    return data.reindex(template)

