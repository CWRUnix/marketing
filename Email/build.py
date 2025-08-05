import subprocess

roles: list[tuple[str, str]] = [
    ("Trevor Nichols", "President and Treasurer"),
    ("Wolf Mermelstein", "VP and Treasurer"),
    ("Evan Harnak", "Secretary"),
    ("Matias Torres", "Risk Manager"),
]

script = '''
    set -euxo pipefail
    mkdir -p ./out
'''

for [name, role] in roles:
    script += f'''
        export NAME="{name}"
        export ROLE="{role}"
        envsubst -i ./signature.svg -o "out/{name}.svg"
        inkscape -o "out/{name}.svg" --export-type=svg "out/{name}.svg"
    '''

_ = subprocess.run(["bash", "-c", script], check=True)
