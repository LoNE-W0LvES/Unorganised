from PyPDF2 import PdfReader
import openai

reader = PdfReader('sadf.pdf')
print(len(reader.pages))
strX = []
for i in reader.pages:
    try:
        textEX = i.extract_text()
        text = textEX.replace('\r', '').replace('\x81', '')
        strX.append(text)
    except UnicodeEncodeError as e:
        print(e)


print(len(strX))

ss = ' '.join(strX).split('References')
dd = ss[len(ss) - 1]


openai.api_key = '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'

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": f'{dd} make a list without numbering'}
  ]
)

print(completion.choices[0].message.content.split('\n'))
print()
print()










