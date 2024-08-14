



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

 - run ``` docker-compose up -d ``` (deploy the pdp, the db ,and the app)

 ## Use The App
 Now it all setup to use our design app!

 open [swagger](http://127.0.0.1:8000/docs)

 - Signup a new user with the email **viewer@gmail.com** using the [sign up request](http://127.0.0.1:8000/docs#/auth/create_user_route_auth_signup__post)

 - Assign **viewer** role to the user using [assigned role request](http://127.0.0.1:8000/docs#/auth/assigned_role_to_user_auth_assign_role_post)
    
- paste it to the request body 
   ```
  {   
    "user":"user|viewer@gmail.com",
    "role": "viewer"
  }
    ```
 ### Lets try to create new design when we signed as viewer 
 - Signin (In the swagger page press on the authorized button and paste the user email)
 - Try to create design using the [create design request](http://127.0.0.1:8000/docs#/design/create_design_design_post)
 #### We get an 403 status with the message Not authorized 🔒

 ### Now Lets create new user but now with **creator** permissions

  - Signup a new user with the email **creator@gmail.com** using the [sign up request](http://127.0.0.1:8000/docs#/auth/create_user_route_auth_signup__post)

 - Assign **creator** role to the user using [assigned role request](http://127.0.0.1:8000/docs#/auth/assigned_role_to_user_auth_assign_role_post)
    
- paste it to the request body 
   ```
  {   
    "user":"user|creator@gmail.com",
    "role": "creator"
  }
    ```
 ### Lets try to create new design when we signed as viewer 
 - Signin (In the swagger page press on the authorized button and paste the user email)
 - Try to create design using the [create design request](http://127.0.0.1:8000/docs#/design/create_design_design_post)
 - The design should be created
 - Lets comment on the design with creator user

 ## Abac case 
 - Now we are going to delete the comment the creator just write  
 
 ## Rebac case 
 - Now lets create new user with permissions of admin 
 - Lets try to delete the design we created before using the creator user
 

    

