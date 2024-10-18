# AWS SOC 2 Compliance Settings

## Overview

This repository contains AWS CDK code in Python to help set up and maintain various AWS controls required for SOC 2 compliance. The project aims to automate the creation and management of AWS resources that support SOC 2 trust service criteria: Security, Availability, Processing Integrity, Confidentiality, and Privacy.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Project Structure](#project-structure)
4. [Usage](#usage)
5. [Implemented Controls](#implemented-controls)
6. [Customization](#customization)
7. [Clean Up](#clean-up)
8. [Contributing](#contributing)
9. [License](#license)
10. [Disclaimer](#disclaimer)

## Prerequisites

- Python 3.12 or higher
- AWS CLI configured with appropriate credentials
- AWS CDK CLI installed (v2.x)
- An AWS account with necessary permissions to create and manage resources

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/aws-soc2-settings.git
   cd aws-soc2-settings
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Bootstrap your AWS environment (if not already done):
   ```
   cdk bootstrap
   ```

## Project Structure

The project is organized into several stacks, each responsible for a specific aspect of SOC 2 compliance:

- `MainStack`: Orchestrates the creation of other stacks
- `NetworkStack`: Sets up VPC and subnet configurations
- `NetworkSecurityStack`: Configures AWS Network Firewall
- `VulnerabilityAssetStack`: Sets up AWS Inspector for vulnerability assessments
- `LoggingStack`: Configures CloudTrail and CloudWatch Logs
- `IdentityAccessStack`: Manages IAM policies and roles
- `EncryptionStack`: Implements KMS for data encryption

## Usage

1. Review and customize the stack configurations in each file under the `aws_soc2_settings/` directory.

2. Synthesize the CloudFormation template:
   ```
   cdk synth
   ```

3. Deploy the stack:
   ```
   cdk deploy --all
   ```

4. To deploy a specific stack:
   ```
   cdk deploy StackName
   ```

## Implemented Controls

This project implements the following SOC 2 related controls:

1. Network Security:
   - VPC with public and private subnets
   - AWS Network Firewall for traffic filtering
   - Security Groups and Network ACLs

2. Vulnerability Management:
   - AWS Inspector for automated vulnerability assessments
   - Amazon GuardDuty for threat detection

3. Identity and Access Management:
   - IAM policies and roles with least privilege principle
   - Multi-factor authentication (MFA) enforcement

4. Encryption and Data Protection:
   - AWS Key Management Service (KMS) for encryption key management
   - S3 bucket encryption
   - EBS volume encryption

5. Logging and Monitoring:
   - AWS CloudTrail for API activity logging
   - Amazon CloudWatch Logs for centralized logging
   - CloudWatch Alarms for monitoring critical metrics

6. Compliance and Auditing:
   - AWS Config for resource inventory and compliance rules
   - AWS Security Hub for security posture management

## Customization

To customize the infrastructure according to your specific SOC 2 requirements:

1. Modify the stack files in the `aws_soc2_settings` directory.
2. Adjust parameters such as VPC CIDR ranges, subnet configurations, or firewall rules in the respective stack files.
3. Add or remove resources as needed to meet your specific compliance requirements.
4. Update the `cdk.json` file to include any new context parameters or configuration options.

## Clean Up

To avoid incurring unnecessary costs, destroy the stacks when they're no longer needed:

```
cdk destroy --all
```

## Contributing

Contributions to improve the project are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is intended to assist with SOC 2 compliance but does not guarantee full compliance. Always consult with a certified auditor or compliance expert to ensure your AWS environment fully meets SOC 2 requirements. The authors and contributors of this project are not responsible for any compliance failures or security breaches that may occur in your AWS environment.
