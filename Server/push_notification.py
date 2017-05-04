'''Push notification'''
from apns import APNs, Payload

def alert():
    '''Alert user using push notification'''
    apns = APNs(use_sandbox=True, cert_file='CertificatesPush.pem', key_file='key.pem')

    # send a notification to app
    # NOTE this is a hard code of a specific device token
    token_hex = 'xxx'
    payload = Payload(alert="Alert! Intrusion Detected!", sound="default", badge=1)
    apns.gateway_server.send_notification(token_hex, payload)

def main():
    '''Main function'''
    alert()

if __name__ == '__main__':
    main()
