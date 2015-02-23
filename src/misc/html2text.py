import html2text
import sys

def main(file, args):
    h = html2text.HTML2Text()
    if "--ignore-links" in args:
	h.ignore_links = True
    if "--protect-links" in args:
	h.protect_links = True
    if "--ignore-images" in args:
	h.ignore_images = True
    if "--images-to-alt" in args:
	h.images_to_alt = True
    if "--google-doc" in args or "-g" in args:
	h.google_doc = True
    if "--dash-unordered-list" in args or "-d" in args:
	h.dash_unordered_list = True
    if "--hide-strikethrough" in args or "-s" in args:
	h.hide_strikethrough = True
    if "--escape-all" in args:
	h.escape_all = True
    if "--bypass-tables" in args:
	h.bypass_tables = True
    if "--single-line-break" in args:
	h.single_line_break = True
    with open(file, "r") as html:
	return result = h.handle(html)



if __name__ == "__main__":
  print main(sys.argv[1],sys.argv[2:])