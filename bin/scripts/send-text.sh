#!/bin/bash
# Splunk Perimeter Security - Twilio-Powered Alert Script Wrapper

if [ ! -f "$SPLUNK_HOME/var/log/splunk/perimeter-security-alerts.log" ]; then
	touch $SPLUNK_HOME/var/log/splunk/perimeter-security-alerts.log
fi

{
	#echo "0 = [$0]"
	#echo "1 = [$1]"
	#echo "2 = [$2]"
	#echo "3 = [$3]"
	#echo "4 = [$4]"
	#echo "5 = [$5]"
	#echo "6 = [$6]"
	#echo "7 = [$7]"
	#echo "8 = [$8]"
	#echo ""
	ScriptPath="$( cd "$(dirname "$0")" ; pwd -P )"
	#echo "$ScriptPath/send-text.py \"$4\" \"$8\""
	env - $ScriptPath/send-text.py "$4" "$8"
} >> $SPLUNK_HOME/var/log/splunk/perimeter-security-alerts.log
