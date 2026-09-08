from __future__ import annotations

from typing import Any, Dict, Mapping, Optional
from urllib.parse import urlencode, urljoin

import httpx

from ._core import OwlVigilError, OwlVigilOAuthError


class OAuth2:
    def __init__(self, base_url: str, client: httpx.Client, timeout: float) -> None:
        self.base_url = base_url.rstrip("/")
        self.client = client
        self.timeout = timeout

    def authorization_url(
        self,
        client_id: str,
        redirect_uri: str,
        scopes: Optional[list[str]] = None,
        state: Optional[str] = None,
        code_challenge: Optional[str] = None,
        code_challenge_method: Optional[str] = None,
        parameters: Optional[Mapping[str, str]] = None,
    ) -> str:
        return _authorization_url(self.base_url, client_id, redirect_uri, scopes, state, code_challenge, code_challenge_method, parameters)

    def exchange(self, client_id: str, code: str, redirect_uri: str, client_secret: Optional[str] = None, code_verifier: Optional[str] = None) -> Dict[str, Any]:
        return self._token("oauth/token", {"grant_type": "authorization_code", "client_id": client_id, "client_secret": client_secret, "code": code, "redirect_uri": redirect_uri, "code_verifier": code_verifier})

    def refresh(self, client_id: str, refresh_token: str, client_secret: Optional[str] = None) -> Dict[str, Any]:
        return self._token("oauth/token/refresh", {"grant_type": "refresh_token", "client_id": client_id, "client_secret": client_secret, "refresh_token": refresh_token})

    def client_credentials(self, client_id: str, client_secret: str, scopes: Optional[list[str]] = None) -> Dict[str, Any]:
        return self._token("oauth/token", {"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret, "scope": " ".join(scopes) if scopes else None})

    def revoke(self, token: str) -> None:
        if not token.strip():
            raise OwlVigilError("OAuth token is required")
        self._token("oauth/revoke", {"token": token}, allow_empty=True)

    def user_info(self, access_token: str) -> Dict[str, Any]:
        if not access_token.strip():
            raise OwlVigilError("OAuth access token is required")
        try:
            response = self.client.get(urljoin(self.base_url + "/", "oauth/userinfo"), headers={"accept": "application/json", "authorization": "Bearer " + access_token}, timeout=self.timeout)
        except httpx.TransportError as error:
            raise OwlVigilError("owlvigil: OAuth request failed") from error
        if not response.is_success:
            raise _oauth_error(response)
        return _json_object(response)

    def _token(self, path: str, values: Mapping[str, Optional[str]], allow_empty: bool = False) -> Dict[str, Any]:
        form = {key: value for key, value in values.items() if value not in (None, "")}
        try:
            response = self.client.post(urljoin(self.base_url + "/", path), data=form, headers={"accept": "application/json"}, timeout=self.timeout)
        except httpx.TransportError as error:
            raise OwlVigilError("owlvigil: OAuth request failed") from error
        if not response.is_success:
            raise _oauth_error(response)
        if not response.content and allow_empty:
            return {}
        return _json_object(response)


class AsyncOAuth2:
    def __init__(self, base_url: str, client: httpx.AsyncClient, timeout: float) -> None:
        self.base_url = base_url.rstrip("/")
        self.client = client
        self.timeout = timeout

    def authorization_url(self, client_id: str, redirect_uri: str, scopes: Optional[list[str]] = None, state: Optional[str] = None, code_challenge: Optional[str] = None, code_challenge_method: Optional[str] = None, parameters: Optional[Mapping[str, str]] = None) -> str:
        return _authorization_url(self.base_url, client_id, redirect_uri, scopes, state, code_challenge, code_challenge_method, parameters)

    async def exchange(self, client_id: str, code: str, redirect_uri: str, client_secret: Optional[str] = None, code_verifier: Optional[str] = None) -> Dict[str, Any]:
        return await self._token("oauth/token", {"grant_type": "authorization_code", "client_id": client_id, "client_secret": client_secret, "code": code, "redirect_uri": redirect_uri, "code_verifier": code_verifier})

    async def refresh(self, client_id: str, refresh_token: str, client_secret: Optional[str] = None) -> Dict[str, Any]:
        return await self._token("oauth/token/refresh", {"grant_type": "refresh_token", "client_id": client_id, "client_secret": client_secret, "refresh_token": refresh_token})

    async def client_credentials(self, client_id: str, client_secret: str, scopes: Optional[list[str]] = None) -> Dict[str, Any]:
        return await self._token("oauth/token", {"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret, "scope": " ".join(scopes) if scopes else None})

    async def revoke(self, token: str) -> None:
        if not token.strip():
            raise OwlVigilError("OAuth token is required")
        await self._token("oauth/revoke", {"token": token}, allow_empty=True)

    async def user_info(self, access_token: str) -> Dict[str, Any]:
        if not access_token.strip():
            raise OwlVigilError("OAuth access token is required")
        try:
            response = await self.client.get(urljoin(self.base_url + "/", "oauth/userinfo"), headers={"accept": "application/json", "authorization": "Bearer " + access_token}, timeout=self.timeout)
        except httpx.TransportError as error:
            raise OwlVigilError("owlvigil: OAuth request failed") from error
        if not response.is_success:
            raise _oauth_error(response)
        return _json_object(response)

    async def _token(self, path: str, values: Mapping[str, Optional[str]], allow_empty: bool = False) -> Dict[str, Any]:
        form = {key: value for key, value in values.items() if value not in (None, "")}
        try:
            response = await self.client.post(urljoin(self.base_url + "/", path), data=form, headers={"accept": "application/json"}, timeout=self.timeout)
        except httpx.TransportError as error:
            raise OwlVigilError("owlvigil: OAuth request failed") from error
        if not response.is_success:
            raise _oauth_error(response)
        if not response.content and allow_empty:
            return {}
        return _json_object(response)


def _json_object(response: httpx.Response) -> Dict[str, Any]:
    try:
        payload = response.json()
    except ValueError as error:
        request_id = response.headers.get("x-request-id", response.headers.get("request-id", ""))
        suffix = f" request_id={request_id}" if request_id else ""
        raise OwlVigilError(f"owlvigil: invalid OAuth JSON response status={response.status_code}{suffix}") from error
    if not isinstance(payload, dict):
        raise OwlVigilError(f"owlvigil: invalid OAuth JSON response status={response.status_code}")
    return payload


def _authorization_url(base_url: str, client_id: str, redirect_uri: str, scopes: Optional[list[str]], state: Optional[str], code_challenge: Optional[str], code_challenge_method: Optional[str], parameters: Optional[Mapping[str, str]]) -> str:
    values: Dict[str, str] = {"response_type": "code", "client_id": client_id, "redirect_uri": redirect_uri}
    if scopes:
        values["scope"] = " ".join(scopes)
    if state:
        values["state"] = state
    if code_challenge:
        values["code_challenge"] = code_challenge
    if code_challenge_method:
        values["code_challenge_method"] = code_challenge_method
    values.update(parameters or {})
    return urljoin(base_url.rstrip("/") + "/", "oauth/authorize") + "?" + urlencode(values)


def _oauth_error(response: httpx.Response) -> OwlVigilOAuthError:
    code = ""
    description = response.reason_phrase or "OAuth request failed"
    uri = ""
    try:
        payload = response.json()
        if isinstance(payload, dict):
            code = str(payload.get("error", ""))
            description = str(payload.get("error_description", description))
            uri = str(payload.get("error_uri", ""))
    except ValueError:
        pass
    return OwlVigilOAuthError(response.status_code, code, description, uri)
