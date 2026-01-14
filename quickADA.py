#THE IDEA OF THIS SCRIPT IS TO BE FOR HASTILY MAKING A PDF ACCESSIBLE (AT LEAST IN THE FEW WAYS I NORMALLY PRACTICE BEFORE UPLOADING TO THE WEBSITE). I DON'T ACTUALLY INTEND TO USE THIS OFTEN, BUT THATS WHAT THIS IS IF ANYONE ELSE IS CURIOUS. NOTE: I DON'T TRUST THAT THIS SCRIPT ACTUALLY DOES ANYTHING MEANINGFUL WITH ALT TEXT. SO IF YOU WANT TO CHANGE THAT YOU WILL HAVE TO DO IT IT WITHIN A PDF MANUALLY
#MUCH OF THIS WAS PUT TOGETHER WITH AI. I RESTRUCTURED IT FOR INPUT.

from pathlib import Path
import sys
import pikepdf
from pikepdf import Name, String, Dictionary, Array

# --- CONFIG ---
language_tag = "en-US"  # use 'en' or 'en-US' as needed

input_file = input("Input file name: ")
output_file = input("Please input outfile name: ")

#input_path = Path(r"C:\Users\cwhistler\Desktop\testMyCode.pdf")
#output_path = input_path.with_name(input_path.stem + "_lang.pdf")
#new_title = "Quarterly Report – Q4 2025" #FOR TESTING
new_title = input("Input Document Properties Title: ")

def mark_figures_alt_empty(struct_root: Dictionary): #I DON'R THINK THIS REALLY DOES ANYTHING WHEN I CHECK IT IN ADOBE #I actually think this just sets the alt text of everthing to "" and #shouldn't be used


    """Walk the StructTreeRoot and set /Alt "" for all /Figure elements."""
    def walk(node):
        # node can be a Dictionary (struct elem), Array (children list), or other
        if isinstance(node, Dictionary):
            # If this struct element is a Figure, set empty alt
            if node.get(Name('/S')) == Name('/Figure'):
                # Remove any existing /Alt to avoid merges, then set empty
                if node.get(Name('/Alt')) is not None:
                    del node[Name('/Alt')]
                node[Name('/Alt')] = String('')  # mark as decorative via empty alt

            # Recurse into /K (kids)
            kids = node.get(Name('/K'))
            if kids is not None:
                walk(kids)

        elif isinstance(node, Array):
            for item in node:
                walk(item)
        # If node is a number (MCID) or a reference, just ignore here

    walk(struct_root)

# --- VALIDATE PATH --- #AI generated this but I don't really care for it
#if not input_path.exists():
#if not input_file.exists():
    #print(f"[ERROR] File not found:\n  {input_path}")
   # print(f"[ERROR] File not found:\n  {input_file}")
    #sys.exit(1)

#with pikepdf.open(input_path) as pdf:
with pikepdf.open(input_file) as pdf:
    # Handle version differences (root vs Root)
    catalog = getattr(pdf, "root", getattr(pdf, "Root"))
    struct_root = catalog.get(Name('/StructTreeRoot'))

    if struct_root is None:
        print("[WARN] PDF is not tagged; there is no structure tree to edit.")
        print("       You must tag the PDF first; programmatically tagging is non-trivial.")
    else:
        print("")
        #mark_figures_alt_empty(struct_root)

    # Save
    #pdf.save(output_path)
    pdf.save(output_file)

    # 1) Document language (Catalog)
    catalog[Name('/Lang')] = String(language_tag)

    # 2) Classic Info dictionary title
    if pdf.docinfo is None:
        pdf.docinfo = pikepdf.Dictionary()
    pdf.docinfo[Name('/Title')] = String(new_title)


    # 2) Set ViewerPreferences /DisplayDocTitle = true
    vp = catalog.get(Name('/ViewerPreferences'))
    if vp is None:
        vp = Dictionary()
        catalog[Name('/ViewerPreferences')] = vp
    vp[Name('/DisplayDocTitle')] = True  # show document title in title bar


    # 3) XMP metadata (plain string title, language array)
    with pdf.open_metadata() as meta:
        # Optional: remove prior dc:title to avoid merge warnings
        if "dc:title" in meta:
            del meta["dc:title"]

        meta["dc:title"] = new_title
        meta["dc:language"] = [language_tag]

    
    #pdf.save(output_path)






    pdf.save(output_file)#JUST DO THIS ONCE AS TO NOT OVERWRITE AND MISS PREVIOUS CHANGES


print(f"[OK] Saved: {output_file}")