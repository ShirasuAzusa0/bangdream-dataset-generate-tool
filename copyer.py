"""
 copyer.py
 将下载的目录中的 *.asset 文件复制到 /assets 文件夹下，方便后面的数据处理
"""
import os
import shutil

ASSET_DIR = 'assets'

def copy_and_save():
    asset_dir = os.path.join(os.getcwd(), ASSET_DIR)

    # 不存在则创建新文件夹
    os.makedirs(asset_dir, exist_ok=True)

    # 计数器
    copy_count = 0
    overwritten_count = 0
    renamed_count = 0

    print("📂 assets move progress started...")

    for folder_name, _, filenames in os.walk('.'):
        # 跳过目标文件夹本身
        if os.path.abspath(folder_name) == os.path.abspath(asset_dir):
            continue

        for filename in filenames:
            if filename.lower().endswith('.asset'):
                src_path = os.path.join(folder_name, filename)

                # 设置目标文件路径
                dest_path = os.path.join(asset_dir, filename)

                # 处理文件名冲突
                counter = 1
                base_name, ext = os.path.splitext(filename)
                while os.path.exists(dest_path):
                    # 检查是否是完全相同的文件
                    if os.path.samefile(src_path, dest_path):
                        print(f"跳过自身：{src_path}")
                        break

                    # 生成新的文件名
                    new_filename = f"{base_name}_{counter}{ext}"
                    dest_path = os.path.join(asset_dir, new_filename)
                    counter += 1
                else:
                    # 文件被重命名了
                    if counter > 1:
                        renamed_count += 1
                        print(f"重命名以避免冲突：{filename} -> {os.path.basename(dest_path)}")

                    # 复制文件
                    shutil.copy2(src_path, dest_path)

                    if counter == 1 and os.path.exists(dest_path):
                        overwritten_count += 1
                        print(f"覆盖已有文件：{dest_path}")
                    else:
                        print(f"已复制：{src_path} -> {dest_path}")

                    copy_count += 1

    print("\nfinish! result:")
    print(f"- 📘total copied files: {copy_count}")
    print(f"- 📘total renamed files: {renamed_count}")
    print(f"- 📘total overwritten files: {overwritten_count}")
    print(f"- ✅all files have saved in: {asset_dir}")

if __name__ == '__main__':
    copy_and_save()