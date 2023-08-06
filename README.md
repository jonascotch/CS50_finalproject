# The Drugs Shortage Database
#### Video Demo:  <URL HERE>
#### Description:

### Background
#### Hospital Pharmacy and Drug Shortages
I've been working as a hospital pharmacist and there's always beeen a problem with drug shortages.  
But lately that problem has been growing as some drugs are not profitable to manufacture and yet there are no equivalent substitutes.  
These shortages have to be closely monitored, along with looking for alternative manufacturers and managing stocks to avoid interrupting treatments or running out of stock.  
The information on these shorteges is ussually kept in a Excel worksheet and is difficult to update and to extract meaningful data from.

### My solution
I've spotted an oportunity to put my newly acquired skills to help in this matter and to further make information available to others, namely doctors and nurses.  
So I created a web-based app that has a public page where the information about these shortages is displayed (estimated date to receive the drug, therapeutic alternatives).  
It also has an Admin profile that gives access to all the information and to its management (insert new info, update, and delete, if needed).

### Flask/Python
Firstly I created the "app.py" file to be the brain of the app.  

There are the different routes:  
```
@app.route('/')
```  
- Accessible to everyone, shows the information on the database that is classified as 'public'  


```
@app.route('/login')
```  
- Gives access to the app administrator. Checks for username and password against data in database.  

```
@app.route('/logout')
```  
- Logs the admin out, cleans the session info.  

```
@app.route('/newform')
```  
- Presents the form to insert new data and manages the submmission of this data, creating a new row in the database.  
The "try-excepts" were used to manage the checkboxes absence of value when not checked.  

```
@app.route('/list')
```  
- Shows a table with the info requested by the admin, according to several search parameters (public info, unsolved shortages or all info).  

```
@app.route('/details')
```  
- Shows all the data on a specific row, selected on the list view.  

```json
@app.route('/delete')
```  
- Deletes the selected info from the database, after several confirmations. 

This gave me the opportunity to work with SQLite3 on FLask without the CS50 library "training wheels".  
For it I needed the ``` sql_open(): ``` function, to easily access the database when needed.  

Also used hashlib instead of hash for password encryption.

## HTML
The bones of the front-end, located in the **templates** folder:
- ``` home.html ``` - the base of the html layout. Includes:
    - CSS stylesheets for Bootstrap, DataTables (including jQuery), Google Fonts files for tables font-family and my own ``` styles.css ``` file
    - Navbar
    - Jinja block for flash messages
    - Jinja blocks for other pages body and scripts
- ``` landing.html ``` - the front end for the public  
- ``` login.html ``` - login form
- ``` menu.html ``` - admin menu
- ``` newform.html ``` - form to insert new data, used bootstrap forms to shape it
- ``` editform.html ``` - twin form to newform but to edit data already in the database. Has a link to delete the data from database.
- ``` list.html ``` - table with data from the database, according to what admin selected in the menu pageband link to details
- ``` details.html ``` - table with all info from row selected in list. Has a link to edit the data.

## Some Javascript
Not a lot, just enough to make the pages a little more "reactive":  
- The menu page and the editform have some "pop-up" buttons
- The editform has a little script to fill the select option according to data from database. In this json.dumps methods was used to pass data to Javascript. And JSON.parse / tojson was used to retrieve it and use it in the script.


## DataTables

## Booststrap
