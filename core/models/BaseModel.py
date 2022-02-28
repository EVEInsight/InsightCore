from dataclasses import dataclass, asdict, fields


@dataclass
class BaseModel:
    def to_json(self) -> dict:
        """Converts the class object to a json compatible dictionary

        :return: The json compatible dictionary of this object
        """
        return asdict(self)

    @classmethod
    def from_json(cls, dct: dict):
        """Returns an instance of class from a json dictionary

        :param dct: Dictionary returned from the to_json() method
        :return: An instance of the class
        :rtype: cls
        """
        if not isinstance(dct, dict):
            raise TypeError("Expected dictionary")
        expected_fields = set(str(f.name) for f in fields(cls))
        for k in dct.keys():
            if k not in expected_fields:
                raise TypeError(f"Unexpected key {k}")
        c = cls(**dct)
        c.validate()
        return c

    def validate(self) -> None:
        return  # todo validate
