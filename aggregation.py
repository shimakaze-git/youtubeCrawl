import sys
import boto3
import logging

from botocore.exceptions import ClientError

# S3リソースを作成します。これでS3サービスへのリクエストと応答が可能なります。
s3 = boto3.resource('s3')


def copy_object(
    src_bucket_name,
    src_object_name,
    dest_bucket_name,
    dest_object_name=None
):
    """Copy an Amazon S3 bucket object

    :param src_bucket_name: string
    :param src_object_name: string
    :param dest_bucket_name: string. Must already exist.
    :param dest_object_name: string. If dest bucket/object exists, it is
    overwritten. Default: src_object_name
    :return: True if object was copied, otherwise False
    """
    # Construct source bucket/object parameter
    copy_source = {'Bucket': src_bucket_name, 'Key': src_object_name}
    if dest_object_name is None:
        dest_object_name = src_object_name

    print(copy_source)
    print(dest_object_name)
    print(src_bucket_name)

    try:
        s3.meta.client.copy(copy_source, dest_bucket_name, dest_object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def ext_files_convert(ext_files):

    convert_file_name_list = []
    for f in ext_files:
        dir_name, filename = f.split('/')
        convert_file_name = dir_name + '_' + filename
        convert_file_name_list.append(convert_file_name)
    return convert_file_name_list


def aggregation_images(bucket_name, rate, out_dir):
    bucket = s3.Bucket(bucket_name)

    result = bucket.meta.client.list_objects(
        Bucket=bucket.name,
        Delimiter='/'
    )

    for obj in result.get('CommonPrefixes'):
        directory = obj.get('Prefix')
        files = bucket.meta.client.list_objects_v2(
            Bucket=bucket_name, Prefix=directory
        ).get('Contents')

        ext_files = [
            files[i].get('Key') for i in range(rate, len(files), rate)
        ]
        ext_files.append(files[len(files)-1].get('Key'))

        ext_files_list = ext_files_convert(ext_files)
        for ext_file, convert_ext_file in zip(ext_files, ext_files_list):

            # s3の別のディレクトリにコピー
            copy_object(
                bucket.name,
                ext_file,
                bucket.name,
                out_dir + '/' + convert_ext_file
            )

        print('---' * 20)


def main():
    if len(sys.argv) >= 4:
        bucket_name = sys.argv[1]
        rate = int(sys.argv[2])
        out_dir = sys.argv[3]

        aggregation_images(bucket_name, rate, out_dir)


if __name__ == "__main__":
    main()
