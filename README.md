<h1 align="center"> Slang Bot </h1> <br>
<p align="center">
  <a href="https://gitpoint.co/">
    <img alt="GitPoint" title="GitPoint" src="https://www.joeyoungblood.com/wp-content/uploads/2018/05/reddit-logo-alienhead.png" width="450">
  </a>
</p>

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Usage](#usage)
- [Feedback](#feedback)
- [Build Process](#build-process)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Introduction

Slang Bot is a Reddit bot that will define slang terms using Urban Dictionary. The bot also has a frontend to view all the requests that have been made.

## Usage

Bot requests can be on Reddit using the command `!slangbot <term>`. The bot will take approximately 1 minute to respond with the slang definition for your term. Currently the bot is only active and live on https://reddit.com/r/testingground4bots

An overview of the requests that have been made can be viewed at: https://slang-bot.herokuapp.com/#/

## Features

* Python Flask
* Vue.js
* Axios
* PSQL

## Feedback

Please feel free to send feedback by creating [an issue](https://github.com/gitpoint/git-point/issues/new). Feature requests are always welcome.

## Build Process

##### Before you start

Before getting started, you should have the following installed and running:

- [X] Yarn - [instructions](https://yarnpkg.com/en/docs/install#mac-stable)
- [X] Vue Cli 3 - [instructions](https://cli.vuejs.org/guide/installation.html)
- [X] Python 3
- [X] Pipenv (optional)
- [X] Heroku Cli (if deploying to Heroku)

**Development Keys**: To run the project locally, you will need a couple keys for development. For using the database, `DATABASE_URL` must be defined. For PRAW (Reddit API) to work properly, it needs `reddit_client_id`, `reddit_secret`, `reddit_user_agent`, `reddit_username`, and `reddit_password` which can be taken from https://www.reddit.com/prefs/apps. Put all the PRAW keys in a file named api_secrets.py in the project's base directory.

##### Database Setup

`python3 manage.py db init`
`python3 manage.py db migrate`
`python3 manage.py db upgrade`

##### Template and Dependencies

* Clone this repository:

	```
	$ git clone https://github.com/cbaron3/reddit-bot.git
	```

* Setup virtual environment, install dependencies, and activate it:

	```
	$ pipenv install --dev
	$ pipenv shell
	```

* Install JS dependencies

	```
	$ yarn install
	```


## Development Server

Run Flask Api development server:

```
$ python run.py
$ rq worker reddit-tasks
```

From another tab in the same directory, start the webpack dev server:

```
$ yarn serve
```

The Vuejs application will be served from `localhost:8080` and the Flask Api
and static files will be served from `localhost:5000`.

The dual dev-server setup allows you to take advantage of
webpack's development server with hot module replacement.

Proxy config in `vue.config.js` is used to route the requests
back to Flask's Api on port 5000.

If you would rather run a single dev server, you can run Flask's
development server only on `:5000`, but you have to build build the Vue app first
and the page will not reload on changes.

```
$ yarn build
$ python run.py
```

## Production Server

This template is configured to work with Heroku + Gunicorn and it's pre-configured
to have Heroku build the application before releasing it.

#### JS Build Process

Heroku's nodejs buidlpack will handle install for all the dependencies from the `packages.json` file.
It will then trigger the `postinstall` command which calls `yarn build`.
This will create the bundled `dist` folder which will be served by whitenoise.

#### Python Build Process

The python buildpack will detect the `Pipfile` and install all the python dependencies.

#### Production Sever Setup

Here are the commands we need to run to get things setup on the Heroku side:

	```
	$ heroku apps:create flask-vuejs-template-demo
	$ heroku git:remote --app flask-vuejs-template-demo
	$ heroku buildpacks:add --index 1 heroku/nodejs
	$ heroku buildpacks:add --index 2 heroku/python
	$ heroku config:set FLASK_ENV=production
	$ heroku config:set FLASK_SECRET=SuperSecretKey
	$ heroku addons:create redistogo

	$ git push heroku master
	$ heroku scale worker=1
	```
	
