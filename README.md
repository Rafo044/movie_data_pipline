


# Movie Database

This is a simple data pipeline.

![Data Pipeline](./image/pipeline.png)

# Requirements to run the project

You must get OMDB and TVDB API keys and put them in the places shown in the .env file.


# How to use

1.With this command you create a virtual environment and activate it:

```
make venv
```

2.To activate use the following commands:
```
make activate
```
3.Clone the repo:
```
https://github.com/Rafo044/movie_data_pipline.git
cd movie_data_pipline
```

4.Install the dependencies:
```
make install
```

6.Bring up the containers:
```
make up
```

If the containers are healthy continue
7.Create JetStream (By default the nats server does not enable it. In the compose file we enabled it with -js but the stream itself is not created)

```
make jetstream
```
8.Start the publishers
```
make omdb_publisher
```

```
make tvdb_publisher
```

9.Start the subscriber.
```
make subscriber
```


# About TVDB and OMDB databases

You can get API keys from these platforms and request movie information


# OMDb (Open Movie Database):


A database that provides movie and TV show information via an open API.

It allows you to get data in JSON format such as movie title, release year, director, actors, IMDb rating and poster.

Very useful for movie projects because it offers a free and RESTful API.
![Omdb](./image/omdb.png)


# TVDB (TheTVDB):

A database specialized for TV series and shows.

It provides episode, season, cast, poster and other metadata for each series.

Widely used for tracking series and integrating into applications via its API.
![Oomdb](./image/tvdb.png)


# Conf file

In the Conf folder, conf files are provided for Supervisor. Supervisor is a service like systemctl.
If you want, you can use this service to start Python files. If not, you can start them the traditional way (using make).

Supervisor service website:
https://supervisord.org/
