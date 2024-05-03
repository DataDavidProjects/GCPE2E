from google.cloud import bigquery
from typing import List
from pathlib import Path

from jinja2 import Template  # pylint: disable=E0401


def generate_query(input_file: Path, **replacements) -> str:
    """
    Read input file and replace placeholder using Jinja.

    Args:
        input_file (Path): input file to read
        replacements: keyword arguments to use to replace placeholders
    Returns:
        str: replaced content of input file
    """

    with open(input_file, "r", encoding="utf-8") as f:
        query_template = f.read()

    return Template(query_template).render(**replacements)


class BigQueryExternalTable:
    """
    Initialize a BigQueryExternalTable object.

    Args:
        project_id (str): The ID of the Google Cloud project.
    """

    def __init__(self, project_id: str):
        self.client: bigquery.Client = bigquery.Client(project=project_id)

    def create_external_table(
        self,
        dataset_id: str,
        table_id: str,
        data_uri: str,
        schema: List[bigquery.SchemaField],
        format: str = "CSV",
        skip_leading_rows: int = 1,
    ) -> bigquery.Table:
        """
        Create an external table in BigQuery that references data in Google Cloud Storage.

        Args:
            dataset_id (str): The ID of the dataset in BigQuery.
            table_id (str): The ID of the table in BigQuery.
            data_uri (str): The URI of the data in Google Cloud Storage.
            schema (List[bigquery.SchemaField]): The schema of the table.
            format (str, optional): The format of the data. Defaults to 'CSV'.
            skip_leading_rows (int, optional): The number of leading rows to skip. Defaults to 1.

        Returns:
            bigquery.Table: The created table.
        """
        # Define your table reference
        table_ref = self.client.dataset(dataset_id).table(table_id)

        # Define your external table configuration
        external_config = bigquery.ExternalConfig(format)
        external_config.source_uris = [data_uri]
        external_config.schema = schema
        external_config.options.skip_leading_rows = skip_leading_rows

        # Create the external table
        table = bigquery.Table(table_ref, schema=schema)
        table.external_data_configuration = external_config
        table = self.client.create_table(table)  # API request

        print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")

        return table
