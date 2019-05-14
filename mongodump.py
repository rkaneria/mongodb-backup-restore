#shell to backup mongo database with json file
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
    
    
def run_command(popenCmd):
    try:
        if popenCmd: 
            print('start {0} ...'.format('backup'))
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


#if server item doesn't exist, it see use one server to backup 
serverSource = serversConfig['source'] if 'source' in serversConfig else [];

#create backup command and append arguments
command = ''

programs = config['programs']
command = programs['dump']
command += append_arguments(serverArgs, serverSource)

#create dictionary for now that used parse output folder
out_dict = {'$today': datetime.datetime.now()}

#get datebases from config node
popenCmd = ''

database = get_databases(serverSource)

if len(database) == 0:
    popenCmd = command + str.format(' --out {}', config['output'].format(**out_dict))
    run_command(popenCmd)
else:
    command = command + str.format(' --out {}', config['output'].format(**out_dict))
    for i in range(len(database)):
        db_col = database[i].split (",")
        for i in range(len(db_col)):
            db = db_col[i].split (".")
            popenCmd = command + str.format(' --db {} ', format(db[0]))
            if len(db) == 1:
                run_command(popenCmd)
            else:
                command = command + str.format(' --db {} ', format(db[0]))
                db.pop(0)
                for x in db:
                    popenCmd = command + str.format(' --collection {} ', format(x))
                    run_command(popenCmd)
