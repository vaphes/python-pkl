# package pkl

# import (
# 	"fmt"
# 	"reflect"
# )

# func (d *decoder) decodeMap(inType reflect.Type) (*reflect.Value, error) {
# 	_, code, err := d.decodeObjectPreamble()
# 	if err != nil {
# 		return nil, err
# 	}
# 	if code == codeSet {
# 		return d.decodeSet(inType)
# 	}
# 	if code != codeMap && code != codeMapping {
# 		return nil, fmt.Errorf("invalid code for slices: %d", code)
# 	}
# 	return d.decodeMapImpl(inType)
# }

# func (d *decoder) decodeMapImpl(inType reflect.Type) (*reflect.Value, error) {
# 	mapLen, err := d.dec.DecodeMapLen()
# 	if err != nil {
# 		return nil, err
# 	}
# 	ret := reflect.MakeMapWithSize(inType, mapLen)
# 	keyType := inType.Key()
# 	valueType := inType.Elem()
# 	for i := 0; i < mapLen; i++ {
# 		key, err := d.Decode(keyType)
# 		if err != nil {
# 			return nil, err
# 		}
# 		value, err := d.Decode(valueType)
# 		if err != nil {
# 			return nil, err
# 		}
# 		ret.SetMapIndex(*key, *value)
# 	}
# 	return &ret, nil
# }

# var emptyMirror = reflect.ValueOf(empty)

# // decodeSet decodes into `map[T]struct{}`
# func (d *decoder) decodeSet(inType reflect.Type) (*reflect.Value, error) {
# 	length, err := d.dec.DecodeArrayLen()
# 	if err != nil {
# 		return nil, err
# 	}
# 	ret := reflect.MakeMapWithSize(inType, length)
# 	keyType := inType.Key()
# 	for i := 0; i < length; i++ {
# 		elem, err := d.Decode(keyType)
# 		if err != nil {
# 			return nil, err
# 		}
# 		ret.SetMapIndex(*elem, emptyMirror)
# 	}
# 	return &ret, nil
# }


def decode_map(d, in_type):
    _, code, err = d.decode_object_preamble()
    if err is not None:
        return None, err
    if code == code_set:
        return d.decode_set(in_type)
    if code != code_map and code != code_mapping:
        return None, f"invalid code for slices: {code}"
    return d.decode_map_impl(in_type)


def decode_map_impl(d, in_type):
    map_len, err = d.dec.decode_map_len()
    if err is not None:
        return None, err
    ret = reflect.make_map_with_size(in_type, map_len)
    key_type = in_type.key()
    value_type = in_type.elem()
    for i in range(map_len):
        key, err = d.decode(key_type)
        if err is not None:
            return None, err
        value, err = d.decode(value_type)
        if err is not None:
            return None, err
        ret.set_map_index(key, value)
    return ret, None


empty_mirror = reflect.value_of(empty)


def decode_set(d, in_type):
    length, err = d.dec.decode_array_len()
    if err is not None:
        return None, err
    ret = reflect.make_map_with_size(in_type, length)
    key_type = in_type.key()
    for i in range(length):
        elem, err = d.decode(key_type)
        if err is not None:
            return None, err
        ret.set_map_index(elem, empty_mirror)
    return ret, None
