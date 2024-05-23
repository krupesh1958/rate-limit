"""This module contains Rate Limit Algorithm.
If incase user want to hit API offten; user throttled.

```Token Bucket Algorithm:```
Every request used one token,
After token not present in bucket; user throttled.
Will fill token every x time frame.

For example;
    Bucket capacity = 60 (tokens)
    Refill Time Frame = 1 (Token/Seconds)
    Last Refill Time Frame

    5 Request comming withing just one seconds...
    Tokens = 55
    Last Time - Current Time = 1 seconds

    Add token;
    Tokens = 56

    Now, every user have only 56 tokens.
Note: Buckets are widespread among all users. There are no separate buckets for each user.
"""
import json
from datetime import datetime
from typing import Any

from werkzeug.wrappers import Response


# Typings
class Environ(object): ...


class TokenBucketRateLimit:

    def __init__(
        self,
        app,
        refill_token: int = 1,
        max_tokens: int = 60,
        refill_time: int = 5
    ) -> None:
        """
        Every request one token will be left from the bucket.
        """
        self.app = app
        self.bucket = 0
        self.refill_token = refill_token
        self.max_token = max_tokens
        self.last_refill_time = None
        self.refill_time = refill_time

    def process_request_limit(self) -> bool:
        """
        Remove token at each and every user's request,

        We will find difference between last refill token time and current time frame.
        Fill the token into the bucket as per the refill token. Incase bucket is full
        then we will skip and just remove current token and user's will be able to access.

        Usage:
        - Refill bucket as per the left the time frame.
        - Incase no any token found and there are time frame are left; user's not able to access.
        """
        # Incase, first request come.
        if not self.last_refill_time:
            self.last_refill_time = datetime.now()

        # Get elapsed
        elapsed = int((datetime.now() - self.last_refill_time).total_seconds())
        elapsed //= self.refill_time

        # Checking bucket is full or not.
        if self.bucket < self.max_token:
            self.bucket += elapsed
            if self.bucket >= self.max_token:
                self.bucket = self.max_token
            if elapsed:
                self.last_refill_time = datetime.now()

        # Now check the bucket is empty or not!
        if not self.bucket:
            return False
        self.bucket -= 1
        return True

    def __call__(self, environ: Environ, start_response) -> Any:
        """
        Handles API access requests by invoking the `process_request_limit` method.

        Behavior:
        - If `process_request_limit` returns False, the user is throttled.
        - If True, access to the API is granted.
        """
        # Check the rate limit is not exceed.
        if self.process_request_limit():
            return self.app(environ, start_response)

        # If the rate limit exceed will show static message,
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
