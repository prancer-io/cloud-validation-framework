""" Tests for ARN Parser"""
from processor.connector import arn_parser

def test_arnparse():
    arn_str = "arn:aws:s3:us-west-1::"
    arn_object = arn_parser.arnparse(arn_str)
    assert isinstance(arn_object, arn_parser.Arn)

    arn_str = "arn:aws:ec2:us-west-1::uniqueid"
    arn_object = arn_parser.arnparse(arn_str)
    assert isinstance(arn_object, arn_parser.Arn)

    arn_str = "arn:partition:service:region:account-id:resource-type/resource-id"
    arn_object = arn_parser.arnparse(arn_str)
    assert isinstance(arn_object, arn_parser.Arn)



def test_exception_arnparser():
    arn_str = "aws:s3:us-west-1::"
    try:
        arn_object = arn_parser.arnparse(arn_str)
    except Exception as e:
        arn_object = str(e)
    assert type(arn_object) is str

