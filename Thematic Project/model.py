# I am defining a data model for non-mandatory fields to define a base model
# It defines a data model for an api to pass the dates:
from pydantic import BaseModel, Field

class QueryDates(BaseModel):
    fromtime : str = Field(default=None)
    totime : str = Field(default=None)
