# app/schemas/base.py
from pydantic import BaseModel
from typing import Any, Dict


def to_camel_case(snake_str: str) -> str:
    """Convert snake_case to camelCase"""
    components = snake_str.split('_')
    return components[0] + ''.join(word.capitalize() for word in components[1:])


def to_snake_case(camel_str: str) -> str:
    """Convert camelCase to snake_case"""
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class CamelCaseModel(BaseModel):
    """Base model that automatically converts between camelCase and snake_case"""
    
    class Config:
        alias_generator = to_camel_case
        populate_by_name = True  # Allow both field name and alias
        
    def dict(self, by_alias: bool = True, **kwargs) -> Dict[str, Any]:
        """Override dict to return camelCase by default"""
        return super().dict(by_alias=by_alias, **kwargs)


