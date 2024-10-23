# iOS Image Obfuscation Tool (imagetool)

[中文版 README](README_CN.md)

imagetool is a powerful command-line tool designed for iOS projects to automate image resource obfuscation and management. It effectively renames images, updates code references, and modifies image hash values, enhancing application security and resource management efficiency.

## Features

- **Image Renaming**: Automatically generates new random names for image resources in the project.
- **Code Reference Updates**: Automatically updates all references to renamed images in code files.
- **Image Hash Modification**: Makes minor modifications to each image, changing its hash value without affecting visual appearance.
- **Empty Imageset Cleanup**: Automatically removes empty imageset folders from the project.
- **Report Generation**: Creates detailed Excel reports documenting all image modifications.
- **Configurability**: Customizes tool behavior through a JSON configuration file.
- **Flexible Naming Rules**: Supports adding custom prefixes to renamed images.
- **Standalone Empty Imageset Cleanup**: Provides a separate command to clean only empty imageset directories.

## Installation

1. Ensure you have Python 3.6 or higher installed on your system.

2. Clone this repository or download the source code:
   ```
   git clone https://github.com/lexiaoyao20/imagetool.git
   cd imagetool
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To see usage instructions and available options, simply run:

```
python imagetool.py --project <iOS_project_path> [--prefix <image_name_prefix>] [--output <report_output_path>]
```

Parameters:
- `--project`: (Required) Specifies the root directory path of the iOS project.
- `--prefix`: (Optional) Adds a custom prefix to renamed images.
- `--output`: (Optional) Specifies the output path for the generated Excel report. Default is "obfuscation_report.xlsx".

Example:
```
python imagetool.py --project /path/to/your/ios/project --prefix OBF --output report.xlsx
```

## Configuration

The tool uses a `config.json` file for configuration. You can specify:

- `excluded_dirs`: List of directories to exclude.
- `excluded_files`: List of files to exclude.

Example `config.json`:
```json
{
  "excluded_dirs": ["Pods", "Carthage"],
  "excluded_files": ["AppIcon.appiconset", "LaunchImage.launchimage"]
}
```

## Important Notes

1. Make sure to backup your project before using this tool.
2. The tool modifies project files, so operate on a new branch in your version control system (e.g., Git).
3. After running the tool, carefully review the generated report and the modified project to ensure all changes meet expectations.
4. Some complex image references (e.g., dynamically generated strings) may not be automatically updated and might require manual checking and modification.

## Contributing

Contributions are welcome! If you have any suggestions for improvements or bug reports, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Releases

You can find pre-built binaries for the latest release on the [Releases page](https://github.com/lexiaoyao20/imagetool/releases).

To use the pre-built binary:

1. Download the `imagetool` executable from the latest release.
2. Make it executable: `chmod +x imagetool`
3. Run it: `./imagetool --project <iOS_project_path> [--prefix <image_name_prefix>] [--output <report_output_path>]`
