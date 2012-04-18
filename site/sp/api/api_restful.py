

restful_list = [
	[ r"^org$", 'org.index' ],
	[ r"^org/(?P<oid>\w{32})$", 'org.view' ],
	[ r"^org/(?P<oid>\w{32})/clients$", 'org.client.index' ],
	[ r"^org/(?P<oid>\w{32})/client/(?P<cid>\d+)$", 'org.client.view' ],
	[ r"^org/(?P<oid>\w{32})/client/(?P<cid>\d+)$", 'org.client.view' ],
]


