### contester [![Build Status](https://travis-ci.org/radiasoft/contester.svg?branch=master)](https://travis-ci.org/radiasoft/contester)

Automates configuration and execution of tests within docker containers

### Requirements

*contester* requires *Git* and *docker* to be installed and available through 
the `PATH` enviroment variable.

#### Installation

```sh
pip install git+https://github.com/radiasoft/contester.git
```

#### Configuration

*contester* uses a YAML file to describe the steps necessary to setup the
environment and execute the test. Place a file named `.contester.yml` in 
the root of your Git repository.

Example:

```yaml
container: radiasoft/python2:latest
packages:
  - docker-io
files:
  - requirements.txt
  - requirements-test.txt
prepare_script:
  - pip install -r requirements.txt
  - pip install -r requirements-test.txt
test: PYTHONPATH=$(pwd) py.test
```

#### Execute

Run `contester run [/Path/to/Git/Repo]`. The path is optional; if missing *contester* will assume the `CWD` is the Git repository being tested.

#### Execution Lifecycle

Using the `.contester.yml` scripts, *conster* will execute several steps in the order as follows:

##### Fetch base docker container

The `container` field defines the name of a docker container that will serve as the basis to build the test enviroment.
 
##### Install packages

The `packages` field defines a list of packages to install in the container. Currently it only supports `yum.

##### Copy files for Image preparation

The `files` field specifies a list of files from the repo to be used within the setup of the test container. The files are copied to a specific work directory within the repo.

##### Command execution for Image preparation

The `prepare_script` field specified a list of bash commands to be executed remotely. These commands are executed as user with `UID` 1000. These commands are executed inside a `bash` interpreter.

##### Image tagging

If all the previous steps are successful, a new docker container will be commited locally with the following names:

- `contester/<repo_name>_<repo_branch>:<git_commit>`
- `contester/<repo_name>_<repo_branch>:latest`

##### Test execution 

The `test` field defines a single `bash` command to execute on the previously commited container.

#### License

License: http://www.apache.org/licenses/LICENSE-2.0.html

Copyright (c) 2016 RadiaSoft LLC.  All Rights Reserved.
