## Let's have deep dive into the Rate Limit.

## Description:
Rate limit is the restriction on the number of the total request hit by server perticular time frame.

In rate limit can be applied to requests based on various criteria, such as the user's IP Address, Authentication Credentials, etc ...

## Detailed Explaination:
For example, 
    we assume an API has rate limit of 1000 request per minutes. Now, user idetified by
    it's IP Address; suppose user hit 1000 request per minute still user continuesly hiting; after 1001th request user will not able to access the application and 
    application throttle polite response to user.

Now there are several ways to achive the requests,

    1. Token Bucket
    2. Leaky Bucket
    3. Fixed Window Counter
    4. Sliding Window Counter
    5. IP Throtting

Token Bucket:
As per the name, it's one bucket with multiple tokens. 
Imagine a bucket filled with tokens. Each token represents something you want to control, like data packets in a network or money in your pocket. So, let's say you've got this bucket and it can only hold a limited number of tokens, just like your pocket can only hold a limited amount of money. If you try to put more tokens in the bucket than it can hold, it's like trying to stuff too much money in your pocket – it just overflows and causes a mess!

Once the bucket is full, no new user will be able to access APIs.
Now, after the expiration time frame, the bucket is empty. As you're on a journey from one place to another, you use these tokens along the way, just like spending money as you travel. Ready to be refilled for your next adventure!

One advantage of the token bucket algorithm is for memory efficiency, as it requires a fixed number of tokens to be stored in memory. This can be important to implement a fixed number of tokens to be stored in memory.
