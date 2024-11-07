import re
import sys
from subprocess import run
import json
BAR='='*60

REPO = "{{ cookiecutter.github_repo_name }}"
MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'
module_name = '{{ cookiecutter.project_slug}}'
HOOK_BASH =  "{{ cookiecutter.hook_bash }}".lower()
DEPLOY = '{{ cookiecutter.github_deploy }}'.lower()

def main():
    print( f"{BAR}\nENTER pre_gen_project\n{BAR}" )
    print( f"HOOK_BASH: [{HOOK_BASH}]" )
    verify_plug_or_die()
    verify_deploy_die()
    die(0)

def verify_plug_or_die():
    if not re.match(MODULE_REGEX, module_name):
        print('ERROR: The project slug (%s) is not a valid Python module name. '
              'Please do not use a - and use _ instead' % module_name)
        die(1)

def verify_deploy_die():
    if DEPLOY == 'y':
        print( 'deploying. Checking for existance of repo' )
        exists( REPO ) and die( 101, 'repo already existss' )


def exists(name):
     it = run( 'gh repo list --json name'.split(), capture_output=True)
     names = [ item['name'] for item in json.loads(it.stdout) ]
     return name in names

def torf(prompt):
    while True:
        answer = input( f'{prompt} [y/n]?' ).lower()
        if answer=='y': return True
        if answer=='n': return False

def die( code, msg='no message' ):
    print(f"{BAR}\nEXIT pre_gen_project\n[{code}]: {msg}\n{BAR}")
    if HOOK_BASH == 'y' and torf( 'run bash' ): run( ['bash'] )
    sys.exit(code)


if __name__ == '__main__':
    main()
