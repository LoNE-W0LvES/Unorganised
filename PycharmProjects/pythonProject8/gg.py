
ht = open('w.html', 'r').read().split('</tbody></table>')


new_arr = [m.replace('\n', '').replace('<font color="red">', '').replace('</font>', '').replace('</td></tr><tr',
                                                                                                        '</td><td valign="top">').split(
            '</td><td valign="top">')[1:9] for m in ht if '</td><td valign="top">' in m.lower()]
print(new_arr)
print(len(new_arr))

# for i in new_arr:
