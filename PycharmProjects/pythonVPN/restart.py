from subprocess import call, PIPE

call('wmic path win32_networkadapter where PhysicalAdapter=True call disable',
     shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
call('wmic path win32_networkadapter where PhysicalAdapter=True call enable',
     shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
