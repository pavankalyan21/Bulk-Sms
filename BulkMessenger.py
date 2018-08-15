import warnings
import requests
import contextlib

#Handling SSL Certification.
try:
    from functools import partialmethod
except ImportError:
    from functools import partial

    class partialmethod(partial):
        def __get__(self, instance, owner):
            if instance is None:
                return self

            return partial(self.func, instance, *(self.args or ()), **(self.keywords or {}))

@contextlib.contextmanager
def no_ssl_verification():
    old_request = requests.Session.request
    requests.Session.request = partialmethod(old_request, verify=False)

    warnings.filterwarnings('ignore', 'Unverified HTTPS request')
    yield
    warnings.resetwarnings()

    requests.Session.request = old_request


#sends msg to the given number by using given apikey.
def send_msg(apikey,msg,number):
    with no_ssl_verification():
        url = "https://www.fast2sms.com/dev/bulk"
        payload = "sender_id=FSTSMS&message={0}&language=english&route=p&numbers={1}&flash=1".format(msg,number)
        headers = {
            'authorization':apikey,
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        return response.text


#Generates api_keys from a list of given api keys one by one.
def gen_api_key_from_list(api_keys):
    i=0
    length=len(api_keys)
    if length>0:
        while(True):
            if i<len(api_keys):
                yield api_keys[i]
                i+=1
            else:
                i=0
    else:
        return "NO API WITH FREE MSGS"


"""
This is the actual logic.
1.Gets generator object for the api_keys from the gen_api_key_from_list() function.
2.It will send msg to each number given to the function.
3.If api_key has no free msgs then it will it will remove from the api_keys list and again it will get the generator object of 
  updated api_keys list.
4.If all api_keys have no free msgs then it will print the remaning numbers and exists from the program.
5.If msg is sent to all numbers then it will print  "Successfull.....!!!!" 
"""
def send_msgs(api_keys,numbers,msg):
    api_gen=gen_api_key_from_list(api_keys)
    while len(numbers)>0:
        try:
            api_key=next(api_gen)
            result=send_msg(api_key,msg,numbers[-1])
            if "You does not have sufficient amount in your wallet." in result:
                print("NO free msgs available in this api: ",api_key)
                api_keys.remove(api_key)
                api_gen=gen_api_key_from_list(api_keys)
            else:
                numbers.pop()
        except StopIteration:
            print("We can't send msgs to these numbers:",*numbers,"\n Because there are no free msgs available avaiable")
            break
    else:
        if len(numbers)==0:
            print("Successfull.....!!!!")
    pass


if __name__=='__main__':
    #Valid api's should be used. It will dont generate any errors if Invalid api is used.
    #These are not the actual api_keys. I replaced them.
    api_keys = [
        "BUGeZEAd8s6jYtTixa4qOCyHVNXb05vJWoI9r1pFSkQKhd9iZycCtlWhOn4UjaFVruQ7D2Iz0fY",
        "Mm6aJVjWQdkTLKIP9xRnptcslhOFyi8HvUubS42NwCYqzodRGHZciwmOy8pCLbDzuI6FnVvJNMA",
        "fAmHCOlYGPhFoWZXaxNV6US3brdDB9ys04j7JtnquwvicqhkcKNljYoFAmPweSb4JD9tgyCnV3M",
        "h2usSE5QnvtkYL8piXTVr1ajoqR4FfyAN6U9BMZPbl7D0ZewPmNCvVlUi20KEkOH9gADX8uyMsx",
        "SL9BVoYvCJOmelspHk62xfwXPu43za7bjdgyWntAGEZUKzS2VbjxqKTnH57ecawA3LfrWFEvJkm"
    ]

    numbers=["8179305701","9999999999","9889998899","9988998899","9090909090","9898989898","9944332211",
             "9999999999", "9889998899", "9988998899", "9090909090", "9898989898", "9944332211",
             "9999999999", "9889998899", "9988998899", "9090909090", "9898989898", "9944332211",
             "9999999999", "9889998899", "9988998899", "9090909090", "9898989898", "9944332211",
             "9999999999", "9889998899", "9988998899", "9090909090", "9898989898", "9944332211",
             "9999999999", "9889998899", "9988998899", "9090909090", "9898989898", "9944332211",
             "9999999999", "9889998899", "9988998899", "9090909090", "9898989898", "9944332211",
             ]

    msg="Hi! this msg is sent from a program.  --msvsr"

    send_msgs(api_keys,numbers,msg)