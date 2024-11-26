$TTL 1h
@ IN SOA rasmus.rikard.com. rikve916.student.liu.se.(
	202411220; SERIAL
	2h	; Refresh
	1h	; Retry
	1w	; Expire
	1h    ) ; Minimum

;
@	IN	NS	rasmus.rikard.com.


rasmus.rikard.com. IN	A     10.0.0.2
server		   IN	CNAME rasmus.rikard.com.
client-1	   IN	A     10.0.0.3
client-2	   IN	A     10.0.0.4
gw		   IN	A     10.0.0.1
