"""
 filter_dialogs.py
 使用 LLM 筛选目标角色在场的对话片段
"""
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from openai import OpenAI, OpenAIError

# LLM API 配置
API_KEY = "YOUR_API_KEY"            # 这里放你自己的 LLM API KEY
MODEL_NAME = "YOUR_MODEL_NAME"      # 这里放你自己的 LLM 名称
OPENAI_BASE_URL = "YOUR_URL"        # 这里放你的大模型地址
MAX_WORKERS = 5
WAIT_SECONDS = 15                   # 余额不足时的等待时间（可自调整）

# 保存路径
FILTER_DIALOG_DIR = 'filtered_dialogs'
RELATED_DIALOG_DIR = 'related_dialogs'

SYSTEM_PROMPT = """
你是一个对话场景筛选助手。任务目标：**从输入文本中保留所有“目标角色在场”的完整场景片段**，并以严格指定的格式输出，方便后续程序直接处理。

输入文本说明：
- 文本由若干对话块组成。对话块之间可能用三条连字符 `---` 明确分隔，或者用一个或多个空行分隔。把任意一处 `---` 或一段连续空行视为“场景边界”。
- 每行通常为“角色名: 说话内容”。可能有换行导致的续行（即某些行没有冒号），这些应当被归并为上一个有角色标识的台词的延续。

严格输出规则（请**严格**遵守，不要多写一字）：
1. 将输入切分成若干“场景块”（以 `---` 或空行为分界）。对于每个场景块：
   - 如果该场景块中**至少出现一次目标角色名**（精确匹配，例如“香澄”），则**输出该整个场景块的所有对话行**（保持原有顺序）；
   - 如果该场景块中**不包含目标角色名**，则**忽略此场景块**（不输出）。
2. 场景块内部处理：
   - 每个角色的一条发言应占一行，格式为：`角色名: 发言内容`（冒号请使用英文冒号 `:`）。
   - 如果某一行不包含冒号（例如因换行断开），将该行视为“上一行发言的续行”，并拼接（以空格或直接连接都可），最终依然输出为单行 `角色名: 完整内容`。
   - 保留场景中所有其他角色的发言（不要只输出目标角色）。
3. 场景之间：如果多个场景被保留，按原顺序用单独一行 `---` 分隔（即输出中也使用 `---` 作为场景边界）。
4. 内容约束：**不得输出任何解释、注释、元信息、原因说明或多余文字**。输出只能包含对话行与 `---`。每行都必须是对话或分隔符。
5. 如果输入中没有任何场景包含目标角色，则**输出空内容**（即不输出任何对话行）。
6. 切勿改变角色名拼写或台词内容（仅允许合并因换行导致的多行为单行）。
7. 输出必须保留原始对话的顺序与相对内容完整性，不作删节（除了删除完全不含目标角色的场景块之外）。

示例 1（输入）：
里美: 哇~！快看！
香澄: 能够一边欣赏这样的美景……
我真是好幸福啊~
沙绫: 是啊
（空行）
香澄: 我回来了
里美: 欢迎回来

示例 1（输出）：
里美: 哇~！快看！
香澄: 能够一边欣赏这样的美景…… 我真是好幸福啊~
沙绫: 是啊
---
香澄: 我回来了
里美: 欢迎回来

示例 2（输入，不包含目标角色）：
A: 你好
B: 早上好

示例 2（输出）：
（空输出）

【目标角色】：香澄
"""

client = OpenAI(api_key=API_KEY, base_url=OPENAI_BASE_URL)

def process_file(dialog_file_path:Path, output_dir: Path):
    clipped_path = output_dir / (dialog_file_path.stem + "_clipped.txt")
    if clipped_path.exists():
        print(f"[skip] {clipped_path} existed")
        return

    print (f"[process] {dialog_file_path}")

    # 处理 402 返回，循环等待至成功
    while True:
        try:
            with dialog_file_path.open("r", encoding="utf-8") as f:
                user_prompt = f.read()
                f.close()

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )

            result = response.choices[0].message.content.strip()

            with clipped_path.open("w", encoding="utf-8") as f:
                f.write(result)
                f.close()

            print(f"[finish] {clipped_path.name} saved")
            break  # 成功后跳出循环
        except OpenAIError as e:
            # 请求速率限制
            if "429" in str(e):
                print(f"[error] {dialog_file_path.name} error: {e}")
                print(f"[limit] {dialog_file_path.name} wait for {WAIT_SECONDS} seconds and retry...")
                time.sleep(WAIT_SECONDS)
                continue  # 重新尝试
            else:
                print(f"[error] {dialog_file_path.name} error: {e}")
                break
        except Exception as e:
            print(f"[error] {dialog_file_path.name} error: {e}")
            break

def main():
    filtered_dir = Path.cwd() / FILTER_DIALOG_DIR
    related_dir = Path.cwd() / RELATED_DIALOG_DIR

    # 不存在则创建新文件夹
    os.makedirs(filtered_dir, exist_ok=True)

    dialog_files = [f for f in related_dir.glob("*.txt") if not f.name.endswith("_clipped.txt")]

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_file = {executor.submit(process_file, f, filtered_dir): f for f in dialog_files}
        for future in as_completed(future_to_file):
            future.result()

    print("✅ process finished! ")

if __name__ == "__main__":
    main()