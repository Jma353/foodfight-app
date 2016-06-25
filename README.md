# Push for Food Backend 

Backend system supporting collaborative restaurant recommendation app

Made as part of AT&T June 2016 Hackathon (NYC)

**Base URL:** `foodfight-app.herokuapp.com/`


## Virtual Environment Setup
Run the following arguments to setup the virtual environment necessary to maintain packages 

```bash 
[sudo] pip install https://github.com/pypa/virtualenv/tarball/develop # to update virtualenv
virtualenv venv # to create virtualenv 
```

Once the `venv` is created, you can activate it by running the following: 

```bash 
source venv/bin/activate 
```

Once you have activated `venv`, run the following to install all package requirements

```bash 
pip install -r requirements.txt
```

At this point, if you run `pip freeze`, **only** packages in `requirements.txt` should be shown 


## Autoenv 
For environment variable loading, we run `autoenv` 

To set this up, run the following: 

```bash 
deactivate # if you're running your venv
pip install autoenv # to install if you haven't already installed it 
touch .env 
```

The `.env` file is where you can declare environment variables specific to this app.  These variables are loaded on `cd`-ing into the directory with the `.env` file.  Your `.env` file should look like this.  

```python
export APP_SETTINGS="sample_settings_string"
export DATABASE_URL="postgresql://localhost/sample_db"
... 
```

## DB Setup 
Run the following: 

```bash
mkdir -p data/db # to setup document directory for MongoDB 
mongod --dbpath data/db 
```





