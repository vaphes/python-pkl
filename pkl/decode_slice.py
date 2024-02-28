# package pkl

# import (
# 	"fmt"
# 	"reflect"
# )

# func (d *decoder) decodeSlice(inType reflect.Type) (*reflect.Value, error) {
# 	length, code, err := d.decodeObjectPreamble()
# 	if err != nil {
# 		return nil, err
# 	}
# 	if length != 2 {
# 		return nil, fmt.Errorf("expected array length 2 but got %d", length)
# 	}
# 	if code != codeList && code != codeListing {
# 		return nil, fmt.Errorf("invalid code for slices: %d. Expected %d or %d", code, codeList, codeListing)
# 	}
# 	return d.decodeSliceImpl(inType)
# }

# func (d *decoder) decodeSliceImpl(inType reflect.Type) (*reflect.Value, error) {
# 	sliceLen, err := d.dec.DecodeArrayLen()
# 	if err != nil {
# 		return nil, err
# 	}
# 	elemType := inType.Elem()
# 	ret := reflect.MakeSlice(reflect.SliceOf(elemType), sliceLen, sliceLen)
# 	for i := 0; i < sliceLen; i++ {
# 		v := ret.Index(i)
# 		decoded, err := d.Decode(elemType)
# 		if err != nil {
# 			return nil, err
# 		}
# 		v.Set(*decoded)
# 	}
# 	return &ret, nil
# }


def decode_slice(d, in_type):
    length, code, err = d.decode_object_preamble()
    if err != None:
        return None, err
    if length != 2:
        return None, f"expected array length 2 but got {length}"
    if code != code_list and code != code_listing:
        return (
            None,
            f"invalid code for slices: {code}. Expected {code_list} or {code_listing}",
        )
    return d.decode_slice_impl(in_type)


def decode_slice_impl(d, in_type):
    slice_len, err = d.dec.decode_array_len()
    if err != None:
        return None, err
    elem_type = in_type.elem()
    ret = reflect.make_slice(reflect.slice_of(elem_type), slice_len, slice_len)
    for i in range(slice_len):
        v = ret.index(i)
        decoded, err = d.decode(elem_type)
        if err != None:
            return None, err
        v.set(*decoded)
    return ret, None
