package cmd

import (
	"fmt"
	"media-refolder/folder"
	"os"
	"path/filepath"

	"github.com/spf13/cobra"
)

var (
	withSubFolder bool
	distFolder    string
	folderRule    string
	nameRule      string
	copyRule      bool
	overwriteRule bool
	isDryRun      bool
	excludePath   []string
)

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "media-refolder [source folder]",
	Short: "Auto rename and refold your medias",
	Long:  "Auto rename and refold your medias",
	// Uncomment the following line if your bare application
	// has an action associated with it:
	Run: func(cmd *cobra.Command, args []string) {
		dir := args[0]
		files, _ := folder.ReadFolder(dir, withSubFolder)
		for index, file := range files {
			os.Rename(file.Path, filepath.Join(dir, "dist", fmt.Sprintf("%v%v", index, filepath.Ext(file.Path))))
		}
	},
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	// Here you will define your flags and configuration settings.
	// Cobra supports persistent flags, which, if defined here,
	// will be global for your application.

	rootCmd.PersistentFlags().StringVarP(&distFolder, "dist", "d", "", "dist folder")
	rootCmd.PersistentFlags().BoolVarP(&withSubFolder, "sub", "s", false, "recursing process sub folder of source folder")
	rootCmd.PersistentFlags().StringArrayVarP(&excludePath, "exclude", "e", nil, "exclude file/folder(s)")
	rootCmd.PersistentFlags().StringVarP(&folderRule, "folder", "f", "", "folder rule\n/2006/01 will create a folder 2022(年) and a sub folder 8(月)\n(what a suck time format in go)")
	rootCmd.PersistentFlags().StringVarP(&nameRule, "name", "n", "", "name rule\n02 15:04:05 will named 12(日) 18(时):22(分):33(秒)\n(what a suck time format in go)")
	rootCmd.PersistentFlags().BoolVarP(&copyRule, "copy", "r", false, "copying instead of moving")
	rootCmd.PersistentFlags().BoolVarP(&overwriteRule, "overwrite", "o", false, "overwrite dist file when it has same name with source file?\nif this flag not been set, will do nothing for the source file")
	rootCmd.PersistentFlags().BoolVar(&isDryRun, "dry-run", false, "dry run and print result")

	rootCmd.MarkFlagRequired("dist")
	rootCmd.MarkFlagRequired("folder")
	rootCmd.MarkFlagRequired("name")

	// Cobra also supports local flags, which will only run
	// when this action is called directly.
	// rootCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
