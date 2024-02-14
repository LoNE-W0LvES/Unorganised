import pandas as pd


def check_ref(refer, df):
    ref_browser = pd.DataFrame(columns=['Reference', 'BibTex', 'EndNote', 'RefMan'])
    for ff in range(len(refer)):
        ref = refer['Reference'][ff]
        try:
            index_ref = df.loc[df['Reference'] == ref].index[0]
            print(index_ref)
            bib_check = df['BibTex'][index_ref]
            if bib_check is None or not pd.notna(bib_check):
                ref_browser = pd.concat([ref_browser, refer.iloc[[ff]]], ignore_index=True)
        except IndexError:
            ref_browser = pd.concat([ref_browser, refer.iloc[[ff]]], ignore_index=True)
    return ref_browser
