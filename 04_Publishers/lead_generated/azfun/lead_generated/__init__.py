import logging
import azure.functions as func

def main(event: func.EventHubEvent):

    data = event.get_body()

    logging.info(f'Event received')
    logging.info(str(data))
