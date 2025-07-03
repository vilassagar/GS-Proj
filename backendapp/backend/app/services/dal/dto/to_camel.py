
class ToCamel:

    __abstract__ = True

    def to_camel(self):
        def snake_to_camel(s: str) -> str:
            parts = s.split('_')
            return parts[0] + ''.join(word.capitalize() for word in parts[1:])

        camel_dict = {}
        for key, value in self.__dict__.items():
            new_key = snake_to_camel(key)
            # Check if the value has a to_camel method (nested DTO)
            if hasattr(value, "to_camel") and callable(value.to_camel):
                camel_dict[new_key] = value.to_camel()
            # If the value is a list, convert each item if possible
            elif isinstance(value, list):
                camel_dict[new_key] = [
                    item.to_camel() if hasattr(item, "to_camel") and callable(item.to_camel) else item
                    for item in value
                ]
            else:
                camel_dict[new_key] = value
        return camel_dict
