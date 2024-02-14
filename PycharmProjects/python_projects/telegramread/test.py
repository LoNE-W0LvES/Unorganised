import urllib.request
from bs4 import BeautifulSoup
import requests, warnings


def get_questions():
    TEST_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSdrgTYowTpH6lIMYNecgrfA3zrfz5YCBJ4uqj2HXKiid45GDQ/viewform"

    res = urllib.request.urlopen(TEST_FORM)
    soup = BeautifulSoup(res, 'html.parser')
    # print(soup)
    for para in soup.find_all("p"):
        print(para.get_text())

    #
    # get_names = lambda f: [v for k,v in f.attrs.items() if 'label' in k]
    # get_name = lambda f: get_names(f)[0] if len(get_names(f))>0 else 'unknown'
    # all_questions = soup.form.findChildren(attrs={'name': lambda x: x and x.startswith('entry.')})


    # print(get_names)
    # print(get_name)
    # print(all_questions)
    # return {get_name(q): q['name'] for q in all_questions}

get_questions()
def submit_response(form_url, cur_questions, verbose=False, **answers):
    submit_url = form_url.replace('/viewform', '/formResponse')
    form_data = {'draftResponse':[],
                'pageHistory':0}
    print(form_data)
    for v in cur_questions.values():
        form_data[v] = ''
    for k, v in answers.items():
        if k in cur_questions:
            form_data[cur_questions[k]] = v
        else:
            warnings.warn('Unknown Question: {}'.format(k), RuntimeWarning)
    if verbose:
        print(form_data)
    user_agent = {'Referer':form_url,
                  'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"}
    return requests.post(submit_url, data=form_data, headers=user_agent)

