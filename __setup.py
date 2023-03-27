import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='py_console',  # should match the package folder
    packages=['py_console'],  # should match the package folder
    version='0.1.4',  # important for updates
    license='MIT',  # should match your chosen license
    description='Colorfull JavaScript-like console logging',
    long_description=long_description,  # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Mike Huls',
    author_email='mikehuls42@gmail.com',
    url='https://github.com/mike-huls/py-console',
    project_urls={  # Optional
        "Bug Tracker": "https://github.com/mike-huls/py-console/issues"
    },
    install_requires=['colorama'],  # list all packages that your package uses
    keywords=["pypi", "console", "log", "color", "print", "debug", "warn", "info", "error"],  # descriptive meta-data
    classifiers=[  # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],

    download_url="https://github.com/mike-huls/py-console/archive/refs/tags/0.1.4.tar.gz",
)