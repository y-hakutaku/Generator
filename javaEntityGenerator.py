#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import string
import os

def createClass(className,fieldDatas,setterDatas) :
  field = ''
  setter = ''
  for fieldData in fieldDatas :
    field += fieldData
  for setterData in setterDatas :
    setter += setterData

  return 'public class %s {\n%s\n%s}\n' % (className, field, setter)

def setterCreator(key, type) :
  return '  public void set%s(%s %s) {\n    this.%s = %s;\n  }\n  public %s get%s() {\n    return %s;\n  }\n' %(string.capwords(key), type, key, key, key, type, string.capwords(key), key)

def stringFieldCreator(key,type):
  if key is None:
    raise Exception
  if type != 'String':
    raise Exception
  fieldDatas = '  private %s %s;\n' % (type, key)
  return fieldDatas

def numFieldCreator(key,type):
  if key is None:
    raise Exception

  fieldDatas = '  private %s %s;\n' % (type, key)
  return fieldDatas

f = open("./entity.json")
datas = json.load(f)
f.close()
for data in datas :

  className = data.get('className')
  stringProperties = data.get('stringProperties')

  fieldDatas = []
  setterDatas = []

  for strProp in stringProperties :
    key = strProp.get('key')
    type = 'String'

    fieldDatas.append(stringFieldCreator(key, type))
    setterDatas.append(setterCreator(key, type))

  numberProperties = data['numberProperties']
  for numProp in numberProperties :
    key = numProp.get('key')
    type = numProp.get('type')

    fieldDatas.append(numFieldCreator(key, type))
    setterDatas.append(setterCreator(key, type))
  classData = createClass(className, fieldDatas, setterDatas)
  home = os.environ['HOME']
  f = open('%s/Desktop/%s.java'%(home, className),'w+')
  f.write(classData)
  f.close()
