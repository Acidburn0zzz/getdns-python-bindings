#!/usr/bin/env python
#

"""
Lookup an MX record and printout all the MX preference, target, and
associated IP addresses of the targets.
"""

import getdns, pprint, sys

extensions = { "return_both_v4_and_v6" : getdns.GETDNS_EXTENSION_TRUE }


def get_ip(ctx, qname):
    iplist = []
    results = ctx.address(name=qname, extensions=extensions)
    if results['status'] == getdns.GETDNS_RESPSTATUS_GOOD:
        for addr in results['just_address_answers']:
            iplist.append(addr['address_data'])
    else:
        print "getdns.address() returned an error: %d" % results['status']
    return iplist


if __name__ == '__main__':

    qname = sys.argv[1]

    ctx = getdns.Context()
    results = ctx.general(name=qname, request_type=getdns.GETDNS_RRTYPE_MX)
    status = results['status']

    hostlist = []
    if status == getdns.GETDNS_RESPSTATUS_GOOD:
        for reply in results['replies_tree']:
            answers = reply['answer']
            for answer in answers:
                if answer['type'] == getdns.GETDNS_RRTYPE_MX:
                    iplist = get_ip(ctx, answer['rdata']['exchange'])
                    for ip in iplist:
                        hostlist.append( (answer['rdata']['preference'], \
                                          answer['rdata']['exchange'], ip) )
    elif status == getdns.GETDNS_RESPSTATUS_NO_NAME:
        print "%s, %s: no such name" % (qname, qtype)
    elif status == getdns.GETDNS_RESPSTATUS_ALL_TIMEOUT:
        print "%s, %s: query timed out" % (qname, qtype)
    else:
        print "%s, %s: unknown return code: %d" % results["status"]

    for (pref, mx, addr) in sorted(hostlist):
        print pref, mx, addr
