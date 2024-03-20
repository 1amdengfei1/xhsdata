import json
import re

# 提取中文汉字的正则表达式
pattern = re.compile(r'[\u4e00-\u9fa5]+')

new_data = []

# 从原始数据文件中读取数据
with open('all.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    # 提取标题中的中文汉字部分
    title_cn = ''.join(pattern.findall(item['title']))

    # 提取描述中的中文汉字部分
    desc_cn = ''.join(pattern.findall(item['desc']))

    new_item = {
        "input": title_cn,
        "output": desc_cn
    }

    new_data.append(new_item)

# 保存提取后的数据到新的JSON文件
with open('extracted_data.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

