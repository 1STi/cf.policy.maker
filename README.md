# Read Cloudformation File and create Policy
This little component read a cloudformation or serverless.yml file and create a policy documento to AWS IAM.

## Requirements
In this first version, the cloudformation or serverless file need to stay in same location to this program

## Executing
```console
(venv) python main.py
```

After run, one file named "policy.json" will be created and need to be imported to AWS.


## TODO

- Implement CI
    - Point to origin file
    - Accept serverless or cloudformation like a option
- Implement upload to AWS option