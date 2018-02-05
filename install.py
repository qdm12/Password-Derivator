import pip
from sys import version_info
from sys import argv

def install(packages, pipOptions=[]):
    for package in packages:
        pip.main(['install', package] + pipOptions)

if __name__ == '__main__':
	install(["argon2_cffi"])
	if version_info[0] == 2:
		install("pysha3")
	for arg in argv[1:]:
		if arg == "terminal":
			install(["qrcode", "pyperclip"])
		elif arg == "ui":
			install(["kivy", "kivy.deps.sdl2", "kivy.deps.glew"])
		elif arg == "dev":
			install(["nose", "rednose", "coverage", "coveralls"])
			if version_info[0] == 2:
				install(["mock"])