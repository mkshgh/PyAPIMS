# Import libraries
import rsa
import json
import base64
import requests
from datetime import datetime
from rsa.key import PrivateKey

# This is how an private RSA key should look like
pvtKey:str = """-----BEGIN RSA PRIVATE KEY-----
MIIEoQIBAAKCAQB+JjM3uxtJ3K9gNTEp/7ACchDlrQbVESeJKUwVKG444UEPKFM5
BBBu2Cx4BqWq41aUyjIxaolpO8AX7pNNWX0WF04VoRP9Xq65wBDADit+R9eKEXNm
fkjzXZWyVtIiBo1bJ+wIy2FFikNqW5NXnvuvmMm6uo4UmenzrGqxfL5V3ChAR7XO
svpMnq/75wsZ96sieSFSwnibEHNzbZsA0Y265ZniD2uggqQqLPrVbdwfvK7xPBCI
ifjgtPxEppBGC6D3fIzKlOUDpPlO9VEuQkLLFpc0onBGxa1Nwg3CSYeBj/a7+wgH
bUMb4ZFKoeg3TuXXFDxojWeeq5XHeSJWqDf3AgMBAAECggEAYM4Ht9jJ1CCaJIYt
OEGSXA4UkWv6Nj93y3X5gLMKAnQ5bNxRIQvRYH5bga/4Ke9TXdLcObe7wxmrC7J1
L4JgzzcLIOX/ZQvnoXuWXwuArOOMr9M8b4axjLBgU/70OlA04aL9KrKH7slveorT
wwWpttLU24qVxZFnSysgpRtJJLE2i97TOZWd6HccsggfH+f9gjaCNBkzDIgk2fVJ
SDhdpiWBPt0p7ZocCvprRIPcxJ+z4FYdD85wn3ls0s5Gi5CnriAGTqRVYzyU4X5f
HF3zwjanTfNZxWlvTTWOW3neh5bdQx9hQN5BbDEw59S3JCm9wtejAxGg5L1VOt0P
a8WnAQKBgQDi4Mn8mcGtUFGZxI1csAiGd4/ZapR2mBZitgRGekZajBkLRkXLNyGK
AFFU4Bi09x6FR8zZ4tWzCkFjtLjZMB+z/c7UTHZbxjFr24DqCqEyp5OG5+cYS/LP
d6YLJNd1y0Uwjm5Z81sEISHvyPAW56vXYN9fT2GMVKb7nQlppirgFwKBgQCOV3Y8
NT5j8TgwvasUPU6hKhtd9xEUPxEGkao5j0+dJkWlxxAiDpbJOP5+ulnZj2C7FKAd
Gs2pMKk+866hMCaW/yMKAUBqs1o5BfoXOnLShnRgJyG4fMrm18ZQBcuGjpSzb4Ql
k433/P7ORoRbRfs10RdfEdvBmgvMzYRgVqFzIQKBgFz1BU1+IiDE2+pI4jKr3ZJa
wpGuXY4J2oIvWakWyGSpKkm4TThqKk/EuY4xE25yIgsx0/kiO7TT6t7TWTmDwjmZ
MHlDqusHVZB/q145ZLrAdm277q/Bzoa620mNmsokswCmGwi38P7MJH9+sQBxg7MH
ef4vJCS/Onu1Z/nln4OZAoGAY4xTimQKUEdBbwUXAr6loR0bqqnB7hD1TUzOahcK
LPO5PelsJQVi+zO6+NJHSFp34h7Yo8I9FxiLJRWzidNtCalBzht1+6mXbc36TAh6
iTWzahO0B5xvIubBMPH8lwxcful81/LMFSWA5q52nobg25Bx8fFBabLckc0hyWaM
30ECgYBpnaZh1Dd0V2KuQnHyJPwH7HZ8LhlEpS/bc/UpLtjfBMCrugWVm6RBTTyd
6F8YVMCzmQGkdT4oW0d/aNJYzJI39xxwnzGQ56b5IlJksaBO2vG3uHh/I1JW63Ht
0UoUJLdPvtAbRQ6oyK8G+nBHSzC0yPqA9acSfUZ29TEB71LPGA==
-----END RSA PRIVATE KEY-----"""


"""ApiEndPoint and UserCreds"""
pvtKey:str = "see_above_for_format"
api_url:str = 'http://mukeshg.com.np/api/v1/connect'
my_user:str = "mukes@123"
my_pass:str = "mukes@123"

"""Required Payload Method, Data and Signature"""
# private key loaded
privateRSAkey:PrivateKey = rsa.PrivateKey.load_pkcs1(pvtKey)
# Generate Dynamically  # TimeStamp = str(datetime.datetime.now()).replace(" ","T")
TimeStamp = str(datetime.today().strftime('%Y-%m-%dT%H:%M:%S.000%z'))
# Used balanceEnquiry method as an example
function_name:str = "BalanceEnquiry" #name of the function
payload_data:dict = {"TransactionId":"123","AccountNumber":"1900000001"}
signature_payload:dict = {"Model":payload_data,"TimeStamp":TimeStamp} # Added the Time Stamp here


"""Convert Data and Signature to bytes and sign the payload"""
# Data to Bytes
payload_data_bytes:bytes=json.dumps(payload_data).replace(" ","").encode()
signature_payload_bytes:bytes = json.dumps(signature_payload).replace(" ","").encode()
#Load the private Key and sign the payload
signature:bytes = rsa.sign(signature_payload_bytes, privateRSAkey, 'SHA-256') # Signature is hash of the data generated with the private key loaded above

"""Forming the payload data and signature as mentioned in the documentation"""
# Encode the data to base64 format + Decode the data back to string as input is string in the request format
payload_data:str = base64.b64encode(payload_data_bytes).decode('UTF-8') # payload_data
# Signature is hash of the data generated with the private key loaded above
payload_signature:str = base64.b64encode(signature).decode('UTF-8') # payload_signature

# Creating the payload json
real_payload:json = json.dumps(
    {"FunctionName" : function_name,
    "Data": payload_data,
    "Signature": payload_signature,
    "TimeStamp": TimeStamp
    }
)

"""Forming the header as mentioned in the documentation"""
#base64 credentials for authentication
base64_credentials:str = str(base64.b64encode((my_user+':'+my_pass).encode()).decode())

# Creating the header dictionary
Header_dict:dict= {
    'Authorization' : 'Basic %s' % base64_credentials,
    "Content-Type": "application/json"
}


"""Sending the request and Receiving the response"""
# Your request is sent now somewhere in the magiclands to the server
resp:json = requests.request("POST",api_url, headers=Header_dict, data=real_payload )
# Response from the Server
print(resp.headers)
print(resp.status_code)
# Response Json when you actually hit the API
print(resp.text)
