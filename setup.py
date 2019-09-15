# Copyright (C) 2019 Jonathan T. Moore
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

def read(filename):
    with open(filename) as f:
        return f.read()

setup(
    name = 'ddbhcache',
    version = read('VERSION'),
    description = 'use DynamoDB as a heuristic cache for another API',
    long_description = read('README.md'),
    long_description_content_type="text/markdown",
    author = 'Jon Moore',
    url = 'https://github.com/jonm/dynamodb-heuristic-cache',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'boto3~=1.9',
        'python-dateutil~=2.8'
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    keywords="aws DynamoDB heuristic cache",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: System"
    ]
)
