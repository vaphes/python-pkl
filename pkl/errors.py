# package pkl

# import (
# 	"errors"
# 	"fmt"
# )

# // EvalError is an error that occurs during the normal evaluation of Pkl code.
# //
# // This means that Pkl evaluation occurred, and the Pkl runtime produced an error.
# type EvalError struct {
# 	ErrorOutput string
# }

# var _ error = (*EvalError)(nil)

# func (r *EvalError) Error() string {
# 	return r.ErrorOutput
# }

# // Is implements the interface expected by errors.Is.
# func (r *EvalError) Is(err error) bool {
# 	if err == nil {
# 		return false
# 	}
# 	var evalError *EvalError
# 	ok := errors.As(err, &evalError)
# 	return ok
# }

# // InternalError indicates that an unexpected error occured.
# type InternalError struct {
# 	err error
# }

# var _ error = (*InternalError)(nil)

# func (r *InternalError) Error() string {
# 	return fmt.Sprintf("an internal error ocurred: %v", r.err)
# }

# // Is implements the interface expected by errors.Is.
# func (r *InternalError) Is(err error) bool {
# 	if err == nil {
# 		return false
# 	}
# 	var internalError *InternalError
# 	ok := errors.As(err, &internalError)
# 	return ok
# }

# // Unwrap implements the interface expected by errors.Unwrap.
# func (r *InternalError) Unwrap() error {
# 	return r.err
# }
