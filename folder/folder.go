package folder

import (
	"io/fs"
	"os"
	"path/filepath"

	"github.com/samber/lo"
)

type SourceFile struct {
	Info       os.DirEntry
	Path       string
	ParentPath string
}

func ReadFolder(dir string, sub bool) ([]SourceFile, error) {
	if sub {
		var result []SourceFile
		filepath.WalkDir(dir, func(path string, d fs.DirEntry, err error) error {
			if err != nil {
				return nil
			}
			if !d.IsDir() {
				result = append(result, SourceFile{
					Info:       d,
					Path:       path,
					ParentPath: filepath.Dir(path),
				})
			}
			return nil
		})
		return result, nil
	}
	files, err := os.ReadDir(dir)
	if err != nil {
		return nil, nil
	}
	return lo.Map(lo.Filter(files, func(item fs.DirEntry, _ int) bool {
		return !item.IsDir()
	}), func(item fs.DirEntry, index int) SourceFile {
		return SourceFile{
			Info:       item,
			Path:       filepath.Join(dir, item.Name()),
			ParentPath: dir,
		}
	}), nil
}
