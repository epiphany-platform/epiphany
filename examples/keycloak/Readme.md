# KeyCloak examples readme

This directory contains example applications built on top of keycloak.

## Contents

- [Introduction](#introduction)
- [Security concerns](#security-concerns)
- [Prerequisites](#prerequisites)
- [Setup test instance of KeyCloak](#setup-test-instance-of-KeyCloak)
- [Implicit flow examples](#implicit-flow-examples)
  - [Implicit ReactJS SPA](#implicit-reactjs-spa)
  - [Implicit Python](#implicit-python)
  - [Implicit .NET Core](#implicit-.net-core)
  - [Implicit Java](#implicit-java)
- [Authorization flow examples](#authorization-flow-examples)
  - [Authorization ReactJS SPA](#authorization-reactjs-spa)
  - [Authorization Python](#authorization-python)
  - [Authorization .NET Core](#authorization-.net-core)
  - [Authorization Java](#authorization-java)  

## Introduction

This folder contains examples on how to implement authorization in [KeyCloak](https://www.keycloak.org/) using the OpenID standart in .NET core, python and Java (In progress). The examples cover the implicit and authorization flows and also show how to dail with role based access.

An easy overview of the flows can be found [here](https://medium.com/google-cloud/understanding-oauth2-and-building-a-basic-authorization-server-of-your-own-a-beginners-guide-cf7451a16f66).

## Security concerns

While the examples cover implicit flow it`s not recommanded for security concerns and should be avoided. You can read more [here](https://oauth.net/2/grant-types/implicit/).

## Prerequisites

- **Keycloak**
  - Docker
- **React**
  - nodejs => 10.13.0
  - yarn => 1.12.3
  - create-react-app => 2.1.1
- **Python**
  - python 2.7.15
  - pipenv
- **Dotnet**
  - .Net SDK 2.1.6
- **Java**
  - JDK => 1.8

## Setup test instance of KeyCloak

This part describes the steps to setup a local KeyCloak instance for running the demos:

1. Start the local KeyCLoak container with:

    ```bash
    docker run -p 8080:8080 -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin jboss/keycloak
    ```

    This will start a new container running on port 8080. It will have the user `admin` with password `admin`.

2. Import the pre-prepared realm into the local KeyCloack container:

    - Goto <http://localhost:8080> and login to the administration console with the `admin` account.
    - Goto `Import` and select the `realm-export.json`. Set `If a resource exists` to `Skip`.

The master realm now has 2 clients (`demo-app-authorization`,`demo-app-implicit`) which both contain 2 roles (`Administrator`,`User`) which are used in the examples.

Note: Users should be added manually and assigned one of the 2 (`Administrator`,`User`) client roles for testing.

## Implicit flow examples

### Implicit ReactJS SPA

The .NET core, python and Java examples all relly on the same ReactJS SPA. This first needs to be build and deployed before any of the examples can be started:

- Open a terminal here `examples/keycloak/implicit/react`
- Run the folling to provision the project:

    ```bash
    yarn install
    ```
- Run the folling to build the project and copy the artifacts to the .NET core, python and Java examples:

    ```bash
    yarn build
    ```

### Implicit Python

The Python example is based on a [flask](http://flask.pocoo.org/) and uses [JoseJWT](https://github.com/mpdavis/python-jose) for validation.

To run the example:

- Open a terminal here `examples/keycloak/implicit/python`
- Run the following to provision the project:

    ```bash
    pipenv install
    ```
- Run the following start the app server on <http://localhost:8090> where it can be opened:

    ```bash
    pipenv install run python
    ```

### Implicit .NET core

The .NET core example uses [IdentityServer4](http://docs.identityserver.io/en/latest/) todo the validation.

To run the example:

- Open a terminal here `examples/keycloak/implicit/dotnet/KeyCloak`
- Run the following to provision and build the project:

    ```bash
    dotnet build
    ```
- Run the following start the app server on <http://localhost:8090> where it can be opened:

    ```bash
    dotnet run
    ```

### Implicit Java

The Java example uses [Spring Boot](http://spring.io/projects/spring-boot) with [WebFlux](https://docs.spring.io/spring/docs/current/spring-framework-reference/web-reactive.html).

To run the example:

- Open a terminal here `examples/keycloak/implicit/java`
- Run the following to provision:

    ```bash
    mvnw install
    ```
- Run the following start the app server on <http://localhost:8090> where it can be opened:

    ```bash
    mvnw spring-boot:run
    ```

## Authorization flow examples

### Authorization ReactJS SPA

The .NET core, python and Java examples all relly on the same ReactJS SPA. This first needs to be build and deployed before any of the examples can be started:

- Open a terminal here `examples/keycloak/authorization/react`
- Run the folling to provision the project:

    ```bash
    yarn install
    ```
- Run the folling to build the project and copy the artifacts to the .NET core, python and Java examples:

    ```bash
    yarn build
    ```

### Authorization Python

The Python example is based on a [flask](http://flask.pocoo.org/) and uses [flas-oidc](https://flask-oidc.readthedocs.io/en/latest/) for validation.

To run the example:

- Open a terminal here `examples/keycloak/authorization/python`
- Run the following to provision the project:

    ```bash
    pipenv install
    ```
- Run the following start the app server on <http://localhost:8090> where it can be opened:

    ```bash
    pipenv install run python
    ```

It might be the case that after the import of the `realm-export.json` the secret clientkey of `demo-app-authorization` needs to be reset. This can be done here in the KeyCloak administrator console:

`Clients` > `demo-app-authorization` > `Credentials` > `Regenerate Secret`

The new secret then needs the be update here:

`examples/keycloak/authorization/python/appsettings.json`

At the entry `client_secret`.

### Authorization .NET core

The .NET core example uses [IdentityServer4](http://docs.identityserver.io/en/latest/) todo the validation.

To run the example:

- Open a terminal here `examples/keycloak/authorization/dotnet/KeyCloak`
- Run the following to provision and build the project:

    ```bash
    dotnet build
    ```
- Run the following start the app server on <http://localhost:8090> where it can be opened:

    ```bash
    dotnet run
    ```

 It might be the case that after the import of the `realm-export.json` the secret clientkey of `demo-app-authorization` needs to be reset. This can be done here in the KeyCloak administrator console:

`Clients` > `demo-app-authorization` > `Credentials` > `Regenerate Secret`

The new secret then needs the be update here:

`examples/keycloak/authorization/dotnet/KeyCloak/appsettings.json`

At the entry `Jwt:ClientSecret`.

### Authorization Java

The Java example uses [Spring Boot](http://spring.io/projects/spring-boot) with [WebFlux](https://docs.spring.io/spring/docs/current/spring-framework-reference/web-reactive.html).

To run the example:

- Open a terminal here `examples/keycloak/authorization/java`
- Run the following to provision:

    ```bash
    mvnw install
    ```
- Run the following start the app server on <http://localhost:8090> where it can be opened:

    ```bash
    mvnw spring-boot:run
    ```

 It might be the case that after the import of the `realm-export.json` the secret clientkey of `demo-app-authorization` needs to be reset. This can be done here in the KeyCloak administrator console:

`Clients` > `demo-app-authorization` > `Credentials` > `Regenerate Secret`

The new secret then needs the be update here:

`examples/keycloak/authorization/java/src/main/resources/application.properties`

At the entry `keycloak.credentials.secret`.