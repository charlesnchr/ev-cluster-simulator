# data-research
A space for collaborative R&D

## Tooling.

To reduce bugs and improve the quality of our code we should utilize the following tools to make our lives easier; black, pylint, mypy.

```
pip install -r requirements-dev.txt
```

## Sharing data

Try:

```
dvc pull
```
### Adding data to dvc

Adding data for dvc should be as easy as 
```
dvc add <file_to_be_added>
```
You will then get some updated git files to add. See here: https://dvc.org/doc/start/data-management/data-versioning. 

High level:

* Your actual data is stored in a remote (currently for us google drive); that you dvc push, and dvc pull from. 
* What data to download is stored in *.dvc files that you commit along side with your code; and a commit against .gitignore.
* So when you check out somones git commit; you can dvc pull; and it will retrieve the data they had when they comitted it; these data files can change over time; and dvc tracks that for you.  

There is a vscode extension dvc, that can help with this tracking and uploading. 