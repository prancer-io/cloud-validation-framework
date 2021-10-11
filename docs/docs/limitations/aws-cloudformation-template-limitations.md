# AWS Cloudformation Unsupported Scenarios

### We apply our compliance rules on your YAML and JSON templates to find security threats, but to do that we have to process the parameters, functions, and attributes of your template. we are able to process many things from it still there are some functions that we can't process because contains such a value that only can be available after a resource gets created. therefor we put those attributes as it is in the generated snapshot.
<br/>

#### Here is the [link](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/rules-section-structure.html) of AWS Cloudformation supported Functions<br/><br/>


**List of Unsupported Scenarios**
| Function Name | Note |
| ------------- | ---- |
Fn::EachMemberEquals|Some of the values only can be processed at the runtime
Fn::EachMemberIn|Some of the values only can be processed at the runtime
Fn::RefAll|For example, it returns all values of AWS::EC2::VPC::Id
Fn::ValueOf|Returns an attribute value or list of values for a specific parameter and attribute.
Fn::ValueOfAll|Returns an attribute value or list of values for a specific parameter and attribute.
Fn::Transform|specifies one or more macros that AWS CloudFormation uses to process your template
Fn::GetAtt|It returns the value of the attribute after the creation of the resource
Fn::GetAZs|The intrinsic function Fn::GetAZs returns an array that lists Availability Zones for a specified region
Fn::ImportValue|returns the value of an output exported by another stack
Fn::Contains| There are some scenarios in which some resources dependent on the output of the other resource

<br/>

**All Pseudo parameters reference**
- AWS::AccountId
- AWS::NotificationARNs
- AWS::NoValue
- AWS::Partition
- AWS::Region
- AWS::StackId
- AWS::StackName
- AWS::URLSuffix