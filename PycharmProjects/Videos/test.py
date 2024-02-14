from subprocess import PIPE, Popen

new_scheme = str(Popen('powercfg /GetActiveScheme', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE
                       ).communicate()[0].decode("utf-8")).replace(')', '').split('(')

print(new_scheme)