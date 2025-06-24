from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel  # ✅ Updated import

class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )