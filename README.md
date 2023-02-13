# Webscrapping using selenium with Multiprocessing
- Login into Tripadvisor website with multiple account asynchronously using multiple processing
- Search for the givven country name and select all destination 
- Comment on the most viwed question of destinaton forums.

### Clone project use follwing command
```
git clone https://github.com/ongraphpythondev/Tripadvisor.git
```
### Create virtual enviorment and activate it 
```
python -m venv venv
source venv/bin/activate
```
### Install the requirements file
```
pip install -r requirements.txt
```
### Make sure you have redis install on your machine
### Follow this link to install redis on your machine 
```
https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-22-04
```
### Provide the login credential inside account.csv file

### Change the OPENAI_API_KEY in .env file
```
OPENAI_API_KEY=<Enter Your API_KEY>
```

### run the script
```
python3 run.py
```

