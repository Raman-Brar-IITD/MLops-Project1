import sys
import pandas as pd
import numpy as np
from typing import Optional

from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME
from src.exception import MyException


class Proj1Data:
    """
    A class to export mongodb records as a pandas DataFrame """

    def __init__(self) -> None :
        """Intializes the MongoDB client connection"""

        try:
            self.mongo_client=MongoDBClient(database_name=DATABASE_NAME) 
        except Exception as e:
            raise MyException(e,sys) 
        
    def export_collection_as_dataframe(self,collection_name:str,database_name:Optional[str]=None)->pd.DataFrame:
        """
        Exports an entire MongoDB collection as a pandas DataFrame.

        Parameters:
        ----------
        collection_name : str
            The name of the MongoDB collection to export.
        database_name : Optional[str]
            Name of the database (optional). Defaults to DATABASE_NAME.

        Returns:
        -------
        pd.DataFrame
            DataFrame containing the collection data, with '_id' column removed and 'na' values replaced with NaN.
        """
        try:
            #Acess specified colllection from default or specific database
            if database_name is None:
                collection=self.mongo_client.database[collection_name]
            else:
                collection=self.mongo_client.client[database_name][collection_name]
            
            #convert collection data to Dataframe and preprocess

            print("Fetching data from MongoDB")

            df=pd.DataFrame(list(collection.find()))
            print(f"Data fetched with len:{len(df)}")

            if "id" in df.columns.tolist():
                df=df.drop(columns=["id","_id"],axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise MyException(e,sys) 

