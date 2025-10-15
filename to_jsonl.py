"""
 to_jsonl.py
 遍历 /filtered_dialogs 内的 *.txt 文件，转化为 shareGPT 格式
 完成训练数据集的构建
"""
import os
import json
import re

# 角色选择与输出配置
TARGET_ROLE = "香澄"
OUTPUT_JSONL_DIR = 'Output_JSONL'
OUTPUT_FILE = "./Output_JSONL/dataset.jsonl"

def build_dataset_with_responses(target_role, prompt_template=None):
    output_dir = os.path.join(os.getcwd(), OUTPUT_JSONL_DIR)
    os.makedirs(output_dir, exist_ok=True)

    if prompt_template is None:
        prompt_template = f"你是角色{target_role}，现在正在和其他人进行对话，请以{target_role}的口吻进行自然回应。"

    dataset = []

    dir_path = os.path.join(os.getcwd(), "filtered_dialogs")

    for filename in os.listdir(dir_path):
        if not filename.endswith('.txt'):
            continue

        file_path = os.path.join(dir_path, filename)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            f.close()

        # 用 --- 分割出不同的对话块
        conversations = re.split(r'-{3,}', content)

        for conv in conversations:
            conv = conv.strip()
            if not conv:
                continue

            lines = [line.strip() for line in conv.split('\n') if line.strip()]
            conversation_history = []

            for i, line in enumerate(lines):
                if line.startswith(f'{target_role}:'):
                    # 提取指定角色的对话话语
                    role_line = line.split(':', 1)[1].strip()

                    messages = [
                        {"role": "system", "content": prompt_template}
                    ]

                    # 构造对话历史
                    for msg in conversation_history:
                        if msg.startswith(f'{target_role}:'):
                            content = msg.split(':', 1)[1].strip()
                            messages.append({
                                "role": "assistant",
                                "content": content
                            })
                        else:
                            messages.append({
                                "role": "user",
                                "content": msg
                            })

                    # 当前发言作为 assistant 响应
                    messages.append({
                        "role": "assistant",
                        "content": role_line
                    })
                    dataset.append({"messages": messages})

                # 无论是谁说的话，都放到对话历史中
                conversation_history.append(line)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"✅ dataset created successfully with {len(dataset)} samples")
    print(f"✅ dataset has been saved in {OUTPUT_FILE}")

if __name__ == '__main__':
    build_dataset_with_responses(target_role=TARGET_ROLE)
