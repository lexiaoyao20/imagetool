import os
import argparse
from PIL import Image, UnidentifiedImageError
import random
import hashlib
import re
import json
import shutil
import string
from openpyxl import Workbook

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

config = load_config()

def should_exclude(path):
    for excluded_dir in config['excluded_dirs']:
        if excluded_dir in path.split(os.path.sep):
            return True
    return os.path.basename(path) in config['excluded_files']

def find_xcassets(project_path):
    xcassets = []
    for root, dirs, files in os.walk(project_path):
        if should_exclude(root):
            continue
        for dir in dirs:
            if dir.endswith('.xcassets'):
                xcassets.append(os.path.join(root, dir))
    return xcassets

def find_imagesets(xcassets_path):
    imagesets = []
    for root, dirs, files in os.walk(xcassets_path):
        if should_exclude(root):
            continue
        for dir in dirs:
            if dir.endswith('.imageset'):
                imagesets.append(os.path.join(root, dir))
    return imagesets

def find_code_files(project_path):
    code_extensions = ('.swift', '.m', '.h', '.xib', '.storyboard')
    code_files = []
    for root, dirs, files in os.walk(project_path):
        if should_exclude(root):
            continue
        for file in files:
            if file.lower().endswith(code_extensions):
                code_files.append(os.path.join(root, file))
    return code_files

def generate_new_name(old_name, prefix):
    # 生成随机后缀
    suffix_length = 3
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=suffix_length))
    
    # 组合新名称
    if prefix:
        new_name = f"{prefix}_{old_name}_{suffix}"
    else:
        new_name = f"{old_name}_{suffix}"
    
    return new_name

def calculate_image_hash(image_path):
    with open(image_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def obfuscate_image(input_path):
    try:
        # 计算修改前的哈希值
        original_hash = calculate_image_hash(input_path)
        print(f"修改前图片哈希值: {original_hash}")

        with Image.open(input_path) as img:
            width, height = img.size
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            pixel = img.getpixel((x, y))
            
            if isinstance(pixel, int):  # 对于某些图片格式，可能返回单个整数
                new_color = (pixel + 1) % 256
            elif len(pixel) == 4:  # RGBA
                r, g, b, a = pixel
                new_color = (r, g, (b + 1) % 256, a)
            elif len(pixel) == 3:  # RGB
                r, g, b = pixel
                new_color = (r, g, (b + 1) % 256)
            else:
                raise ValueError(f"Unexpected pixel format: {pixel}")
            
            if isinstance(new_color, tuple):
                img.putpixel((x, y), new_color)
            else:
                img = img.convert('L')
                img.putpixel((x, y), new_color)
            
            img.save(input_path, format=img.format)

        # 计算修改后的哈希值
        new_hash = calculate_image_hash(input_path)
        print(f"修改后图片哈希值: {new_hash}")
        print(f"成功处理图片: {input_path}")
    except (UnidentifiedImageError, OSError) as e:
        print(f"警告: 无法处理图片 {input_path}. 错误: {str(e)}")
    except Exception as e:
        print(f"警告: 处理图片时出错，跳过: {input_path}. 错误: {str(e)}")

def update_code_references(code_files, old_name, new_name):
    for file_path in code_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 更新图片名称引用
            updated_content = re.sub(r'(?<=["\'])' + re.escape(old_name) + r'(?=["\'])', new_name, content)
            
            if updated_content != content:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(updated_content)
                print(f"更新文件中的图片引用: {file_path}")
        except PermissionError:
            print(f"警: 无权限修改文件，跳过: {file_path}")
        except Exception as e:
            print(f"警告: 处理文件时出错，跳过: {file_path}. 错误: {str(e)}")

def process_imagesets(project_path, prefix):
    xcassets = find_xcassets(project_path)
    code_files = find_code_files(project_path)
    modifications = []
    
    for xcasset in xcassets:
        imagesets = find_imagesets(xcasset)
        for imageset in imagesets:
            old_name = os.path.basename(imageset).replace('.imageset', '')
            
            try:
                # 首先修改图片的哈希值，但不改变文件名
                contents_path = os.path.join(imageset, 'Contents.json')
                if not os.path.exists(contents_path):
                    print(f"警告: Contents.json 不存在，跳过: {imageset}")
                    continue

                with open(contents_path, 'r') as f:
                    contents = json.load(f)
                
                for image_info in contents['images']:
                    if 'filename' in image_info:
                        image_path = os.path.join(imageset, image_info['filename'])
                        if os.path.exists(image_path):
                            obfuscate_image(image_path)
                        else:
                            print(f"警告: 图片文件不存在，跳过: {image_path}")
                
                # 生成新名称
                new_name = generate_new_name(old_name, prefix)
                
                # 重命名 .imageset 目录
                new_imageset = os.path.join(os.path.dirname(imageset), f"{new_name}.imageset")
                os.rename(imageset, new_imageset)
                
                print(f"处理图片集: {old_name} -> {new_name}")
                
                # 记录修改
                modifications.append({
                    'old_name': old_name,
                    'new_name': new_name,
                    'path': os.path.relpath(new_imageset, project_path)
                })
                
                # 更新代码中的引用
                update_code_references(code_files, old_name, new_name)
            except PermissionError:
                print(f"警告: 无权限修改图片集，跳过: {imageset}")
            except FileNotFoundError:
                print(f"警告: 文件或目录不存在，跳过: {imageset}")
            except Exception as e:
                print(f"警告: 处理图片集时出错，跳过: {imageset}. 错误: {str(e)}")
    
    return modifications

def generate_excel_report(modifications, output_path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Image Obfuscation Report"

    # 添加表头
    ws.append(["Old Name", "New Name", "Path"])

    # 添加数据
    for mod in modifications:
        ws.append([mod['old_name'], mod['new_name'], mod['path']])

    # 调整列宽
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column_letter].width = adjusted_width

    wb.save(output_path)

def clean_empty_imagesets(project_path):
    xcassets = find_xcassets(project_path)
    cleaned_count = 0
    
    for xcasset in xcassets:
        for root, dirs, files in os.walk(xcasset):
            for dir in dirs:
                if dir.endswith('.imageset'):
                    imageset_path = os.path.join(root, dir)
                    contents_path = os.path.join(imageset_path, 'Contents.json')
                    
                    if not os.path.exists(contents_path):
                        try:
                            shutil.rmtree(imageset_path)
                            print(f"已删除空的 imageset: {imageset_path}")
                            cleaned_count += 1
                        except Exception as e:
                            print(f"警告: 无法删除 {imageset_path}. 错误: {str(e)}")
    
    print(f"清理完成，共删除 {cleaned_count} 个空的 imageset 文件夹。")

def main():
    parser = argparse.ArgumentParser(description="iOS项目图片混淆工具")
    parser.add_argument("--project", required=True, help="iOS项目路径")
    parser.add_argument("--prefix", default="", help="图片名称前缀")
    parser.add_argument("--output", default="obfuscation_report.xlsx", help="输出报告的Excel文件路径")
    args = parser.parse_args()
    
    project_path = args.project
    prefix = args.prefix
    output_path = args.output
    
    if not os.path.isdir(project_path):
        print(f"错误: {project_path} 不是有效的目录")
        return
    
    # 自动执行清理操作
    print("开始清理空的 imageset 文件夹...")
    clean_empty_imagesets(project_path)
    
    print("开始执行图片混淆操作...")
    modifications = process_imagesets(project_path, prefix)
    generate_excel_report(modifications, output_path)
    print(f"图片混淆完成，报告已生成: {output_path}")

if __name__ == "__main__":
    main()
