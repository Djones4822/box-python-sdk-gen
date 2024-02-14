from typing import Optional

from typing import Dict

from typing import List

from box_sdk_gen.managers.authorization import RequestAccessTokenGrantType

from box_sdk_gen.managers.authorization import RequestAccessTokenSubjectTokenType

from box_sdk_gen.auth import Authentication

from box_sdk_gen.network import NetworkSession

from box_sdk_gen.schemas import AccessToken

from box_sdk_gen.schemas import PostOAuth2Token

from box_sdk_gen.schemas import PostOAuth2Revoke

from box_sdk_gen.managers.authorization import AuthorizationManager

from box_sdk_gen.token_storage import TokenStorage

from box_sdk_gen.token_storage import InMemoryTokenStorage

from box_sdk_gen.json_data import sd_to_url_params

from box_sdk_gen.utils import prepare_params

from box_sdk_gen.errors import BoxSDKError

box_oauth_2_auth_url: str = 'https://account.box.com/api/oauth2/authorize'


class OAuthConfig:
    def __init__(
        self, client_id: str, client_secret: str, token_storage: TokenStorage = None
    ):
        if token_storage is None:
            token_storage = InMemoryTokenStorage()
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_storage = token_storage


class GetAuthorizeUrlOptions:
    def __init__(
        self,
        client_id: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        response_type: Optional[str] = None,
        state: Optional[str] = None,
        scope: Optional[str] = None,
    ):
        """
        :param client_id: Box API key used for identifying the application the user is authenticating with
        :type client_id: Optional[str], optional
        :param redirect_uri: The URI to which Box redirects the browser after the user has granted or denied the application permission. This URI match one of the redirect URIs in the configuration of your application.
        :type redirect_uri: Optional[str], optional
        :param response_type: The type of response we would like to receive.
        :type response_type: Optional[str], optional
        :param state: A custom string of your choice. Box will pass the same string to the redirect URL when authentication is complete. This parameter can be used to identify a user on redirect, as well as protect against hijacked sessions and other exploits.
        :type state: Optional[str], optional
        :param scope: A space-separated list of application scopes you'd like to authenticate the user for. This defaults to all the scopes configured for the application in its configuration page.
        :type scope: Optional[str], optional
        """
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.state = state
        self.scope = scope


class BoxOAuth(Authentication):
    def __init__(self, config: OAuthConfig, **kwargs):
        """
        :param config: Configuration object of OAuth.
        :type config: OAuthConfig
        """
        super().__init__(**kwargs)
        self.config = config
        self.token_storage = self.config.token_storage

    def get_authorize_url(self, options: GetAuthorizeUrlOptions = None) -> str:
        """
        Get the authorization URL for the app user.
        """
        if options is None:
            options = GetAuthorizeUrlOptions()
        params: Dict[str, str] = prepare_params(
            {
                'client_id': (
                    options.client_id
                    if not options.client_id == None
                    else self.config.client_id
                ),
                'response_type': (
                    options.response_type
                    if not options.response_type == None
                    else 'code'
                ),
                'redirect_uri': options.redirect_uri,
                'state': options.state,
                'scope': options.scope,
            }
        )
        return ''.join([box_oauth_2_auth_url, '?', sd_to_url_params(params)])

    def get_tokens_authorization_code_grant(
        self, authorization_code: str, network_session: Optional[NetworkSession] = None
    ) -> AccessToken:
        """
        Acquires token info using an authorization code.
        :param authorization_code: The authorization code to use to get tokens.
        :type authorization_code: str
        :param network_session: An object to keep network session state
        :type network_session: Optional[NetworkSession], optional
        """
        auth_manager: AuthorizationManager = (
            AuthorizationManager(network_session=network_session)
            if not network_session == None
            else AuthorizationManager()
        )
        token: AccessToken = auth_manager.request_access_token(
            grant_type=RequestAccessTokenGrantType.AUTHORIZATION_CODE.value,
            code=authorization_code,
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
        )
        self.token_storage.store(token)
        return token

    def retrieve_token(
        self, network_session: Optional[NetworkSession] = None
    ) -> AccessToken:
        """
        Get the current access token. If the current access token is expired or not found, this method will attempt to refresh the token.
        :param network_session: An object to keep network session state
        :type network_session: Optional[NetworkSession], optional
        """
        token = self.token_storage.get()
        if token == None:
            raise BoxSDKError(
                message='Access and refresh tokens not available. Authenticate before making any API call first.'
            )
        return token

    def refresh_token(
        self,
        network_session: Optional[NetworkSession] = None,
        refresh_token: Optional[str] = None,
    ) -> AccessToken:
        """
        Get a new access token for the app user.
        :param network_session: An object to keep network session state
        :type network_session: Optional[NetworkSession], optional
        :param refresh_token: A refresh token to use
        :type refresh_token: Optional[str], optional
        """
        old_token: Optional[AccessToken] = self.token_storage.get()
        token_used_for_refresh = (
            refresh_token
            if not refresh_token == None
            else old_token.refresh_token if not old_token == None else None
        )
        auth_manager: AuthorizationManager = (
            AuthorizationManager(network_session=network_session)
            if not network_session == None
            else AuthorizationManager()
        )
        token: AccessToken = auth_manager.request_access_token(
            grant_type=RequestAccessTokenGrantType.REFRESH_TOKEN.value,
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            refresh_token=token_used_for_refresh,
        )
        self.token_storage.store(token)
        return token

    def revoke_token(self, network_session: Optional[NetworkSession] = None) -> None:
        """
        Revoke an active Access Token, effectively logging a user out that has been previously authenticated.
        :param network_session: An object to keep network session state
        :type network_session: Optional[NetworkSession], optional
        """
        token: Optional[AccessToken] = self.token_storage.get()
        if token == None:
            return None
        auth_manager: AuthorizationManager = (
            AuthorizationManager(network_session=network_session)
            if not network_session == None
            else AuthorizationManager()
        )
        auth_manager.revoke_access_token(
            self.config.client_id, self.config.client_secret, token.access_token
        )
        self.token_storage.clear()
        return None

    def downscope_token(
        self,
        scopes: List[str],
        resource: Optional[str] = None,
        shared_link: Optional[str] = None,
        network_session: Optional[NetworkSession] = None,
    ) -> AccessToken:
        """
        Downscope access token to the provided scopes. Returning a new access token with the provided scopes, with the original access token unchanged.
        :param scopes: The scope(s) to apply to the resulting token.
        :type scopes: List[str]
        :param resource: The file or folder to get a downscoped token for. If None and shared_link None, the resulting token will not be scoped down to just a single item. The resource should be a full URL to an item, e.g. https://api.box.com/2.0/files/123456.
        :type resource: Optional[str], optional
        :param shared_link: The shared link to get a downscoped token for. If None and item None, the resulting token will not be scoped down to just a single item.
        :type shared_link: Optional[str], optional
        :param network_session: An object to keep network session state
        :type network_session: Optional[NetworkSession], optional
        """
        token: Optional[AccessToken] = self.token_storage.get()
        if token == None or token.access_token == None:
            raise BoxSDKError(message='No access token is available.')
        auth_manager: AuthorizationManager = (
            AuthorizationManager(network_session=network_session)
            if not network_session == None
            else AuthorizationManager()
        )
        downscoped_token: AccessToken = auth_manager.request_access_token(
            grant_type=RequestAccessTokenGrantType.URN_IETF_PARAMS_OAUTH_GRANT_TYPE_TOKEN_EXCHANGE.value,
            subject_token=token.access_token,
            subject_token_type=RequestAccessTokenSubjectTokenType.URN_IETF_PARAMS_OAUTH_TOKEN_TYPE_ACCESS_TOKEN.value,
            resource=resource,
            scope=' '.join(scopes),
            box_shared_link=shared_link,
        )
        return downscoped_token
