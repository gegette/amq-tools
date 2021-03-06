# -*- coding: utf-8 -*-

LOGLEVEL = "DEBUG"

# Environnements
ENVIRONNEMENTS = {
    "LOCALHOST": {
        "name": "LOCALHOST",
        "hostname": "http://localhost:8161",
        "broker": "localhost"
    },
    "DEV": {
        "name": "DEV",
        "hostname": "http://mom-tst-01:1161",
        "broker": "ACTIVEMQ-DEV1"
    },
    "INT": {
        "name": "INT",
        "hostname": "http://mom-tst-01:2161",
        "broker": "ACTIVEMQ-INT"
    },
    "VAL": {
        "name": "VAL",
        "hostname": "http://mom-tst-01:3161",
        "broker": "ACTIVEMQ-VAL"
    }
}

# Login/Pswd
USERNAME = "admin"
PASSWORD = "admin"

# Messages processing
URL_GET_ALL_MESSAGES = "{}/api/jolokia/exec/org.apache.activemq:type=Broker,brokerName={},destinationType=Queue,destinationName={}/browse()"
URL_RETRY_MESSAGES = "{}/api/jolokia/exec/org.apache.activemq:type=Broker,brokerName={},destinationType=Queue,destinationName={}/retryMessages()"
#URL_GET_ONE_MESSAGE = "{}/api/jolokia/exec/org.apache.activemq:type=Broker,brokerName={},destinationType=Queue,destinationName={}/browseMessages(java.lang.String)/JMSMessageID={}"
URL_POST_MESSAGE = "{}/api/jolokia/"
BODY_POST_MESSAGE = '{"type":"EXEC", "mbean":"org.apache.activemq:type=Broker,brokerName=[BROKER],destinationType=Queue,destinationName=[QUEUE]", "operation":"sendTextMessage(java.util.Map,java.lang.String,java.lang.String,java.lang.String)", "arguments":[ARGUMENTS]}'

# Queues
ALL_DLQ_QUEUES = [
    "DLQ.Consumer.SGENBPM.VirtualTopic.TGENEDI",
    "DLQ.QGENGPP.TDATALEGACY",
    "DLQ.QGENCLI.TDATASYNC",
    "DLQ.QGENDIF.TDATASYNC",
    "DLQ.QGENGPP.TDATASYNC",
    "DLQ.QDATALEGACY",
    "DLQ.QGENCLI",
    "DLQ.QGENDIF",
    "DLQ.QGENGPP",
    "DLQ.QGENMAS",
    "DLQ.SGENBPM",
    "DLQ.SGENGED",
    "DLQ.SRECDEC",
    "DLQ.SRECDNO",
    "DLQ.SRECOBL",
    "DLQ.SRECREG",
    "DLQ.SRECVIS"
]

# Excel file configuration
OUTPUT_FOLDER = "output\\"
EXCEL_FILE_NAME = "_Messages_MQ_Bloques.xlsx"
EXCEL_COLUMNS_DLQ_QGENGPP_TDATALEGACY = ["TABLE", "OPERATION", "dlqDeliveryFailureCause", "StringProperties", "Text"]
EXCEL_COLUMNS = ["dlqDeliveryFailureCause", "StringProperties", "Text"]

EXCEL_COLUMNS = {
    "QGENCLI.TDATASYNC": ["dlqDeliveryFailureCause", "StringProperties", "Text"],
    "QGENGPP.TDATALEGACY": ["TABLE", "OPERATION", "dlqDeliveryFailureCause", "StringProperties", "Text"],
    "QGENGPP": ["dlqDeliveryFailureCause", "StringProperties", "Text"],
    "QGENCLI": ["dlqDeliveryFailureCause", "StringProperties", "Text"]
}
