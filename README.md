Test the run time characteristics of your Docker containers.

# Install

```sh
pip install git+https://github.com/patricknevindwyer/docker-unit.git
```

# Test Description

`docker-unit` tests are described via Yaml, similar to how `docker-compose`
files are described. The `docker-unit` file determines which Docker
 image to test, and how to generate information from that image.
 
The basic structure of a test file is:

```yaml
version: "1.0"
image: "patricknevindwyer/pinned-apache:latest"
tests: []
```

This file selects an image for testing, but doesn't describe any
tests. Suppose for our first test we want to make sure that our
container is running as the *root* user:

```yaml
version: "1.0"
image: "patricknevindwyer/pinned-apache:latest"
tests:
  - name: "Running as root"
    run: "whoami"
    use: "lines"
    check:
      - entry: any
        contains: root
```

We've defined the image to test, as well as a single test. After
running the `whoami` command inside our container, we split the
result into lines, and then check that any of the lines contains
the term _root_. we can run the test with:

```sh
> ./docker-unit examples/root_test.yaml 
Version (1.0)
  = Using image (patricknevindwyer/pinned-apache:latest)
  + 1 tests defined
  @ [Running as root] == Pass
     - Contains root ... Pass
```

We described one test, and it passed.

Every `docker-unit` test follows a similar format; specify a command
to run in the container, define how to parse the output of the 
command, and then assess the parsed output. 

There are two fundamental types of parsers in `docker-unit`: the _line_
oriented parsers, and the _key/value_ parsers. The various parsers
that fit into these broad categories are described later.

# Key/Value Tests

Key value tests compare the an entry in the parsed output of a command run in a
container with a user defined value. Expanding on the test above
trying to assure that we run as _root_ in our container, we could add
a test that checks the path of the users home directory:

```yaml
version: "1.0"
image: "patricknevindwyer/pinned-apache:latest"
tests:
  - name: "Running as root"
    run: "whoami"
    use: "lines"
    check:
      - entry: any
        contains: root
  - name: "Environment check"
    run: "env"
    use: ["env"]
    check:
      - key: "HOME"
        equals: "/root"
```

Running this test generates:

```sh
./docker-unit examples/root_test.yaml 
Version (1.0)
  = Using image (patricknevindwyer/pinned-apache:latest)
  + 2 tests defined
  @ [Running as root] == Pass
     - Contains root ... Pass
  @ [Environment check] == Pass
     - HOME ... Pass
```

We added a _key/value_ test, and it passed! All key/value tests include
 the _key_ definition (our key in the test above was *HOME*).

As well as defining which key in our parsed output we want to check,
we need to determine how we want to match the value that key maps to.

Currently there are two ways to describe a match with a _key_: _equals_,
 and _contains_. An _equals_ test does an exact string comparison between the
 test value and the value extracted from the container. The _contains_ test
 does a substring test. An example to illustrate the difference:
 
 ```yaml
 version: "1.0"
image: "patricknevindwyer/pinned-apache:latest"
tests:
  - name: "Environment check"
    run: "env"
    use: ["env"]
    check:
      - key: "HOME"
        equals: "/root"
      - key: "PATH"
        contains: "/usr/local/bin"
 ```
 
 After running the `env` command on the container we use two tests, and
 _equals_ exact comparison to check the home directory, and a _contains_
 comparison to make sure that _/usr/local/bin_ is in the *PATH*.
 
# List Tests

 * any
 * all
 
 Include an example of checking the Apachectl output using both KV and LINES
 checks (check a module and check the fork mode)

# Extractors

 * kv
 * env
 * lines