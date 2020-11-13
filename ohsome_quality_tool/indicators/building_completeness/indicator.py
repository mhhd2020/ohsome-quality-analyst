from geojson import FeatureCollection

from ohsome_quality_tool.base.indicator import BaseIndicator
from ohsome_quality_tool.utils.definitions import logger


class Indicator(BaseIndicator):
    """The Building Completeness Indicator."""

    name = "Building Completeness"

    def __init__(
        self,
        dynamic: bool,
        bpolys: FeatureCollection = None,
        table: str = None,
        feature_id: int = None,
    ) -> None:
        super().__init__(
            dynamic=dynamic, bpolys=bpolys, table=table, feature_id=feature_id
        )

    def preprocess(self):
        logger.info(f"run preprocessing for {self.name} indicator")

    def calculate(self):
        logger.info(f"run calculation for {self.name} indicator")
        self.results["score"] = 0.5

    def export_figures(self):
        # TODO: maybe not all indicators will export figures?
        logger.info(f"export figures for {self.name} indicator")
