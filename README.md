[![Build Status](https://travis-ci.org/smomni/ignore-file.svg?branch=master)](https://travis-ci.org/smomni/ignore-file)

# ignore-file

Ignore glob-style patterns similar to .gitignore and .dockerignore.

## Usage

```python
from ignore import iterdir
from pathlib import Path

dir_path = Path('dir')
for path in iterdir(dir_path, ignore_file='.myignore'):
    print(path)
```

Pattern examples:

* `dir/*`: All files in directory `dir/` and its subdirectories
* `*.ext`: All files with extension `.ext`

## Installing

The source code is currently hosted on [GitHub](https://github.com/smomni/ignore-files).

You can use git clone and pip to install from sources:

```bash
git clone https://github.com/smomni/ignore-files
cd ignore-files
pip install .[test]
```

## Running the tests

The tests can be run using pytest as the test runner:

```bash
pytest
```


## Workflow

* File issues for features. They can be small or big, as long as they are solvable. You should be able to tell when something is done from reading the issue. Too open ended and it cannot be closed.

* Develop created issues

* Commits should touch one thing, preferably, with a label that matches the code. For example, a change that reads "reformat foo" shouldn't add new features, etc.

* Open a pull request (PR) for review from the branch to master

* Try to keep the commits on a PR branch below a dozen

* Keep the PR open for 24 hours to give people the chance to comment and look at it

* Review the changes

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/smomni/ignore-files/tags). 

## Authors

* **Simo Tumelius** - *Initial work* - [smomni](https://github.com/smomni)

See also the list of [contributors](https://github.com/smomni/ignore-files/contributors) who participated in this project.

## License

This project is licensed under the MIT license - see the [LICENSE.md](LICENSE.md) file for details.