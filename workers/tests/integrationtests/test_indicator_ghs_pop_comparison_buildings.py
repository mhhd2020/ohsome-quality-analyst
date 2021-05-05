import asyncio
import os
import unittest

import geojson
from asyncpg import Record

from ohsome_quality_analyst.indicators.ghs_pop_comparison_buildings.indicator import (
    GhsPopComparisonBuildings,
)

from .utils import oqt_vcr


class TestIndicatorGhsPopComparisonBuildings(unittest.TestCase):
    def setUp(self):
        infile = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "fixtures",
            "heidelberg_altstadt.geojson",
        )
        with open(infile, "r") as f:
            bpolys = geojson.load(f)
        self.indicator = GhsPopComparisonBuildings(
            bpolys=bpolys, layer_name="building_count"
        )

    @oqt_vcr.use_cassette("test_indicator_ghs_pop_comparison.json")
    def test(self):
        asyncio.run(self.indicator.preprocess())
        self.assertIsNotNone(self.indicator.pop_count)
        self.assertIsNotNone(self.indicator.area)
        self.assertIsNotNone(self.indicator.feature_count)
        self.assertIsNotNone(self.indicator.feature_count_per_sqkm)
        self.assertIsNotNone(self.indicator.pop_count_per_sqkm)

        self.indicator.calculate()
        self.assertIsNotNone(self.indicator.result.label)
        self.assertIsNotNone(self.indicator.result.value)
        self.assertIsNotNone(self.indicator.result.description)

        self.indicator.create_figure()
        self.assertIsNotNone(self.indicator.result.svg)

    @oqt_vcr.use_cassette("test_indicator_ghs_pop_comparison.json")
    def test_get_zonal_stats_population(self):
        result = asyncio.run(
            self.indicator.get_zonal_stats_population(self.indicator.bpolys)
        )
        self.assertIsInstance(result, Record)


if __name__ == "__main__":
    unittest.main()
