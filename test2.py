from http import HTTPStatus
import dashscope
import json

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

    result_data = []
    for item in data:
        user_input = 'input:' + item['input'] + '。output:' + item[
            'output'] + '/n/n' + '请你帮我把这两段文字稍作修改，变成有逻辑的一问一答,并且以问：..../n/n答：...的形式进行回复'
        print(user_input)
        messages = [{'role': 'system', 'content': '你是一位语文老师'},
                    {'role': 'user', 'content': user_input}]
        chat_response = call_with_messages(messages)

        if chat_response:
            response_parts = chat_response.split("答：")
            question = response_parts[0].replace("问：", "").strip()
            answer = response_parts[1].strip()
            result_data.append({'input': question, 'output': answer})
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    input_file_path = 'test.json'
    output_file_path = 'your_output_json_file_path.json'

    process_json_file(input_file_path, output_file_path)
