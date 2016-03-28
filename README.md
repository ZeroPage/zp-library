# requirements
* [python2 and pip](https://www.python.org/)
* [GAE SDK for Python](https://cloud.google.com/appengine/downloads)
* [Bower](http://bower.io/)

# Setup
1. Download and unarchive on the project root
1. Run ```pip install -t lib -r requirement.txt```
1. Run ```bower install```
1. Copy `app.yaml.template` to `app.yaml`.
1. Get Github Client Key from [here](https://github.com/settings/developers).
    * Homepage URL must be set correctly. If you're just testing on your local, use ```http://127.0.0.1:8080```.
    * 'Authorization callback URL' must be ```(host)/#!/auth/github```. Just like ```http://127.0.0.1:8080/#!/auth/github```
1. Set your application ID on [GAE](https://console.developer.google.com) and Github API keys from above step in ```app.yaml```
1. Run ```dev_appserver.py .```
1. Visit ```(host)/init``` on your browser and log in as Administrator.

# How to use on local
1. Run ```dev_appserver.py .``` on the project root.
1. Visit one of the URLs below on your browser:
    * ```http://127.0.0.1:8080```: Client
    * ```https://127.0.0.1/api/ui```: API Client.
    * ```https://127.0.0.1:8000```: Admin console

# How to deploy on GAE
1. Run ```appcfg.py update .``` on the project root.
1. Visit one of the URLs below on your browser:
    * ```http://(your-project-id).appspot.com```: Client
    * ```http://(your-project-id).appspot.com/api/ui```: API Client.
    * ```https://console.developer.google.com```: Admin console