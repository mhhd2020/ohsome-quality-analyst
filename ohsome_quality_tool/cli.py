import ast

import click
import geojson
import yaml

from ohsome_quality_tool import oqt
from ohsome_quality_tool.cli_opts import (
    dataset_name_opt,
    feature_id_opt,
    indicator_name_opt,
    infile_opt,
    layer_name_opt,
    report_name_opt,
)
from ohsome_quality_tool.utils.definitions import (
    DATASET_NAMES,
    load_layer_definitions,
    load_metadata,
    logger,
)


class PythonLiteralOption(click.Option):
    def type_cast_value(self, ctx, value):
        try:
            return ast.literal_eval(value)
        except ValueError as e:
            logger.exception(e)
            raise click.BadParameter(value)


def add_opts(options):
    """Adds options to cli."""

    def _add_opts(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_opts


@click.group()
@click.version_option()
@click.option("--verbose", "-v", is_flag=True, help="Enable logging.")
def cli(verbose):
    if not verbose:
        logger.disabled = True
    else:
        logger.info("Logging enabled")


@cli.command("list-indicators")
def list_indicators():
    """List available indicators and their metadata."""
    metadata = load_metadata("indicators")
    metadata = yaml.dump(metadata, default_style="|")
    click.echo(metadata)


@cli.command("list-reports")
def list_reports():
    """List available reports and their metadata."""
    metadata = load_metadata("reports")
    metadata = yaml.dump(metadata, default_style="|")
    click.echo(metadata)


@cli.command("list-layers")
def list_layers():
    """List available layers and how they are definied (ohsome API parameters)."""
    layers = load_layer_definitions()
    layers = yaml.dump(layers, default_style="|")
    click.echo(layers)


@cli.command("list-datasets")
def list_datasets():
    """List in the Geodatabase available datasets."""
    click.echo(DATASET_NAMES)


@cli.command("create-indicator")
@add_opts(indicator_name_opt)
@add_opts(layer_name_opt)
@add_opts(infile_opt)
@add_opts(dataset_name_opt)
@add_opts(feature_id_opt)
def create_indicator(
    indicator_name: str, infile: str, layer_name: str, feature_id, dataset_name
):
    """Create an Indicator and print results to stdout."""
    # TODO: replace this with a function that loads the file AND
    #    checks the validity of the geometries, e.g. enforce polygons etc.
    if infile:
        with open(infile, "r") as file:
            bpolys = geojson.load(file)
    else:
        bpolys = None
    indicator = oqt.create_indicator(
        indicator_name=indicator_name,
        bpolys=bpolys,
        layer_name=layer_name,
        feature_id=feature_id,
        dataset=dataset_name,
    )
    # TODO: Print out readable format.
    click.echo(indicator.metadata)
    click.echo(indicator.result)


@cli.command("create-report")
@add_opts(report_name_opt)
@add_opts(infile_opt)
@add_opts(dataset_name_opt)
@add_opts(feature_id_opt)
def create_report(report_name: str, infile: str, dataset_name: str, feature_id: int):
    """Create a Report and print results to stdout."""
    if infile:
        with open(infile, "r") as file:
            bpolys = geojson.load(file)
    report = oqt.create_report(
        report_name=report_name,
        bpolys=bpolys,
        dataset=dataset_name,
        feature_id=feature_id,
    )
    # TODO: Print out readable format.
    click.echo(report.metadata)
    click.echo(report.result)


@cli.command("process-all-indicators")
@add_opts(dataset_name_opt)
def process_all_indicators(dataset: str):
    raise NotImplementedError()


@cli.command("get-static-indicator")
@add_opts(indicator_name_opt)
@add_opts(dataset_name_opt)
@add_opts(feature_id_opt)
@add_opts(layer_name_opt)
def get_static_indicator(
    indicator_name: str, dataset: str, feature_id: int, layer_name: str
):
    raise NotImplementedError("Depricated. Use 'create_indicator' instead.")


@cli.command("get-dynamic-report")
@add_opts(report_name_opt)
@add_opts(infile_opt)
def get_dynamic_report(report_name: str, infile: str):
    raise NotImplementedError("Depricated. Use 'create_report' instead.")


@cli.command("get-static-report")
@add_opts(report_name_opt)
@add_opts(dataset_name_opt)
@add_opts(feature_id_opt)
def get_static_report(report_name: str, dataset: str, feature_id: int):
    raise NotImplementedError("Depricated. Use 'create_report' instead.")


@cli.command("get-static-report-pdf")
@add_opts(report_name_opt)
@add_opts(dataset_name_opt)
@add_opts(feature_id_opt)
def get_static_report_pdf(report_name: str, dataset: str, feature_id: int):
    raise NotImplementedError("Depricated. Use 'create_report' instead.")
