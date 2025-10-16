# Bang Dream! Dataset generator

## 😋简介
本项目是一套适用于处理《BanG Dream!》相关剧情文件构建数据集，用于进行 LLM 微调与训练的自动化脚本

## 📁项目结构
1. **数据收集**
2. **数据处理**
3. **数据存储**

## 🔑使用说明
### 🧰可改配置项
每个脚本文件中都有集中的配置区，根据注释按需进行修改即可

每个脚本文件下载或处理得到的文件存储的路径可以自定义修改，下面的数据下载处理教程使用的是默认设置，使用者可按需调整

### ⬇️数据收集
运行`downloader.py`下载邦邦的剧情文件到`/Downloaded_Stories`路径下，也可以根据自己的需要下载不同的剧情文件，具体选择已通过注释给出，默认条件下下载主线剧情文件

### 📄数据处理
运行`copyer.py`提取`/Downloaded_Stories`路径下的`*.asset`文件到`/assets`中，方便后面的数据处理

运行`to_dialogs.py`将`/assets`中的`*.asset`文件转化成对话文本形式并保存到`/dialogs`路径下，格式样例如下：
``` 
灯: 「啊……」
爽世:「小祥！
太好了~你来了！」
睦・立希: 「…………」
爽世: 「我们一直都很担心你哦。
不仅学校那边请假，还完全不回消息——」
祥子: 「今天我是有话要说才来的」
祥子: 「……我要退出CRYCHIC」
```

运行`replace_text.py`替换对话文件`*.txt`中的特殊字符，替换规则可按需自定义增加，默认条件下只处理"「"和"」"这俩特殊符号，处理后默认保存到`/replaced_dialogs`路径下，处理后的格式如下：
``` 
灯: 啊……
爽世: 小祥！太好了~你来了！
睦・立希: …………
爽世: 我们一直都很担心你哦。不仅学校那边请假，还完全不回消息——
祥子: 今天我是有话要说才来的
祥子: ……我要退出CRYCHIC
```

运行`delete_unrelated.py`从`/replaced_dialogs`中提取出包含指定角色（通过KEYWORD配置项设定，需要哪个角色就写哪个角色的名字）的对话文件`*.txt`，保存到`related_dialogs`路径下，降低后续调用大模型处理文本的成本

运行`filter_dialogs.py`，使用 LLM 筛选目标角色在场的对话片段，处理得到的文件统一放到`/filtered_dialogs`路径下，格式和`/replaced_dialogs`下的类似，但是只保留了指定角色登场的部分

运行`to_jsonl.py`，遍历`/filtered_dialogs`内的`*.txt`文件，转化为 shareGPT 格式，完成训练数据集的构建，格式如下：
```json
   {
     "messages": [
       {"role": "system", "content": "爱音是...你是角色爱音..."},
       {"role": "user", "content": "立希: ..."},
       {"role": "assistant", "content": "爱音: ..."}
     ]
   }
```

## 📂脚本文件列表
| 脚本名                   | 功能简述           |
|-----------------------| -------------- |
| `downloader.py`       | 批量下载剧情`.asset`文件 |
| `copyer.py`           | 整理并统一收集所有`.asset`文件 |
| `to_dialogs.py`       | 将`.asset`文件转为文本对话格式 |
| `replace_texts.py`    | 去除特殊字符         |
| `delete_unrelated.py` | 删除与目标角色无关的对话文本 |
| `filter_dialogs.py`   | 使用 LLM 筛选目标角色在场的对话片段 |
| `to_jsonl.py`         | 生成 ShareGPT 格式的训练数据集 |

## ❗注意事项
* 若发现某些剧情有错漏，可能源于原始来源不一致
* 若发现本项目存在bug请通过 issue 告知，我会尽快修复
* 大模型 API 调用可能因频次限制报错，请适当设置 `MAX_WORKERS`（已有默认值）

> 🚫 本项目禁止用于商业用途。如你使用本项目生成dataset，或者用所生成的数据训练 AI，请注明原作者信息

> **提示**：本项目涉及的所有剧情文件归属权属于 Bushiroad，本项目不拥有这些剧情内容，仅用于技术研究与教学用途  
> **鸣谢**：感谢 [bestdori.com](https://bestdori.com/) 提供的数据整理支持，但请不要滥用爬虫或大量使用下载脚本，以免给其服务器造成不必要的负担  
> **特别鸣谢**：感谢 [ChaRoSaMa](https://github.com/ChaRoSaMa) 的开源项目提供的灵感