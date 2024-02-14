import subprocess

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def make_pdf(file_name, out):
    code_x = open(file_name, "r").readlines()
    code_x.extend(out)
    open(f"{file[:-3]}.txt", "w")
    ff = 0
    f = open(f"{file[:-3]}.txt", "a")
    c = canvas.Canvas(f"{file[:-3]}.pdf", pagesize=letter)
    c.setFont("Helvetica", 12)

    while ff != len(code_x) - 1:
        for i in range(700, 100, -20):
            line = code_x[ff].replace('\n', '')
            c.drawString(100, i, line)
            f.write(line)
            if ff == len(code_x) - 1:
                break
            ff += 1
        c.showPage()
    c.save()


file = '1.py'
output = subprocess.getoutput(f"python {file} {11}").split('\n')
make_pdf(file, output)

file = '2.py'
output = subprocess.getoutput(f"python {file}").split('\n')
make_pdf(file, output)

file = '3.py'
output = subprocess.getoutput(f"python {file} {11}").split('\n')
make_pdf(file, output)

file = '4.py'
output = subprocess.getoutput(f"python {file} {11}").split('\n')
make_pdf(file, output)

file = '5.py'
output = subprocess.getoutput(f"python {file} {11}").split('\n')
make_pdf(file, output)