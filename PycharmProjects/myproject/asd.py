import re
from refextract import extract_references_from_file


def extract_ref(pdfs):
    ref_dat = []
    for pdf in pdfs:
        references = []
        ref = extract_references_from_file(pdf)
        for i in ref:
            if i['raw_ref'][0] not in references:
                references.append(i['raw_ref'][0])
        f_ref, nf_ref, temp = [], [], []
        for line in references:
            if line.endswith("."):
                if bool(re.findall(r'\[\d+\]', line)):
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
                if bool(re.findall(r'\[\d+\]', line)):
                    nf_ref.append(line)
                    temp.clear()
                else:
                    nf_ref.append((" ".join(temp)).strip() if len(temp) == 0 else "".join(temp).strip())
                temp.clear()
                temp.append(line)
            else:
                if bool(re.findall(r'\[\d+\]', line)):
                    nf_ref.append(line)
                    temp.clear()
                temp.append(line)
        nf_ref = [re.sub(r'\[\d+\]', '', x) for x in nf_ref if x]
        ref_dat.extend(nf_ref)
