from pyrevit import revit, DB, script, forms

output = script.get_output()
output.close_others()

doc = revit.doc

legends = [
    x for x in DB.FilteredElementCollector(doc)
    .OfCategory(DB.BuiltInCategory.OST_Views)
    .WhereElementIsNotElementType()
    .ToElements()
    if x.ViewType == DB.ViewType.Legend]

legends_ids = [x.Id.IntegerValue for x in legends]

sheets = (
    DB.FilteredElementCollector(doc)
    .OfCategory(DB.BuiltInCategory.OST_Sheets)
    .WhereElementIsNotElementType()
    .ToElements()
)

results = []

for sheet in sheets:
    vps = sheet.GetAllPlacedViews()
    for vp in vps:
        if vp.IntegerValue in legends_ids:
            results.append((output.linkify(doc.GetElement(vp).Id), doc.GetElement(
                vp).Name, output.linkify(sheet.Id), sheet.SheetNumber, sheet.Name))

if len(results) != 0:
    results = sorted(results, key=lambda x: (x[1], x[3]))
    output.print_md("## Legends on Sheets")
    headers = ["Legend selector", "Legend Name",
               "Sheet selector", "Sheet Number", "Sheet Name"]
    output.print_table(results, headers)
else:
    forms.alert("No legends found on sheets.")
