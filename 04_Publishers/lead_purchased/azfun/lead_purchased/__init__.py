import logging

import azure.functions as func
import csv
import codecs

def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    reader=csv.reader(codecs.iterdecode(myblob,'utf-8'),)
    headers = next(reader)
    data = [{h:x for (h,x) in zip(headers,row)} for row in reader]
    logging.info(data)


