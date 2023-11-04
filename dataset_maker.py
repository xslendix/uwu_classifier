import json
import os
import requests

input_file_path = "train.json"

output_file_path = "messages.txt"

if not os.path.exists(input_file_path):
    print('Downloading Topical Chat dataset')
    url = "https://raw.githubusercontent.com/alexa/Topical-Chat/master/conversations/train.json"
    response = requests.get(url)
    with open(input_file_path, 'wb') as file:
        file.write(response.content)

with open(input_file_path, 'r') as json_file, open(output_file_path, 'w') as output_file:
    data = json.load(json_file)

    for key, value in data.items():
        if "content" in value:
            for message_item in value["content"]:
                if "message" in message_item:
                    message = message_item["message"]
                    output_file.write(message + '\n')

print("Messages extracted and saved to", output_file_path)

# Split 50/50
input_file_path = "messages.txt"

output_file_path_1 = "messages_to_be_uwuified.txt"
output_file_path_2 = "messages_good.txt"

with open(input_file_path, 'r') as input_file:
    messages = input_file.readlines()

split_point = len(messages) // 2

messages_split_1 = messages[:split_point]
messages_split_2 = messages[split_point:]

with open(output_file_path_1, 'w') as output_file_1:
    output_file_1.writelines(messages_split_1)

with open(output_file_path_2, 'w') as output_file_2:
    output_file_2.writelines(messages_split_2)

print("Messages split into two files:", output_file_path_1, "and", output_file_path_2)
