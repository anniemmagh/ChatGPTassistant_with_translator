import concurrent.futures
import requests
import re
import os
import html
import urllib.parse
from gpt import get_prompt

class GoogleTranslateRequest:

    def __init__(self, source_language='en', target_language='ka', timeout=5):
        self.source_language = source_language
        self.target_language = target_language
        self.timeout = timeout
        self.pattern = r'(?s)class="(?:t0|result-container)">(.*?)<'

    def make_request(self, target_language, source_language, text, timeout):
        escaped_text = urllib.parse.quote(text.encode('utf8'))
        url = 'https://translate.google.com/m?tl=%s&sl=%s&q=%s'%(target_language, source_language, escaped_text)
        response = requests.get(url, timeout=timeout)
        result = response.text.encode('utf8').decode('utf8')
        result = re.findall(self.pattern, result)
        if not result:
            print('\nError: Unknown error.')
            f = open('error.txt')
            f.write(response.text)
            f.close()
            exit(0)
        return html.unescape(result[0])

    def translate(self, text, target_language='ka', source_language='en', timeout=5):
        if not target_language:
            target_language = self.target_language
        if not source_language:
            source_language = self.source_language
        if not timeout:
            timeout = self.timeout
        if len(text) > 5000:
            print('\nError: It can only detect 5000 characters at once. (%d characters found.)'%(len(text)))
            exit(0)
        if type(target_language) is list:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.make_request, target, source_language, text, timeout) for target in target_language]
                return_value = [f.result() for f in futures]
                return return_value
        return self.make_request(target_language, source_language, text, timeout)

    def translate_file(self, file_path, target_language='ka', source_language='en', timeout='10'):
        if not os.path.isfile(file_path):
            print('\nError: The file or path is incorrect.')
            exit(0)
        f = open(file_path)
        text = self.translate(f.read(), target_language, source_language, timeout)
        f.close()
        return text

if __name__ == "__main__":
    translator = GoogleTranslateRequest()

    while True:
        user_input = input("სტუდენტი: ")
        if user_input.lower() in ["quit","exit","bye"]:
            break
        prompt = translator.translate(user_input, target_language='en', source_language="ka")

        answer = get_prompt(prompt)

        result = translator.translate(answer, target_language='ka',source_language="en")


        print(f"ბოტი: {result}")

