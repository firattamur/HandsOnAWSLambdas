<h3 align="center">
7 Days Of AWS Lambdas
</h3>

<!-- badges -->
<p align="center">

<!-- language -->
<img src="https://img.shields.io/badge/-AWS-orange" alt="AWS">

<!-- inprogress or completed -->
<!-- <img src="https://img.shields.io/badge/-completed-green" alt="completed"> -->
	
<!-- inprogress or completed -->
<img src="https://img.shields.io/badge/-in%20progress-red" alt="in progress">
	
<!-- licence -->
<a href="https://github.com/ftamur/iOSPencilKitDrawApp/blob/main/LICENSE">
<img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="License: MIT">
</a>
	
<!-- week of year -->
<img src="https://img.shields.io/badge/week-29-green" alt="in progress">

</p>

<h4 align="center">
Learn fundamentals of AWS Lambdas and Practice with examples.
</h4>

<h3>
Notes:
</h3><hr>

```properties

# sls is shortening for serverless
# create a lambda project 
sls

# deploy lambda
# -v -> verbose prints events during deployment
sls deploy -v

# deploy only function instead of whole stack
sls deploy function -f hello

# invoke lambda by function name 'hello' 
# -l -> logs function call
sls invoke -f hello -l 

# remove lambda from aws
sls remove

```

<h3>
Goals:
</h3><hr>

- [X] Learn fundamentals of AWS Lambdas.
- [ ] Build a project contains AWS services S3, DynamoDB and Lambdas. 

<h3>
References:
</h3><hr>

1. [AWS Lambda and the Serverless Framework](https://www.udemy.com/course/aws-lambda-serverless/)
