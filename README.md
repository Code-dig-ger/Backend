# CodeDigger Backend

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Apache License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Contributor Covenant][code-of-conduct-shield]][code-of-conduct-url]

## Features

#### Setting Environment First Time
Below commands will setup the environment for the first time.

#### Windows
```
py -m pip install --user virtualenv
py -m venv env
```
#### Linux
```
python3 -m pip install --user virtualenv
python3 -m venv env
```

### This project uses MySQL database , first you have to setup MySQL database. 
```
Download XAMPP from [here](https://www.apachefriends.org/download.html)
Start MySQL server.
```

#### Starting Virtual Env. and Setting up the Project
Below are the commands for project Initialization into your local computer
#### For Windows
```
. env/Scripts/activate -- If using gitbash
. env\Scripts\activate -- If using Windows Powershell
pip install -r requirements.txt
cd codedigger
py manage.py migrate
py manage.py runserver
```
- This would start the development server

#### For Linux
```
source env/bin/activate
pip3 install -r requirements.txt
cd codedigger
python3 manage.py migrate
python3 manage.py runserver
```
- This would start the development server 

### Leaving the virtual environment
```
deactivate
```

### To update requirements file 
```
pip freeze > requirements.txt
```


<!-- LICENSE -->
## License

Copyright 2021 Codedigger

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


<!-- CONTACT -->
## Contact

Codediger - contact.codedigger@gmail.com

Project Link: [https://github.com/Code-dig-ger/Backend](https://github.com/Code-dig-ger/Backend)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Code-dig-ger/Backend.svg?style=for-the-badge
[contributors-url]: https://github.com/Code-dig-ger/Backend/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Code-dig-ger/Backend.svg?style=for-the-badge
[forks-url]: https://github.com/Code-dig-ger/Backend/network/members
[stars-shield]: https://img.shields.io/github/stars/Code-dig-ger/Backend.svg?style=for-the-badge
[stars-url]: https://github.com/Code-dig-ger/Backend/stargazers
[issues-shield]: https://img.shields.io/github/issues/Code-dig-ger/Backend.svg?style=for-the-badge
[issues-url]: https://github.com/Code-dig-ger/Backend/issues
[license-shield]: https://img.shields.io/github/license/Code-dig-ger/Backend.svg?style=for-the-badge
[license-url]: https://github.com/Code-dig-ger/Backend/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/
[code-of-conduct-shield]: https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg
[code-of-conduct-url]: CODE_OF_CONDUCT.md
