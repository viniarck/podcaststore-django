from setuptools import setup

desc = "Podcaststore API"

setup(
    name="podcaststore_site",
    version="1.0",
    description=desc,
    author="Vinicius Arcanjo",
    author_email="viniarck@gmail.com",
    packages=["podcaststore_api"],
    install_requires=[
        "django==2.2.13",
        "djangorestframework==3.9.2",
        "psycopg2-binary==2.8.1",
        "gunicorn==19.9.0",
        "djangorestframework-simplejwt==4.3.0",
        "python-rapidjson==0.7.1",
        "django-extensions==2.1.7",
        "django-redis==4.10.0",
        "django-model-utils==3.2.0",
        "ipython==7.5.0",
        "django-rest-swagger==2.2.0",
        "packaging==19.0",
        "drf-yasg==1.16.1",
        "django-cors-headers==3.0.2",
    ],
    extras_require={
        "dev": [
            "pytest==4.5.0",
            "pytest-django==3.4.8",
            "pytest-cov==2.7.1",
            "flake8==3.7.7",
            "mypy==0.701",
            "black==19.3b0",
            "requests==2.22.0",
        ]
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    zip_safe=False,
)
