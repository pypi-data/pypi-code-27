from .convert_module import convert_objects

def commands(args):
    """
    Starts the program to convert CSV objects to Parquet.
    
    Required flags:
    -a or --apikey      -   IBM Cloud API Key
    -e or --endpoint    -   URI endpoint of the COS bucket being used
    -b or --bucket      -   COS bucket that will be used to check for objects, convert then, and place them back into the bucket

    Future TODO: Users can select a different output bucket as long as they are have the same COS endpoint
    """

    converter = convert_objects(args.apikey, args.cos_endpoint, args.cos_bucket)

    if args.list_all:
        """ 
        -l - Lists all the files in a COS bucket
        """
        print(converter.list_bucket_objects())
        return

    if args.csv:
        """ 
        -c - Lists only CSV files in a COS bucket
        """
        print(converter.list_csv_objects())
        return

    if args.files:
        """ 
        Flags -f and -n must be used together and the number of CSV objects names must match the new Parquet object names.

        -f - Names CSV objects to convert. Since objects are placed in a Python set, if you attempt to name the same object twice,
            it will only accept the name once.
        -n - New names of converted objects to Parquet. Names can include prefixes like `my/new/object.parquet`. 
            Do not put the `.parquet` file name after the new name. It's already added for you. The number of new names must
            equal the number of object names you want converted or it will not convert the objects.
        """

        objs_to_convert = set(args.files)
        csv_objs_in_bucket = set(converter.list_csv_objects_names())
        objs_new_names = args.names

        if len(objs_to_convert) != len(objs_new_names):
            print("The number of objects to convert doesn't equal the new names you provided.")
            return

        if not objs_new_names:
            print("You need to provide new name(s) for the objects you want to convert.")
            return

        non_convertable_objects = objs_to_convert - csv_objs_in_bucket
        convertable_objects = objs_to_convert & csv_objs_in_bucket

        if not convertable_objects:
            print("Convertable objects found in bucket: None")
            return
        else:
            print("Convertable objects found in bucket: {}".format(', '.join(list(convertable_objects))))

        if not non_convertable_objects:
            print("Non-Convertable objects found in bucket: None")
        else:
            print("Objects not found in bucket: {}".format(', '.join(list(non_convertable_objects))))
        
        for converted_obj, name in zip(convertable_objects, objs_new_names):
            print("Now Converting: {} --> {}.parquet".format(converted_obj, name))
        
        converter.convert_selected_objects(convertable_objects, objs_new_names)
    
    elif not args.files:
        print("You need to provide the names of objects you want to convert.")
