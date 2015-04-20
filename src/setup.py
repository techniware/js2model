#!/usr/bin/env python
__author__ = 'kevin'

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

'''
js2Model.py Reference
=====================

Version 0.1 Beta DRAFT

Goal
----

Make it easy to use JSON data as native class models.

JSON is ubiquitous and convenient, but parsing JSON into generic data
structures like dictionaries and arrays precludes the use of many native
language features. The goal of js2Model.py is to generate model classes
and custom deserialization code from JSON schema definitions. Currently,
only Objective-C is supported, but the source is architected in to make
it easy to add new languages.

Installation
------------

To install js2Model:

1. Clone the repository
2. Install the python module

    ::

        $cd js2Model
        $python setup.py install

Running it
----------

    .. raw:: html

       <pre>
       js2model.py [-h] [-l LANG] [--prefix PREFIX] [--rootname ROOTNAME] [-p]
                          [-x] [-o OUTPUT] [--implements IMPLEMENTS] [--super SUPER]
                          [--import IMPORTFILES]
                          FILES [FILES ...]

       Generate native data models from JSON.

       positional arguments:
         FILES                 JSON files input for model generation

       optional arguments:
         -h, --help            show this help message and exit
         -l LANG, --lang LANG  language (default: objc)
         --prefix PREFIX       prefix for class names (default: TR)
         --rootname ROOTNAME   Class name for root schema object (default: fileName)
         -p, --primitives      Use primitive types in favor of object wrappers
         -x, --noadditional    Do not include additionalProperties in models
         -o OUTPUT, --output OUTPUT
                               Target directory of output files
         --implements IMPLEMENTS
                               Comma separated list of interface(s)|protocol(s)
                               supported by the generated classes
         --super SUPER         Comma separated list of super classes. Generated
                               classes inherit these
         --import IMPORTFILES  Comma separated list of files to @import
       </pre>

A simple sample
---------------

Given the JSON schema definition:

.. code:: json

        {
           "$schema": "http://json-schema.org/draft-04/schema#",
           "title": "address",
           "type": "object",
           "properties": {
              "street": { "type": "string" },
              "city": { "type": "string" },
              "county": { "type": "string" },
              "state": { "type": "string" },
              "zip": { "type": "string" }
           }
        }

js2Model will generate the class source files:

**address.h**

.. code:: objc

        @interface Address : NSObject <JSONModelSerialize>

        @property(strong, nonatomic) NSString * county;
        @property(strong, nonatomic) NSString * city;
        @property(strong, nonatomic) NSString * state;
        @property(strong, nonatomic) NSString * street;
        @property(strong, nonatomic) NSString * zip;

        @end

**address.m**

.. code:: objc

        @implementation Address{
            NSMutableDictionary *_additionalProperties;
        }

        - (instancetype)init
        {
            self = [super init];
            if (self) {
            // custom intialization code
                     _additionalProperties = [NSMutableDictionary new];
            }
            return self;
        }


        - (instancetype) initWithJSONData:(NSData *)data
                        error:(NSError* __autoreleasing *)error {
            self = [self init];
            if (self) {
                     [TRJSONModelLoader load:self withJSONData:data error:error];
            }
            return self;
        }

        //
        // Code removed for clarity
        //

        @end

To deserialize JSON data into an instance of Address:

.. code:: objc

           NSError *error;

           NSData *jsonData = [self getSomeJSONFromSomewhere];

           Address *address = [Address alloc] initWithJSONData:data error:&error];

           if( !error ) {
                 NSLog(@"Street = %@", address.street);
           }
'''

setup(
    name='js2model',
    version='0.2.dev6',
    packages=find_packages(),
    package_data={'tr.jsonschema': [
        'templates.objc/*.mako',
        'templates.objc/dependencies/*.h',
        'templates.objc/dependencies/*.c',
        'templates.objc/dependencies/*.m',
        'templates.objc/static/*.*',
        'templates.cpp/*.mako',
        'templates.cpp/dependencies/*.h',
        'templates.cpp/rapidjson/*.h',
        'templates.cpp/rapidjson/error/*.h',
        'templates.cpp/rapidjson/internal/*.h',
        'templates.cpp/rapidjson/msinttypes/*.h',
        'templates.cpp/static/*.*',
    ]},
    include_package_data=True,
    scripts=['js2model.py', 'js2model', 'ez_setup.py'],
    keywords=['Requires: Mako, jsonpointer, jsonref, jsonschema',
              'json',
              'schema',
              'jsonschema',
              'json-schema',
              'json schema',
              'json object',
              'generate',
              'generator',
              'builder',
              'draft 4',
    ],
    license='BSD',
    author='Kevin Zimmerman',
    author_email="%s.%s@%s.%s"%('kevin', 'zimmerman', 'thomsonreuters', 'com'), # half hearted attempt to avoid spam
    description='A fine attempt to auto-generate source models + deserialization code from JSON schema definitions.',
    long_description=__doc__,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'mako>=1.0.1',
        'jsonpointer>=1.4',
        'jsonref>=0.1',
        'jsonschema>=2.4',
    ],
    dependency_links = [
        'https://pypi.python.org/simple'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
],
)
