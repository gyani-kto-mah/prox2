# (no name decided yet) but codenamed as "prox2"

(will add description and everything else later.)

## Contributing

How to help?

```sh
$ git clone <repo_url>
$ cd <repo>
$ virtualenv .venv  # Make sure you use python3
$ source .venv/bin/activate
$ pip install -r requirements.txt  # Install all dependencies within venv.
$ ./run.sh  # This just does stuff up for you.
$ echo "Wait for  while (dependig upon your PC's capacity.)"
$ echo ""
$ echo "Head over http://127.0.0.1:8000/ using the web browser you use."
$ echo ""
$ curl -x http://127.0.0.1:8080/ http://httpbin.org/anything  # You are now basically proxying the conn. Also, make sure you use `HTTP` and `not httpS` for testing. I'll make it useable later.
$ echo ""
$ echo "Now, again check your browser."
```

The above command-line instructions will help you get the idea, regarding what's going on.

Now, all I want to do is there should be an editable Raw HTTP Request somehow matching Repeater's UI of Burp Suite. But it is supposed to be used within phone, so make sure it's Responsive UI.

And, web is simply choosen to make sure it's cross platform (front-end) and even if the backend is run in VPS, it should also work within an iOS(client). I'll PWA it after it's done.

But, in most of the used case; It will be used with `termux` and `python` so, not using frameworks; since there is already load of `mitmproxy` and `FastAPI` I don't wanna use up `Vue` again (phone padhkela lmao)