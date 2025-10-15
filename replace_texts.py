"""
 replace_texts.py
 替换对话文件 *.txt 中的特殊字符
 替换规则可按需自定义增加
"""
import os
# 替换规则配置
replacement_rules = {
    "「": "",
    "」": ""
}

# 保存路径
REPLACE_DIR = 'replaced_dialogs'
KEYWORD_RELATE_DIR = 'related_dialogs'

def replacer():
    replaced_dir = os.path.join(os.getcwd(), REPLACE_DIR)
    related_dir = os.path.join(os.getcwd(), KEYWORD_RELATE_DIR)

    # 不存在则创建新文件夹
    os.makedirs(replaced_dir, exist_ok=True)
    os.makedirs(related_dir, exist_ok=True)

    # 获取所有对话文件 *.txt
    dialog_files = [f for f in os.listdir('./dialogs')
                    if f.endswith('.txt') and os.path.isfile(os.path.join('./dialogs', f))]

    if not dialog_files:
        print("can't find any dialog files! (*.txt)")
        return

    processed_counter = 0

    for file in dialog_files:
        try:
            modified = False
            with open("dialogs/" + os.path.join(file), 'r', encoding='utf-8') as f:
                content = f.read()
                new_content = content
                for old_text, new_text in replacement_rules.items():
                    # 用精确字符串匹配
                    if old_text in new_content:
                        count = new_content.count(old_text)
                        new_content = new_content.replace(old_text, new_text)
                        modified = True
                        print(f"file {file}: change '{old_text}' -> '{new_text}' ({count} places)")
                f.close()

            # 有修改就保存
            if modified:
                with open(replaced_dir + "/" + os.path.join(file), 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    f.close()
                with open(related_dir + "/" + os.path.join(file), 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    f.close()
                processed_counter += 1
                print(f"{file} updated")
            else:
                print(f"{file} match failed")
        except Exception as e:
            print(f"❌ unexpected error appeared during {file} processing: {str(e)}")

    print(f"\n✅ processing finished! successfully updated {processed_counter}/{len(dialog_files)} files")

if __name__ == "__main__":
    replacer()