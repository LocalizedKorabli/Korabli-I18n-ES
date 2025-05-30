import os
import subprocess
import sys
from pathlib import Path
from typing import Dict

import polib

gettext_tools_dir = r'C:\Program Files\Poedit\GettextTools\bin'

english_po_path = r'D:\dev\wows\Korabli-LESTA-I18N\Localizations\latest\global.po'

wip_po_path = Path('latest').joinpath('wip.po')

version_info = Path('latest').joinpath('version.info')

def main():
    english_po = polib.pofile(english_po_path)

    wip_po = polib.pofile(str(wip_po_path))

    en_dict: Dict[str, polib.POEntry] = {ent.msgid: ent for ent in english_po}

    wip_dict: Dict[str, polib.POEntry] = {ent.msgid: ent for ent in wip_po if not ent.fuzzy}

    merged_po = polib.POFile(wrapwidth=0)

    merged_po.metadata = wip_po.metadata

    with open(version_info, 'r', encoding='utf-8') as f:
        version = f.readline().strip()

    for msgid in en_dict:
        merged_po.append(en_dict[msgid] if msgid not in wip_dict else wip_dict[msgid])

    # dir0 = Path(sys.executable).parent

    target_dir = Path('latest').absolute()

    merged_po.save(str(target_dir.joinpath('global.po')))

    merged_po.save(str(target_dir.joinpath(f'{version}.po')))

    os.chdir(gettext_tools_dir)

    subprocess.run(['msgfmt.exe', str(target_dir.joinpath('global.po')), '-o', str(target_dir.joinpath('global.mo'))])

    subprocess.run(['msgfmt.exe', str(target_dir.joinpath(f'{version}.po')), '-o', str(target_dir.joinpath(f'{version}.mo'))])


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print('Exception: ')
        print(ex)
    input('Press Enter to exit.')