"""An Indicator for testing purposes."""
from string import Template

import dateutil.parser
from geojson import Feature

from ohsome_quality_analyst.indicators.base import BaseIndicator
from ohsome_quality_analyst.ohsome import client as ohsome_client
from ohsome_quality_analyst.topics.models import BaseTopic as Topic


class Minimal(BaseIndicator):
    def __init__(self, topic: Topic, feature: Feature) -> None:
        super().__init__(topic=topic, feature=feature)
        self.count = 0

    async def preprocess(self) -> None:
        query_results = await ohsome_client.query(self.topic, self.feature)
        self.count = query_results["result"][0]["value"]
        self.result.timestamp_osm = dateutil.parser.isoparse(
            query_results["result"][0]["timestamp"]
        )

    def calculate(self) -> None:
        description = Template(self.metadata.result_description).substitute()
        self.result.value = 1.0
        self.result.description = description + self.metadata.label_description["green"]

    def create_figure(self) -> None:
        pass
