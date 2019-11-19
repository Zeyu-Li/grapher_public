import os, winshell

url = 'https://docs.google.com/spreadsheets/d/'
path = os.path.join("C:/Users/zeyul/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup", "important.url")
if os.path.exists(path):
    os.remove(path)
with open(path, 'w') as fp:
    fp.write(f'[InternetShortcut]\n')
    fp.write('URL=%s' % url)