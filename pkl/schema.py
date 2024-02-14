# package pkl

# import "reflect"

# var schemas = make(map[string]reflect.Type)

# // RegisterMapping associates the type given the Pkl name to the corresponding Go type.
# //
# //goland:noinspection GoUnusedExportedFunction
# func RegisterMapping(name string, value any) {
# 	schemas[name] = reflect.TypeOf(value)
# }

from typing import Any

schemas: dict[str, type] = {}


def register_mapping(name: str, value: Any):
    schemas[name] = type(value)
