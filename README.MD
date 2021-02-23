## FastApi JWT Authentication

This is meant to visualise a sample jwt-authentication app with <a href="https://fastapi.tiangolo.com">***FastApi***</a>

```
pip install -r requirements.txt
```

Generate your secret key with openssl

```
openssl rand -hex 32
```

Then export it to your environment in terminal as so:

```
export SECRET_KEY=ca05b35bd405406b575941d6a43e4ab2b21b969b540c914fb5cc1b7429095ea0
```

NOTE: The above secret key is just a sample. Do not use it in production.

Now you can run your app 

```
python main.py
```
Go to the documentation at <a href="http://127.0.0.1:8000/docs">***http://127.0.0.1:8000/docs***</a> and test it out.

I have used normal lists for models in this example so as to leave room for any ORM integration.