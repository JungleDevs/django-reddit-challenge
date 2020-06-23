"""
Accounts: Custom providers
"""
###
# Libraries
###
import requests
from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.models import (
    SocialLogin,
    SocialAccount
)
from allauth.socialaccount.providers.facebook.provider import (
    GRAPH_API_URL,
    FacebookProvider
)
from allauth.socialaccount.providers.facebook.views import (
    FacebookOAuth2Adapter,
    compute_appsecret_proof
)
from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter


###
# Auxiliary functions
###
def custom_social_login_from_response(provider, request, response):
    adapter = get_adapter(request)
    uid = provider.extract_uid(response)
    extra_data = provider.extract_extra_data(response)
    common_fields = provider.extract_common_fields(response)
    socialaccount = SocialAccount(
        extra_data=extra_data, uid=uid, provider=provider.id
    )
    common_fields['photo'] = socialaccount.get_avatar_url()
    email_addresses = provider.extract_email_addresses(response)
    provider.cleanup_email_addresses(
        common_fields.get('email'), email_addresses
    )
    sociallogin = SocialLogin(
        account=socialaccount, email_addresses=email_addresses
    )
    if request.user.is_authenticated:
        sociallogin.user = request.user
        sa = SocialAccount.objects.filter(uid=uid, provider=provider.id).first()
        if sa:
            if request.user != sa.user:
                # TODO: Merge
                sa.user.delete()
    else:
        user = sociallogin.user = adapter.new_user(request, sociallogin)
        user.set_unusable_password()
        adapter.populate_user(request, sociallogin, common_fields)

    return sociallogin


def fb_custom_login(request, app, token):
    provider = CustomFacebookProvider(request)
    resp = requests.get(
        GRAPH_API_URL + '/me',
        params={
            'fields': ','.join(provider.get_fields()),
            'access_token': token.token,
            'appsecret_proof': compute_appsecret_proof(app, token)
        })
    resp.raise_for_status()
    extra_data = resp.json()
    login = provider.sociallogin_from_response(request, extra_data)
    return login


def google_custom_login(request, app, token, profile_url):
    provider = CustomGoogleProvider(request)
    resp = requests.get(
        profile_url, params={'access_token': token.token, 'alt': 'json'}
    )
    resp.raise_for_status()
    extra_data = resp.json()
    login = provider.sociallogin_from_response(request, extra_data)
    return login


###
# Custom classes
###
# Facebook
class CustomFacebookOAuth2Adapter(FacebookOAuth2Adapter):
    def complete_login(self, request, app, access_token, **kwargs):
        return fb_custom_login(request, app, access_token)


class CustomFacebookProvider(FacebookProvider):
    def sociallogin_from_response(self, request, response):
        return custom_social_login_from_response(self, request, response)


# Google
class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def complete_login(self, request, app, access_token, **kwargs):
        return google_custom_login(request, app, access_token, self.profile_url)


class CustomGoogleProvider(GoogleProvider):
    def sociallogin_from_response(self, request, response):
        return custom_social_login_from_response(self, request, response)


###
# Signals
###
