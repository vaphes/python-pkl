# package pkl

# import (
# 	"reflect"

# 	"github.com/vmihailenco/msgpack/v5/msgpcode"
# )

# func (d *decoder) decodeBool() (*reflect.Value, error) {
# 	b, err := d.dec.DecodeBool()
# 	if err != nil {
# 		return nil, err
# 	}
# 	ret := reflect.ValueOf(b)
# 	return &ret, nil
# }

# func (d *decoder) decodeString() (*reflect.Value, error) {
# 	b, err := d.dec.DecodeString()
# 	if err != nil {
# 		return nil, err
# 	}
# 	ret := reflect.ValueOf(b)
# 	return &ret, nil
# }

# func (d *decoder) decodeInt() (*reflect.Value, error) {
# 	b, err := d.dec.DecodeInt()
# 	if err != nil {
# 		return nil, err
# 	}
# 	ret := reflect.ValueOf(b)
# 	return &ret, nil
# }

# func (d *decoder) decodeInt8() (*reflect.Value, error) {
# 	b, err := d.dec.DecodeInt8()
# 	if err != nil {
# 		return nil, err
# 	}
# 	ret := reflect.ValueOf(b)
# 	return &ret, nil
# }

# func (d *decoder) decodeInt16() (*reflect.Value, error) {
# 	b, err := d.dec.DecodeInt16()
# 	if err != nil {
# 		return nil, err
# 	}
# 	ret := reflect.ValueOf(b)
# 	return &ret, nil
# }

# func (d *decoder) decodeInt32() (*reflect.Value, error) {
# 	b, err := d.dec.DecodeInt32()
# 	if err != nil {
# 		return nil, err
# 	}
# 	ret := reflect.ValueOf(b)
# 	return &ret, nil
# }

# func (d *decoder) decodeInt64() (*reflect.Value, error) {
# 	b, err := d.dec.DecodeInt64()
# 	if err != nil {
# 		return nil, err
# 	}
# 	ret := reflect.ValueOf(b)
# 	return &ret, nil
# }

# func (d *decoder) decodeUint() (*reflect.Value, error) {
# 	b, err := d.dec.DecodeUint()
# 	if err != nil {
# 		return nil, err
# 	}
# 	ret := reflect.ValueOf(b)
# 	return &ret, nil
# }

# func (d *decoder) decodeUint8() (*reflect.Value, error) {
# 	b, err := d.dec.DecodeUint8()
# 	if err != nil {
# 		return nil, err
# 	}
# 	ret := reflect.ValueOf(b)
# 	return &ret, nil
# }

# func (d *decoder) decodeUint16() (*reflect.Value, error) {
# 	b, err := d.dec.DecodeUint16()
# 	if err != nil {
# 		return nil, err
# 	}
# 	ret := reflect.ValueOf(b)
# 	return &ret, nil
# }

# func (d *decoder) decodeUint32() (*reflect.Value, error) {
# 	b, err := d.dec.DecodeUint32()
# 	if err != nil {
# 		return nil, err
# 	}
# 	ret := reflect.ValueOf(b)
# 	return &ret, nil
# }

# func (d *decoder) decodeUint64() (*reflect.Value, error) {
# 	b, err := d.dec.DecodeUint64()
# 	if err != nil {
# 		return nil, err
# 	}
# 	ret := reflect.ValueOf(b)
# 	return &ret, nil
# }

# func (d *decoder) decodeFloat64() (*reflect.Value, error) {
# 	c, err := d.dec.PeekCode()
# 	if err != nil {
# 		return nil, err
# 	}
# 	switch c {
# 	// We translate `pkl.Number` to float64 in Go.
# 	// The messagepack encoding for `pkl.Number` may either be an Int64 or a Float64.
# 	case msgpcode.Int64:
# 		b, err := d.dec.DecodeInt64()
# 		if err != nil {
# 			return nil, err
# 		}
# 		ret := reflect.ValueOf(float64(b))
# 		return &ret, nil
# 	default:
# 		b, err := d.dec.DecodeFloat64()
# 		if err != nil {
# 			return nil, err
# 		}
# 		ret := reflect.ValueOf(b)
# 		return &ret, nil
# 	}
# }
