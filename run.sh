#!/usr/bin/env bash

echo "Enter the HX Cluster IP Address: "
read HX_IP
echo "Enter your HX Connect Username: "
read HX_USERNAME
echo "Enter your HX Connect Password: "
read -s HX_PASSWORD
echo "Enter your HX Client ID: "
read HX_CLIENT_ID
echo "Enter your HX Client Secret: "
read -s HX_CLIENT_SECRET
echo "Enter the Redirect URI:  "
read HX_REDIRECT_URI


export HX_IP
export HX_USERNAME
export HX_PASSWORD
export HX_CLIENT_ID
export HX_CLIENT_SECRET
export HX_REDIRECT_URI

python hx_connect.py
