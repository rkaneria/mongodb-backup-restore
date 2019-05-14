## OverView

This is simply python scripts to backup and restore mongodb with json config

## Usage

To backup database use following syntax 
> python mongodump.py

To restore a database from local backup folder
> python mongorestore.py

The config file has two parts as source and target. Source is for backup and Target is for restore.

If you have another config file, pass as an arguments as below -
 
- python mongodump.py -config configfile

## Config file

### Backup 

Take backup of all databases by keeping the database element empty in config file -

- "databases": []

Take backup of specific database by giving database names in config file - 

- "databases": [ "db1", "db2", "db3" ]

Take backup of specific collections of a database by using below syntax in config file -

- "databases": [ "db1.collection1.collection2", "db2.collection1", "db3" ]

### Restore

Mention database backup directory path of your local machine, to restore whole database from the same. 

Additionally you can provide database names in config file to restore only specific databases from backup directory. 

