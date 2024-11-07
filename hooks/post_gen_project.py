#!/usr/bin/env python
import sys
import pathlib
import subprocess

RUNME = './__run_me__.sh'
REPO = "{{ cookiecutter.github_repo_name }}"
MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'
module_name = '{{ cookiecutter.project_slug}}'
HOOK_BASH =  "{{ cookiecutter.hook_bash }}".lower()
DEPLOY = '{{ cookiecutter.github_deploy }}'.lower() == 'y'
BAR='='*60

def main():
    print( f"{BAR}\nENTER post_gen_project\n{BAR}" )
    process_authors()
    process_cli()
    process_open_source()
    process_deploy_or_die()
    die(0, "script ended normally")

def process_deploy_or_die():
    if DEPLOY:
        code = subprocess.run( [ RUNME ] ).returncode
        print( f"[{RUNME}] exited with exit code [{code}]" )
        code == 0 or die(0, "script ended with bad initialization")

def process_authors():
    if '{{ cookiecutter.create_author_file }}' != 'y':
        pathlib.Path('AUTHORS.rst').unlink()
        pathlib.Path('docs', 'authors.rst').unlink()

def process_cli():
    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        pathlib.Path('src', '{{ cookiecutter.project_slug }}', 'cli.py').unlink()

def process_open_source():
    if 'Not open source' == '{{ cookiecutter.open_source_license }}':
        pathlib.Path('LICENSE').unlink()



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
    print(f"{BAR}\nEXIT pre_post_project\n[{code}]: {msg}\n{BAR}")
    if HOOK_BASH == 'y' and torf( 'run bash' ): run( ['bash'] )
    sys.exit(code)

if __name__ == '__main__':
    main()

