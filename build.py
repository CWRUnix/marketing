from collections.abc import Mapping
import subprocess
from pathlib import Path
import json
from typing import Any

colors = list(Path("./colors").glob("*"))

svgs = list(Path("./source").glob("**/*.svg"))

sizes = [ 500, 10000 ]

script = ""

for svg in svgs:
    for size in sizes:
        name = svg.name.split(".")[0]
        parent = svg.parent
        template = (parent / f"{name}.json")
        for color in colors:
            cname = color.name.split(".")[0]
            fname = svg.parent / f"{cname}-{size}-{svg.name}"
            script += f'''
                source {color.absolute()}
                cat {svg.absolute()} |
                    xmlstarlet ed -N s=http://www.w3.org/2000/svg -u "/s:svg/s:defs/s:linearGradient[@inkscape:label='FG']/s:stop/@style" -v "stop-color:$FG;stop-opacity:1;" |\
                    xmlstarlet ed -N s=http://www.w3.org/2000/svg -u "/s:svg/s:defs/s:linearGradient[@inkscape:label='BG']/s:stop/@style" -v "stop-color:$BG;stop-opacity:1;" >\
                    ./{fname}
            '''
            if template.exists():
                temp_vals: list[Mapping[str, Any]] = json.loads(template.read_text())  # pyright: ignore[reportExplicitAny, reportAny]
                for item in temp_vals:
                    temp_fname = fname.parent / f"{item.get("id", "")}-{fname.name}"
                    for val in item:
                        script += f'''
                            export {val}="{item[val]}"
                        '''
                    script += f'''
                        mkdir -p out/{svg.parent}
                        envsubst -i ./{fname} -o "out/{temp_fname}"
                        inkscape -o "./out/{temp_fname}" --export-type=svg --export-plain-svg "./out/{temp_fname}"
                        inkscape -o "./out/{temp_fname.parent}/solid-{temp_fname.name}" --export-type=png --export-width={size} --export-background=$BG "./out/{temp_fname}"
                        inkscape -o "./out/{temp_fname.parent}/clear-{temp_fname.name}" --export-type=png --export-width={size} "./out/{temp_fname}"
                    '''
            else:
                script += f'''
                    inkscape -o "./out/{fname}" --export-type=svg --export-plain-svg "./{fname}"
                    inkscape -o "./out/{fname.parent}/solid-{fname.name}" --export-type=png --export-width={size} --export-background=$BG "./out/{fname}"
                    inkscape -o "./out/{fname.parent}/clear-{fname.name}" --export-type=png --export-width={size} "./out/{fname}"
                '''

print(script)
_ = subprocess.run(["bash", "-c", script], check=True, stderr=subprocess.STDOUT)
