"""This module contains rate limitation of the all APIs.
If incase user want to hit API offten; user throttled.

This module contains `Sliding Window` rate limit. Which is effient
as per the `Fix Window`.

Description:
This algorithm uses a queue to keep track of the timestamps of the requests 
processed in a sliding time window. If the difference between the current time 
and the earliest request in the queue is greater than the time window, 
that request is popped from the queue. If the length of the queue is less 
than the limit, the current request is allowed and its timestamp is appended 
to the queue. If the length of the queue is equal to or greater than the limit, 
the request is denied.

For example,
    Queue Limit: 10
    Time Window: 60 seconds
    Earliy TimeStamp - Current TimeStamp: 45seconds (If queue is not full append
    new request, else throttled user.)
    Earliy TimeStamp - Current TimeStamp: 80seconds (Just remove first user and
    allow to access the queue.)
"""
import json
import datetime
from typing import Any
from queue import Queue

from werkzeug.wrappers import Response


class Environ(object): ...


class SlidingWindowRateLimit:

    def __init__(
        self,
        app,
        request_limit: int = 50,
        expiration: int = 60
    ) -> None:
        """
        Will store TimeStamp into the Queue.
        NOTE: In this window we are not create seprate Queue for every users.
        For every users have Common Queue to store first request time stamp.
        """
        self.app = app
        self.expiration = expiration
        self.queue = Queue(maxsize=request_limit)

    def process_request_limit(self) -> bool:
        """
        Checks if a user can access the API within the current rate limits.

        Usage:
        - If queue is not full just append new time stamp.
        - If queue is full and earlier time stamp is greter just remove they all
        timestamps.
        - If queue is full and earlier time stamp is not greter just throttle user.
        """
        ctime = datetime.datetime.now()

        # If Queue is full and earlier time stamp is greater remove they all timestamps from Queue.
        while (
            self.queue.full()
            and (ctime - self.queue.queue[0]).seconds > self.expiration
        ):
            self.queue.get()

        if self.queue.full():
            return False
        self.queue.put(ctime)
        return True

    def __call__(self, environ: Environ, start_response) -> Any:
        """
        Handles API access requests by invoking the `process_request_limit` method.

        Behavior:
        - Checks the `user_id` against the request limit.
        - If `process_request_limit` returns False, the user is throttled.
        - If True, access to the API is granted.
        """
        if self.process_request_limit():
            return self.app(environ=environ, start_response=start_response)

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
