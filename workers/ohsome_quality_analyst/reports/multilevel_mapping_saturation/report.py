from geojson import Feature

from ohsome_quality_analyst.definitions import get_attribution
from ohsome_quality_analyst.reports.base import BaseReport, IndicatorTopic


class MultilevelMappingSaturation(BaseReport):
    def __init__(
        self,
        feature: Feature,
        blocking_red: bool = None,
        blocking_undefined: bool = None,
    ):
        super().__init__(
            indicator_topic=(
                IndicatorTopic("mapping-saturation", "infrastructure_lines"),
                IndicatorTopic("mapping-saturation", "poi"),
                IndicatorTopic("mapping-saturation", "lulc"),
                IndicatorTopic("mapping-saturation", "building_count"),
            ),
            feature=feature,
            blocking_red=blocking_red,
            blocking_undefined=blocking_undefined,
        )

    def combine_indicators(self) -> None:
        super().combine_indicators()

    @classmethod
    def attribution(cls) -> str:
        return get_attribution(["OSM"])
