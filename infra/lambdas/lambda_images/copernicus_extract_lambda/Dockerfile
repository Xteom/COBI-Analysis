FROM public.ecr.aws/lambda/python:3.8 AS ECR

# Copy function code into var/task directory
# Optimal Attempt
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

RUN python3.8 -m pip install -r requirements.txt --target ${LAMBDA_TASK_ROOT}

COPY ./ ${LAMBDA_TASK_ROOT}/

RUN yum clean all & rm -rf /var/cache/yum
