
import re

# 示例字符串
text = "鱼子酱Fish – 内购无水印 顺风车[752MB-82photos]"
text = 'Pure Media Vol.283 – Jia (지아) Tie me up with a rope[592MB-174photos]'
# text = '[SEESHE] HANNA – Chapter 03[611MB-67photos]'
text = '虎森森-阿努比斯[78MB-88photos]'
# 正则表达式提取最后一个方括号内的内容
match = re.search(r'\[([^\[\]]*)\]$', text)
if match:
    content_inside_brackets = match.group(1)
    print("提取的最后一个方括号内的内容：", content_inside_brackets)

    # 去除末尾的方括号内容
    cleaned_text = re.sub(r'\[([^\[\]]*)\]$', '', text).strip()
    print("清理后的内容：", cleaned_text)

    # 分割剩余的字符串，这里假设使用 " – " 进行分割
    parts = cleaned_text.rsplit("–", 1)  # 使用 rsplit 来确保只从最后一个破折号分割
    if len(parts) == 2:
        part_one, part_two = parts
        print("第一部分：", part_one)
        print("第二部分：", part_two)
    else:
        print("分割后不符合预期的两部分")
else:
    print("没有找到匹配的方括号内容")
