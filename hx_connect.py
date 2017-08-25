# -*- coding: utf-8 -*-
import json
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# ** FIX THIS
# Suppress the  InsecureRequestWarning: Unverified HTTPS request
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# FUTURE - get user info from BASH Script
# ---- sort user info from bash script section  -------
# Get user provided information from bash script and parse it
hx_ip = os.environ['HX_IP']
hx_username = os.environ['HX_USERNAME']
hx_password = os.environ['HX_PASSWORD']
hx_client_id = os.environ['HX_CLIENT_ID']
hx_client_secret = os.environ['HX_CLIENT_SECRET']
hx_redirect_uri = os.environ['HX_REDIRECT_URI']


def connect_hx(hx_ip):
    # -- connect to HyperFlex Connect section  --
    # Generate base login URl
    # (myhx_ip variable defined by user via bash script)
    base_url = 'https://' + hx_ip
    return base_url


def get_token(base_url):
    name_pwd = {"username": hx_username,
                "password": hx_password,
                "client_id": hx_client_id,
                "client_secret": hx_client_secret,
                "redirect_uri": hx_redirect_uri}

    payload = json.dumps(name_pwd)

    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"}

    querystring = {"grant_type": "password"}

    # Generate login url
    login_url = base_url + '/aaa/v1/auth'

    # to avoid failure due to  an untrusted SSL certificate.
    # set verify=False
    # FUTURE -  ** FIX THIS !!
    post_response = requests.request("POST", login_url,
                                     data=payload, headers=headers,
                                     params=querystring, verify=False)
    json_data = json.loads(post_response.text)

    if post_response.status_code == 200:
        print "200:OK"
        return json_data
    elif post_response.status_code == 201:
        print "SSL:InsecureRequestWarning"
        return json_data
    else:
        print "Trouble getting ACCESS TOKEN"
        # FUTURE - Create graceful way to end


def refresh_token(json_data):
    refresh_token = json_data['refresh_token']
    return refresh_token


def access_token(json_data):
    access_token = json_data['access_token']
    return access_token


def get_clusterinv(base_url, access_token):
    url = base_url + '/rest/appliances'
    auth = "Bearer " + access_token
    headers = {
        'content-type': "application/json",
        'authorization': auth,
        'cache-control': "no-cache"}

    # FUTURE - Possibly VERIFY Token here again to be safe??

    inv = requests.request("GET", url, headers=headers, verify=False)
    inventory = json.loads(inv.text)
    return inventory


def get_vms(base_url, access_token):
    url = base_url + '/rest/virtplatform/vms'
    auth = "Bearer " + access_token
    headers = {
        'content-type': "application/json",
        'authorization': auth,
        'cache-control': "no-cache"}

    querystring = {"entityType": "VIRTCLUSTER"}
    # FUTURE - Possibly VERIFY Token here again to be safe??
    inv = requests.request("GET", url, headers=headers,
                           params=querystring, verify=False)
    vms = json.loads(inv.text)
    return vms


base_url = connect_hx(hx_ip)
json_data = get_token(base_url)
refresh_token = refresh_token(json_data)
access_token = access_token(json_data)
inventory = get_clusterinv(base_url, access_token)
vms = get_vms(base_url, access_token)


# PRINT RESULTS
# print "\r\n"
# pretty print the JSON inventory results
# print json.dumps(inventory, indent=4, sort_keys=True)
print "\r\n"
print json.dumps(vms, indent=4, sort_keys=True)
