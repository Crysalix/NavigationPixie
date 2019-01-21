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
    res = subprocess.run(['python3.5', '-m', 'py_compile', 'modules/' + module + '.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return res

def checkModuleConfig(module, id):
    defaultlistmodule = getDefault()
    serverlistmodule = readData('server', id)
    if defaultlistmodule[module]['config'] == "None":
        return True
    else:
        for configKey in serverlistmodule[module]['config']:
            if serverlistmodule[module]['config'][configKey]['value'] == "None":
                return False
        return True

def readData(file, id = None, module = None):
    if file == 'main':
        with open('data/modules.json') as e:
            data = json.load(e)
    elif file == 'list':
        with open('data/serverslist.json') as e:
            data = json.load(e)
    elif file == 'locales':
        with open('data/locales.json') as e:
            data = json.load(e)
        for lang in data:
            with open('data/locales/{}.json'.format(lang)) as e:
                data[lang] = json.load(e)
    elif file == 'server':
        try:
            with open('data/servers/{}.json'.format(id)) as e:
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
        with open('data/servers/{}.json'.format(id), 'w') as e:
            json.dump(data, e)

def getDefault():
    with open('data/default.json') as e:
        data = json.load(e)
    return data

def getValidAction(module, configKey):
    data = getDefault()
    #actions = ''
    if (data[module]['config'][configKey]['type'] == 'chantag' or data[module]['config'][configKey]['type'] == 'usertag' or data[module]['config'][configKey]['type'] == 'str'):
        actions = '<set/clear>'
    elif (data[module]['config'][configKey]['type'] == 'chantaglist' or data[module]['config'][configKey]['type'] == 'usertaglist'):
        actions = '<add/remove/clear>'
    return actions

def validateModuleName(moduleName):
    listmodule = readData('main')
    try:
        listmodule[moduleName]
    except KeyError:
        return False
    return True

def validateConfigKey(id, module, configKey = None):
    defaultlistmodule = getDefault()
    #serverlistmodule = readData('server', id)
    try:
        defaultlistmodule[module]['config'][configKey]
    except KeyError:
        return False
    return True

def validateConfigKeyType(id, type, module, configKey, value):
    defaultlistmodule = getDefault()
    #serverlistmodule = readData('server', id)
    try:
        if type == 'bool':
            bool(value)
        elif type == 'str':
            str(value)
        elif type == 'chantag':
            if re.search('^<#([0-9])+>$', value):
                value = int(''.join(filter(str.isdigit, value)))
                int(value)
        elif type == 'usertag':
            if re.search('^<@([0-9])+>$', value):
                value = int(''.join(filter(str.isdigit, value)))
                int(value)
        elif type == 'int':
            int(value)
    except:
        return False
    return True

def validateValue(module, configKey, left):
    defaultlistmodule = getDefault()
    try:
        validate = defaultlistmodule[module]['config'][configKey]['validate']
    except:#no validation info
        return True
    else:
        fighters = validate.split("/")
        for right in fighters:
            #Fight !
            if left == right:
                return True #left win !
        return False #right win !
    
def removeConfig(action, id, module, configKey, value = None):
    if action == 'clear':
        defaultlistmodule = getDefault()
        serverlistmodule = readData('server', id, module)
        serverlistmodule[module]['config'][configKey]['value'] = defaultlistmodule[module]['config'][configKey]['value']
        saveData('server', serverlistmodule, id)
    elif action == 'remove':
        return