"""
 delete_unrelated.py
 删除不存在 KEYWORD 的文本文件
 把 KEYWORD 设置为角色名，去除与目标任务无关的剧情，方便后续调用大模型处理文本的成本
"""
import os
from replace_texts import KEYWORD_RELATE_DIR

# KEYWORD 设置
KEYWORD = "香澄"          # 按需进行修改

def delete_files_without_keyword():
    target_dir = os.path.join(os.getcwd(), KEYWORD_RELATE_DIR)

    for filename in os.listdir(target_dir):
        filepath = os.path.join(target_dir, filename)

        # 检查是否为文本文件
        if filename.endswith('.txt') and os.path.isfile(os.path.join(target_dir, filename)):
            try:
                # 检查文件是否包含关键词
                found = False
                with open(os.path.join(target_dir, filepath), 'r', encoding='utf-8') as f:
                    for line in f:
                        if KEYWORD in line:
                            found = True
                            break
                    f.close()

                # 如果不包含关键词则删除文件
                if not found:
                    os.remove(filepath)
                    print(f"delete file: {filename}")

            except Exception as e:
                print(f"❌ unexpected error appeared during {filename} processing: {str(e)}")

    print("✅ process finished! ")

if __name__ == "__main__":
    delete_files_without_keyword()