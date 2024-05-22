"""This module contain rate limitation of the all APIs.
If incase user want to hit API offten; user throttled.

For this application usecase, impliment `Fix Window` with individual storage 
Rate Limit Algorithms

Fix Window Description:
Every use has own storage with fix rate window,
If use hit offten request; storage will be full and user threttled.

For example,
    Time Window = 60
    Request Limit = 100

Note: We have used Redis server for storing every seprate user requests.
"""
import os

import json
from typing import Any

from redis import Redis
from werkzeug.wrappers import Request, Response


rds = Redis(
    host=os.getenv("RHost", "localhost"), 
    port=os.getenv("RPort", 6379), 
    db=os.getenv("RDB", 0),
    decode_responses=True,
    retry_on_timeout=True
)

# Typings
class Environ(object): ...


class FixWindowRateLimit:

    def __init__(
        self,
        app,
        request_limit: int = 50,
        expiration: int = 60
    ) -> None:
        """
        Will fetch IP Address for user's and store into Redis HashSet.
        For efficient Count of requests.
        """
        self.app = app
        self.rlimit = request_limit
        self.expiration = expiration

    def process_request_limit(self, IPAddress: Any) -> bool:
        """
        Checks if a user can access the API within the current rate limits.

        Usage:
        - Renew storage if the current timestamp exceeds the expiration time.
        - Deny access if the user's request count exceeds the set limit.
        - Otherwise, increment the user's request count and allow API access.

        Examples:
        - If the current timestamp minus the start time exceeds the expiration time, renew storage.
        - If user's request limit is exceeded, access is denied.
        - If conditions are met, increment the request count and allow access.
        """
        urlimit = rds.get(name=IPAddress)
        if not urlimit:
            rds.set(name=IPAddress, value=1)
            rds.expire(name=IPAddress, time=60, nx=True)
            return True

        # If rate limit above the mentionded limit,
        if int(urlimit) >= self.rlimit:
            return False

        # Add number of counts,
        rds.set(name=IPAddress, value=int(urlimit)+1, ex=rds.ttl(name=IPAddress))
        return True

    def __call__(self, environ: Environ, start_response) -> Any:
        """
        Handles API access requests by invoking the `process_request_limit` method.

        Behavior:
        - Checks the `user_id` against the request limit.
        - If `process_request_limit` returns False, the user is throttled.
        - If True, access to the API is granted.
        """
        ip = Request(environ=environ).remote_addr

        if self.process_request_limit(IPAddress=ip):
            return self.app(environ, start_response)

        resp = Response(
            response=json.dumps({
                "status": "error",
                "message": (
                    "Rate Limit Exceeded: You have exceeded the maximum number of requests"
                    + "allowed within a certain time period. Please try again later."
                ),
                "data": None
            }),
            mimetype="application/json",
            status=429
        )
        return resp(environ=environ, start_response=start_response)
