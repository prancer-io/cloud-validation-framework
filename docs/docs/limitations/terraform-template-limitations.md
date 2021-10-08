# Terraform Template Unsupported Scenarios

The `prancer-basic` supports the processing of terraform templates and generates the snapshot with processed values. Terraform provides some [`Built-In`](https://www.terraform.io/docs/configuration/functions.html) functions to define the attribute value dynamically. Out of these functions, `prancer-basic` does not supports the processing of following `Built-In` functions.

**Numeric Functions**

| Function Name | Reference Link: |
|---------------|---------------|
| parseint | [https://www.terraform.io/docs/language/functions/parseint.html](https://www.terraform.io/docs/language/functions/parseint.html)|


**String Functions**

| Function Name | Reference Link |
|---------------|---------------|
| chomp | [https://www.terraform.io/docs/language/functions/chomp.html](https://www.terraform.io/docs/language/functions/chomp.html) |
| format | [https://www.terraform.io/docs/language/functions/format.html](https://www.terraform.io/docs/language/functions/format.html) |
| formatlist | [https://www.terraform.io/docs/language/functions/formatlist.html](https://www.terraform.io/docs/language/functions/formatlist.html) |
| indent | [https://www.terraform.io/docs/language/functions/indent.html](https://www.terraform.io/docs/language/functions/indent.html) |
| regex | [https://www.terraform.io/docs/language/functions/regex.html](https://www.terraform.io/docs/language/functions/regex.html) |
| regexall | [https://www.terraform.io/docs/language/functions/regexall.html](https://www.terraform.io/docs/language/functions/regexall.html) |



**Collection Functions**

| Function Name | Reference Link |
|---------------|---------------|
| flatten | [https://www.terraform.io/docs/language/functions/flatten.html](https://www.terraform.io/docs/language/functions/flatten.html) |
| matchkeys | [https://www.terraform.io/docs/language/functions/matchkeys.html](https://www.terraform.io/docs/language/functions/matchkeys.html) |
| setsubtract | [https://www.terraform.io/docs/language/functions/setsubtract.html](https://www.terraform.io/docs/language/functions/setsubtract.html) |
| setunion | [https://www.terraform.io/docs/language/functions/setunion.html](https://www.terraform.io/docs/language/functions/setunion.html) |
| slice | [https://www.terraform.io/docs/language/functions/slice.html](https://www.terraform.io/docs/language/functions/slice.html) |
| sort | [https://www.terraform.io/docs/language/functions/sort.html](https://www.terraform.io/docs/language/functions/sort.html) |
| sum | [https://www.terraform.io/docs/language/functions/sum.html](https://www.terraform.io/docs/language/functions/sum.html) |
| transpose | [https://www.terraform.io/docs/language/functions/transpose.html](https://www.terraform.io/docs/language/functions/transpose.html) |
| values | [https://www.terraform.io/docs/language/functions/values.html](https://www.terraform.io/docs/language/functions/values.html) |
| zipmap | [https://www.terraform.io/docs/language/functions/zipmap.html](https://www.terraform.io/docs/language/functions/zipmap.html) |


**Encoding Functions**

| Function Name | Reference Link |
|---------------|---------------|
| base64decode | [https://www.terraform.io/docs/language/functions/base64decode.html](https://www.terraform.io/docs/language/functions/base64decode.html) |
| base64encode | [https://www.terraform.io/docs/language/functions/base64encode.html](https://www.terraform.io/docs/language/functions/base64encode.html) |
| base64gzip | [https://www.terraform.io/docs/language/functions/base64gzip.html](https://www.terraform.io/docs/language/functions/base64gzip.html) |
| csvdecode | [https://www.terraform.io/docs/language/functions/csvdecode.html](https://www.terraform.io/docs/language/functions/csvdecode.html) |
| jsondecode | [https://www.terraform.io/docs/language/functions/jsondecode.html](https://www.terraform.io/docs/language/functions/jsondecode.html) |
| jsonencode | [https://www.terraform.io/docs/language/functions/jsonencode.html](https://www.terraform.io/docs/language/functions/jsonencode.html) |
| urlencode | [https://www.terraform.io/docs/language/functions/urlencode.html](https://www.terraform.io/docs/language/functions/urlencode.html) |
| yamldecode | [https://www.terraform.io/docs/language/functions/yamldecode.html](https://www.terraform.io/docs/language/functions/yamldecode.html) |
| yamlencode | [https://www.terraform.io/docs/language/functions/yamlencode.html](https://www.terraform.io/docs/language/functions/yamlencode.html) |


**Filesystem Functions**

| Function Name | Reference Link |
|---------------|---------------|
| abspath | [https://www.terraform.io/docs/language/functions/abspath.html](https://www.terraform.io/docs/language/functions/abspath.html) |
| dirname | [https://www.terraform.io/docs/language/functions/dirname.html](https://www.terraform.io/docs/language/functions/dirname.html) |
| pathexpand | [https://www.terraform.io/docs/language/functions/pathexpand.html](https://www.terraform.io/docs/language/functions/pathexpand.html) |
| basename | [https://www.terraform.io/docs/language/functions/basename.html](https://www.terraform.io/docs/language/functions/basename.html) |
| file | [https://www.terraform.io/docs/language/functions/file.html](https://www.terraform.io/docs/language/functions/file.html) |
| fileexists | [https://www.terraform.io/docs/language/functions/fileexists.html](https://www.terraform.io/docs/language/functions/fileexists.html) |
| fileset | [https://www.terraform.io/docs/language/functions/fileset.html](https://www.terraform.io/docs/language/functions/fileset.html) |
| filebase64 | [https://www.terraform.io/docs/language/functions/filebase64.html](https://www.terraform.io/docs/language/functions/filebase64.html) |
| templatefile | [https://www.terraform.io/docs/language/functions/templatefile.html](https://www.terraform.io/docs/language/functions/templatefile.html) |


**Date and Time Functions**

| Function Name | Reference Link |
|---------------|---------------|
| formatdate | [https://www.terraform.io/docs/language/functions/formatdate.html](https://www.terraform.io/docs/language/functions/formatdate.html) |
| timeadd | [https://www.terraform.io/docs/language/functions/timeadd.html](https://www.terraform.io/docs/language/functions/timeadd.html) |
| timestamp | [https://www.terraform.io/docs/language/functions/timestamp.html](https://www.terraform.io/docs/language/functions/timestamp.html) |


**Hash and Crypto Functions**

| Function Name | Reference Link |
|---------------|---------------|
| base64sha256 | [https://www.terraform.io/docs/language/functions/chomp.html](https://www.terraform.io/docs/language/functions/base64sha256.html) |
| base64sha512 | [https://www.terraform.io/docs/language/functions/chomp.html](https://www.terraform.io/docs/language/functions/base64sha512.html) |
| bcrypt | [https://www.terraform.io/docs/language/functions/chomp.html](https://www.terraform.io/docs/language/functions/bcrypt.html) |
| filebase64sha256 | [https://www.terraform.io/docs/language/functions/chomp.html](https://www.terraform.io/docs/language/functions/filebase64sha256.html) |
| filebase64sha512 | [https://www.terraform.io/docs/language/functions/chomp.html](https://www.terraform.io/docs/language/functions/filebase64sha512.html) |
| filemd5 | [https://www.terraform.io/docs/language/functions/chomp.html](https://www.terraform.io/docs/language/functions/filemd5.html) |
| filesha1 | [https://www.terraform.io/docs/language/functions/chomp.html](https://www.terraform.io/docs/language/functions/filesha1.html) |
| filesha256 | [https://www.terraform.io/docs/language/functions/chomp.html](https://www.terraform.io/docs/language/functions/filesha256.html) |
| filesha512 | [https://www.terraform.io/docs/language/functions/chomp.html](https://www.terraform.io/docs/language/functions/filesha512.html) |
| md5 | [https://www.terraform.io/docs/language/functions/chomp.html](https://www.terraform.io/docs/language/functions/md5.html) |
| rsadecrypt | [https://www.terraform.io/docs/language/functions/chomp.html](https://www.terraform.io/docs/language/functions/rsadecrypt.html) |
| sha1 | [https://www.terraform.io/docs/language/functions/chomp.html](https://www.terraform.io/docs/language/functions/sha1.html) |
| sha256 | [https://www.terraform.io/docs/language/functions/chomp.html](https://www.terraform.io/docs/language/functions/sha256.html) |
| sha512 | [https://www.terraform.io/docs/language/functions/chomp.html](https://www.terraform.io/docs/language/functions/sha512.html) |
| uuid | [https://www.terraform.io/docs/language/functions/chomp.html](https://www.terraform.io/docs/language/functions/uuid.html) |
| uuidv5 | [https://www.terraform.io/docs/language/functions/chomp.html](https://www.terraform.io/docs/language/functions/uuidv5.html) |

| Function Name | Reference Link |
|---------------|---------------|
| formatdate | [https://www.terraform.io/docs/language/functions/formatdate.html](https://www.terraform.io/docs/language/functions/formatdate.html) |
| timeadd | [https://www.terraform.io/docs/language/functions/timeadd.html](https://www.terraform.io/docs/language/functions/timeadd.html) |
| timestamp | [https://www.terraform.io/docs/language/functions/timestamp.html](https://www.terraform.io/docs/language/functions/timestamp.html) |

**IP Network Functions**

| Function Name | Reference Link |
|---------------|---------------|
| cidrhost | [https://www.terraform.io/docs/language/functions/cidrhost.html](https://www.terraform.io/docs/language/functions/cidrhost.html) |
| cidrnetmask | [https://www.terraform.io/docs/language/functions/cidrnetmask.html](https://www.terraform.io/docs/language/functions/cidrnetmask.html) |
| cidrsubnet | [https://www.terraform.io/docs/language/functions/cidrsubnet.html](https://www.terraform.io/docs/language/functions/cidrsubnet.html) |
| cidrsubnets | [https://www.terraform.io/docs/language/functions/cidrsubnets.html](https://www.terraform.io/docs/language/functions/cidrsubnets.html) |


**Type Conversion Functions**

| Function Name | Reference Link |
|---------------|---------------|
| can | [https://www.terraform.io/docs/language/functions/can.html](https://www.terraform.io/docs/language/functions/can.html) |
| tobool | [https://www.terraform.io/docs/language/functions/tobool.html](https://www.terraform.io/docs/language/functions/tobool.html) |
| tolist | [https://www.terraform.io/docs/language/functions/tolist.html](https://www.terraform.io/docs/language/functions/tolist.html) |
| tomap | [https://www.terraform.io/docs/language/functions/tomap.html](https://www.terraform.io/docs/language/functions/tomap.html) |
| tonumber | [https://www.terraform.io/docs/language/functions/tonumber.html](https://www.terraform.io/docs/language/functions/tonumber.html) |
| toset | [https://www.terraform.io/docs/language/functions/toset.html](https://www.terraform.io/docs/language/functions/toset.html) |
| tostring | [https://www.terraform.io/docs/language/functions/tostring.html](https://www.terraform.io/docs/language/functions/tostring.html) |
| try | [https://www.terraform.io/docs/language/functions/try.html](https://www.terraform.io/docs/language/functions/try.html) |
