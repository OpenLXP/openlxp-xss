
# OPENLXP-XSS

## Experience Schema Service


The Experience Schema Service maintains referential representations of domain entities, as well as transformational mappings that describe how to convert an entity from one particular schema representation to another.

This component responsible for managing pertinent object/record metadata schemas, and the mappings for transforming records from a source metadata schema to a target metadata schema. This component will also be used to store and link vocabularies from stored schema.


# Prerequisites
`Python >=3.7`  *Download and install Python from here [Python](https://www.python.org/downloads/).*

`Docker`  *Download and install Docker from here [Docker](https://www.docker.com/products/docker-desktop).*


# Environment Variables

### To run this project, you will need to add the following environment variables to your .env file

`DB_NAME` - MySql database name

`DB_USER` - MySql database user

`DB_PASSWORD` - MySql database password

`DB_ROOT_PASSWORD` - MySql database root password

`DB_HOST` - MySql database host

`DJANGO_SUPERUSER_USERNAME` - Django admin user name

`DJANGO_SUPERUSER_PASSWORD` - Django admin user password

`DJANGO_SUPERUSER_EMAIL` -Django admin user email

`AWS_ACCESS_KEY_ID` - AWS access keys

`AWS_SECRET_ACCESS_KEY` - AWS access password

`AWS_DEFAULT_REGION` - AWS region

`SECRET_KEY_VAL` -Django Secret key to put in Settings.py

`CERT_VOLUME` - Path for the where all the security certificates are stored

`LOG_PATH` - Log path were all the app logs will get stored


# Installation

1. Clone the Github repository:

   [GitHub-XSS](https://github.com/OpenLXP/openlxp-xss.git)

2. Open terminal at the root directory of the project.
    
    example: ~/PycharmProjects/openlxp-xss

3. Run command to install all the requirements from requirements.txt 
    
    docker-compose build.

4. Once the installation and build are done, run the below command to start the server.
    
    docker-compose up

5. Once the server is up, go to the admin page:
    
    http://localhost:8000/admin (replace localhost with server IP)


# Configuration

1. On the Admin page, log in with the admin credentials 


2. **Add Schema Ledger:** 
   
   *Registry for Maintaining and Managing Schemas*

   - `Schema Name` Schema file title
   - `Schema IRI` Schema files corresponding IRI
   - `Schema File` Upload the Schema file in the required format
   - `Status` Select if the Schema is Published or Retired
   - `Major version` Add the Major value of the schema version
   - `Minor Version` Add the Minor value of the schema version
   - `Patch Version` Add the Patch version number of the schema
   

3.  **Add Transformation Ledger:**
    
      *Registry for Maintaining and Managing the Mapping of Schemas*
      - `Source Schema` Select Schema file from drop-down
      - `Target Schema` Select Target Schema file from drop-down to be mapped to
      - `Schema Mapping File` Upload the Schema Mapping file to be referenced for mapping in the required format
      - `Status` Select if the Schema Mapping is Published or Retired
   
# API's 
 **XSS contains API endpoints which can be called from other components**
 
      http://localhost:8080/api/schemas/
    
*This API fetches the required schema from the repository using the Name and Version parameters*

      http://localhost:8080/api/mappings/
    
*This API fetches the required mapping schema from the repository using the Source Name, Source Version, Target Name and Target Version parameters*
   
# Update

To update an existing installation, pull the latest changes using git

Then restart the application using `docker-compose restart`

Occasionally some updates may require the application be rebuilt using `docker-compose up --build`, but this can also rebuild the database resulting in data loss

# Testing

To run the automated tests on the application run the command below

Test coverage information will be stored in an htmlcov directory

```bash
docker-compose --env-file .env run app sh -c "coverage run manage.py test && coverage html && flake8"
```

# Logs
Check the logs of application in the docker container.


# License

 This project uses the [MIT](http://www.apache.org/licenses/LICENSE-2.0) license.
  
