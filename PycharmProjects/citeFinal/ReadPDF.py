import re

from refextract import extract_references_from_file
import pandas as pd


def read_pdf(pdf_name_list):
    ref_data = []
    pattern = r'\[\d+\]'
    for pdf in pdf_name_list:
        references = []
        ref = extract_references_from_file('./pdf/' + pdf)
        for i in ref:
            if i['raw_ref'][0] not in references:
                references.append(i['raw_ref'][0])

        f_ref, nf_ref, temp = [], [], []

        for line in references:
            if line.endswith("."):
                if bool(re.findall(pattern, line)):
                    for t in temp:
                        f_ref.append(t.strip())
                    temp.clear()
                f_ref.append((" ".join(temp) + " " + line).strip() if temp else line.strip())
                temp.clear()
            else:
                temp.append(line)

        for line in f_ref:
            if [x for x in [re.findall(pattern, line) for pattern in
                            [r'\(\d{4}, [A-Za-z]+\)', r'\([A-Za-z]+, \d{4}\)', r'\((\d{4})\)']] if x]:
                if bool(re.findall(pattern, line)):
                    nf_ref.append(line)
                    temp.clear()
                else:
                    nf_ref.append((" ".join(temp)).strip() if len(temp) == 0 else "".join(temp).strip())
                temp.clear()
                temp.append(line)
            else:
                if bool(re.findall(pattern, line)):
                    nf_ref.append(line)
                    temp.clear()
                temp.append(line)
        nf_ref = [re.sub(pattern, '', line).split('Available at')[0] for line in nf_ref if line]
        nf_ref = [line[1:] if line[0] == ' ' else line for line in nf_ref]
        for x in nf_ref:
            ref_data.append({'Reference': x, 'BibTex': None, 'EndNote': None, 'RefMan': None})

    df = pd.DataFrame(ref_data)

    return df
