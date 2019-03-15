This is the documentation for the IoT device that can connect through MQTT (websocket) with the AWS-IoT-SDK to AWS IoT Core. 

## Minimum Requirements

*   Python 2.7.10+ or Python 3.5+ for X.509 certificate-based mutual authentication      via port 443

*  OpenSSL version 1.0.1+ (TLS version 1.2) compiled with the Python executable for     X.509 certificate-based mutual authentication

To check for Python version:

    python --version

To check your version of OpenSSL, use the following command in a Python interpreter:

    >>> import ssl
    >>> import ssl.OPENSSL_VERSION

Use The Client:

    python client.py -e (Endpoint) -r (Root CA Path) -d ("Device ID for topic details)