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
    "COUCH_URL": "https://98ff71f8-4e54-4bcc-bfbd-e91475399743-bluemix.cloudantnosqldb.appdomain.cloud/",
    "IAM_API_KEY": "WFGtu2LO6Ng7oLDafSfQNv0bYGvbVbJ76Y6jwguVeE39",
    "COUCH_USERNAME": "98ff71f8-4e54-4bcc-bfbd-e91475399743-bluemix"
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
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}

test = main(myDict)
