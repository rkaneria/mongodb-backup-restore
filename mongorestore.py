#shell to restore mongo database with json file
import datetime
import json
import os
import sys
import subprocess

def get_arguments():

    args = {}
    for i in range(len(sys.argv)):
        if sys.argv[i].startswith('-'):
            args[sys.argv[i]] = sys.argv[i + 1] if (((i + 1) < len(sys.argv)) and not sys.argv[i + 1].startswith('-')) else sys.argv[i]
            print sys.argv
        else:
            pass

    return args

#Return database list that defined in config node
def get_databases(serverConfig):
    databases = serverConfig['databases'] if 'databases' in serverConfig else []    
    if type(databases) == type(''):
        return [databases]
    else:
        return databases

#Return command arguments that defined in config node
def append_arguments(serverArgs, serverConfig):
    #init variants
    args = ''

    #append server arguments to command
    for arg in serverArgs:
        if arg in serverConfig and serverConfig[arg]:
            fr = str.format(' --{} {{', arg) + arg + '}'
            args += fr.format(**serverConfig)

    return args
    
#Execute the command    
def run_command(popenCmd):
    try:
        if popenCmd: 
            print('start {0} ...'.format('restore'))
            print(popenCmd)
            subprocess.call(popenCmd, shell=True)
            print('finished!')
        else: print('invalid command')
    except Exception as err:
        print("{0}".format(err))

#get arguments in main method
args = get_arguments()

    
#get the path of configuration file, default is config.json
configFile = args['-config'] if '-config' in args else 'config.json'


#read json configuration file
f = open(configFile, 'r')
config = json.load(f);

#get server item and prase server arguments to append command line.
serversConfig = config['servers'] if 'servers' in config else {}
serverArgs = serversConfig['arguments'] if 'arguments' in serversConfig else ['host', 'port']


#if target item doesn't exist, it see use one server to backup and restore
serverTarget = serversConfig['target'] if 'target' in serversConfig else [];


#create restore command and append arguments
command = ''

programs = config['programs']
command = programs['restore']
command += append_arguments(serverArgs, serverTarget)


#create dictionary for now that used parse output folder
out_dict = {'$today': datetime.datetime.now()}

#get datebases from config node
popenCmd = ''
database = get_databases(serverTarget)
if len(database) == 0:
    popenCmd = command + str.format(' {} --noIndexRestore', config['backupdir'])
    run_command(popenCmd)
else:
    for i in range(len(database)):
        popenCmd = command + str.format(' --db {} {}/{} --noIndexRestore', database[i], config['backupdir'], database[i])
        run_command(popenCmd)  
