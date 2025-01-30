from io import BytesIO
import logging
import os
from pprint import pprint
from zipfile import ZipFile
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from decimal import Decimal

from domain.entity.movie import Movie, MovieForm
from usecase.interface.i_movie_repo import IMovieRepo

LOGGER = logging.getLogger(__name__)

class MovieRepo(IMovieRepo):

    def __init__(self):
        self.__table_name = "dev-manage-photo"
        self.__client = boto3.resource("dynamodb", endpoint_url="http://localhost:3000")
        self.__table = None
    
    def exists(self):
        try:
            table = self.__client.Table(self.__table_name)
            table.load()
            exists = True
        except ClientError as err:
            if err.response["Error"]["Code"] == "ResourceNotFoundException":
                exists = False
            else:
                LOGGER.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    self.__table_name,
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                )
                raise
        else:
            self.__table = table
        return exists
    
    def create_table(self):
        try:
            self.__table = self.__client.create_table(
                TableName=self.__table_name,
                KeySchema=[
                    {"AttributeName": "PK", "KeyType": "HASH"},
                    {"AttributeName": "SK", "KeyType": "RANGE"},
                ],
                AttributeDefinitions=[
                    {"AttributeName": "PK", "AttributeType": "S"},
                    {"AttributeName": "SK", "AttributeType": "S"},
                    {"AttributeName": "GSI1PK", "AttributeType": "S"},
                    {"AttributeName": "GSI1SK", "AttributeType": "S"},
                    {"AttributeName": "GSI2PK", "AttributeType": "S"},
                    {"AttributeName": "GSI2SK", "AttributeType": "S"},
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10,
                },
                GlobalSecondaryIndexes=[
                    {
                        "IndexName": "GSIndex1",
                        "KeySchema": [
                            {"AttributeName": "GSI1PK", "KeyType": "HASH"},
                            {"AttributeName": "GSI1SK", "KeyType": "RANGE"},
                        ],
                        "Projection": {
                            "ProjectionType": "ALL",
                        },
                        "ProvisionedThroughput": {
                            "ReadCapacityUnits": 10,
                            "WriteCapacityUnits": 10
                        }
                    },
                    {
                        "IndexName": "GSIndex2",
                        "KeySchema": [
                            {"AttributeName": "GSI2PK", "KeyType": "HASH"},
                            {"AttributeName": "GSI2SK", "KeyType": "RANGE"},
                        ],
                        "Projection": {
                            "ProjectionType": "ALL",
                        },
                        "ProvisionedThroughput": {
                            "ReadCapacityUnits": 10,
                            "WriteCapacityUnits": 10
                        }
                    },
                ],
            )
            self.__table.wait_until_exists()
        except ClientError as err:
            LOGGER.error(
                "Couldn't create table %s. Here's why: %s: %s",
                self.__table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return self.__table

    def list_tables(self):
        try:
            tables = []
            for table in self.__client.tables.all():
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
    
    def add_movie(self, data: MovieForm):
        item = Movie.to_db(data)
        try:
            self.__table.put_item(Item=item)
        except ClientError as err:
            LOGGER.error(
                "Couldn't add movie %s to table %s. Here's why: %s: %s",
                data.title,
                self.__table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
    
    def get_movie(self, year, title):
        try:
            response = self.__table.get_item(Key={"PK": f"Movie|{str(year)}", "SK": title})
        except ClientError as err:
            LOGGER.error(
                "Couldn't get movie %s from table %s. Here's why: %s: %s",
                title,
                self.__table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
        else:
            if not "Item" in response:
                return None
            
            return response["Item"]
    
    def update_movie(self, data: MovieForm):
        try:
            response = self.__table.update_item(
                Key={"PK": f"Movie|{str(data.year)}", "SK": data.title},
                UpdateExpression="set info.rating=:r, info.plot=:p",
                ExpressionAttributeValues={":r": Decimal(data.rating), ":p": data.plot},
                ReturnValues="UPDATED_NEW",
            )
        except ClientError as err:
            LOGGER.error(
                "Couldn't update movie %s in table %s. Here's why: %s: %s",
                data.title,
                self.__table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return response["Attributes"]
    
    def query_movies(self, year):
        try:
            key_condition = Key("PK").eq(f"Movie|{str(year)}")
            kwargs = {"KeyConditionExpression": key_condition}
            response = self.__table.query(**kwargs)
        except ClientError as err:
            LOGGER.error(
                "Couldn't query for movies released in %s. Here's why: %s: %s",
                year,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return response["Items"]
    
    def list_movie(self):
        try:
            key_condition = Key("GSI1PK").eq("Movie")
            kwargs = {
                "IndexName": "GSIndex1",
                "KeyConditionExpression": key_condition
            }
            response = self.__table.query(**kwargs)
        except ClientError as err:
            LOGGER.error(
                "Couldn't query for movie list. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return response["Items"]
        
    def delete_movie(self, title, year):
        try:
            self.__table.delete_item(Key={"PK": f"Movie|{str(year)}", "SK": title})
        except ClientError as err:
            LOGGER.error(
                "Couldn't delete movie %s. Here's why: %s: %s",
                title,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise