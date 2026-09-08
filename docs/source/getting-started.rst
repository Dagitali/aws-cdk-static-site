Getting Started
===============

Requirements
------------

Use Python 3.13 or 3.14, AWS CDK v2, and an AWS account bootstrapped for CDK
deployments. A custom CloudFront domain also requires an ACM certificate in
``us-east-1``.

Install for Development
-----------------------

Clone the repository, then install the package and development dependencies:

.. code-block:: console

   $ python -m pip install -e '.[dev,docs]'

Build the Documentation
-----------------------

Build the local HTML site with warnings treated as errors:

.. code-block:: console

   $ make docs-strict

Open ``docs/build/html/index.html`` in a browser. Generated documentation is a
local build artifact and is not committed or published by this project.

Choose a Composition Pattern
----------------------------

Start with the :doc:`examples` page, choose the smallest pattern that meets
the site's requirements, and inspect the synthesized CloudFormation template
before deploying into a bootstrapped AWS account.
