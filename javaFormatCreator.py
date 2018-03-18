#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import string
import os

def actionTypeId(typeId) :
  return '  @Override\n  public int getActionTypeId() {\n    return %d;\n  }' % (typeId)

def actionClassCreator(typeId,name,restrictionDatas,setterDatas) :
  restriction = ''
  setter = ''
  for restrictionData in restrictionDatas :
    restriction += restrictionData
  else:
    restriction=restriction[:-2]

  for setterData in setterDatas :
    setter += setterData
  actionTypeIdGetter = actionTypeId(typeId)
  return 'public class %sAction extends Action {\n  private static final Restriction [] restriction;\n  static {\n    restriction = {\n%s\n    }\n  }\n%s\n%s}\n' % (name, restriction, actionTypeIdGetter, setter)


def classBaseCreator(typeId,objectType,name,restrictionDatas,setterDatas) :
  if objectType == 'action':
    return actionClassCreator(typeId, name, restrictionDatas, setterDatas)

def setterCreator(key, type) :
  return '  public void set%s(%s %s) {\n    setObject(%s);\n  }\n' %(string.capwords(key), type, key, key)

def stringRestrictionClassCreator(key,type,mandatory,regex,strMinSize,strMaxSize):
  if key is None:
    raise Exception

  if type != 'String':
    raise Exception
  if regex is None:
    regex = "null"
  if strMinSize < 0:
    strMinSize = 0

  restrictionClass = '      new RestrictionString("%s",%s,%s,%d,%d),\n' % (key, mandatory, regex, strMinSize, strMaxSize)
  return restrictionClass

def numRestrictionClassCreator(key,type,mandatory,numMinSize,numMaxSize):
  if key is None:
    raise Exception
  if numMinSize < 0:
    numMinSize = 0

  if type != 'Long' and type != 'Integer':
    raise Exception

  restrictionClass = '      new Restriction%s("%s",%s,%d,%d),\n' % (string.capwords(type), key, mandatory, numMinSize, numMaxSize)
  return restrictionClass

f = open("./acton.json")
datas = json.load(f)
f.close()
for data in datas :
  objectType = data.get('objectType')

  print(objectType)
  if objectType == 'action':
    print('objectType is Action')
  else:
    print('unknown type')

  typeId = data.get('typeId')
  name = data.get('name')
  stringProperties = data.get('stringProperties')

  restrictionDatas = []
  setterDatas = []

  for strProp in stringProperties :
    key = strProp.get('key')
    type = 'String'
    regex = strProp.get('regex')
    strMinSize = strProp.get('minStringSize')
    strMaxSize = strProp.get('maxStringSize')
    mandatory = strProp.get('mandatory')
    if mandatory :
      mandatory = 'true'
    else :
      mandatory = 'false'

    restrictionDatas.append(stringRestrictionClassCreator(key, type, mandatory, regex ,strMinSize, strMaxSize))
    setterDatas.append(setterCreator(key, type))

  numberProperties = data['numberProperties']
  for numProp in numberProperties :
    key = numProp.get('key')
    type = numProp.get('type')
    numMinSize = numProp.get('minNumberSize')
    numMaxSize = numProp.get('maxNumberSize')
    mandatory = numProp.get('mandatory')
    if mandatory :
      mandatory = 'true'
    else :
      mandatory = 'false'

    restrictionDatas.append(numRestrictionClassCreator(key, type, mandatory ,numMinSize, numMaxSize))
    setterDatas.append(setterCreator(key, type))

  classData = classBaseCreator(typeId, objectType, name, restrictionDatas, setterDatas)
  home = os.environ['HOME']
  f = open('%s/Desktop/%sAction.java'%(home, name),'w+')
  f.write(classData)
  f.close()
