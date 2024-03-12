# %%
from helpers import ObsidianFile, yield_papers

def toggle_abstract_collapsing(vault_path: str, become_open: bool, limit: int = -1, copy_files: bool = False):
    """ Toggles open and closed abstract headers in each paper in a vault. """
    for file in yield_papers(vault_path, limit=limit):
        file: ObsidianFile
        if file.property_contains_value('tags', 'stub'): continue  # keep stubs unfolded

        # Toggle abstract headers
        for idx, line in enumerate(file):
            line: str
            if not line.startswith("> [!my-abstract]"): continue

            # Toggle callout
            if become_open:
                file[idx] = line.replace("[!my-abstract]-", "[!my-abstract]+")
            else:
                file[idx] = line.replace("[!my-abstract]+", "[!my-abstract]-")
        
        file.write_file(copy=copy_files)

def update_zotero_links(vault_path: str, limit: int = -1, copy_files: bool = False):
    """ Update zotero links to the new format. """

    for file in yield_papers(vault_path, limit=limit):
        file: ObsidianFile

        # Find citation key and zotero link
        citation_key = file.return_property_values('citation key')[0]
        
        # Find old format zotero link
        for link in file.return_property_values('links'):
            if 'zotero://select/' in link:
                zotero_link = link
                break
        
        # Replace and update properties
        new_zotero_link = f'zotero://select/items/@{citation_key}'
        file.replace_property_value(zotero_link, new_zotero_link)
        file.write_file(copy=copy_files)  # write files
