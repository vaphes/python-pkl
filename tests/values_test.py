# package pkl

# import (
# 	"testing"

# 	"github.com/stretchr/testify/assert"
# )

# func TestDataSize_String(t *testing.T) {
# 	tests := []struct {
# 		name     string
# 		input    DataSize
# 		expected string
# 	}{
# 		{
# 			name: "bytes",
# 			input: DataSize{
# 				Value: 1.0,
# 				Unit:  Bytes,
# 			},
# 			expected: "1.b",
# 		},
# 		{
# 			name: "kebibytes",
# 			input: DataSize{
# 				Value: 5.3,
# 				Unit:  Kibibytes,
# 			},
# 			expected: "5.3.kib",
# 		},
# 		{
# 			name: "invalid",
# 			input: DataSize{
# 				Value: 5.0,
# 			},
# 			expected: "5.<invalid>",
# 		},
# 	}
# 	for _, test := range tests {
# 		t.Run(test.name, func(t *testing.T) {
# 			assert.Equal(t, test.expected, test.input.String())
# 		})
# 	}
# }
