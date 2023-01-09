#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    authenticator = IAMAuthenticator("C8MMcmyzCvtx4ir7Q1hgcaXIIczBkURAScRGys3Gc7G3")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://apikey-v2-2sd76a0jxkyktdflxbypp5n2u2iq7zjx60nn1ja9w7mm:b4e172bb6be98e1d138d32e666876922@76ff4ea4-f27a-47e5-8087-9f43fa42f5e3-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_find(
                db='reviews',
                selector={'dealership': {'$eq': int(dict['id'])}},
            ).get_result()
    if len(response['docs']) == 0:
        return {
            'statusCode': 404,
            'message': 'dealerId does not exist'
            }
    try:
        result = {
            'headers': {'Content-Type':'application/json'},
            'body': {'data':response}
            }
        return result
    except:
        return {
            'statusCode': 500,
            'message': 'Something went wrong on the server'
            }