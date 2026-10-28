This is the repo for the 'orchestrator' workflow for the testing continuously assignment

The starter code just creates the .github/workflows directory
and includes a .yml file with the workflow_dispatch - this is the 'orchestrator'
and you will need to add your code to this workflow so that it checks out
each of your repos and runs the appropriate tests.

You will have to run this orchestrator manually.

Each of the repos will need their own workflow file that runs the tests for that repo 
whenever there is a push to that repo. You'll need to add these workflow files.


