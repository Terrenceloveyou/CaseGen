
from openai import OpenAI

class Deepseek:
    def __init__(self, config):
        self.APIKey = config.get('api_key', "")
    def chat(self, req):
        client = OpenAI(api_key="sk-90fb39aeb8354bf193e7228920c9850d", base_url="https://api.deepseek.com")
        # 改一下 api key为config提取的

        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": req},
            ],
            stream=False
        )

        return response.choices[0].message.content
    
if __name__ == '__main__':
    ds = Deepseek({})
    print(ds.chat("你的平均返回时间是多少"))