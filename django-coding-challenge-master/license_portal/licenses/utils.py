from .models import Client, License, LicenseType
from django.http.response import HttpResponse
import json


def json_response(data={}, status=200):
    return HttpResponse(
        content=json.dumps(data), status=status, content_type="application/json"
    )



def get_License_Details(license):

    """
    Input: License Object
    Output: License details 
    """
    try:
        client = Client.objects.get(id = license.client.id)
    
        return {"name_poc": client.poc_contact_name,
                "email_poc": client.poc_contact_email,
                "package": license.package,
                "license_id": license.id,
                "license_type" : license.license_type,                    
                "exp_time": str(license.expiration_datetime.date())}
    except Client.DoesNotExist:
        return json_response({"error": "No Client matches the given query"}, 404)
    

def get_All_license():

    """
        Input: No Args required
        Output: All license Objects
    """

    try:
        all_licenses = License.objects.all()
        return all_licenses
    except License.DoesNotExist:
        return json_response({"error": "No license matches the given query"}, 404)

def get_License(license_id): 
    """
        Input: License id as required
        Output: return valid License object

    """

    try:
        license = License.objects.get(id = license_id)
        return license
    except License.DoesNotExist:
        return None 