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
