# Device-Code-Flow-Python
OAuth 2.0 device code flow, Python version - simplified


For more information on the flow - https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code

## Installing Requirements in local python

``` pip install -r requirements.txt ```

## Installing Requirements in an environment

Download the project and create python environment using below command

```python -m venv env```
<br/>
``` pip install -r requirements.txt ```

### Setup env

Open cmd in the current directory and enter the following:

``` .\env\Scripts\activate.bat ```

## Edit env.json file
```
{
    "client_id":"e>>>>>>>->>>>->>>>->>>>->>>>>>>>>>>>",
    "scope":"offline_access User.read mail.read"
}
```

## Run the flow using driver.py

```
> py driver.py

```
