from subprocess import PIPE, Popen, check_output
import subprocess
import shlex
import configparser
import pathlib

def get_lichess_api():
    global config
    lichess_api = config["lichess"]["api_token"]
    return lichess_api

def get_lichess_range():
    global config
    lichess_range = config["lichess"]["range"]
    return lichess_range

def get_sound():
    global config
    centaur_sound = config["sound"]["sound"]
    return centaur_sound

def set_lichess_api(key):
    global config
    global config_file
    config.set('lichess', 'api_token', key)
    with open(config_file, 'w') as configfile:
        config.write(configfile)
        configfile.close()

def set_lichess_range(newrange):
    global config
    global config_file
    config.set('lichess', 'range', newrange)
    with open(config_file, 'w') as configfile:
        config.write(configfile)
        configfile.close()

def set_sound(onoff):
    global config
    global config_file
    config.set('sound', 'sound', onoff)
    with open(config_file, 'w') as configfile:
        config.write(configfile)
        configfile.close()

def rel_path():
    return str(pathlib.Path(__file__).parent.resolve()) + "/.."

def shell_run(rcmd):
    cmd = shlex.split(rcmd)
    executable = cmd[0]
    executable_options=cmd[1:]
    proc  = Popen(([executable] + executable_options), stdout=PIPE, stderr=PIPE)
    response = proc.communicate()
    response_stdout, response_stderr = response[0], response[1]
    if response_stderr:
        print(response_stderr)
        return -1
    else:
        print(response_stdout)
        return response_stdout

config_file = rel_path() + "/config/centaur.ini"
config = configparser.ConfigParser()
config.read(config_file)

# Import configs
try:
    lichess_api = config["lichess"]["api_token"]
except:
    lichess_api = ""
try:
    lichess_range = config["lichess"]["range"]
except:
    lichess_range = ""
try:
    centaur_sound = config["sound"]["sound"]
except:
    centaur_sound = "on"