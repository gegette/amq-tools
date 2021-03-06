# -*- coding: utf-8 -*-
import requests
import json
import difflib
import csv
import re
import os
import time
from tqdm import tqdm
import sys, getopt
from openpyxl import Workbook
import src.AMQConfig as cfg
import src.AMQLog as log


def processJsonResponse(method, response, exitOnError=True):
    if (response.status_code == 200):
        jsonResponse = json.loads(response.text)
        responseCode = jsonResponse["status"]
        log.info("%s - HTTP Status %s" %(method, str(jsonResponse["status"])))

        if responseCode != 200:
            log.error(response.text)
            if exitOnError:
                sys.exit(2)

        return jsonResponse
    else:
        log.error(method)
        log.error(response)


def getAllMessages(environnement, queue):
    response = requests.get(cfg.URL_GET_ALL_MESSAGES.format(environnement["hostname"], environnement["broker"], queue), params=None, verify=False, auth=(cfg.USERNAME, cfg.PASSWORD))
    return processJsonResponse("getAllMessages", response)


def formatMessages(jsonResponse, environnement, queue, writeExcelFile):
    messageList = []
    if writeExcelFile:    
        wb = Workbook()
        ws1 = wb.active
        ws1.title = queue[0 : 31]
        ws1.append(cfg.EXCEL_COLUMNS[queue])

        #ws2 = wb.create_sheet(title="TEST2")

    if not jsonResponse["value"]:
        log.error("Rien a formater")
        sys.exit(2)

    for message in tqdm(jsonResponse["value"], desc="formatMessages"):
        
        #properties = json.dumps(message["StringProperties"]).replace("u'", "'")
        properties = "{"
        headers = message["StringProperties"]
        for header in headers:
            if header != 'dlqDeliveryFailureCause':
                properties = properties + "\"" + header + "\":\"" + message["StringProperties"][header] + "\", "

        headers = message["LongProperties"]
        for header in headers:
            properties = properties + "\"" + header + "\":\"" + str(message["LongProperties"][header]) + "\", "

        headers = message["BooleanProperties"]
        for header in headers:
            properties = properties + "\"" + header + "\":\"" + str(message["BooleanProperties"][header]) + "\", "

        properties = properties + "\"JMSType\":\"" + message["JMSType"] + "\""
        properties = properties + ", \"JMSDeliveryMode\":\"" + message["JMSDeliveryMode"] + "\""
        properties = properties + ", \"JMSPriority\":\"" + str(message["JMSPriority"]) + "\""
        properties = properties + "}"

        # 1ere passe de formatage
        if "TDATALEGACY" in queue:
            text = json.dumps(message["Text"]).replace(' ', '').replace('\\\"', '"').replace('\\n', '')
        elif "SRECDNO" in queue:
            # Cas particulier DNO : le contenu du message n'est pas utilisé
            text = ''    
        else:
            text = json.dumps(message["Text"]).replace(' ', '').replace('\\\"', '"').replace('\"{', '{').replace('}\"', '}').replace('\\n', '')    

        # ajout dans le fichier excel
        if writeExcelFile: 
            dlqDeliveryFailureCause = message["StringProperties"]['dlqDeliveryFailureCause']

            if "TDATALEGACY" in queue:
                table = message["StringProperties"]['TABLE']
                operation = message["StringProperties"]['OPERATION']
                ws1.append([table, operation, dlqDeliveryFailureCause, properties, text.replace('\\\"', '"').replace('"{"', '{"').replace('"}"', '"}')])
            else:
                ws1.append([dlqDeliveryFailureCause, properties, text.replace('\\\"', '"').replace('"{"', '{"').replace('"}"', '"}')])

        argument = []
        argument.append(properties)
        argument.append(text)
        argument.append(cfg.USERNAME)
        argument.append(cfg.PASSWORD)

        # 2eme passe de formatage pour préparer le body
        argumentText = json.dumps(argument).replace('\\\"', '"').replace('\\\"', '"').replace('\\\"', '"').replace('\\\"', '"').replace('"{"', '{"').replace('"{"', '{"').replace('"}"', '"}').replace('"}"', '"}').replace('}"",', '},')
        # log.debug(argumentText)
        
        messageList.append(argumentText)

    if writeExcelFile:
        pathFolder = os.path.dirname(__file__)[0:len(os.path.dirname(__file__))-4] + '\\' + cfg.OUTPUT_FOLDER
        if not os.path.exists(pathFolder):
            os.mkdir(pathFolder)
        path = pathFolder + environnement["name"] + cfg.EXCEL_FILE_NAME
        log.info("Fichier excel: %s" %path)
        wb.save(path)
    
    time.sleep(0.1)
    log.info("FormatMessages - {} messages traites".format(len(messageList)))
    return messageList


def postMessage(environnement, queue, message):
    if(environnement["name"] == "PRD" or environnement["hostname"] == "http://mom-prd-01:8161"):
        log.error("postMessage - Environnement PRD interdit")
        return

    textBody = cfg.BODY_POST_MESSAGE.replace("[BROKER]", environnement["broker"]).replace("[QUEUE]", queue).replace("[ARGUMENTS]", message)
    log.debug(textBody)
    jsonBody = json.loads(textBody)

    response = requests.post(cfg.URL_POST_MESSAGE.format(environnement["hostname"]), json=jsonBody, auth=(cfg.USERNAME, cfg.PASSWORD))
    return processJsonResponse("postMessage", response)


def retryMessages(environnement, queue):
    response = requests.get(cfg.URL_RETRY_MESSAGES.format(environnement["hostname"], environnement["broker"], queue), params=None, verify=False, auth=(cfg.USERNAME, cfg.PASSWORD))
    jsonResponse = processJsonResponse("retryMessages", response, exitOnError=False)

    if jsonResponse:
        if 'value' in jsonResponse:
            log.info("Queue %s - Nb message rejoues: %s" %(queue, str(jsonResponse["value"])))
        return jsonResponse

