
# import openai
# openai.api_key = 'sk-gB4hO5dbzWBcDf2iB9A77302D1Ad47839dF76fEfDe83F599'
import json
import requests



def openai(content):
  api_key='sk-MWIphp0lKDogFTmvD18859F3BbEf49C2B7FfF37f1e9f22Ef'
  api_url='https://api.aiability.net/v1/chat/completions'

  original_text = '你好'
  headers={
      'Authorization': f'Bearer {api_key}',
      'Content-Type': 'application/json'
  }

  data={
      "model":'gpt-3.5-turbo',
      "messages":[
          {
              "role":"user",
              "content":content
          }
      ]
  }

  response = requests.post(api_url, data=json.dumps(data), headers=headers)
  if response.status_code == 200:
      result = response.json()
    #   print(result)
      return result
  else:
      print(f"Error: {response.status_code} - {response.text}")
  return None

# completion = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )

# print(completion.choices[0].message)
# openai.api_key = 'sk-gB4hO5dbzWBcDf2iB9A77302D1Ad47839dF76fEfDe83F599'

if __name__ == '__main__':
    result = openai('提取出来下面摄影作品的出品方,编号,人物名字,作品名字,{Pure Media Vol.224 Yeha (예하)   The Secret XXX Class}')
    print(result)



    