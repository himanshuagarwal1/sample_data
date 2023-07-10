from django.shortcuts import render
from django.views.generic import View
import json
from datetime import datetime
from .utils import  get_All_license , get_License, get_License_Details, json_response
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect


from django.contrib.auth.models import User
from .models import Client, License, LicenseType
# Create your views here.

class LicenseListView(View):

    def get(self, request, *args, **kwargs):
        """
        Input: No args taken

        Output: Will return the all the detalis of all the licenses
        """
        data =[]
        all_licenses = get_All_license()
        for license in all_licenses:
            data.append(get_License_Details(license))

        return json_response(data=data)
    
    def post(self, request, *args, **kwargs):

        """
        Input: No args taken

        Output: Wil send the emails sent to all the clients whose expiration conditions are met.
        """

        all_licenses = get_All_license()
        email_details= []
        result = []

        for license in all_licenses:
            exp_date = license.expiration_datetime.date()
            cur_date = datetime.utcnow().date()
            days_left = int((exp_date - cur_date).days)
            
            if days_left == 120:
                email_details.append(get_License_Details(license))
            elif days_left < 30 and int(cur_date.weekday())  == 0:
                email_details.append(get_License_Details(license))
            elif days_left < 8:
                email_details.append(get_License_Details(license))
            

        for email in email_details:

            email_body = "Hi " + email.get("name_poc", "All") + " the license with following details is going to expire on " + email.get("exp_time", None) + " license id : " + str(email.get("license_id", None)) + ", License Type : " + str(email.get("license_type", None)) +" Package name " + str(email.get("package", None))
            
            sent = send_mail(
                        "Regarding the expiration of License",
                        email_body,
                        "admin@him.com",
                        [str(email.get("email_poc"))],
                        fail_silently=True,
                        )
            
            result.append(email_body)

        data =  {"following emials were sent out :-": result}
        
        return json_response(data=data)

class LicenseView(View):
    """
        Input: Take valid license ID

        Output: Will return the all the detalis of the license
    """
    def get(self, request,license_id ,*args, **kwargs): 

        license = get_License(license_id)
        if not license:
            return json_response({"error": "No License matches the given query"}, 404 )
        data = get_License_Details(license)

        return json_response(data= data)

    