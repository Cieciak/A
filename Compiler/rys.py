import os, sys

try:
	work_d = ''
	for i in sys.argv[0].split('\\')[:-1]:
		work_d += i + '\\'
	
	os.chdir(work_d)
	
	file_name = sys.argv[1]
	
	out = file_name.split('.')[0]
	
	os.system(f'Translator.exe "{out}.a" -s')
	os.system(f'ml64.exe /Fo "{out}.obj" {out}.asm /link /OUT:"{out}.exe" /entry:main')
	os.remove(f'{out}.obj')
	os.remove(f'{out}.asm')
except:
	print(sys.exc_info()[1])