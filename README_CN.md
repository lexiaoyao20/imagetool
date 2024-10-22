# iOS 图片混淆工具 (imagetool)

[English README](README.md)

imagetool 是一个强大的命令行工具，专为 iOS 项目设计，用于自动化图片资源的混淆和管理。它能够有效地重命名图片、更新代码引用，并修改图片哈希值，从而增强应用的安全性和资源管理效率。

## 功能特性

- **图片重命名**: 自动为项目中的图片资源生成新的随机名称。
- **代码引用更新**: 自动更新代码文件中对重命名图片的所有引用。
- **图片哈希值修改**: 对每张图片进行微小修改，改变其哈希值，但不影响视觉效果。
- **空 imageset 清理**: 自动删除项目中空的 imageset 文件夹。
- **生成报告**: 创建详细的 Excel 报告，记录所有图片修改。
- **可配置性**: 通过 JSON 配置文件自定义工具行为。
- **灵活的命名规则**: 支持添加自定义前缀到重命名的图片。

## 安装

1. 确保你的系统已安装 Python 3.6 或更高版本。

2. 克隆此仓库或下载源代码：
   ```
   git clone https://github.com/lexiaoyao20/imagetool.git
   cd imagetool
   ```

3. 安装所需依赖：
   ```
   pip install -r requirements.txt
   ```

## 使用说明

基本用法：

```
python imagetool.py --project <iOS项目路径> [--prefix <图片名称前缀>] [--output <报告输出路径>]
```

参数说明：
- `--project`: （必需）指定 iOS 项目的根目录路径。
- `--prefix`: （可选）为重命名的图片添加自定义前缀。
- `--output`: （可选）指定生成的 Excel 报告的输出路径。默认为 "obfuscation_report.xlsx"。

示例：
```
python imagetool.py --project /path/to/your/ios/project --prefix OBF --output report.xlsx
```

## 配置说明

工具使用 `config.json` 文件进行配置。你可以在此文件中指定：

- `excluded_dirs`: 需要排除的目录列表。
- `excluded_files`: 需要排除的文件列表。

示例 `config.json`:
```json
{
  "excluded_dirs": ["Pods", "Carthage"],
  "excluded_files": ["AppIcon.appiconset", "LaunchImage.launchimage"]
}
```

## 注意事项

1. 在使用此工具之前，请确保对你的项目进行备份。
2. 工具会修改项目文件，请在版本控制系统（如 Git）的新分支上进行操作。
3. 运行工具后，请仔细检查生成的报告和修改后的项目，确保所有更改都符合预期。
4. 某些复杂的图片引用（如动态生成的字符串）可能无法被自动更新，可能需要手动检查和修改。

## 贡献指南

欢迎贡献！如果你有任何改进建议或 bug 报告，请创建一个 issue 或提交一个 pull request。

## 许可证

本项目采用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。
