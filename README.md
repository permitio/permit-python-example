



# Permit Python With FastAPI Example


The app demonstrate a design collaboration app
for users to share designs(like figma) and comment on them. the app policy will be enforce by permit. there are 3 types of users.
viewer, editor, and admin.

- **Viewer** can only view design and comments on design, he can delete and edit his own comments.
- **Creator** can create and edit,delete his own designs ,but not others users, he can comment on his design. and other design but can only delete his own comments.
- **Admin** allow to create, edit, delete designs and comments of other users.

The app enable to signup a user, and expose route to sync user to permit system to 
set his authority 


## Machine Prerequisities
- python^3.10 [python install](https://www.python.org/downloads/)
- pip (or any package installer you prefer) [pip install](https://pip.pypa.io/en/stable/cli/pip_install/)
- terraform cli [terraform install](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
- docker [docker install](https://docs.docker.com/engine/install/)
- docker-compose [docker-compose install](https://docs.docker.com/compose/install/)

## Permit Prerequisities
- Signup to permit.io create your first project and grab your **api key** 
    <video width="320" height="240" controls>
  <source src="upload after commit .webm" type="video/webm">
  Your browser does not support the video tag.
</video>

### Ok, lets start with the fun 🐶

## Set App Permit Policy Using permit-terraform-provider

- Paste the api key to the .env file 
```
PERMIT_API_KEY=<API_KEY_HERE>
TF_VAR_permit_api_key=<API_KEY_HERE>
```
- Load the variables into your shell
```
source .env
```
- Applying terraform plan
```
cd terraform && terraform init && terraform plan && terraform apply
```
- write yes in the command line and press enter

go to your project dashboard you should see your policies resources and roles 


## Launch FastAPI App
 - Deploy to your docker enviorment db(postgres)and the pdp
 - Create the schema for your app via alembic
 - Create venv enviorment and activate it
 - Run the web server with the command ``` uvicorn app.main:app --reload ```

 ## Use The App
 Now it all setup to use our design app!

 - Signup  new user
 - Signin (get fake jwt for the demonstration)
 - use the set_role route and add add to the user a creator role.
 - use the create_design route and pass the user details
 - use the create_comment route and create comment on that    design
 - Signup  new user
 - Signin (get fake jwt for the demonstration)
 - use the set_role route and add to the user a viewer role.
 - try to delete the design of user CreatorUser with the email of ViewerUser - it should be rejected.




## The App Stack
    - Web Server 
 Web Server
    permit
    fastapi
    sqlalchemy
    uvicorn
    pydantic
    alemcib

    Database

    postgresql
    pdp

    terraform

    
## Init
    install venv 
    

