'''Push notification'''
from apns import APNs, Payload

def alert():
    '''Alert user using push notification'''
    apns = APNs(use_sandbox=True, cert_file='CertificatesPush.pem', key_file='key.pem')

    # send a notification to app
    # NOTE this is a hard code of a specific device token
    token_hex = '6FFC2016CAE8BF9310774DDC52CB00F72F6E7386AD2167B8DE5A42471FC8C789'
    payload = Payload(alert="alert", sound="default", badge=1)
    apns.gateway_server.send_notification(token_hex, payload)

def main():
    '''Main function'''
    alert()

if __name__ == '__main__':
    main()
