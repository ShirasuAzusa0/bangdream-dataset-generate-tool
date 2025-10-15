"""
 to_dialogs.py
 将 *.asset 文件转化成对话文本形式并保存到 /dialogs 路径下，格式样例如下：
 # 灯: 「啊……」
 # 爽世:「小祥！
 # 太好了~你来了！」
 # 睦・立希: 「…………」
 # 爽世: 「我们一直都很担心你哦。
 # 不仅学校那边请假，还完全不回消息——」
 # 祥子: 「今天我是有话要说才来的」
 # 祥子: 「……我要退出CRYCHIC」
"""
import glob
import json
import os.path
import re

DIALOG_DIR = 'dialogs'

# 处理 JSON 文件并导出成文本格式
def process_json_file(input_path):
    dialog_dir = os.path.join(os.getcwd(), DIALOG_DIR)

    # 不存在则创建新文件夹
    os.makedirs(dialog_dir, exist_ok=True)

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            f.close()

        # 提取基础文件名
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(dialog_dir, f"{base_name}.txt")

        base = data.get("Base", [])
        talk_data = base.get("talkData", [])
        output_lines = []

        for item in talk_data:
            name = item.get("windowDisplayName", "")
            body = item.get("body", "")
            # 去除 body 键值中可能出现的额外的引号
            cleaned_body = re.sub(r'^["“]+|["”]+$', '', body)
            output_lines.append(f"{name}: 「{cleaned_body}」")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))
            f.close()

        print(f"✅ : {input_path} -> {output_path} ({len(output_lines)} dialogs changed successfully)")
        return True

    except Exception as e:
        print(f"❌ process failed {input_path}: {str(e)}")
        return False

def main():
    # 获取当前目录下的所有匹配的JSON文件（也即经copyer整理后的所有 *.asset 文件）
    # 通过 asset/*-*.asset 规避掉之前 download 时有问题的文件
    json_files = glob.glob('assets/*-*.asset')

    if not json_files:
        print("can't match any JSON file in mode *-*.json")
        return

    print(f"find {len(json_files)} JSON files waiting to process...")
    success_counter = 0

    for json_file in json_files:
        if process_json_file(json_file):
            success_counter += 1

    print("\n processing finished!")
    print(f"✅ success: {success_counter}/{len(json_files)} files")
    print(f"❌ fail: {len(json_files) - success_counter} files")

if __name__ == "__main__":
    main()