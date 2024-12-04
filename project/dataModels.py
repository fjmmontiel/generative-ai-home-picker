from pydantic import BaseModel, Field

# Pydantic model for a House
class House(BaseModel):
    title: str = Field(alias="Title")
    description: str = Field(alias="Description")
    price: str = Field(alias="Price")
    location: str = Field(alias="Location")
    number_of_rooms: int = Field(alias="Number of Rooms")
    number_of_bathrooms: int = Field(alias="Number of Bathrooms")
    distance_to_city_center: float = Field(alias="Distance to City Center")



