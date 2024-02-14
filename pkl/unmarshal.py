# package pkl

# import (
# 	"errors"
# 	"fmt"
# 	"reflect"
# )

# // Unmarshal parses Pkl-encoded data and stores the result into
# // the value pointed by v.
# //
# // This is a low-level API. Most users should be using Evaluator.Evaluate instead.
# //
# // The following struct tags are supported:
# //
# //	pkl:"Field"     Overrides the field's name to map to.
# //
# //goland:noinspection GoUnusedExportedFunction
# func Unmarshal(data []byte, v any) error {
# 	value := reflect.ValueOf(v)
# 	if value.Kind() != reflect.Ptr {
# 		return fmt.Errorf("cannot unmarshal non-pointer. Got kind: %v", value.Kind())
# 	}
# 	if value.IsNil() {
# 		return errors.New("cannot unmarshal into nil")
# 	}
# 	res, err := newDecoder(data, schemas).Decode(value.Elem().Type())
# 	if err != nil {
# 		return err
# 	}
# 	value.Elem().Set(*res)
# 	return nil
# }
