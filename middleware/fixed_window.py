"""
This module implements a fixed window rate limiting algorithm. 
It is designed to restrict the rate at which
requests can be made by an entity within a specified time window, 
thus preventing abuse and ensuring fair use of resources.

Example:
    Time Window = 60
    Request Limit = 100
"""
import datetime
import logging
import jwt

from typing import Any
from werkzeug.wrappers import Request, Response


# Logger Basic Configuration
logging.basicConfig(level=logging.INFO)


class Environ(object): ...


class FixWindowRateLimit:

    def __init__(
        self, 
        app, 
        request_limit: int = 100, 
        expiration: int = 60
    ) -> None:
        """
        Every upcoming request will be stored in RAM for quick fetch.
        For quick fetch from the RAM will use hash table (BuiltIn Dictionary)

        Args:
            app: Application level
            request_limit: Ever user have maximum default limit is 100 withing 60 second time window.
            expiration: After expiration time request_limit will automatically renew.
        """
        self.app = app
        self.storage = dict()
        self.request_limit = request_limit
        self.expiration = expiration
    
    def process_request_limit(self, user_id: Any) -> bool:
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

        if not self.storage.get(user_id, None):
            self.storage[user_id] = {
                "limit": 1,
                "start_time": datetime.datetime.now()
            }
        
        user_req_limit =  self.storage[user_id]["limit"]
        start_time = self.storage[user_id]["start_time"]

        if (
            (datetime.datetime.now() - start_time).seconds > self.expiration
        ):
            self.bucket[user_id]["limit"] = 1
            self.bucket[user_id]["start_time"] = datetime.datetime.now()

            return True
        
        if user_req_limit >= self.request_limit:
            return False
        
        self.storage[user_id]["limit"] += 1
        return True

    def __call__(self, environ: Environ) -> Any:
        """
        Handles API access requests by invoking the `process_request_limit` method.

        Behavior:
        - Checks the `user_id` against the request limit.
        - If `process_request_limit` returns False, the user is throttled.
        - If True, access to the API is granted.
        """
        auth_token = Request(environ=environ).authorization
        
        # Fetch user_id from payload
        user_id = jwt.decode(auth_token, "signature", algorithms="HS256")
        
        if self.process_request_limit(user_id=user_id):
            return self.app(environ)

        resp = Response(
            response=str({
                "message": (
                    "Unfortunately, you've reached the maximum number of requests allowed at this time.",
                    + "Please try again after a few minutes."
                )
            }),
            mimetype="application/json",
            status=429
        )
        return resp(environ=environ)
