# svnrankr
SVN user ranking by revision/commit interesting numbers

"Interesting" numbers criteria

* Prime numbers
* Stair numbers (1234, 2345, 3456, etc)
* Symmetrical numbers (1221, 1111, 34344343)
* Multiples of 100 (100, 900, 1000, 5000, etc)
* Mirror numbers (1414, 123123, etc)

Feel free to fork and add other interesting criterias!

#Log
SVNRankr needs a valid SVN log export to work
Run the following code from the command line to obtain a full log export:
svn log -q > svn.log

#Use
python svnrankr.py svn.log
