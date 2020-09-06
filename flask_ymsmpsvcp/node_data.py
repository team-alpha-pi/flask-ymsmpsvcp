from dataclasses import dataclass, field
from typing import List
from dataclasses_json import dataclass_json
from enum import Enum

class InputType(Enum):
    Text = 'text'
    Toggle = 'toggle'


class Methods(Enum):
    Get = 'GET'
    Put = 'PUT'


@dataclass_json
@dataclass
class Branch:
    uri: str
    display_name: str
    description: str
    child_nodes: list = field(default_factory=lambda: [])
    node_type: str = 'Branch'

    @classmethod
    def from_data(cls, uri, child_nodes, **kwargs):
        try:
            display_name = kwargs['display_name']
            description = kwargs['description']
        except KeyError as e:
            raise KeyError(f'Missing key {e} in {uri}')

        return cls(
            uri=uri,
            child_nodes=child_nodes,
            display_name=display_name,
            description=description
        )

@dataclass_json
@dataclass
class Leaf:
    uri: str
    display_name: str
    description: str
    input_type: InputType
    actions: List[Methods]
    node_type: str = 'Leaf'

    @classmethod
    def from_data(cls, uri, actions, **kwargs):
        try:
            display_name = kwargs['display_name']
            description = kwargs['description']
        except KeyError as e:
            raise KeyError(f'Missing key {e} in {uri}')

        input_type = InputType(kwargs.get('input_type', 'text'))

        return cls(
            uri=uri,
            display_name=display_name,
            description=description,
            input_type=input_type,
            actions=actions,
        )
