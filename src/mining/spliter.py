import re
content = open("books/PIH/data/book.tex").read()
chaps = re.split('\\chapter\*?\{[^\}]*}', content)
for i, chap in enumerate(chaps):
	open("books/PIH/data/chapter" + str(i) + ".tex", "write").write(chap)