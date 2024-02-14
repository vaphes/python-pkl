# package pkl

# import (
# 	"io/fs"
# 	"net/url"
# 	"strings"
# )

# type fsReader struct {
# 	fs     fs.FS
# 	scheme string
# }

# func (f *fsReader) Scheme() string {
# 	return f.scheme
# }

# func (f *fsReader) IsGlobbable() bool {
# 	return true
# }

# func (f *fsReader) HasHierarchicalUris() bool {
# 	return true
# }

# func (f *fsReader) ListElements(url url.URL) ([]PathElement, error) {
# 	path := strings.TrimSuffix(strings.TrimPrefix(url.Path, "/"), "/")
# 	if path == "" {
# 		path = "."
# 	}
# 	entries, err := fs.ReadDir(f.fs, path)
# 	if err != nil {
# 		return nil, err
# 	}
# 	var ret []PathElement
# 	for _, entry := range entries {
# 		// copy Pkl's built-in `file` ModuleKey and don't follow symlinks.
# 		if entry.Type()&fs.ModeSymlink != 0 {
# 			continue
# 		}
# 		ret = append(ret, NewPathElement(entry.Name(), entry.IsDir()))
# 	}
# 	return ret, nil
# }

# var _ Reader = (*fsReader)(nil)

# type fsModuleReader struct {
# 	*fsReader
# }

# func (f fsModuleReader) IsLocal() bool {
# 	return true
# }

# func (f fsModuleReader) Read(url url.URL) (string, error) {
# 	contents, err := fs.ReadFile(f.fs, strings.TrimPrefix(url.Path, "/"))
# 	return string(contents), err
# }

# var _ ModuleReader = (*fsModuleReader)(nil)

# type fsResourceReader struct {
# 	*fsReader
# }

# func (f fsResourceReader) Read(url url.URL) ([]byte, error) {
# 	return fs.ReadFile(f.fs, strings.TrimPrefix(url.Path, "/"))
# }

# var _ ResourceReader = (*fsResourceReader)(nil)
