# Introduction
This is a simple tool to manage a database containing information on various condominiums, most notably their city, department code, zip code and annual condominium fees. 
To run this tool with a fresh Python install, you need to install two packages, Django and requests. You can run the following commands : 
```
$ python -m pip install Django
$ python -m pip install requests
```

# Setup
The database is already filled with the provided data for the test, but if you want to try and import it yourself, or reset it after you've added multiple addresses, you will need to fill the `IMPORT_PATH` environment variable in the technical_test/bienici/settings.py file. 
Else, you're ready to go! Simply run the following command when in the right folder :
`python manage.py runserver`
Once the server is running, you will be able to visit the various URLs to try and run the code.

## Import data
If you want to try and reimport data, if you have filled the environment variable, you can simply visit http://127.0.0.1:8000/bienici_api/import, and the data will be cleaned and reimported.

## Check overall stats
To check quantiles and average on the provided document, you can visit http://127.0.0.1:8000/bienici_api/overall_stats, and it will display the 10% and 90% quantiles, as well as the average of all condominium fees.

## Check specific stats
In case you want to limit the scope of your stats, you can check http://127.0.0.1:8000/bienici_api/query_stats. Fill the data that interests you, click submit, and the result will appear.

## Add a condominium to the database with a link
To add a new condominium on the Bien ici site, go to http://127.0.0.1:8000/bienici_api/add_url, and enter the url of your choice. If the url is valid, and condominium fees are available on the offer, the entry will be added to the database.

# Known shortcomings
Condominiums are named Locations in the code, the name is bad, but there were a lot of names I had to change and didn't do it in the end.
You cannot refresh forms pages once they have been submitted and have to go back on your browser or type the url again to access the form once more, you cannot refresh. I deemed it acceptable for a sort of proof of concept, but a good solution would need to be found on production code.
The project was generated with the Django tutorial, starting here : https://docs.djangoproject.com/en/5.2/intro/tutorial01/, and therefore there are files of which I don't know the use in the folder, such as admin.py and tests.py, but did not delete in case they were important.
On http://127.0.0.1:8000/bienici_api/add_url, I did not manage to display a proper error message when the url has a bad format, even though it is checked in the code, so the page just refreshes when it happens.
