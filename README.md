# DRF Starter

**Django Rest Framework (DRF) starter project template.**

**NOTE**: Find the specific branch based on your required templates.

## Templates

### custon-user-phone-verify-knox-taggit-notifications
```bash
git clone -b templates/custon-user-phone-verify-knox-taggit-notifications git@github.com:belal-bh/DRF-starter.git
```

## Django Starter Steps to follow
-   Clone this repository (choose the right branch as your need)
-   Check `python runtime (Compatible Python version)` in `runtime.txt` file. Update `runtime.txt` if needed.
-   Create virtual environment `venv` according to `python runtime` defined in `runtime.txt` file.


    Using [Virtualenv](https://pypi.org/project/virtualenv/), run the following command in the root directoroy of this repository. It will create a virtual environment inside `venv` directory.
    ```
    virtualenv venv
    ```
    You have to activate virtualenv to work with this environment. To activate `venv` run the dollowing command:
    ```
    # for windows machine
    venv\Scripts\activate

    # for linux machine
    source venv/bin/activate
    ```
-   Install packages using `pip`.
    
    There are to requirements file named `main_requirements.txt` and `requirements.txt`. First one is only listed the main pacakages without it's `version` and `dependencies`. And second one was generated using `pip freeze > requirements.txt` command after intalling packages beginning of this project. It is recommended to use latest version of these packages and to do that `main_requirements.txt` can be installed.

    -   For the `latest versions` run the following command
        ```
        pip install -r main_requirements.txt
        ```
    -   **OR** For the `starter versions` run the following command
        ```
        pip install -r requirements.txt
        ```
-   Create `.env` file in the root directory of this repository and update  it's content according to your project. List of required environment variable list are given in the `.env.example` file. Follow the [python-decouple](https://pypi.org/project/python-decouple/) packeg's rules for more customisations.

-   RUN the the server after activating `venv`.
    ```
    python manage.py runserver
    ```
-   That's it in starter phage. Now it's your time to build something cool!

**Happy coding :)**


## Setup static directory and default files
To work properly **static directory** (i.e. `static_cdn`) need to add at the directory according to `settings.py`'s `STATIC_ROOT`, `MEDIA_ROOT` and `PROTECTED_ROOT` settings.
Sometimes it's need to add default file in a specific directory manually (Because it depends on the implementation in every django-app and file structure described in implementation).
Folder structure looks like:
```
static_cdn
├───media_root
│   └───accounts
│       └───user
│           └───image
└───static_root
```
Here `static_root` store all **static** files and `media_root` stores all **media** files.
Inside `media_root` folder, path pattern looks like:
```
media_root
└───<app_label>
    └───<model>
        └───<field_name>
```
In the previous case, `accounts` is `<app_label>`, `user` is `<model>` and `image` is `<field_name>` which was set at the model implementation time.
Inside the `<field_name>` directory more complicated file path could be set up. It's depend on implementation. There can have default file. In case of `user` model there has a default image inside the `image` directory named `default.png` which must be set to work the app properly.

Therefore, it is responsible to the developer to keep track on the implementation as well as static path.

### static_cdn
**NOTE:** An initial copy of the `static_cdn` can be found at [dev_extras/](./dev_extras/static_cdn/).

There can have file at the end of every directory.
Example: inside `image` directory there must have a `default.png` file.
```
static_cdn
├───media_root
│   ├───accounts
│   │   └───user
│   │       └───image
│   ├───products
│   │   ├───cuisine
│   │   │   └───image
│   │   └───product
│   │       └───image
│   └───vendors
│       └───store
│           └───logo
└───static_root
```
