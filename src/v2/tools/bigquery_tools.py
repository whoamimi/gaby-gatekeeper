"""
bigquery_tools.py

This module contains SQL templates and functions to interact with
Google BigQuery for data cleaning and assist generative models in making decisions.

"""

from ...v1.core.config import Config
from ..agent.registry import Toolbox
from ..config.consts import SQL_DESCRIBE_DATA_FIELD_LABEL, SQL_DETECT_NUMERIC_FIELD

bq_profilers = Toolbox('bigquery_tools')
config = Config()

@bq_profilers
def describe_data_field(
    data_summary_id: str,
    connection_id: str | None = config.bq_model_connection,
    endpoint: str | None = config.default_model_type
):
    return SQL_DESCRIBE_DATA_FIELD_LABEL.format(
        data_summary_id=data_summary_id,
        connection_id=connection_id,
        endpoint=endpoint
    )

@bq_profilers
def detect_numeric_field(
    data_summary_id: str,
    connection_id: str | None = config.bq_model_connection,
    endpoint: str | None = config.default_model_type
):
    return SQL_DETECT_NUMERIC_FIELD.format(
        data_summary_id=data_summary_id,
        connection_id=connection_id,
        endpoint=endpoint
    )
