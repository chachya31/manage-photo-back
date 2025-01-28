import boto3

from logging import getLogger

from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError
from injector import inject

from domain.entity.test import TestMaster


LOGGER = getLogger(__name__)

class TestRepo():

    GSI1_INDEX = "GSI1Index"
    GSI2_INDEX = "GSI2Index"

    def __init__(self, dyn_resource):
        self.dyn_resource = dyn_resource
        self.table = None
        #self.__table_name = "dev-manage-photo"
        #self.__client = boto3.client("dynamodb", endpoint_url="http://localhost:3000")

    def exists(self, table_name):
        try:
            table = self.dyn_resource.Table(table_name)
            table.load()
            exists = True
        except ClientError as err:
            if err.response["Error"]["Code"] == "ResourceNotFoundException":
                exists = False
            else:
                LOGGER.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    table_name,
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                )
                raise
        else:
            self.table = table
        return exists

    def upsert_test(self, test_data: TestMaster) -> None:
        try:
            self.__client.put_item(
                TableName= self.__table_name,
                Item=test_data,
            )
        except ClientError as err:
            LOGGER.error(
                "Put Item Failed",
                self.__table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
            
    def list_tables(self):
        """
        Lists the Amazon DynamoDB tables for the current account.

        :return: The list of tables.
        """
        try:
            tables = []
            for table in self.dyn_resource.tables.all():
                print(table.name)
                tables.append(table)
        except ClientError as err:
            LOGGER.error(
                "Couldn't list tables. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return tables