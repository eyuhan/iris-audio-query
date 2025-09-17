# iris-audio-query

## Description

A web application which allows users to upload audio as a knowledge base and query with text.

## Architecture

The uploaded audio files are stored in IRIS as persistent objects, 
and are also embedded using TwelveLabs API then stored as vectors.
To perform a query, the query text is first embedded using TwelveLabs API, 
then a vector search is performed to find the most relevant audio embeddings, 
then the corresponding audio files are retrieved, 
and finally the query text is answered with the audio files as context using OpenAI API.

The upload and query operations are built as Business Operations using the IRIS Native Python SDK. 
The FastAPI backend provides a REST API for external applications to interact with this system, 
while the React frontend provides a UI to interact with the backend.

## Required Installations and Setup

- **Python 3.8+** - For embedded language development and backend application
- **Node.js & npm** - For frontend application development
- **Docker** - For containerization and running the IRIS database

### TwelveLabs API

The (unpaid) TwelveLabs API is used for generating embeddings for uploaded audio files and query text.

To get your TwelveLabs API key:

1. Go to https://playground.twelvelabs.io and create an account (or log in).
2. Once logged in, navigate to the `API Keys` section under `Settings`.
3. Click `Create API Keys` to create a new key, and copy the generated key.

### OpenAI API

The (paid) OpenAI API is used for answering queries using audio files as context.

**Note**: Any API supported by BAML can be used in place of OpenAI. 
Check the [BAML docs](https://docs.boundaryml.com/ref/baml/client-llm#fields) for the list of supported APIs. 

To get your OpenAI API key:

1. Go to https://platform.openai.com and create an account (or log in).
2. Once logged in, go to the [Billling page](https://platform.openai.com/settings/organization/billing/overview) and add payment details.
3. Next, go to the [API Keys page](https://platform.openai.com/api-keys).
3. Click `Create new secret key` to create a new key, and copy the generated key.

## Installation

1. Clone the repository
    ```bash
   git clone
    cd iris-audio-query
    ```
2. Create a virtual environment
    ```bash
   python3 -m venv .venv
    source .venv/bin/activate
   ```
3. Install the requirements
    ```bash
   pip install -r requirements.txt
   npm --prefix community/ui/ install
   ```
4. Configure environmental variables
   1. Copy the template in `.env.example` as `.env`.
   2. Configure the environmental variables as appropriate.
5. Run the docker-compose file
    ```bash
   docker-compose up
   ```
6. Import the Audio class in IRIS 
   1. Access the IRIS Management Portal by going to `http://localhost:53795/csp/sys/UtilHome.csp`
   2. Sign in using username `superuser` and password `SYS`, or otherwise as specified in `.env`.
   3. Navigate to `System Explorer` > `Classes`.
   4. Select the `IRISAPP` namespace, or otherwise as specified in `.env`.
   5. Click `Import` and specify that the import file resides on `My Local Machine`, and choose the file `community/iris/IrisAudioQuery.Audio.cls`.
   6. Click `Next` then `Import` to import the `Audio` class.
7. Start the FastAPI backend.
   ```bash
   docker exec -it iris-audio-query-iris-1 bash
   ```
   Then from within the container,
    ```bash
   python3 community/main.py 
   ```
8. Start the React frontend.
    ```bash
   npm --prefix community/ui/ run dev
   ```
9. Access the application at `http://localhost:5173`.

## Project Structure

```
community/
├── app/                   # FastAPI backend application
├── baml_client/           # Generated BAML client code
├── baml_src/              # BAML configuration files
├── interop/               # IRIS interoperability components
├── iris/                  # IRIS class definitions
├── models/                # Data models and schemas
├── twelvelabs_client/     # TwelveLabs API client
├── ui/                    # React frontend application
├── main.py                # FastAPI application entry point
└── settings.py            # IRIS interoperability entry point
```
