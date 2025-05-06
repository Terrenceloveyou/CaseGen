from ds import Deepseek
from parse_swagger import SwaggerParser
import json,re

class DocExtract:
  def __init__(self, config, api_list):
    self.doc = None#todo：  config.doc  待修改
    self.api_list = api_list
    self.config = config
  def extract(self):

    # temp: 暂时这样写
    doc_path = "C:\\Users\\HP1\\Desktop\\paper\\vulnerable-petstore\\README.md"
    with open(doc_path, 'r', encoding='utf-8') as file:
      self.doc = file.read()

    # 只提取 path 和 method
    simplified_api_list = [
      {'path': api['path'], 'method': api['method']}
      for api in self.api_list
    ]

    prompt = f"""下面是接口文档：
    {self.doc}

    下面是接口文档中需要提取出来的 API 列表：
    {json.dumps(simplified_api_list, ensure_ascii=False)}

    请你从接口文档中提取出每个 API 的解释文段，并以 JSON 格式返回，格式如下：
    {{
    "apis": [
      {{
        "path": "API 路径",
        "method": "API 方法",
        "description": "API 的解释文段"
      }},
      ...
    ]
    }}
    """
    # 保存 prompt 到文本文件
    prompt_file_path = "C:\\Users\\HP1\\Desktop\\paper\\code\\CaseGen\\prompt\\prompT1.txt"
    with open(prompt_file_path, 'w', encoding='utf-8') as prompt_file:
      prompt_file.write(prompt)

    ds = Deepseek(self.config)
    response = ds.chat(prompt)
    print(response)

    # 使用正则表达式提取 JSON 
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        print()
        print(json_str)
        doc_api_list = json.loads(json_str)
    else:
        raise ValueError("无法从ds的回答中提取有效的 JSON 数据")
    
    for api in self.api_list:
      for doc_api in doc_api_list['apis']:
        if api['path'] == doc_api['path'] and api['method'] == doc_api['method']:
          api['doc'] = doc_api['description']
    return self.api_list
  

if __name__ == "__main__":
    swagger_file =  "C:\\Users\\HP1\\Desktop\\paper\\vulnerable-petstore\\petstore.json"
    parser = SwaggerParser(swagger_file)
    api_list = parser.api_list()
    ext = DocExtract({}, api_list)
    print(ext.extract())
