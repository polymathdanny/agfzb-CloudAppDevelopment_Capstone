#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

myDict = {
    "COUCH_URL": "https://59e8d0a8-4b92-4e5f-b6e9-97065c14665c-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "gmRktU8iPRLIMuP7TU0KxMV0bJZ3VYKw7opsQpCqCGEW",
    "COUCH_USERNAME": "59e8d0a8-4b92-4e5f-b6e9-97065c14665c-bluemix"
}

def main(dict):
    databaseName = "dealerships"

    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        print("Databases: {0}".format(client.all_dbs()))
        dealerships = client['dealerships']
        for document in dealerships:
            print(document)
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}

test = main(myDict)
