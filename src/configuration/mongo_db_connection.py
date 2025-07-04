import os
import sys
import pymongo
import certifi

from src.logger import logging
from src.exception import MyException
from src.constants import DATABASE_NAME,MONGODB_URL_KEY

# load the certificate authority file to avoid timeout errors when connectin to MongoDB
ca=certifi.where()

class MongoDBClient:
    """
    MangoDB client is responsible for establishing a connection to the MongoDB database
    
    Atrributes:
    - client:MongoDBClient  (A shared MongoClient instance for the class)
    - database:Database  (The specific database instances that Mongo client connects to.)

    Methods:
    - _init_(database_name:str)->None (  Initializes the MongoDB connection using the given database name.)  
    """


    client=None # Shared MongoClient instance across all MongoDBClient instances

    def _init_(self,database_name:str=DATABASE_NAME)->None:
        """
        Initializes a connection to the MongoDB database. If no existing connection is found, it establishes a new one.

        Parameters:
        ----------
        database_name : str, optional
            Name of the MongoDB database to connect to. Default is set by DATABASE_NAME constant.

        Raises:
        ------
        MyException
            If there is an issue connecting to MongoDB or if the environment variable for the MongoDB URL is not set.
        """
        try:
            if MongoDBClient.client is None:
                mongo_db_url=os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment variable'{MONGODB_URL_KEY}' is not set")
                
                MongoDBClient.client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)

            self.client=MongoDBClient.client
            self.database=self.client[database_name]
            self.database_name=database_name
            logging.info("MongoDB connection succesful")
        except Exception as e :
             raise MyException(e,sys) # type: ignore
            

               
         
        
        

