# gse
Go Somwhere Else (GSE) is a HTTP redirection management system

### Step 1  
Running the server:  
>```python gse.py```  

### Step 2  
Configuring Domains  
>Set your DNS to point to the IP of the GSE server.  If you wish to use port 80 you will have to either figure out a way for GSE to run on port 80 (to avoid OS-level port restrictions) or use a port translation mechanism of some sort.  

### Step 3  
Add Redirects  
>```./gse.sh DOMAIN /path http://domain.to/redirect/to```
