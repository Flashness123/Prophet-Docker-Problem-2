#TODO: check why there is a semicolon in with open 
#       also why the commata at init ProphetPredictor
#       calculate for x dates into the future
import sys
import pickle
import datetime
import prophet
from typing import List
import pandas as pd
import os
from abc import ABC, abstractmethod

class DailySalesPredictor(ABC):
    def __init__(self, model_name) -> None:

        """For the correct Path:"""
        # # Get the directory in which utils.py is located
        # utils_dir = os.path.dirname(os.path.abspath(__file__))
        # # Now build the path to the pickle_models directory
        # pickle_models_dir = os.path.join(utils_dir, 'pickle_models')
        # # Use this path when opening the file
        # model_path = os.path.join(pickle_models_dir, f"{model_name}.pckl")

        """ 
        This one loads the model from the given file
        """
        with open(f"models/{model_name}.pckl", "rb",) as fin:    #custom
            try:
                #print("-------------Fin: " + fin, file=sys.stderr)
                self.model = pickle.load(fin)
            except (OSError, FileNotFoundError, TypeError):
                print("-------------Fin: ", file=sys.stderr)
                print(fin, file=sys.stderr)
                print("wrong path / model not available")
                exit(-1)

    def calculate_next_date(self, prev_date):
        """
        This one calculates the next date
        Will have output format of yyyy-mm-dd
        """
        self.next_date = datetime.datetime(
            *list(map(lambda x: int(x), prev_date.split("-")))
        ) + datetime.timedelta(
            days=1
        )
    
    def get_next_date(self, prev_date):
        try:
            return self.next_date.strftime("%y-%m-%d")
        except NameError:
            self.calculate_next_date(prev_date)

    @abstractmethod
    def predict(self, prev_date) -> List:
        pass
    @abstractmethod
    def preprocess_inputs(self, prev_date):
        pass
    @abstractmethod
    def postprocess_outputs(self, output_from_model) -> List:
        pass

class ProphetPredictor(DailySalesPredictor):
    
    def __init__(self,) -> None:
        """
        This one should load the file from pickle_models/prophet.pckl
        """
        super().__init__("prophet") #custom
    
    def preprocess_inputs(self, prev_date):
        """
        This Model takes in an input as a pandas dataframe having index as the day to be predicted
        """
        self.calculate_next_date(prev_date) #get the self.next_date var

        next_date_series = pd.DataFrame(
            {"ds": pd.date_range(start=self.next_date, end=self.next_date)}
        )
        return next_date_series
    
    def postprocess_outputs(self, output_from_model) -> List:
        """
        This one should return the yhat in the list format
        """
        return output_from_model["yhat"].tolist()
    
    def predict(self, prev_date) -> List:
        next_date_series = self.preprocess_inputs(prev_date) #taking the input from preprocess
        pred = self.model.predict(next_date_series) #new prediction
        pred = self.postprocess_outputs(pred) #postprocess prediction
        return pred
    
        