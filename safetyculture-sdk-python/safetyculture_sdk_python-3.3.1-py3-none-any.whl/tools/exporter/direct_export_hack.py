import csvExporter
import requests
import os

custom_http_headers = {
                'Authorization': 'Bearer ' + 'b2693425e4fd87e54bc90bbca6a0e7fdb60de260a0382dcb6e5a7a53dd37b494'
            }

audit_list = [
    "audit_1ec744ea196945fb8758f157b26f21f0",
    "audit_761fca9ef84941599ddc98801ef3e5dd",
    "audit_DB5994CBFF15478C8522FD3B6E7A3BA4",
    "audit_59819CFEC2D041958AFC46ED333D7929",
    "audit_3D58C12584FA4814A3B4E413BFC46A8A",
    "audit_dfea4844dc3c4a1aa6754017180c4226",
    "audit_A8BEF8A2FCA141C0AF2AAD8DF9405750",
    "audit_1a4cb516a8324e25bf42ffebfaa34768",
    "audit_F3880F8EAC6446479F78C8DDB852A142",
    "audit_CD2AE108FECF428E903B74C70F54B196",
    "audit_ec6515dff24a4ed78b1800f6ebf65ff3",
    "audit_176493b384f54c4abb47fed0e16bca05",
    "audit_809617e5ee2842cdbafcde1fa9c89d73",
    "audit_09114F03D52C4EA88DAD7CDAA54CAD52",
    "audit_0fcd50b4ecc349b7880a732db1aa31ef",
    "audit_5e53bb20082c4b71a9288092ede04d95",
    "audit_e4b00b5397ab4b27a1d35d668002997f",
    "audit_A6105FF7F2B84E1F81FD6C46A164AD80",
    "audit_63df9c6e11b9433ea1abdf25f77e9687",
    "audit_55ce8364e56c413da16bebe207e485df",
    "audit_C7DB3B4C477C44859566B926EBFAE36E",
    "audit_fd926cee330c4ec2959c5a8fad4560c6",
    "audit_257C07D9D75346ACB0A199CFD7CA6D09",
    "audit_8f7b447c761d4e419fd0780bca5470ef",
    "audit_ec0e844ef0264906b251f9fe7ce3ffc9",
    "audit_abf759d3a1894a0783bec324dd046e1e",
    "audit_576EE0E5515B46BB8BF4D4E9F5CFD036",
    "audit_528DF8F17A7C47F790B765BBF8865258",
    "audit_C79B89D6D21D4AEC9914F308751B1B1F",
    "audit_A99B70BBF3EE4A28B1E5496A09A00406",
    "audit_48755779ebc441f29496b4570001565a",
    "audit_5c5b5c6471914d0cab8dcd7e77c5348c",
    "audit_FCE22758C0D3497D94B20F5C2957B8EF",
    "audit_65d5f8102bc847618b97bb75f22e3370",
    "audit_3FCB5FD67603466EA4B82362FCBD4E01",
    "audit_AC585E0B28954E4497B9D8F418057624",
    "audit_b3e9481622304fd5bdea6e4611659430",
    "audit_6237BC5934844CC6ABCB42412841D608",
    "audit_848F5AE1A6D64549A075306C72E0DD6F",
    "audit_A696E8CF435B49C5B5EE17056253C66F",
    "audit_4e4f833509fa4891930918b33efd5567",
    "audit_216e8c61858f4281a4ca6a732fc07b06",
    "audit_1614187c52ad44bfb2c110c47da0190f",
    "audit_894C3825962C4866AFC23E6E9CE95F39",
    "audit_8cdad5667a9d48a18acc34d74d985ccb",
    "audit_1D50F4B351E94AE5A65C448AC570D6CE",
    "audit_41d945732c67459a97671b89f551cc6d",
    "audit_913ecf5fd8394da48dadb7d529ff3699",
    "audit_0ec7b5a523044937a8baa42f773aee69",
    "audit_45fb72a6ec2d4039afc0e6f35b980a6f",
    "audit_386D1E0FC74C4F1789B65040D796C3DB",
    "audit_b669c61fb8a24328ab53687b1f403ce8",
    "audit_14310c4fb92241969d6e29f23b31a2e6",
    "audit_213a296bc4d54016adc740bf1780e873",
    "audit_bb05236558424c118b8d3c6eee7b4036",
    "audit_2F042556FB4D44D1912732C8F4691AC8",
    "audit_3b86af857c5449ddae5f0cb1275d4596",
    "audit_277e8e1afe534061b4489ca92a81de72",
    "audit_24fbd3297cfa405e9d8c9e3965f1fa95",
    "audit_376c0eead20c4bccb96c15a6948ff8a6",
    "audit_a4de6cb948f04772bf26c814ebe3dbf5",
    "audit_045b5476dae04fb8891de5cd90ac26f1",
    "audit_7a9d8d6192c64de3b7bdb1dfe1844639",
    "audit_af99b91813f647f4ae7e28962e76c987",
    "audit_b0fef26d823d470d93755fa370f9fb02",
    "audit_c352a07271204a5a8b97db601a61c226",
    "audit_2e5e82f71ad64caeb6e74f9b0e2c146f",
    "audit_277d1636b8384d64b4d7cdc537391a80",
    "audit_b5aae69070264a208e1241bdeea76e30",
    "audit_cf0aea796b4e4a628a1b104918565cd8",
    "audit_823a689b9f7b43ad8e65da7672e96e85",
    "audit_2862268772a647b59aace13aa963c1aa",
    "audit_424C80DDD3B9443CBFC5C0153D5A77E5",
    "audit_72fc10b107ae42da946443cc6a5edab8",
    "audit_69c0ba5dc55e4cc9a19216a575593a59",
    "audit_1ddfbf5db4ed47c380b8e7d31c574687"
]

audit_json = ''

for audit_id in audit_list:
    print(audit_id)
    get_doc = requests.get('https://api.safetyculture.io/audits/' + audit_id, headers=custom_http_headers)


    if get_doc.status_code == 200:
            audit_json = get_doc.json()

    csv_exporter = csvExporter.CsvExporter(audit_json, True)
    csv_export_filename = audit_json['template_id']
    csv_exporter.append_converted_audit_to_bulk_export_file(
        os.path.join('/Users/alexanderturner/Downloads/temp/', csv_export_filename + '.csv'))