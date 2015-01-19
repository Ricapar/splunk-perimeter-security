# Splunk Perimeter Security
![App Icon](http://i.imgur.com/Saux3ZP.png)

We use tools like Splunk on a daily basis to ensure the security of our most
important assets. From firewall logs, to proxy logs, Unix syslog to
Windows Event Logs, we're able to collect, filter, analyze, and report on all this
information within Splunk to provide a 360 degree view of our security posture.

However, all these things can be rendered meaningless if someone is able to walk into
a closet, an office, or a datacenter and walk out with an asset containing valuable 
information.

It is part of a security engineer's job to ensure that an in-depth security plan
is in place, and that includes logging, monitoring, and auditing of access to
physical assets and entry into restricted areas.

Splunk Perimeter Security is a monitoring package for Splunk with a focus on
logging, monitoring, and alerting on events generated from access to physical
locations using CIM-compliant Alert logs from a pre-existing or custom-made
alarm or security monitoring system. For certain applicaitons, if deployed properly,
it can greatly augment or replace a traditional physical alarm system.

The application includes several dashboards that enable monitoring and include auditing of
physical access events to a home, office, or a datacenter. 

# Warning About Alarm Systems
Alarm systems come in many shapes and forms and can range from simple hard-wired home
systems to millitary grade security. If you are going to make modifications to your
alarm system, please proceed with caution and ensure you aren't disabling or interfering
with something that may sound a panic alarm, call the authorities, or trap you in a room
and proceed to fill it with nerve gas. Treat your alarm system as you would any 
mission-critical production system. 

# Common Information Model Compliance
When possible, the application attempts to generate and use Common Information Model 
compliant events. 

The dashboards, alerting script, and Raspberry Pi monitoring scripts follow the
[Alerts Data Model](http://docs.splunk.com/Documentation/CIM/4.1.0/User/Alerts) 
as defined by the CIM.

To account for specific physical security-related events, the fields listed below
are also expected to be present within events. A `*` indicates the field is not
part of the CIM, but is required to be present in the app for all dashboard features
to work as designed.

Field Name   | Description / Use
------------ | ------------------------------
src          | A unique identifier for the zone being monitored.
src_category | A value of `zone_trigger` is used when a zone changes state, 
body         | A value of `open` or `closed` indicating the state of the zone.
type         | A value of `alert` is used when a zone changes state, `event` for periodic status messages.
*zone        | Aliased from `src`. Used by lookup tables.  
*zone_name   | A display name to be used when alerting and displaying information about a specific zone.
*zone_active | Must be set to "true" for a zone to be able to trigger alerts or be displayed on dashboards. By default this is set using a provided lookup table.


# RaspberryPi Proof of Concept

As a proof of concept, as well as a sample implementation for a home alarm system,
the app includes a TA-PerimeterSecurity package that can be deployed to a RaspberryPi that
is wired into a home security system through the onboard GPIO pins.

The [http://raspberrypi.org](Raspberry Pi) is a small, low-power ARM computer that is ideal for
running small web servers, home automation, and general tinkering. When wired correctly,
it is possible to monitor the GPIO (General Purpose I/O) pins on the computer using a small
Python script. Using the [Splunk Forwarder for Linux ARM](https://apps.splunk.com/app/1611/),
you can monitor the output of the Python script and use it to build a set of dashboards, reports,
and alerts for your alarm system.

For more information about building an alarm system using a Raspberry Pi, see the documentation
for [TA - Splunk Perimeter Security](https://github.com/Ricapar/ta-splunk-perimeter-security).

Included in the Raspberry Pi TA is a sample data file from Sunday, January 18th 2014.

# Requirements 
## Splunk Server Requirements
* Splunk 6 or greater
* Python 2.7 or greater
* [Twilio Python Helper Library](https://www.twilio.com/docs/python/install) for text message alerting


# Twilio Alerting Setup
If enabled, the application supports triggering alerts if the system is in 
an "armed" state. Included is a script that can be triggered via a real-time alert
to notify a list of contacts (populated via a lookup table) via text messaging using
the Twilio API.

The [Twilio Python Helper Library](https://www.twilio.com/docs/python/install) library must be
installed for text message alerting to work. This is not required for the rest of the app to 
function, but you will be unable to send alerts using the provided script if it is not installed.

On your Splunk server, run:

```sudo pip install twilio```

This will install the necessary libraries onto your system Python installation. NOTE: Splunk's Python
installation is not sufficient for this script to work.

Within the Splunk `$SPLUNK_HOME/etc/apps/perimeter-security/bin/scripts/` directory are two files:

File            | Purpose 
--------------- | --------
send-text.sh	| Wrapper script to call send-text.py
send-text.py    | Handles sending of text messages via the Twilio API

You will need to modify `send-text.py` before you can call it within an alert. Open the file, and edit these lines:

```
# =Variable Definitions=
Twilio_From = "<your Twilio phone number>"
Twilio_SID = "<your Twilio SID>"
Twilio_Auth = "<your Twilio Auth key - keep this secret!>"
# /=Variable Definitions=
```

Lastly, you will need to configure a lookup table to list out which phone numbers should be
notified when an alert is triggered.

Open `$SPLUNK_HOME/etc/apps/perimeter-security/lookups/alert_phones.csv` and add phone numbers, one
per line. You must include your country code and area code. 

```
alert_phone
+15550001234
+15550004321
```

# Closing Notes

This app was written by [Rich Acosta](http://ricapar.net/) and [Erica Feldman](www.linkedin.com/in/ericafeldman)
for the [Splunk Apptitude](http://splunk.challengepost.com) contest.

This project is licensed under the MIT License. See `LICENSE` for full details. 

## Future Enhancements

Below are some ideas for enhancements to the application.

* Allow enabling and disabling of the alarm via incoming text messages
* Make use of Splunk's RBAC settings to only allow specific users to enable/disable the alarm system
* Add the user's ID to the audit log of alarm enable/disable settings.
* Heath checks on Raspberry Pi GPIO pin monitoring daemon.
* Compliance with physical access logging and auditing standards defined by various governmental and standards organizations.

## Credits 
Thanks to stackd/wayoutmind for an excellent Python daemon module:

* [https://github.com/stackd/daemon-py](https://github.com/stackd/daemon-py)

 

