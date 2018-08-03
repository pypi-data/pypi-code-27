# ------------------------------------------------------------------------------
# Copyright IBM Corp. 2018
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------
#
#!/usr/bin/env python3
import argparse
from .cli_commands import flags

def main():
    parser = argparse.ArgumentParser(description='Convert CSV Objects to Parquet')

    parser.add_argument('-a', '--apikey', help='IBM Cloud API Key', required=True)
    parser.add_argument('-e', '--cos-endpoint', help='IBM COS Endpoint URL', required=True)
    parser.add_argument('-b', '--cos-bucket', help='IBM COS Bucket Name', required=True)
    parser.add_argument('-l', '--list-all', action="store_true", help='List All Objects in IBM COS Bucket')
    parser.add_argument('-c', '--csv', action="store_true", help='List All CSV Objects in IBM COS Bucket')
    parser.add_argument('-f', '--files', nargs="+", help='Convert Selected Objects in IBM COS Bucket - must use with -n')
    parser.add_argument('-n', '--names', nargs="+", help='Name(s) of the New Parquet Objects - must use with -f')

    args = parser.parse_args()

    flags(args)

if __name__ == "__main__":
    main()
