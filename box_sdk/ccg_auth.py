import json
from urllib.parse import urlencode
from typing import Union

from .auth_schemas import TokenRequestBoxSubjectType, TokenRequest, TokenRequestGrantType, AccessToken
from .fetch import fetch, FetchResponse, FetchOptions


class CCGConfig:
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            enterprise_id: Union[None, str] = None,
            user_id: Union[None, str] = None
    ):
        """
        :param client_id:
            Box API key used for identifying the application the user is authenticating with.
        :param client_secret:
            Box API secret used for making auth requests.
        :param enterprise_id:
            The ID of the Box Developer Edition enterprise.

            May be `None`, if the caller knows that it will not be
            authenticating as an enterprise instance / service account.

            If `user_id` is passed, this value is not used, unless
            `authenticate_enterprise()` is called to authenticate as the enterprise instance.
        :param user_id:
            The user id to authenticate. This value is not required. But if it is provided, then the user
            will be auto-authenticated at the time of the first API call.

            Should be `None` if the intention is to authenticate as the
            enterprise instance / service account. If both `enterprise_id` and
            `user_id` are non-`None`, the `user` takes precedense when `refresh()`
            is called.

            <https://developer.box.com/en/guides/applications/>
            <https://developer.box.com/en/guides/authentication/select/>
        """
        if not enterprise_id and not user_id:
            raise Exception("Enterprise ID or User ID is needed")

        self.client_id = client_id
        self.client_secret = client_secret
        self.enterprise_id = enterprise_id
        self.user_id = user_id


class CCGAuth:
    def __init__(self,  config: CCGConfig):
        """
        :param config:
            Configuration object of Client Credentials Grant auth.
        """
        self.config = config
        self.token: Union[None, str] = None

        if config.enterprise_id:
            self.subject_type = TokenRequestBoxSubjectType.ENTERPRISE
            self.subject_id = self.config.enterprise_id
        else:
            self.subject_id = self.config.user_id
            self.subject_type = TokenRequestBoxSubjectType.USER

    def retrieve_token(self) -> str:
        """
        Return a current token or get a new one when not available.
        :return:
            Access token
        """
        if self.token is None:
            return self.refresh()
        return self.token

    def refresh(self) -> str:
        """
        Fetch a new access token
        :return:
            New access token
        """
        request_body = TokenRequest(
            grant_type=TokenRequestGrantType.CLIENT_CREDENTIALS,
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            box_subject_id=self.subject_id,
            box_subject_type=self.subject_type
        )

        response: FetchResponse = fetch(
            'https://api.box.com/oauth2/token',
            FetchOptions(
                method='POST',
                body=urlencode(request_body.to_dict()),
                headers={'content-type': 'application/x-www-form-urlencoded'})
        )

        token_response = AccessToken.from_dict(json.loads(response.text))
        self.token = token_response.access_token
        return self.token

    def authenticate_user(self, user_id: str):
        """
        Get an access token for a User.

        May be one of this application's created App User. Depending on the
        configured User Access Level, may also be any other App User or Managed
        User in the enterprise.

        <https://developer.box.com/en/guides/applications/>
        <https://developer.box.com/en/guides/authentication/select/>

        :param user_id:
            The id of the user to authenticate.
        :return:
            The access token for the user.
        """
        self.subject_id = user_id
        self.subject_type = TokenRequestBoxSubjectType.USER
        return self.refresh()

    def authenticate_enterprise(self, enterprise_id: str):
        """
        Get an access token for a Box Developer Edition enterprise.

        :param enterprise_id:
            The ID of the Box Developer Edition enterprise.
        :return:
            The access token for the enterprise which can provision/deprovision app users.
        """
        self.subject_id = enterprise_id
        self.subject_type = TokenRequestBoxSubjectType.ENTERPRISE
        return self.refresh()