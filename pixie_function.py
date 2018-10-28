#!/usr/bin/env python3.5
import datetime
import json
import re
import subprocess
import sys
import traceback

def isLoaded(module, id):
    if serverslist[id][module]["last"] == "enabled":#wrong vars
        return True
    else:
        return False

def isEnabled(module, id):
    serverslist = readData('server', id, module)
    if serverslist[module]["last"] == "enabled":
        return True
    else:
        return False

def checkModule(module):
    res = subprocess.run(['python3.5', '-m', 'py_compile', 'module_' + module + '.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return res

def checkModuleConfig(module, id):
    defaultlistmodule = getDefault()
    serverlistmodule = readData('server', id)
    if defaultlistmodule[module]['config'] == "None":
        return True
    else:
        for cfgkey in serverlistmodule[module]['config']:
            if serverlistmodule[module]['config'][cfgkey]['value'] == "None":
                return False
        return True

def readData(file, id = None, module = None):
    if file == 'main':
        with open('data/modules.json') as e:
            data = json.load(e)
    elif file == 'list':
        with open('data/serverslist.json') as e:
            data = json.load(e)
    elif file == 'server':
        try:
            with open('data/servers/' + id + '.json') as e:
                data = json.load(e)
        except:
            with open('data/default.json') as e:
                data = json.load(e)
            saveData('server', data, id)
        else:
            if module == None:
                listmodules = readData('main')
                for module in listmodules:
                    try:
                        data[module]
                    except KeyError:
                        defaultData = getDefault()
                        data[module] = defaultData[module]
            else:
                try:
                    data[module]
                except KeyError:
                    defaultData = getDefault()
                    data[module] = defaultData[module]
            saveData('server', data, id)
    return data

def saveData(file, data, id = None):
    if file == 'main':
        with open('data/modules.json', 'w') as e:
            json.dump(data, e)
    elif file == 'server':
        if id == None:
            return
        with open('data/servers/' + id + '.json', 'w') as e:
            json.dump(data, e)

def getDefault():
    with open('data/default.json') as e:
        data = json.load(e)
    return data
        
def validateModuleName(moduleName):
    listmodule = readData('main')
    try:
        listmodule[moduleName]
    except KeyError:
        return False
    return True

def validateConfigKey(id, module, cfgkey = None):
    defaultlistmodule = getDefault()
    #serverlistmodule = readData('server', id)
    try:
        defaultlistmodule[module]['config'][cfgkey]
    except KeyError:
        return False
    return True

def validateConfigKeyType(id, type, module, cfgkey, value):
    defaultlistmodule = getDefault()
    #serverlistmodule = readData('server', id)
    try:
        if type == 'bool':
            bool(value)
        elif type == 'str':
            str(value)
        elif type == 'tag':
            if re.search('^<#([0-9])+>$', value):
                value = int(''.join(filter(str.isdigit, value)))
            elif re.search('^<@([0-9])+>$', value):
                value = int(''.join(filter(str.isdigit, value)))
            int(value)
        elif type == 'int':
            int(value)
    except:
        return False
    return True

def removeConfig(action, id, module, cfgkey, value = None):
    if action == 'clear':
        defaultlistmodule = getDefault()
        serverlistmodule = readData('server', id, module)
        serverlistmodule[module]['config'][cfgkey]['value'] = defaultlistmodule[module]['config'][cfgkey]['value']
        saveData('server', serverlistmodule, id)
    elif action == 'remove':
        return