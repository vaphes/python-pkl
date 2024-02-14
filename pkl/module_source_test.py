# package pkl

# import (
# 	"testing"

# 	"github.com/stretchr/testify/assert"
# )

# func Test_PathSource(t *testing.T) {
# 	src := FileSource("/usr/local/myfile.pkl")
# 	assert.Equal(t, "file:///usr/local/myfile.pkl", src.Uri.String())
# 	src = FileSource("/usr", "local", "lib", "myotherfile.pkl")
# 	assert.Equal(t, "file:///usr/local/lib/myotherfile.pkl", src.Uri.String())
# }
