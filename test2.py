import re
from http import HTTPStatus
import dashscope
import json
result_data=[]
dashscope.api_key = 'sk-a27bbf526e9e44bd9002a0b7fa05eb48'  # 填入通义千问的 APIKEY



def call_with_messages(messages):
    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',  # 设置返回结果为对话消息格式
    )
    if response.status_code == HTTPStatus.OK:
        return response.output.choices[0].message.content
    else:
        return None


def process_json_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    global result_data
    for item in data:
        try:
            user_input = 'input:' + item['input'] + '\n\noutput:' + item[
                'output'] + '\n\n' + '请你帮我把这两段文字稍作修改，变成有逻辑的问答对,并且以\n\n问：....\n\n答：...\n\n的形式进行回复'
            print(item['id'])
            print(user_input)
            messages = [{'role': 'system', 'content': '你是一位语文老师，请用中文的标点符号进行符合我要求的格式的回答'},
                        {'role': 'user', 'content': user_input}]
            chat_response = call_with_messages(messages)

            if chat_response:
                print(chat_response)
                #将英文标点转化为中文标点
                chat_response = chat_response.replace(":", "：")
                response_parts=re.split(r'问：|答：',chat_response)
                conversations_list=[]
                if len(response_parts) % 2 == 0 or len(response_parts) == 1:
                    result_data.append({"id":item["id"],"conversation": chat_response})
                else:
                    for i in range(1, len(response_parts), 2):
                        question = response_parts[i].strip() if i > 0 and i < len(response_parts) else ''
                        answer = response_parts[i + 1].strip() if i + 1 > 0 and i + 1 < len(response_parts) else ''
                        conversations_list.append({'input': question, 'output': answer})
                    result_data.append({"id":item["id"],"conversation": conversations_list})
                # response_parts = chat_response.split("答：")
                # if len(response_parts)>=2:
                #     question = response_parts[0].replace("问：", "").strip()
                #     answer = response_parts[1].strip()
                #     result_data.append({'id':item['id'],'input': question, 'output': answer})
                # else:
                #     #处理未找到”答：“的情况
                #     result_data.append({'id':item['id'],'input': 'unnormal', 'output': chat_response})
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            continue

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    input_file_path = 'all4000-6000.json'
    output_file_path = 'result/result4000-6000.json'

    try:
        process_json_file(input_file_path, output_file_path)
    except Exception as e:
        print(f"An error occurred during the process: {str(e)}")
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)