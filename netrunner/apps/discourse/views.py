from django.shortcuts import render

import base64
import hmac
import hashlib
import urllib

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.conf import settings

from urllib.parse import parse_qs

@login_required
def sso(request):
    payload = request.GET.get('sso')
    signature = request.GET.get('sig')

    if None in [payload, signature]:
        return HttpResponseBadRequest('No SSO payload or signature. Please contact support if this problem persists.')

    ## Validate the payload

    try:
        payload = urllib.parse.unquote(payload)
        decoded = base64.b64decode(payload)
        assert 'nonce' in decoded.decode('ascii')
        assert len(payload) > 0
    except AssertionError:
        return HttpResponseBadRequest('Invalid payload. Please contact support if this problem persists.')

    key = settings.DISCOURSE_SSO_SECRET # must not be unicode
    h = hmac.new(str.encode(key),str.encode(payload),digestmod=hashlib.sha256)
    this_signature = h.hexdigest()

    if this_signature != signature:
        return HttpResponseBadRequest('Invalid payload. Please contact support if this problem persists.')
    ## Build the return payload

    qs = parse_qs(decoded.decode('ascii'))
    params = {
        'nonce': qs['nonce'][0],
        'email': request.user.email,
        'external_id': request.user.id,
        'username': request.user.username,
    }

    return_payload = base64.b64encode(str.encode(urllib.parse.urlencode(params)))
    h = hmac.new(str.encode(key), return_payload, digestmod=hashlib.sha256)
    query_string = urllib.parse.urlencode({'sso': return_payload, 'sig': h.hexdigest()})

    ## Redirect back to Discourse

    url = '%s/session/sso_login' % settings.DISCOURSE_BASE_URL
    return HttpResponseRedirect('%s?%s' % (url, query_string))