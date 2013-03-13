import csv

def fromCsv(stem):
    reader = csv.reader(open(stem+".csv", 'rb'), delimiter=',', quotechar='"')
    return [x for x in reader]
    
def applyMacro(rows, pos, macro):
    for row in rows:
        column = 0
        for cell in row:
            if (column==pos and cell!=""):
                row[column] = "\\" + macro + "{" + cell + "}"
            column += 1

def dropColumn(rows, pos):
    for row in rows:
        row.pop(pos)

def moveColumn(rows, posFrom, posTo):
    for row in rows:
        cell = row.pop(posFrom)
        row.insert(posTo, cell)

def toTeX(rows, stem):
    writer = open(stem+".tex", 'w')
    for row in rows:
        column = 0
        line = ""
        for cell in row:
            if (column>0):
                line += " & "
                if (cell=="True"):
                    cell = "\\trueCell{}"
                else:
                    if (cell=="False"):
                        cell = "\\falseCell{}"
                    else:
                        if (cell=="0"):
                            cell = "\\zeroCell{}"
            line += cell
            column += 1
        writer.write(line + "\\tableNl\n")

stem = "wikilists/wikiImpllist"
rows = fromCsv(stem)
rows.pop(0)
moveColumn(rows, 2, 9)
moveColumn(rows, 2, 9)
moveColumn(rows, 6, 2)
moveColumn(rows, 6, 3)
list.sort(rows, key=lambda row: int(row[2]))
applyMacro(rows, 0, "implementationName")
applyMacro(rows, 1, "headline")
toTeX(rows, stem)

stem = "wikilists/wikilanglist"
rows = fromCsv(stem)
rows.pop(0)
dropColumn(rows, 2)
dropColumn(rows, 3)
dropColumn(rows, 3)
list.sort(rows, key=lambda row: int(row[2]), reverse=True)
applyMacro(rows, 0, "languageName")
applyMacro(rows, 1, "headline")
toTeX(rows, stem)

stem = "wikilists/wikitechlist"
rows = fromCsv(stem)
rows.pop(0)
dropColumn(rows, 2)
dropColumn(rows, 3)
dropColumn(rows, 3)
list.sort(rows, key=lambda row: int(row[2]), reverse=True)
applyMacro(rows, 0, "technologyName")
applyMacro(rows, 1, "headline")
toTeX(rows, stem)

stem = "wikilists/wikifeatlist"
rows = fromCsv(stem)
rows.pop(0)
dropColumn(rows, 2)
dropColumn(rows, 3)
dropColumn(rows, 3)
list.sort(rows, key=lambda row: int(row[2]), reverse=True)
applyMacro(rows, 0, "featureName")
applyMacro(rows, 1, "headline")
toTeX(rows, stem)

stem = "wikilists/wikitermlist"
rows = fromCsv(stem)
rows.pop(0)
dropColumn(rows, 2)
dropColumn(rows, 3)
applyMacro(rows, 0, "termName")
applyMacro(rows, 1, "headline")
applyMacro(rows, 3, "linkok")
toTeX(rows, stem)
