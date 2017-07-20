# OpenDXL-ATD-WebGateway
This integration is focusing on the automated threat response with McAfee ATD, OpenDXL and McAfee Web Gateway.
McAfee Advanced Threat Defense (ATD) will produce local threat intelligence that will be pushed via DXL. An OpenDXL wrapper will 
subscribe and parse IP indicators ATD produced and will create a subscribed list of IP's for the McAfee Web Gateway.

![41_atd_mwg](https://cloud.githubusercontent.com/assets/25227268/25073995/a043939e-22f2-11e7-8b4f-ce7d43c18ddf.PNG)

## Component Description

**McAfee Advanced Threat Defense (ATD)** is a malware analytics solution combining signatures and behavioral analysis techniques to rapidly 
identify malicious content and provides local threat intelligence. ATD exports IOC data in STIX format in several ways including the DXL.
https://www.mcafee.com/in/products/advanced-threat-defense.aspx

**McAfee Web Gateway (MWG)** delivers comprehensive security for all aspects of web traffic combined with industry-leading, proactive 
detection of zero-day malware with full coverage of web traffic, including SSL. https://www.mcafee.com/au/products/web-gateway.aspx

## Prerequisites
McAfee ATD solution (tested with ATD 3.8)

McAfee Web Gateway (tested with MWG 7.7.1.2)

Download the [Latest Release](https://github.com/mohl1/OpenDXL-ATD-WebGateway/releases)
   * Extract the release .zip file

OpenDXL Python installation
1. Python SDK Installation ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/installation.html))
    Install the required dependencies with the requirements.txt file:
    ```sh
    $ pip install -r requirements.txt
    ```
    This will install the dxlclient, and requests modules. 
2. Certificate Files Creation ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/certcreation.html))
3. ePO Certificate Authority (CA) Import ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/epocaimport.html))
4. ePO Broker Certificates Export ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/epobrokercertsexport.html))

Apache2

## Configuration
McAfee ATD receives files from multiple sensors like Endpoints, Web Gateways, Network IPS or via Rest API. 
ATD will perform malware analytics and produce local threat intelligence. After an analysis every indicator of comprise will be published 
via the Data Exchange Layer (topic: /mcafee/event/atd/file/report). 

McAfee ATD will update the McAfee Threat Intelligence (TIE) server with malicious hash information (MWG is able to lookup TIE). 
However malicious IP's (ATD discovered) are not used in the threat response. With OpenDXL it is possible to extend these capabilities. The script will automatically add the new discovered malicious IP's to a list. The McAfee Web Gateway is able to pull information from this shared lists. (https://community.mcafee.com/docs/DOC-5208)

### atd_subscriber.py
The atd_subscriber.py receives DXL messages from ATD, filters out discovered IP's and loads web.py.

Change the CONFIG_FILE path in the atd_subscriber.py file

`CONFIG_FILE = "/path/to/config/file"`

### web.py
The web.py script receives only the discovered malicious IP's and checks if the IP is already on the subscribed list. If not this IP will be added to the list (/var/www/html/web/subscribedlist). The subscribedlist is in the following format:

`type=ip`

`"1.1.1.1"`

### McAfee Web Gateway
Add a new subscribed list in the McAfee Web Gateway and point it to the subscribed list. (https://community.mcafee.com/docs/DOC-5208)
Also create a new block rule related to the subscribed list.

![42_atd_mwg](https://cloud.githubusercontent.com/assets/25227268/25074249/32d8e912-22f7-11e7-86fc-285bb960024d.PNG)

## Run the OpenDXL wrapper
> python atd_subscriber.py

or

> nohup python atd_subscriber.py &

## Summary
With this use case, ATD produces local intelligence that is immediatly updating cyber defense countermeassures like the 
McAfee Web Gateway with malicious IP's.
