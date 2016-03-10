# svnrankr
SVN user ranking by revision/commit interesting numbers (criterias: prime numbers, simetrical numbers, etc)

SVNRankr needs a valid SVN log export to work

Run the following code from the command line to obtain a full log export:

#!/bin/bash
svn log -q > svn.log

Use:
python svnrankr.py svn.log
