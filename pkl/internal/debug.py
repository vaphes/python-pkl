# package internal

# import (
# 	"fmt"
# 	"os"
# )

# var debugEnabled bool

# func init() {
# 	for _, env := range os.Environ() {
# 		if env == "PKL_DEBUG=1" {
# 			debugEnabled = true
# 			break
# 		}
# 	}
# }

# // Debug writes debugging messages if PKL_DEBUG is set to 1.
# func Debug(format string, a ...any) {
# 	if debugEnabled {
# 		_, _ = os.Stdout.WriteString("[pkl-go] " + fmt.Sprintf(format, a...) + "\n")
# 	}
# }
